import unittest
import os
from seqpostproc.rename import _is_breseq_report
from seqpostproc.rename import _get_serialization_str


class Tests(unittest.TestCase):

    def test_get_serialization_str(self):
        expected_name_list = ["3-110-0-1", "3-181-0-1"]
        for file_name in os.listdir('test_data'):
            if _is_breseq_report(file_name):
                serialization_str = _get_serialization_str(file_name)
                self.assertTrue(serialization_str in expected_name_list)