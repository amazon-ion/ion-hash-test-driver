# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
Provides the build logic for Ion Hash resources required by the ion_hash_test_driver.
"""

import os
import tempfile

from ionhashtest.util import IonBuild, NO_OP_BUILD, log_call

RESULTS_FILE_DEFAULT = 'ion-test-driver-results.ion'
ION_HASH_TEST_SOURCE = 'https://github.com/amzn/ion-hash-test.git'

# Tools expected to be present on the system. Key: name, value: path. Paths may be overridden using --<name>.
# Accordingly, if tool dependencies are added here, a corresponding option should be added to the CLI.
TOOL_DEPENDENCIES = {
    'git': 'git'
}


def install_ion_hash_java(log):
    log_call(log, ('mvn', 'install'))


def install_ion_hash_js(log):
    log_call(log, ('npm', 'install'))
    log_call(log, 'grunt')


def install_ion_hash_python(log):
    pass


ION_BUILDS = {
    'ion-hash-test': NO_OP_BUILD,
    'ion-hash-java': IonBuild(install_ion_hash_java, os.path.join('tools', 'cli', 'ion-hash')),
    'ion-hash-js': IonBuild(install_ion_hash_js, os.path.join('tools', 'cli', 'ion-hash')),
    'ion-hash-python': IonBuild(install_ion_hash_python, os.path.join('tools', 'cli', 'ion-hash-wrapper')),
    # TODO add more implementations here
}

# Ion Hash implementations hosted in Github. Local implementations may be tested using the `--implementation` argument,
# and should not be added here. For the proper description format, see the ion_hash_test_driver CLI help.
ION_IMPLEMENTATIONS = [
    'ion-hash-java,https://github.com/amzn/ion-hash-java.git,master',
    'ion-hash-js,https://github.com/amzn/ion-hash-js.git,master',
    'ion-hash-python,https://github.com/amzn/ion-hash-python.git,master',
    # TODO add more implementations here
]

