#!/usr/bin/env python3
"""Two-tab pinned Sembast browser probe; synthetic only, no LogMate data."""
import http.server
import json
import os
import pathlib
import threading
import traceback
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(os.environ.get("EVIDENCE_OUT", "/tmp/pinned-sembast-evidence.json"))
CHROME = os.environ.get("CHROMIUM_PATH", "/usr/bin/google-chrome")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)
    def log_message(self, *args):
        pass

def start(page, url):
    page.goto(url)
    page.wait_for_function("document.body.dataset.ready === 'true'", timeout=25000)
    page.evaluate("""() => {
      window.__probeReplies = {};
      window.addEventListener('message', e => {
        if (e.origin !== location.origin || typeof e.data !== 'string') return;
        try { const x = JSON.parse(e.data); if (x.probeReply) window.__probeReplies[x.id] = x; } catch {}
      });
    }""")

def send(page, ident, command, delay=0):
    page.evaluate("""arg => window.postMessage(JSON.stringify({
      probeCmd:true,id:arg.id,command:arg.command,delayMs:arg.delay
    }), location.origin)""", {"id": ident, "command": command, "delay": delay})

def receive(page, ident):
    page.wait_for_function("id => !!window.__probeReplies[id]", arg=ident, timeout=30000)
    result = page.evaluate("id => window.__probeReplies[id]", ident)
    assert result["ok"], result
    return result["result"]

def converge(page, prefix, expected, attempts=25):
    """Wait for asynchronous cross-tab propagation; report observed poll count."""
    last = None
    for n in range(attempts):
        ident = f"{prefix}-{n}"
        send(page, ident, "inspect")
        last = receive(page, ident)
        if last == expected:
            return last, n + 1
        page.wait_for_timeout(160)
    raise AssertionError({"expected": expected, "last": last, "polls": attempts})

def main():
    evidence = {"scope": "SYNTHETIC pinned sembast_web 2.4.6 / sembast 3.8.11; two Chromium tabs; NOT LogMate", "checks": []}
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}/index.html"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROME, headless=True, args=["--no-sandbox"])
            context = browser.new_context()
            # Observational instrumentation only: record native IndexedDB transaction
            # options actually requested by the pinned package. Never force strict.
            context.add_init_script("""(() => {
              window.__idbTransactionTrace = [];
              window.__idbTraceState = 'NOT_INSTALLED';
              try {
                const original = IDBDatabase.prototype.transaction;
                IDBDatabase.prototype.transaction = function(...args) {
                  const txn = original.apply(this, args);
                  const trace = window.__idbTransactionTrace;
                  if (trace.length < 100) {
                    trace.push({
                      database: this.name,
                      mode: args[1] ?? null,
                      requestedDurability: args[2]?.durability ?? null,
                      observedDurability: txn.durability ?? null
                    });
                  }
                  return txn;
                };
                window.__idbTraceState = 'INSTALLED';
              } catch (e) {
                window.__idbTraceState = 'UNAVAILABLE:' + String(e);
              }
            })();""")
            a, b = context.new_page(), context.new_page()
            start(a, url)
            start(b, url)
            evidence["browser"] = browser.version
            send(a, "seed", "reset")
            seed = receive(a, "seed")
            assert seed == {"logicalCapability": 17, "counter": 0, "replica": "SYNTHETIC-REPLICA"}, seed
            evidence["checks"].append({"id": "PINNED_LOGICAL_MARKER_SEED", "observed": seed})
            observed, polls = converge(b, "observe", seed)
            evidence["checks"].append({"id": "SECOND_TAB_OBSERVES_SEED", "observed": observed, "polls": polls})
            send(a, "a1", "increment", 350)
            send(b, "b1", "increment", 350)
            ra, rb = receive(a, "a1"), receive(b, "b1")
            final, polls = converge(a, "final", {"logicalCapability": 17, "counter": 2, "replica": "SYNTHETIC-REPLICA"})
            assert final["counter"] == 2, (ra, rb, final)
            evidence["checks"].append({"id": "TWO_TAB_TRANSACTION_FINAL_STATE", "observed": {"a": ra, "b": rb, "final": final, "convergence_polls": polls}, "retry_observed": ra["attempts"] > 1 or rb["attempts"] > 1})
            converge(b, "before-fault", final)
            send(b, "fault", "throw_before_commit")
            fault = receive(b, "fault")
            assert fault["caught"] and fault["counter"] == 2, fault
            evidence["checks"].append({"id": "THROWN_TRANSACTION_NOT_PUBLISHED", "observed": fault})
            # Cross-tab visibility is a separate oracle from the faulting tab's view.
            after_fault, polls = converge(a, "after-fault", final)
            evidence["checks"].append({"id": "OTHER_TAB_SEES_NO_ABORTED_WRITE", "observed": after_fault, "polls": polls})
            send(a, "reopen", "reopen")
            reopen = receive(a, "reopen")
            assert reopen == final, (reopen, final)
            evidence["checks"].append({"id": "REOPEN_PRESERVES_COMMITTED_STATE", "observed": reopen})
            physical = a.evaluate("indexedDB.databases().then(x => x.map(d => ({name:d.name,version:d.version})))")
            evidence["checks"].append({"id": "PHYSICAL_IDB_VERSION_RECORDED_SEPARATELY", "observed": physical})
            traces = {
                "a": a.evaluate("({state:window.__idbTraceState,transactions:window.__idbTransactionTrace})"),
                "b": b.evaluate("({state:window.__idbTraceState,transactions:window.__idbTransactionTrace})")
            }
            evidence["checks"].append({
                "id": "NATIVE_IDB_DURABILITY_HINT_OBSERVATION",
                "observed": traces,
                "interpretation": "OBSERVED" if any(v["transactions"] for v in traces.values()) else "NOT_OBSERVED"
            })
            # Fresh page in the SAME browser context/profile, not an OS crash test.
            a.close()
            b.close()
            c = context.new_page()
            start(c, url)
            send(c, "fresh", "inspect")
            fresh = receive(c, "fresh")
            assert fresh == final, (fresh, final)
            evidence["checks"].append({"id": "FRESH_TAB_SAME_PROFILE_REOPEN", "observed": fresh})
            evidence["result"] = "PASS_SYNTHETIC"
            context.close()
            browser.close()
    except Exception as exc:
        evidence["result"] = "FAIL_OR_NON_EXECUTION"
        evidence["error"] = repr(exc)
        evidence["traceback"] = traceback.format_exc()[-6000:]
        raise
    finally:
        OUT.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
        server.shutdown()
        print(json.dumps(evidence, indent=2))

if __name__ == "__main__":
    main()
