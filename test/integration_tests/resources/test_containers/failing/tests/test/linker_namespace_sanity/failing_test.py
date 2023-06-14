#!/usr/bin/env python3

from exasol_python_test_framework import udf
from exasol_python_test_framework import docker_db_environment


class FailingTest(udf.TestCase):

    def test_dummy(self):
        assert False


if __name__ == '__main__':
    udf.main()

