## Ion Hash Test Driver
A cross-implementation test driver for [Amazon Ion Hash](https://amzn.github.io/ion-hash/) readers and writers.

[![Build Status](https://travis-ci.org/amzn/ion-hash-test-driver.svg?branch=master)](https://travis-ci.org/amzn/ion-hash-test-driver)

## Usage
The Ion Hash Test Driver fetches copies of known Ion Hash implementations and executes each against a set of test data derived from
[ion-hash-test](https://github.com/amzn/ion-hash-test).  It then generates a report indicating how consistent the implementations
are when hashing the test data.

To execute the test driver:
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
$ python ionhashtest/ion_hash_test_driver.py
```

Additional Ion Hash implementations may be tested by adding a command-line tool such as [command-line tool](https://github.com/amzn/ion-hash-python/blob/master/tools/ion-hash), then adding information about the implementation to this project's [config.py](https://github.com/amzn/ion-hash-test-driver/blob/master/ionhashtest/config.py) file.

## License
This project is licensed under the Apache 2.0 License.

