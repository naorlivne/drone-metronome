from unittest import TestCase
from drone_metronome import *
import os


test_files_location = os.getenv("TEST_FILES_LOCATION", "test_files")


class BaseTests(TestCase):

    def test_file_reader_read_file(self):
        reply = read_file(test_files_location + "/test_read_file")
        self.assertEqual(reply, "it_reads!")

    def test_file_reader_read_file_raise_error_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_file(test_files_location + "/non_existing_file")
