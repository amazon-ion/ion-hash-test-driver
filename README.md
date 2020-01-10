## Ion Hash Test Driver
A cross-implementation test driver for [Amazon Ion Hash](https://amzn.github.io/ion-hash/)
readers and writers.

[![Build Status](https://travis-ci.org/amzn/ion-hash-test-driver.svg?branch=master)](https://travis-ci.org/amzn/ion-hash-test-driver)


## Usage
The Ion Hash Test Driver fetches copies of known Ion Hash implementations and executes each
against a set of test data derived from [ion-hash-test](https://github.com/amzn/ion-hash-test).
It then generates a report indicating how consistent the implementations are when hashing the
test data.

To execute the test driver:
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
$ python ionhashtest/ion_hash_test_driver.py
```


## Checking consistency of a new Ion Hash implementation
Additional Ion Hash implementations may be checked for consistency by adding information
about the implementation to this project's
[config.py](https://github.com/amzn/ion-hash-test-driver/blob/master/ionhashtest/config.py)
file, including the location of a command-line tool provided by the implementation.
The ion-hash-test-driver invokes such command-line tools via `command [algorithm] [filename]`,
where `[algorithm]` is the name of the hash function to use when computing the Ion hashes,
and `[filename]` is a file containing one or more top-level Ion values (note that a given
file may be encoded as either Ion text or Ion binary).  For each top-level value in the file,
the command-line tool is expected to print a single line containing the computed Ion Hash as
space-separated hexadecimal bytes.
 
For example, given a file `ion_values.ion` containing the following three top-level Ion text values:
```
$ion_1_0
hello
[1, 2, 3]
{
  a: 1,
  b: 2,
  c: [3, 4, 5],
}
```

an implementation's command-line utility executed as follows:
```
$ tools/ion-hash md5 ion_values.ion
```

should output:
```
2a 2a f7 b7 77 31 b0 ba 4c 2f 63 7d f1 82 96 35
8f 3b f4 b1 93 5c f4 69 c9 c1 0c 31 52 4b 26 25
5c 5e 20 42 f4 ea 70 9a 43 cb c5 f9 e4 79 a4 c0
```

See ion-hash-python's
[command-line tool](https://github.com/amzn/ion-hash-python/blob/master/tools/ion-hash)
as an example.


## License
This project is licensed under the Apache 2.0 License.

