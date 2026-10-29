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

def main():
    evidence = {"scope": "SYNTHETIC pinned sembast_web 2.4.6 / sembast 3.8.11; two Chromium tabs; NOT LogMate", "checks": []}
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}/index.html"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROME, headless=True, args=["--no-sandbox"])
            context = browser.new_context()
            a, b = context.new_page(), context.new_page()
            start(a, url)
            start(b, url)
            evidence["browser"] = browser.version
            send(a, "seed", "reset")
            seed = receive(a, "seed")
            assert seed == {"logicalCapability": 17, "counter": 0, "replica": "SYNTHETIC-REPLICA"}, seed
            evidence["checks"].append({"id": "PINNED_LOGICAL_MARKER_SEED", "observed": seed})
            send(b, "observe", "inspect")
            observed = receive(b, "observe")
            assert observed == seed, observed
            evidence["checks"].append({"id": "SECOND_TAB_OBSERVES_SEED", "observed": observed})
            send(a, "a1", "increment", 350)
            send(b, "b1", "increment", 350)
            ra, rb = receive(a, "a1"), receive(b, "b1")
            send(a, "final", "inspect")
            final = receive(a, "final")
            assert final["counter"] == 2 and final["replica"] == "SYNTHETIC-REPLICA" and final["logicalCapability"] == 17, (ra, rb, final)
            evidence["checks"].append({"id": "TWO_TAB_TRANSACTION_FINAL_STATE", "observed": {"a": ra, "b": rb, "final": final}, "retry_observed": ra["attempts"] > 1 or rb["attempts"] > 1})
            send(b, "fault", "throw_before_commit")
            fault = receive(b, "fault")
            assert fault["caught"] and fault["counter"] == 2, fault
            evidence["checks"].append({"id": "THROWN_TRANSACTION_NOT_PUBLISHED", "observed": fault})
            send(a, "reopen", "reopen")
            reopen = receive(a, "reopen")
            assert reopen == final, (reopen, final)
            evidence["checks"].append({"id": "REOPEN_PRESERVES_COMMITTED_STATE", "observed": reopen})
            physical = a.evaluate("indexedDB.databases().then(x => x.map(d => ({name:d.name,version:d.version})))")
            evidence["checks"].append({"id": "PHYSICAL_IDB_VERSION_RECORDED_SEPARATELY", "observed": physical})
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
