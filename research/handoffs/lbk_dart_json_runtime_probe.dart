// Public, synthetic Dart VM vs dart2js/Node diagnostic.
// No LogMate source, backup bytes, user records, secrets or production endpoints.
import 'dart:convert';

void main() {
  const duplicate = r'{"owner":"old","owner":"new"}';
  const escapedDuplicate = r'{"owner":"old","\u006fwner":"new"}';
  const largeInteger = r'{"value":9007199254740993}';
  const nested = r'{"a":{"key":1},"b":{"key":2}}';
  final duplicateValue = (jsonDecode(duplicate) as Map)['owner'];
  final escapedValue = (jsonDecode(escapedDuplicate) as Map)['owner'];
  final big = (jsonDecode(largeInteger) as Map)['value'];
  final nestedValue = jsonDecode(nested) as Map;
  final reviverKeys = <String>[];
  jsonDecode(duplicate, reviver: (key, value) {
    if (key != null) reviverKeys.add(key.toString());
    return value;
  });
  final escapedReviverKeys = <String>[];
  jsonDecode(escapedDuplicate, reviver: (key, value) {
    if (key != null) escapedReviverKeys.add(key.toString());
    return value;
  });
  final ordered = <String>['\uE000', '\u{10000}']..sort();
  final encodedBig = jsonEncode({'value': big});
  final report = <String, Object?>{
    'probe': 'stage8-lbk-json-cross-runtime-v1',
    'duplicateOwner': duplicateValue,
    'escapedDuplicateOwner': escapedValue,
    'duplicateReviverOwnerVisits': reviverKeys.where((x) => x == 'owner').length,
    'escapedDuplicateReviverOwnerVisits':
        escapedReviverKeys.where((x) => x == 'owner').length,
    'largeIntegerDecodedString': big.toString(),
    'largeIntegerEncoded': encodedBig,
    'largeIntegerRuntimeType': big.runtimeType.toString(),
    'doubleOneRuntimeType': (1.0).runtimeType.toString(),
    'sameNestedKeySeparateObjects': (nestedValue['a'] as Map)['key'] == 1 &&
        (nestedValue['b'] as Map)['key'] == 2,
    'bmpBeforeSupplementary': ordered.first == '\uE000',
    'utf8BmpBeforeSupplementary':
        utf8.encode('\uE000').first < utf8.encode('\u{10000}').first,
    'negativeZeroEncoded': jsonEncode(-0.0),
  };
  print(jsonEncode(report));
}
