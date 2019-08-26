from unittest import TestCase, mock
from drone_metronome import *
import os
import requests_mock


test_files_location = os.getenv("TEST_FILES_LOCATION", "test_files")


class BaseTests(TestCase):

    def test_file_reader_read_file(self):
        reply = read_file(test_files_location + "/test_read_file")
        self.assertEqual(reply, "it_reads!")

    def test_file_reader_read_file_raise_error_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_file(test_files_location + "/non_existing_file")

    def test_read_all_envvars_to_dict_force_uppercase_false(self):
        test_envvars = {"TEST_ENV": "123", "test_env_lowercase": "456"}
        with mock.patch.dict(os.environ, test_envvars):
            reply = read_all_envvars_to_dict()
            self.assertEqual(type(reply), dict)
            self.assertEqual(reply["TEST_ENV"], "123")
            self.assertEqual(reply["test_env_lowercase"], "456")

    def test_populate_template_string_works_simple(self):
        test_template_values_dict = {"test": "test that works"}
        expected_reply = "this is a test that works"
        reply = populate_template_string("this is a $test", test_template_values_dict)
        self.assertEqual(reply, expected_reply)

    def test_populate_template_string_works_complex(self):
        test_template_values_dict = {"test1": "test that", "test2": "works"}
        expected_reply = "this is a $Complex$123 test that works"
        reply = populate_template_string("this is a $Complex$123 $test1 $test2", test_template_values_dict)
        self.assertEqual(reply, expected_reply)

    def test_populate_template_string_no_template_values(self):
        test_template_values_dict = None
        expected_reply = "this is a $test"
        reply = populate_template_string("this is a $test", test_template_values_dict)
        self.assertEqual(reply, expected_reply)

    def test_populate_template_string_no_template_values_no_template_placement(self):
        test_template_values_dict = None
        expected_reply = "this is a test"
        reply = populate_template_string("this is a test", test_template_values_dict)
        self.assertEqual(reply, expected_reply)

    def test_metronome_init(self):
        test_metronome_connection = Metronome()
        expected_test_metronome_connection_headers = {
            'cache-control': "no-cache",
            'Connection': "keep-alive",
            'Content-Type': "application/json",
        }
        expected_test_metronome_connection_metronome_host = "http://metronome.mesos:9000"
        expected_test_metronome_connection_timeout = 60
        self.assertEqual(test_metronome_connection.headers, expected_test_metronome_connection_headers)
        self.assertEqual(test_metronome_connection.metronome_host, expected_test_metronome_connection_metronome_host)
        self.assertEqual(test_metronome_connection.timeout, expected_test_metronome_connection_timeout)

    def test_metronome_check_metronome_job_exists_true(self):
        test_metronome_connection = Metronome()
        with requests_mock.Mocker() as request_mocker:
            request_mocker.head('http://metronome.mesos:9000/v1/jobs/test_job', status_code=200)
            reply = test_metronome_connection.check_metronome_job_exists("test_job")
            self.assertTrue(reply)

    def test_metronome_check_metronome_job_exists_false(self):
        test_metronome_connection = Metronome()
        with requests_mock.Mocker() as request_mocker:
            request_mocker.head('http://metronome.mesos:9000/v1/jobs/test_job', status_code=404)
            reply = test_metronome_connection.check_metronome_job_exists("test_job")
            self.assertFalse(reply)

    def test_metronome_check_metronome_job_exists_connection_or_permission_issue(self):
        test_metronome_connection = Metronome(metronome_host="http://metronome.mesos:9000")
        with requests_mock.Mocker() as request_mocker:
            request_mocker.head('http://metronome.mesos:9000/v1/jobs/test_job', status_code=500)
            with self.assertRaises(Exception):
                test_metronome_connection.check_metronome_job_exists("test_job")

    def test_metronome_create_metronome_job(self):
        test_metronome_connection = Metronome()
        with requests_mock.Mocker() as request_mocker:
            request_mocker.post('http://metronome.mesos:9000/v0/scheduled-jobs', status_code=201,
                                text='{"test_json_key": "test_json_value"}')
            reply = test_metronome_connection.create_metronome_job("{}")
            self.assertDictEqual(reply, {"test_json_key": "test_json_value"})

    def test_metronome_create_metronome_job_failure(self):
        test_metronome_connection = Metronome(metronome_host="http://metronome.mesos:9000")
        with requests_mock.Mocker() as request_mocker:
            request_mocker.post('http://metronome.mesos:9000/v0/scheduled-jobs', status_code=401)
            with self.assertRaises(Exception):
                test_metronome_connection.create_metronome_job("{}")

    def test_metronome_update_metronome_job(self):
        test_metronome_connection = Metronome()
        with requests_mock.Mocker() as request_mocker:
            request_mocker.put('http://metronome.mesos:9000/v0/scheduled-jobs/test', status_code=200,
                               text='{"test_json_key": "test_json_value"}')
            reply = test_metronome_connection.update_metronome_job('{"id": "test"}')
            self.assertDictEqual(reply, {"test_json_key": "test_json_value"})

    def test_metronome_update_metronome_job_failure(self):
        test_metronome_connection = Metronome(metronome_host="http://metronome.mesos:9000")
        with requests_mock.Mocker() as request_mocker:
            request_mocker.put('http://metronome.mesos:9000/v0/scheduled-jobs/test', status_code=401)
            with self.assertRaises(Exception):
                test_metronome_connection.update_metronome_job('{"id": "test"}')

    def test_metronome_create_or_update_metronome_job_create(self):
        test_metronome_connection = Metronome()
        with requests_mock.Mocker() as request_mocker:
            request_mocker.head('http://metronome.mesos:9000/v1/jobs/test', status_code=404)
            request_mocker.post('http://metronome.mesos:9000/v0/scheduled-jobs', status_code=201,
                                text='{"test_json_key": "test_json_value"}')
            reply = test_metronome_connection.create_or_update_metronome_job('{"id": "test"}')
            self.assertDictEqual(reply, {"test_json_key": "test_json_value"})

    def test_metronome_create_or_update_metronome_job_update(self):
        test_metronome_connection = Metronome()
        with requests_mock.Mocker() as request_mocker:
            request_mocker.head('http://metronome.mesos:9000/v1/jobs/test', status_code=200)
            request_mocker.put('http://metronome.mesos:9000/v0/scheduled-jobs/test', status_code=200,
                               text='{"test_json_key": "test_json_value"}')
            reply = test_metronome_connection.create_or_update_metronome_job('{"id": "test"}')
            self.assertDictEqual(reply, {"test_json_key": "test_json_value"})
