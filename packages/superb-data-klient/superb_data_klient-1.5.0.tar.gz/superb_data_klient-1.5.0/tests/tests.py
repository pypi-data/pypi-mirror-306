import hashlib
import os
import os.path
import re
import shutil
import sys
import time
import unittest
from unittest.mock import patch, MagicMock

import requests
from requests import HTTPError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import superbdataklient as sdk

"""
These tests tend to be Integration tests and not real unittests because of the nature of the functionality of the superbdataklient module. 
Mocking the requests wouldn't be of much value for testing.

Testing environment: sdk-dev
Organization, Spaces, Indices, Storage-accounts have been set up manually.
"""


class TestSDKClient(unittest.TestCase):
    user = None
    pwd = None
    env = None

    @classmethod
    def setUp(cls) -> None:
        cls.env = 'sdk-dev'
        # user-roles: {SDK_USER, default-roles-efs-sdk, org-roles}
        cls.user = 'test-user-pythonapi@efs-techhub.com'
        cls.pwd = 'EASoxdhrf97238§$'
        cls.test_organization_id = 448
        cls.test_org_name = 'testorganizationsdk'
        cls.test_space_id = 459
        cls.test_space_name = 'test-space-untittests-pythonapi'
        cls.test_index_name = 'testorganizationsdk_test-space-untittests-pythonapi_analysis_testindex'
        cls.test_application_index_name = "application-test-index"
        cls.test_get_all_documents_index = 'testorganizationsdk_test-space-untittests-pythonapi_analysis_test-index-random-docs'
        cls.test_doc_id = '4xPEEoYBXwCYu18SIg18'
        cls.client = sdk.SDKClient(username=cls.user, password=cls.pwd, env=cls.env)

    def test_get_organization_all(self):
        organizations = self.client.organization_get_all()
        self.assertNotEqual(len(organizations), 0)

    def test_get_organization_by_id(self):
        org = self.client.organization_get_by_id(self.test_organization_id)
        self.assertEqual(org.get('name'), self.test_org_name)
        self.assertEqual(org.get('id'), self.test_organization_id)

    def test_get_organization_by_name(self):
        org = self.client.organization_get_by_name(self.test_org_name)
        self.assertEqual(org.get('id'), self.test_organization_id)

    def test_space_get_all(self):
        try:
            self.client.space_get_all(self.test_organization_id)
        except Exception:
            self.fail(f'{self.id()} should not raise Exception!')

    def test_space_get_by_id(self):
        space = self.client.space_get_by_id(self.test_organization_id, self.test_space_id)
        self.assertEqual(space.get('id'), self.test_space_id)
        self.assertEqual(self.test_space_name, space.get('name'))

    def test_space_get_by_name(self):
        space = self.client.space_get_by_name(self.test_organization_id, self.test_space_name)
        self.assertEqual(space.get('id'), self.test_space_id)
        self.assertEqual(space.get('name'), self.test_space_name)

    def test_index_get_all(self):
        indices = self.client.index_get_all()
        self.assertNotEqual(len(indices), 0)

    def test_index_get_document(self):
        doc = self.client.index_get_document(self.test_index_name, self.test_doc_id)
        self.assertEqual(doc['value'], "got it")

    def test_index_documents_without_custom_id(self):
        test_docs = [
            {
                "value": "test doc id"
            },
            {
                "value": "test doc id 2"
            }
        ]
        try:
            self.client.index_documents(test_docs, self.test_index_name)
        except Exception:
            self.fail(f'{self.id()} should not raise Exception!')

    def test_index_documents_with_custom_id(self):
        test_docs = [
            {
                "_id": '1234',
                "value": "test doc id"
            },
            {
                "_id": '12345',
                "value": "test doc id 2"
            }
        ]
        try:
            self.client.index_documents(test_docs, self.test_index_name)
        except Exception:
            self.fail(f'{self.id()} should not raise Exception!')

    def test_storage_download_files_list_from_root_dir(self):
        local_dir = 'tmp'
        files = [
            "test-file01.txt",
            "test-file02.txt",
        ]
        if not os.path.isdir(local_dir):
            os.mkdir(local_dir)
        self.client.storage_download_files(organization=self.test_org_name, space=self.test_space_name, files=files,
                                           local_dir=local_dir)
        actual = set(os.listdir(f'{local_dir}'))  # all files downloaded
        expected = set(files)
        self.assertTrue(expected.issubset(actual))
        self.assertTrue(actual.issubset(expected))

        # cleanup directory
        shutil.rmtree(local_dir)

    def test_storage_download_files_list_from_directory(self):
        storage_dir = 'test-dir'
        local_dir = 'tmp'
        files = [
            "test-file01.txt",
            "test-file02.txt",
        ]
        if not os.path.isdir(local_dir):
            os.mkdir(local_dir)
        self.client.storage_download_files(organization=self.test_org_name, space=self.test_space_name,
                                           storage_dir=storage_dir, files=files,
                                           local_dir=local_dir)
        actual = set(os.listdir(f'{local_dir}'))  # all files downloaded
        expected = set(files)
        self.assertTrue(expected.issubset(actual))
        self.assertTrue(actual.issubset(expected))

        # cleanup directory
        shutil.rmtree(local_dir)

    def test_storage_download_files_list_direct_path(self):
        storage_dir = 'test-dir'
        local_dir = 'tmp'
        files = [
            "test-file01.txt",
            "test-file02.txt",
        ]
        file_paths = [f'{storage_dir}/{f}' for f in files]
        if not os.path.isdir(local_dir):
            os.mkdir(local_dir)
        self.client.storage_download_files(self.test_org_name, self.test_space_name, file_paths, local_dir)
        actual = set(os.listdir(f'{local_dir}/{storage_dir}'))  # all files downloaded
        expected = set(files)
        self.assertTrue(expected.issubset(actual))
        self.assertTrue(actual.issubset(expected))

        # cleanup directory
        shutil.rmtree(local_dir)

    def test_storage_list_blobs(self):
        expected = [
            'test-dir/test-file01.txt',
            'test-dir/test-file02.txt',
            'test-file01.txt',
            'test-file02.txt'
        ]
        actual = self.client.storage_list_blobs(self.test_org_name, self.test_space_name)
        self.assertTrue(self.is_subset(expected, actual))

    def test_index_search_by_field(self):
        query = {
            "query": {
                "exists": {
                    "field": "kafka"
                }
            }
        }
        expected = [
            {
                "kafka": "»Ach«, sagte die Maus, »,die Welt wird enger mit jedem Tag. Zuerst war sie so breit, daß ich Angst hatte, ich lief weiter und war "
                         "glücklich, daß ich endlich rechts und links in der Ferne Mauern sah, aber diese langen Mauern eilen so schnell aufeinander zu, "
                         "daß ich schon im letzten Zimmer bin, und dort im Winkel steht die Falle, in die ich laufe.« – »Du mußt nur die Laufrichtung "
                         "ändern«, sagte die Katze und fraß sie."
            }
        ]
        actual = self.client.index_search(self.test_index_name, query)
        self.assertEqual(actual, expected)

    def test_index_search_by_match_all(self):
        query = {
            "query": {
                "match_all": {}
            }
        }
        docs = self.client.index_search(self.test_index_name, query)
        self.assertNotEqual(0, len(docs))

    def test_create_application_index(self):
        response = self.client.application_index_create(self.test_application_index_name, self.test_org_name,
                                                        self.test_space_name, {})
        self.assertEqual(response,
                         f'{self.test_org_name}_{self.test_space_name}_analysis_{self.test_application_index_name}')

    def test_delete_application_index(self):
        try:
            self.client.application_index_delete(
                    f'{self.test_org_name}_{self.test_space_name}_analysis_{self.test_application_index_name}')
        except Exception:
            self.fail(f'{self.id()} should not raise Exception!')

    def test_index_filter_by_space(self):
        # works as long as indices in organization don't get deleted/ added
        case_measurment_all_spaces = self.client.index_filter_by_space(self.test_org_name, "*testapplication*",
                                                                       "MEASUREMENTS")
        case_measurment_all_spaces_expected = ['testorganizationsdk_testapplicationindex_measurements']

        case_analysis_all_spaces = self.client.index_filter_by_space(self.test_org_name, "*", "ANALYSIS")
        case_analysis_all_spaces_expected = ['testorganizationsdk_test-space-untittests-pythonapi_analysis_testindex']

        case_measurment_specific_space = self.client.index_filter_by_space(self.test_org_name, "testapplicationindex",
                                                                           "MEASUREMENTS")
        case_measurment_specific_space_expected = ['testorganizationsdk_testapplicationindex_measurements']

        self.assertEqual(case_measurment_all_spaces_expected, case_measurment_all_spaces)
        self.assertTrue(self.is_subset(case_analysis_all_spaces_expected, case_analysis_all_spaces))
        self.assertEqual(case_measurment_specific_space, case_measurment_specific_space_expected)

    def test_index_get_all_documents(self):
        result = self.client.index_get_all_documents(self.test_get_all_documents_index)
        first_document = {'title': 'Police reduce social use.',
                          'content': 'Hand go woman I adult decade responsibility put. Arrive theory choice no under.\nHow only describe natural foot official economy. Send security player away.',
                          'author': 'George Ellison'}
        last_document = {'title': 'Night manager not not which up economy.',
                         'content': 'Manage well time goal low fire behavior. Assume defense yeah share. Guy in manage practice indicate response.\nFinancial myself all difficult concern. Involve loss song. Positive pay budget speech.',
                         'author': 'Terry Green'}
        self.assertEqual(len(result), 20000)
        self.assertEqual(result[0], first_document)
        self.assertEqual(result[19999], last_document)

    def test_index_get_all_documents_generator(self):
        first_document = {'title': 'Police reduce social use.',
                          'content': 'Hand go woman I adult decade responsibility put. Arrive theory choice no under.\nHow only describe natural foot official economy. Send security player away.',
                          'author': 'George Ellison'}
        last_document = {'title': 'Night manager not not which up economy.',
                         'content': 'Manage well time goal low fire behavior. Assume defense yeah share. Guy in manage practice indicate response.\nFinancial myself all difficult concern. Involve loss song. Positive pay budget speech.',
                         'author': 'Terry Green'}
        res = [doc for doc in self.client.index_get_documents(self.test_get_all_documents_index)]
        self.assertEqual(len(res), 20000)
        self.assertEqual(res[0], first_document)
        self.assertEqual(res[19999], last_document)

    def test_index_get_first_document_from_generator(self):
        first = {'title': 'Police reduce social use.',
                 'content': 'Hand go woman I adult decade responsibility put. Arrive theory choice no under.\nHow only describe natural foot official economy. Send security player away.',
                 'author': 'George Ellison'}
        result = next(self.client.index_get_documents(self.test_get_all_documents_index))
        self.assertEqual(first, result)

    def test_index_get_last_document_from_generator(self):
        last = {'title': 'Night manager not not which up economy.',
                'content': 'Manage well time goal low fire behavior. Assume defense yeah share. Guy in manage practice indicate response.\nFinancial myself '
                           'all difficult concern. Involve loss song. Positive pay budget speech.',
                'author': 'Terry Green'}
        generator = self.client.index_get_documents(self.test_get_all_documents_index)
        result = None
        for doc in generator:
            result = doc
        self.assertEqual(last, result)

    def test_validatedJson(self):
        file_string = '{"authors": [], "data": [], "dateTime" : {"createdAt": "now"}, "description":"probably a string", "entities":[], "environment":{' \
                      '"name":"here"}, "name":"Maybe a string", "project": {"confidentiality": "None", "name": "a name", "purpose": "Dunno", "type": "some"}, ' \
                      '"scope": {"confidentiality": "None", "name": "a name", "purpose": "Dunno"} } '
        self.assertTrue(self.client._validate_json(file_string))
        self.assertFalse(self.client._validate_json("{'data': 'wrong json'}"))

    # @unittest.skip(reason='deactivated because this test runs too long (files have to be moved by ingest workflow)')
    def test_storage_upload_files(self):
        test_data_dir = 'tmp'
        magic_nr_testrun = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]

        testfile01 = f'test-upload-file01-{magic_nr_testrun}.txt'
        testfile02 = f'test-upload-file02-{magic_nr_testrun}.txt'
        files = [
            "meta.json",
            testfile01,
            testfile02,
        ]

        if not os.path.isdir(test_data_dir):
            os.mkdir(test_data_dir)

        f = open(f'{test_data_dir}/{testfile01}', 'w')
        f.write('a file to test uploading to the loading zone')
        f.close()
        f = open(f'{test_data_dir}/{testfile02}', 'w')
        f.write('another file to test uploading to the loading zone, surprise!')
        f.close()
        f = open(f'{test_data_dir}/meta.json', 'w')
        f.write(
                '{"authors": [], "data": [], "datetime" : {"createdat": "now"}, "description":"probably a string", "entities":[], "environment":{'
                '"name":"here"}, "name":"maybe a string", "project": {"confidentiality": "none", "name": "a name", "purpose": "dunno", "type": "some"}, '
                '"scope": {"confidentiality": "none", "name": "a name", "purpose": "dunno"} }')
        f.close()

        self.client.storage_upload_files(
                organization=self.test_org_name,
                space=self.test_space_name,
                files=files,
                local_dir=test_data_dir,
                chunked=False
        )

        uploaded_files = []
        files_in_space = []

        time_end = time.time() + 60 * 10  # 10 minutes timeout
        found_all = False
        print('Waiting for files to appear in loading zone', end='', flush=True)

        while time.time() < time_end and not found_all:
            uploaded_files = self.client.storage_list_blobs(self.test_org_name, 'loadingzone')
            found_all = True
            missing_files = []

            for file in files:
                expected_path_pattern = rf'[0-9]{{10}}/{re.escape(test_data_dir)}/{re.escape(file)}'
                if any(re.search(expected_path_pattern, uploaded_file) for uploaded_file in uploaded_files):
                    continue
                else:
                    missing_files.append(file)
                    found_all = False

            if not found_all:
                time.sleep(1)
                print('.', end='', flush=True)
        print('')

        # Assert all files were found, and print missing files if any
        if not found_all:
            print("Timeout reached. The following files were not found in the loading zone:")
            for missing_file in missing_files:
                print(f"  - {missing_file}")

        found = False
        print('Waiting for ingest to finish.', end='', flush=True)
        while time.time() < time_end and not found:
            files_in_space = self.client.storage_list_blobs(self.test_org_name, self.test_space_name)

            found = all(
                    any(re.search(rf'[0-9]{{10}}/{re.escape(test_data_dir)}/{re.escape(file)}', file_in_space)
                        for file_in_space in files_in_space)
                    for file in files
            )
            if found:
                break
            print('.', end='', flush=True)
            time.sleep(1)

        # Use regex for assertions
        for file in files:
            expected_path_pattern = rf'[0-9]{{10}}/{re.escape(test_data_dir)}/{re.escape(file)}'
            self.assertTrue(any(re.search(expected_path_pattern, uploaded_file) for uploaded_file in uploaded_files))
            self.assertTrue(any(re.search(expected_path_pattern, file_in_space) for file_in_space in files_in_space))

    def test_storage_download_files_with_regex(self):
        local_dir = 'tmp'
        files = [
            "test-file01.txt",
            "test-file02.txt"
        ]

        if not os.path.isdir(local_dir):
            os.mkdir(local_dir)

        self.client.storage_download_files_with_regex(organization=self.test_org_name, space=self.test_space_name,
                                                      local_dir=local_dir, regex='dir')
        actual = [os.path.join(dirpath, f) for (dirpath, dirnames, filenames) in os.walk(local_dir) for f in filenames]
        expected = {os.path.join(local_dir, 'test-dir', file) for file in files}
        self.assertTrue(self.is_subset(expected, actual))

        shutil.rmtree(local_dir)

    def test_custom_domain(self):
        """
        Tests, if the custom domain is also set for access- and organizationmanager-endpoints
        """
        domain = 'dev.sdk-cloud.de'
        client1 = sdk.SDKClient(domain=domain, username=self.user, password=self.pwd)
        domain_wildcard = domain.replace('.', '\\.')
        regex = rf'https?://{domain_wildcard}/.+'
        pattern = re.compile(regex)
        self.assertTrue(pattern.match(client1.org_endpoint),
                        f"org_endpoint '{client1.org_endpoint}' does not match the regular expression {regex}")
        self.assertTrue(pattern.match(client1.space_endpoint),
                        f"space_endpoint '{client1.space_endpoint}' does not match the regular expression {regex}")
        self.assertTrue(pattern.match(client1.accessmanager_url),
                        f"accessmanager_url '{client1.accessmanager_url}' does not match the regular expression {regex}")

    def is_subset(self, subset, superset):
        return set(subset).issubset(set(superset))

    # def test_storage_delete_files_azure(self):
    #     files = []
    #     self.client._storage_delete_files_azure(self.test_org_name, space=self.test_space_name, files = files, storage_dir= '.')

    @patch.object(requests.Session, 'get')
    @patch.object(requests.Session, 'delete')
    def test_index_get_documents_scroll_id_expired(self, mock_delete, mock_get):
        # Mock the initial get request to provide the first batch of documents and a scroll ID
        mock_response_initial = MagicMock()
        mock_response_initial.json.return_value = {
            '_scroll_id': 'DXF1ZXJ5QW5vbm1hb',
            'hits': {
                'hits': [
                    {'_source': {'title': 'First document', 'content': 'Content of the first document.', 'author': 'Author1'}}
                ]
            }
        }
        mock_get.side_effect = [mock_response_initial]

        # Mock the second get request to simulate a 404 error (scroll ID expired)
        mock_response_expired = MagicMock()
        mock_response_expired.raise_for_status.side_effect = HTTPError(response=MagicMock(status_code=404))
        mock_get.side_effect = [mock_response_initial, mock_response_expired]

        # Mock the delete request to clean up scroll ID
        mock_delete.return_value = MagicMock(status_code=404)

        # Collect documents from the generator
        documents = [doc for doc in self.client.index_get_documents(self.test_get_all_documents_index)]

        # Verify that only the initial document is returned and no exception was raised
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0], {'title': 'First document', 'content': 'Content of the first document.', 'author': 'Author1'})

        # Ensure the delete scroll ID call was made
        mock_delete.assert_called_once()

    def test_refresh_token(self):
        self.client._token_holder._refresh_tokens()


if __name__ == '__main__':
    unittest.main(verbosity=2)
