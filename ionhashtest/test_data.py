# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at:
#
#    http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the
# License.

"""
Logic for generating the files to be used for testing.
"""

import amazon.ion.simpleion as ion
import base64
import os


_ion_prefix = 'ion::'
_invalid_ion_prefix = 'invalid_ion::'


def generate_tests(base_dir, out_dir, test_files=[]):
    """
    Converts source test files into a stream of Ion values to be hashed.
    :param base_dir: Directory containing source test files.
    :param out_dir: Directory to write files containing Ion values to be hashed.
    :param test_files: If not empty, narrows the set of source test files.
    :return: List of filenames containing Ion avlues to be hashed.
    """
    files = []
    if 'ion_hash_test.ion' in test_files:
        files.extend(generate_tests_ion_hash_tests(base_dir, out_dir))
    if 'big_list_of_naughty_strings.txt' in test_files:
        files.extend(generate_tests_big_list_of_naughty_strings(base_dir, out_dir))
    if len(test_files) == 0:
        files.extend(generate_tests_ion_hash_tests(base_dir, out_dir))
        files.extend(generate_tests_big_list_of_naughty_strings(base_dir, out_dir))

    return files


def generate_tests_ion_hash_tests(base_dir, out_dir):
    """
    Writes each test value in ion_hash_test.ion as a top-level value in new files
    "<out_dir>/ion_hash_tests.ion" and "<out_dir>/ion_hash_tests.10n".
    """
    with open(os.path.join(out_dir, "ion_hash_tests.ion"), "w") as text_file, \
            open(os.path.join(out_dir, "ion_hash_tests.10n"), "wb") as binary_file:

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
                sexp_bytes = sexp_to_bytearray(test['10n'])
                binary_file.write(sexp_bytes)

        return [text_file.name, binary_file.name]


def generate_tests_big_list_of_naughty_strings(base_dir, out_dir):
    """
    Writes each test string in big_list_of_naughty_strings.ion as a series of top-level value
    in new files "<out_dir>/big_list_of_naughty_strings.ion" and "<out_dir>/big_list_of_naughty_strings.10n".
    """
    with open(os.path.join(out_dir, "big_list_of_naughty_strings.ion"), "w") as text_file, \
            open(os.path.join(out_dir, "big_list_of_naughty_strings.10n"), "wb") as binary_file:

        with open(os.path.join(base_dir, "big_list_of_naughty_strings.txt")) as f:
            lines = [line.rstrip('\n') for line in f]

        for line in lines:
            if not (line == '' or line[0] == '#' or line.startswith(_invalid_ion_prefix)):
                for test_text in test_strings_for(line):
                    if not ('$0' in test_text):
                        text_file.write(test_text + "\n")
                        test_binary = ion.dumps(test_text, binary=True)
                        binary_file.write(test_binary)

        return [text_file.name, binary_file.name]


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
    """
    For the provided `line`, returns a list of strings that represent Ion values using `line` in
    a variety of ways.
    """
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
    """
    Utility that converts an sexp that represents a byte array (as found in ion_hash_test.ion)
    to an actual bytearray.
    """
    ba = bytearray()
    for b in sexp:
        ba.append(b)
    return ba
