import amazon.ion.simpleion as ion
import base64
import os


_ion_prefix = 'ion::'
_invalid_ion_prefix = 'invalid_ion::'


def generate_tests(base_dir, out_filename):
    text_filename = out_filename + ".ion"
    text_file = open(text_filename, "w")

    binary_filename = out_filename + ".10n"
    binary_file = open(binary_filename, "wb")

    with open(os.path.join(base_dir, "ion_hash_tests.ion")) as f:
        ion_hash_tests = f.read()

    tests = ion.loads(ion_hash_tests, single_value=False)
    for test in tests:
        if 'ion' in test:
            test_text = ion.dumps(test['ion'], binary=False, omit_version_marker=True)
            if not ('$0' in test_text):
                text_file.write(test_text + "\n")
                test_binary = ion.dumps(test['ion'], binary=True)
                binary_file.write(test_binary)
        if '10n' in test:
            bytes = sexp_to_bytearray(test['10n'])
            binary_file.write(bytes)

    '''
    with open(os.path.join(base_dir, "big_list_of_naughty_strings.txt")) as f:
        lines = [line.rstrip('\n') for line in f]

    def _is_test(string):
        return not (string == '' or string[0] == '#' or string.startswith(_invalid_ion_prefix))

    for line in filter(_is_test, lines):
        for test in test_strings_for(line):
            text_file.write(test + "\n")
    '''

    text_file.close()
    binary_file.close()

    return [text_filename, binary_filename]


class _TestValue:
    def __init__(self, string):
        self.ion = string
        self.valid_ion = None

        if self.ion.startswith(_ion_prefix):
            self.valid_ion = True
            self.ion = self.ion[len(_ion_prefix):]

        if self.ion.startswith(_invalid_ion_prefix):
            self.valid_ion = False
            self.ion = self.ion[len(_invalid_ion_prefix):]

    def symbol(self):
        s = self.ion
        s = s.replace("\\", "\\\\")
        s = s.replace("'", "\\'")
        return "\'" + s + "\'"

    def string(self):
        s = self.ion
        s = s.replace("\\", "\\\\")
        s = s.replace("\"", "\\\"")
        return "\"" + s + "\""

    def long_string(self):
        s = self.ion
        s = s.replace("\\", "\\\\")
        s = s.replace("'", "\\'")
        return "'''" + s + "'''"

    def clob(self):
        s = self.string()
        escaped_s = ''.join(u'\\x{0:x}'.format(b) if (b >= 128) else chr(b) for b in s.encode('utf-8'))
        return u'{{' + escaped_s + u'}}'

    def blob(self):
        return "{{" + base64.b64encode(bytes(self.ion, "utf-8")).decode("utf-8") + "}}"

    def __str__(self):
        return self.ion


def test_strings_for(line):
    strings = []
    tv = _TestValue(line)

    strings.append(tv.symbol())
    strings.append(tv.string())
    strings.append(tv.long_string())
    strings.append(tv.clob())
    strings.append(tv.blob())

    strings.append(tv.symbol() + "::" + tv.symbol())
    strings.append(tv.symbol() + "::" + tv.string())
    strings.append(tv.symbol() + "::" + tv.long_string())
    strings.append(tv.symbol() + "::" + tv.clob())
    strings.append(tv.symbol() + "::" + tv.blob())

    strings.append(tv.symbol() + "::{" + tv.symbol() + ":" + tv.symbol() + "}")
    strings.append(tv.symbol() + "::{" + tv.symbol() + ":" + tv.string() + "}")
    strings.append(tv.symbol() + "::{" + tv.symbol() + ":" + tv.long_string() + "}")
    strings.append(tv.symbol() + "::{" + tv.symbol() + ":" + tv.clob() + "}")
    strings.append(tv.symbol() + "::{" + tv.symbol() + ":" + tv.blob() + "}")

    if tv.valid_ion:
        strings.append(tv.ion)
        strings.append(tv.symbol() + "::" + tv.ion)
        strings.append(tv.symbol() + "::{" + tv.symbol() + ":" + tv.ion + "}")
        strings.append(tv.symbol() + "::{" + tv.symbol() + ":" + tv.symbol() + "::" + tv.ion + "}")

    # list
    strings.append(
          tv.symbol() + "::["
              + tv.symbol() + ", "
              + tv.string() + ", "
              + tv.long_string() + ", "
              + tv.clob() + ", "
              + tv.blob() + ", "
              + (tv.ion if tv.valid_ion else "")
              + "]")

    # sexp
    strings.append(
          tv.symbol() + "::("
              + tv.symbol() + " "
              + tv.string() + " "
              + tv.long_string() + " "
              + tv.clob() + " "
              + tv.blob() + " "
              + (tv.ion if tv.valid_ion else "")
              + ")")

    # multiple annotations
    strings.append(tv.symbol() + "::" + tv.symbol() + "::" + tv.symbol() + "::" + tv.string())

    return strings


def sexp_to_bytearray(sexp):
    ba = bytearray()
    for b in sexp:
        ba.append(b)
    return ba
