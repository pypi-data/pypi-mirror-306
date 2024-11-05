import base64
import hashlib
import os
import re
import textwrap
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from datetime import datetime
from logging import Logger
from typing import List, Generator, Dict, Any, Optional, Tuple, Union, Callable

import requests
from azure.core.exceptions import ClientAuthenticationError
from azure.storage.blob import BlobClient, BlobBlock, StorageErrorCode
from azure.storage.blob import ContainerClient
from azure.storage.blob._generated.models import BlockListType
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk
from requests import HTTPError

from ._internal_utils import TokenHolder, _sanitize_url, _insert_proxy_auth, \
    _parse_azp_from_token, _is_browser_available, _storage_access_info_should_be_renewed, _calculate_chunk_size, AzureStorageAccessInfo
from ._logger_config import _global_logger
from .config import _ENVS, _ACCESS_TOKEN_ENV_KEY, _REFRESH_TOKEN_ENV_KEY, _NR_WORKER_THREADS_UPLOAD


def get_init_message(**kwargs: Union[str, int]) -> str:
    msg = ""
    keys = kwargs.keys()
    for key in keys:
        value = kwargs[key]
        if key == 'password' or key == 'proxy_pass':
            value = '[not set]' if kwargs[key] == '' else '***'
        msg += f"  {key}: {value}\n"
    return msg


class SDKClient:
    f"""
    client class providing methods for accessing SDK services: 
        - organizationmanager (access to organizations/spaces)
        - opensearch
        - storage

    Authorization for the SDK services is done using JWT tokens, which are stored in memory.
    For every request, the access token is refreshed if it is about to expire or has already expired.
    If no login information is passed to the main class 'SDKClient' during initialization, the access and refresh tokens are expected to be stored in the 
    environment variables of the execution environment.

    Usage::
        If access/refresh token can be found int the env-variables {_ACCESS_TOKEN_ENV_KEY} / {_REFRESH_TOKEN_ENV_KEY}
        >>> import superbdataklient as sdk
        >>> client = sdk.SDKClient()

        or with explicit login:
        >>> import superbdataklient as sdk
        >>> client = sdk.SDKClient(username='hasslethehoff', password='lookingforfreedom')

        this module is pre configured for usage with the default instance of the SDK (found here https://app.sdk-cloud.de) and comes with settings for various
        different instances

        choosing different environment:
        >>> client = sdk.SDKClient(env='sdk-dev')

        overwriting settings:
        >>> client = sdk.SDKClient(domain='mydomain.ai', client_id='my-client-id', api_version='v13.37')
    """

    def __init__(self, logger: Logger = None, **kwargs: Union[str, int]) -> None:
        self._env = deepcopy(_ENVS.get(kwargs.get('env', 'sdk')))
        self.session = requests.Session()
        proxy_urls = {}
        _global_logger.set_logger(logger)

        # overwrite settings from args
        if 'domain' in kwargs:
            self._env.domain = kwargs.get('domain')
        if 'realm' in kwargs:
            self._env.realm = kwargs.get('realm')
        if 'client_id' in kwargs:
            self._env.client_id = kwargs.get('client_id')
        if 'api_version' in kwargs:
            self._env.api_version = kwargs.get('api_version')

        _global_logger.debug(f'Initializing SDK-Client with the following parameters: \n{get_init_message(**kwargs)}')
        # http-proxy
        proxy_url = kwargs.get('proxy_http', None)
        if proxy_url:
            proxy_urls['http'] = _insert_proxy_auth(proxy_url, kwargs.get('proxy_user'), kwargs.get('proxy_pass'))
        # https-proxy
        proxy_url = kwargs.get('proxy_https', None)
        if proxy_url:
            proxy_urls['https'] = _insert_proxy_auth(proxy_url, kwargs.get('proxy_user'), kwargs.get('proxy_pass'))
        if 'proxy_http' in kwargs or 'proxy_https' in kwargs:
            self.session.proxies.update(proxy_urls)

        self.org_endpoint = f'https://{self._env.domain}/organizationmanager/api/{self._env.api_version}/organization'
        self.space_endpoint = f'https://{self._env.domain}/organizationmanager/api/{self._env.api_version}/space'
        self.accessmanager_url = f'https://{self._env.domain}/accessmanager/api/v3/accessmanager/'

        # in-memory SAS token cache - requires thread-safe handling due to potential concurrent access.
        # performance is not a primary concern here, as the cache is expected to hold fewer than 100 entries, so we prefer Dict over Tuple for understandability
        self.storage_access_info_cache: Dict[str, AzureStorageAccessInfo] = dict()
        self.storage_access_info_cache_lock = threading.Lock()

        if 'username' in kwargs and 'password' in kwargs:
            self._token_holder = TokenHolder(domain=self._env.domain, realm=self._env.realm,
                                             client_id=self._env.client_id, session=self.session)
            self._token_holder.get_tokens_with_credentials(kwargs['username'], kwargs['password'])
        elif _ACCESS_TOKEN_ENV_KEY in os.environ and _REFRESH_TOKEN_ENV_KEY in os.environ:
            try:
                access_token = os.environ[_ACCESS_TOKEN_ENV_KEY]
                refresh_token = os.environ[_REFRESH_TOKEN_ENV_KEY]

                # Ensure the client_id from the tokens matches the configured client_id for the token refresh to work
                self._env.client_id = _parse_azp_from_token(access_token)

                self._token_holder = TokenHolder(domain=self._env.domain, realm=self._env.realm,
                                                 client_id=self._env.client_id, access_token=access_token,
                                                 refresh_token=refresh_token, session=self.session)
            except KeyError:
                _global_logger.error(
                        f'Cannot read token environment variables {_ACCESS_TOKEN_ENV_KEY}, {_REFRESH_TOKEN_ENV_KEY}')
                _global_logger.error(
                        'Assert that variables are set or try login initializing with username and password.')
        elif _is_browser_available():
            self._token_holder = TokenHolder(domain=self._env.domain, realm=self._env.realm,
                                             client_id=self._env.client_id, session=self.session)
            self._token_holder.get_tokens_by_authflow()
        else:
            self_service_url = f'https://{self._env.domain}/auth/realms/{self._env.realm}/account/'
            raise ClientInitializationError(textwrap.dedent(f"""
                Authentication failed due to missing credentials or missing tokens.

                The provided configuration is missing both a 'username' and 'password', and no OAuth tokens were set via environment variables 
                ({_ACCESS_TOKEN_ENV_KEY}, {_REFRESH_TOKEN_ENV_KEY}).
                Falling back on the authentication code flow failed because a browser environment is required and none is available.

                Please consider the following options:
                1. Use Basic Authentication:
                   Initialize the client with your username and password:
                       client = SDKClient(username="your_username", password="your_password")
                2. If your account is linked to an external identity provider and you do not have a password yet, 
                   you may need to set one via the self-service portal:
                   {self_service_url}
            """))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ organizations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def organization_get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves a list of all organizations that the user can access.

        :return: A list of dictionaries, where each dictionary contains details of an organization.
        """
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = self.session.get(self.org_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

    def organization_get_by_id(self, organization_id: int) -> Dict[str, Any]:
        """
        Retrieves details of the organization with the specified ID.

        :param organization_id: The ID of the organization to be fetched.

        :return: A dictionary containing details of the requested organization.

        """
        url = f'{self.org_endpoint}/{organization_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def organization_get_by_name(self, organization: str) -> Dict[str, Any]:
        """
        Retrieves details of the organization with the specified name.

        :param organization: The name of the organization to be fetched.

        :return: A dictionary containing details of the requested organization.
        """
        url = f'{self.org_endpoint}/name/{organization}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ spaces ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def space_get_all(self, organization_id: int) -> List[Dict[str, Any]]:
        """
        Retrieves a list of all spaces within the specified organization.

        :param organization_id: The unique identifier of the organization whose spaces need to be fetched.

        :return: A list of dictionaries, where each dictionary represents the details of a space within the organization.
        """
        url = f'{self.space_endpoint}/{organization_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def space_get_by_id(self, organization_id: int, space_id: int) -> Dict[str, Any]:
        """
        Retrieves details of a space within a specified organization using the space's name.

        :param organization_id: The unique identifier for the organization under which the space resides.
        :param space_id: The unique identifier of the space to retrieve.

        :return: A dictionary representing the details of the requested space as returned by the API.

        Note:
        Ensure that the provided token has the necessary permissions to access the space details.
        """
        url = f'{self.space_endpoint}/{organization_id}/{space_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def space_get_by_name(self, organization_id: int, space: str) -> Dict[str, Any]:
        """
        Retrieves details of a space within a specified organization using the space's name.

        :param organization_id: The unique identifier for the organization under which the space resides.
        :param space: The name of the space to retrieve.

        :return: A dictionary representing the details of the requested space as returned by the API.
        """
        url = f'{self.space_endpoint}/{organization_id}/name/{space}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def space_create(self, organization_id: int, space: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new space within a specified organization using its ID.

        :param organization_id: The unique identifier for the organization in which the space will be created.
        :param space: A dictionary containing attributes and properties for the new space.

        :return: A dictionary representing the created space as returned by the API.
        """
        url = f'{self.space_endpoint}/{organization_id}'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {self._token_holder.get_token()}'
        }
        response = self.session.post(url, json=space, headers=headers)
        response.raise_for_status()
        return response.json()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ indexing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def index_get_all(self) -> Dict[str, Any]:
        """
        Retrieves all the OpenSearch indices that are accessible.

        :param: None

        :return: A dictionary containing information about all the accessible indices.
        """
        headers = {
            "Authorization": f"Bearer {self._token_holder.get_token()}"
        }
        url = f'https://{self._env.domain}/search/{self._env.api_version}/index'
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        res = response.json()

        return res

    def index_search(self, index: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Executes a search query on the specified OpenSearch index and returns the matching documents.

        :param index: The name of the OpenSearch index to search.
        :param query: The search query represented as a dictionary, typically containing a DSL query structure.
        :return: A list of documents matching the search query. Each document is represented as a dictionary.

        Example:
        To search for documents with the title "sample" in the "MyIndex" index, you might use:
        `results = index_search("MyIndex", {"query": {"match": {"title": "sample"}}})`
        """
        headers = {
            "Authorization": f"Bearer {self._token_holder.get_token()}"
        }
        url = f'https://{self._env.domain}/elastic/api/{index}/_search'

        response = self.session.get(url, headers=headers, json=query)
        response.raise_for_status()
        res = [hit['_source'] for hit in response.json()['hits']['hits']]

        return res

    def index_get_document(self, index: str, doc_id: str) -> Dict[str, Any]:
        """
        Retrieves a specific document from the specified OpenSearch index using its document ID.

        :param index: The name of the OpenSearch index where the document resides.
        :param doc_id: The unique identifier of the desired document within the index.
        :return: The requested document represented as a dictionary.

        Example:
        To fetch a document with ID "doc123" from an index named "SampleIndex", you can call:
        `document = index_get_document("SampleIndex", "doc123")`
        """
        headers = {
            "Authorization": f"Bearer {self._token_holder.get_token()}"
        }
        url = f'https://{self._env.domain}/elastic/api/{index}/_doc/{doc_id}'
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        doc = response.json()['_source']

        return doc

    def _get_scroll_id_and_documents(self, url: str, headers: Dict[str, str]) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        response = self.session.get(url, headers=headers)
        response.raise_for_status()

        response_json = response.json()
        scroll_id = response_json.get('_scroll_id', None)
        documents = [hit['_source'] for hit in response_json.get('hits', {}).get('hits', [])]

        return scroll_id, documents

    def _delete_scroll_id(self, scroll_id: str, headers: Dict[str, str]) -> None:
        delete_url = f"https://{self._env.domain}/elastic/api/_search/scroll/{scroll_id}"
        self.session.delete(delete_url, headers=headers)

    def index_get_documents(self, index: str, scroll_duration: str = '10m', batch_size: int = 10000) -> Generator[Dict[str, Any], None, None]:
        """
        Retrieves documents from a specified OpenSearch index using a generator.

        This method employs the scrolling mechanism of OpenSearch to fetch documents
        in batches, ensuring efficient memory usage, especially for large datasets.
        Each batch fetches a specified number of documents at once.

        :param index: The name of the OpenSearch index from which to retrieve documents.
        :param scroll_duration: Duration a scroll ID remains valid in OpenSearch. It determines
                                the window to keep the search context alive. Defaults to '10m'.
        :param batch_size: Number of documents to fetch in each request to OpenSearch. Defaults to 10,000.

        :yield: Yields individual documents from the OpenSearch index.

        Example:
        To retrieve documents from an index named "SampleIndex" using the default scroll duration
        and batch size, use:
        `documents = [doc for doc in index_get_documents("SampleIndex")]`
        """
        headers = {
            "Authorization": f"Bearer {self._token_holder.get_token()}"
        }
        url = f"https://{self._env.domain}/elastic/api/{index}/_search?scroll={scroll_duration}&size={batch_size}"

        scroll_id, documents = self._get_scroll_id_and_documents(url, headers)
        # yield all documents in the first scroll
        for document in documents:
            yield document

        try:
            while True:
                url = f"https://{self._env.domain}/elastic/api/_search/scroll?scroll={scroll_duration}&scroll_id={scroll_id}"
                try:
                    scroll_id, documents = self._get_scroll_id_and_documents(url, headers)
                except HTTPError as e:
                    if e.response.status_code == 404:
                        # we need to gracefully handle when the scroll_id expires
                        _global_logger.error(
                                f"The Opensearch scroll id has expired. Consider setting a larger scroll_duration than '{scroll_duration}'")
                        break
                    else:
                        raise

                if len(documents) == 0:
                    # the last scroll is reached
                    break

                for document in documents:
                    yield document
        finally:
            # delete scroll context
            self._delete_scroll_id(scroll_id, headers)

    def index_get_all_documents(self, index: str) -> List[Dict[str, Any]]:
        """
        Retrieves all documents from a specified OpenSearch index.

        This method fetches every document from the named index and returns them
        as a list of dictionaries. If the index doesn't exist or is empty, the result
        will be an empty list.

        :param index: The name of the index from which to retrieve documents.
        :return: A list of all documents in the specified index. Each document is
                 represented as a dictionary. An empty list is returned if the index
                 doesn't contain any documents or doesn't exist.

        Example:
        To fetch all documents from an index named "SampleIndex", you can call:
        `all_docs = index_get_all_documents("SampleIndex")`

        Note:
        Ensure the OpenSearch instance is operational and the provided token has the
        necessary permissions to retrieve documents.
        """
        return [doc for doc in self.index_get_documents(index)]

    def index_documents(self, documents: List[Dict[str, Any]], index_name: str, timeout: int = 60,
                        chunk_size: int = 10000) -> None:
        """
        Indexes multiple documents into the specified index in chunks using the bulk API.

        This method establishes a connection to the Opensearch instance and performs
        bulk indexing of the provided documents. Chunking ensures efficient ingestion
        and helps avoid potential timeouts for large datasets.

        :param documents: A list of dictionaries representing the documents to be indexed.
        :param index_name: The name of the index where the documents will be stored.
        :param timeout: Maximum time (in seconds) to wait for a response during the bulk operation. Defaults to 60 seconds.
        :param chunk_size: The number of documents that are indexed in a single bulk operation. Defaults to 10,000.

        Example:
        To index a list of documents into an index named "SampleIndex", you can call:
        `index_documents(document_list, "SampleIndex")`
        """
        url = f'https://{self._env.domain}/elastic/api/'
        es = OpenSearch(url, use_ssl=True, headers={
            "Authorization": "Bearer " + self._token_holder.get_token()
        }, timeout=timeout)

        # Create data for bulk api
        actions = [{
            "_index": index_name,
            "_id": entry.pop('_id') if '_id' in entry else None,
            "_source": entry
        } for entry in documents]

        # Bulk ingest data
        bulk(es, actions, chunk_size=chunk_size)

        # Close Elasticsearch
        es.close()

    def index_filter_by_space(self, organization: str, space: str, index_type: str) -> List[str]:
        """
        Retrieves a list of indexes filtered by the specified organization, space, and index type.

        This method sends a GET request to the search endpoint, filtering indexes based on the provided
        organization name, space name, and index type. It's useful for narrowing down specific indexes
        associated with certain parameters.

        :param organization: The name of the organization associated with the desired indexes.
        :param space: The specific space or partition within the organization.
                      Use '*' to represent all spaces in the organization.
        :param index_type: Specifies the type of index to filter by, such as 'analysis' or 'measurement'.

        :return: A list containing details of the indexes that match the filter criteria.

        :raises: requests.exceptions.HTTPError If the request to filter the indexes fails.

        Example:
        To retrieve indexes of type 'analysis' for an organization "OrgName" and space "SpaceName", call:
        `indexes = index_filter_by_space("OrgName", "SpaceName", "analysis")`

        Note:
        Ensure that the provided token has the necessary permissions to retrieve index details.
        """
        headers = {
            "Authorization": f"Bearer {self._token_holder.get_token()}"
        }
        url = f'https://{self._env.domain}/search/{self._env.api_version}/index?filter={organization}_{space}_{index_type.lower()}*'
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        res = response.json()

        return res

    def application_index_create(self, index_name: str, organization: str, space: str, mapping: object,
                                 index_type: str = 'ANALYSIS') -> str:
        """
        Creates a new application index with the specified parameters.

        This method sends a POST request to the corresponding endpoint with the
        necessary data to create a new application index. The index can be utilized
        for various application-specific functionalities based on its type.

        :param index_name: A custom name assigned to the index for identification.
        :param organization: The name of the organization associated with the index.
        :param space: The specific space or partition within the organization where the index belongs.
        :param mapping: An object representing the structure and relationships of the data within the index.
        :param index_type: The type of the index. Defaults to 'ANALYSIS' if not provided.

        :return: The response body of the HTTP request, typically providing details or a confirmation of the index creation.

        :raises: requests.exceptions.HTTPError If the request to create the application index fails.

        Example:
        To create an index named "SampleIndex" for organization "OrgName" in space "SpaceName" with a specific mapping, you can call:
        `response = application_index_create("SampleIndex", "OrgName", "SpaceName", mapping_object)`
        """

        application_index = {
            "organizationName": organization,
            "spaceName": space,
            "customName": index_name,
            "indexType": index_type,
            "mappings": mapping
        }
        url = f'https://{self._env.domain}/metadata/{self._env.api_version}/application-index'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {self._token_holder.get_token()}'
        }
        response = self.session.post(url, json=application_index, headers=headers)
        response.raise_for_status()
        return response.text

    def application_index_delete(self, application_index_name: str) -> None:
        """
        Deletes the specified application index from the system.

        This method sends a DELETE request to the corresponding endpoint
        to remove an application index based on the provided name.

        :param application_index_name: The unique identifier or name of the application index to be deleted.

        :raises: requests.exceptions.HTTPError If the request to delete the application index fails

        Example:
        To delete an application index named "SampleIndex", you can call:
        `application_index_delete("SampleIndex")`
        """
        url = f'https://{self._env.domain}/metadata/{self._env.api_version}/application-index/{application_index_name}'
        headers = {
            "Authorization": f'Bearer {self._token_holder.get_token()}'
        }
        response = self.session.delete(url, headers=headers)
        response.raise_for_status()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ storage ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def storage_list_blobs(self, organization: str, space: str) -> List[str]:
        """
        Retrieves a list of blob names from the specified storage belonging to the given organization and space.

        :param organization: The name of the organization associated with the storage.
        :param space: The specific space within the organization's storage.

        :return: A list of string names representing the blobs in the specified container.

        Example:
        If you want to get a list of blobs from a storage container for "OrgName" in "SpaceName",
        you might call the function like this:
        `blobs = storage_list_blobs("OrgName", "SpaceName")`
        """
        sas_token = self._get_storage_access_info(organization, space, 'read')
        blob_client = ContainerClient.from_container_url(f'{sas_token.url}?{sas_token.token}')
        blobs = blob_client.list_blobs()
        result = [(b['name']) for b in blobs]
        return result

    def storage_upload_files(
            self,
            organization: str,
            space: str,
            files: List[str],
            local_dir: str,
            progress_callback: Callable[[int, int], None] = None,
            chunked: bool = True,
            concurrent: bool = True
    ) -> None:
        """
        Uploads specified files from a local directory to a designated storage location within a space belonging to a specific organization.

        If 'metadataGenerate' is not enabled on the space, a 'meta.json' file must be included in the list of files for validation.

        :param organization: str
            The name of the organization to which the space belongs.
        :param space: str
            The name of the space to which the files will be uploaded.
        :param files: List[str]
            List of file names to upload, relative to `local_dir`.
            Each file must exist in the specified local directory.
        :param local_dir: str
            The local directory path on your file system from where files are to be uploaded.
            This path should be accessible with appropriate read permissions.
        :param progress_callback: Optional[Callable[[int, int], None]]
            A callback function that is called with the number of bytes uploaded and the total file size.
            The function signature should be:
            def progress_callback(uploaded: int, total: int) -> None:
            where:
              - uploaded: The number of bytes that have been uploaded so far.
              - total: The total size of the file in bytes.
        :param chunked: bool
            If set to True, uploads files in chunks. Default is True.
        :param concurrent: bool
            If set to True, uploads files concurrently which should result in better throughput. Default is True.
        :return: None
            This method does not return a value.
            Any exceptions during the process must be handled by the calling function.
        :raises ValueError:
            If any required arguments are missing or if 'meta.json' is required but not provided.
            Also raised if a specified file does not exist in `local_dir`.
        :raises Exception:
            For any issues that occur during the file upload or commit process.
        """
        if not organization:
            raise ValueError('missing organization name arg')
        if not space:
            raise ValueError('missing space name arg')
        if not files:
            raise ValueError('missing files arg')
        if not local_dir:
            raise ValueError('missing local_dir arg')
        _global_logger.info(f'Uploading files from {local_dir} to {organization}/{space}')

        # if a progress_callback fn is given the upload has to be chunked
        chunked = chunked or progress_callback is not None

        # check if meta.json is needed and/or provided
        org_object = self.organization_get_by_name(organization=organization)
        space_object = self.space_get_by_name(organization_id=org_object['id'], space=space)
        if space_object['metadataGenerate'] is False and 'meta.json' not in files:
            raise ValueError('metadataGenerate on space not set and meta.json is missing - required for upload.')

        if space_object['metadataGenerate'] is False:
            json_file = open(f'{local_dir}/meta.json', 'r')
            json_string = json_file.read()
            json_file.close()
            validated = self._validate_json(json_string)
            if not validated:
                raise ValueError('meta.json invalid')

        # use the current timestamp as temporary directory to upload to the loadingzone
        remote_dir = datetime.now().strftime('%Y%m%d%H%M%S')

        _global_logger.debug(f'Uploading to directory {remote_dir}')
        files_log = "\n  " + "\n  ".join(files)
        _global_logger.debug(f'Uploading files: {files_log}')

        if not concurrent:
            # single threaded
            for file in files:
                file_path = os.path.join(local_dir, file)
                if not os.path.exists(file_path):
                    raise ValueError(f'File {file} does not exist in the specified directory.')
                self._upload_file(organization, space, file_path, remote_dir, chunked, progress_callback)
        else:
            # using ThreadPoolExecutor to parallelize the upload process
            with ThreadPoolExecutor(max_workers=_NR_WORKER_THREADS_UPLOAD) as executor:
                futures = []
                for file in files:
                    file_path = os.path.join(local_dir, file)
                    if not os.path.exists(file_path):
                        raise ValueError(f'File {file} does not exist in the specified directory.')
                    # submit the upload task to the executor
                    futures.append(executor.submit(self._upload_file, organization, space, file_path, remote_dir, chunked, progress_callback))
            # wait for all tasks to complete
            for future in as_completed(futures):
                future.result()  # will raise an exception if any occurred during upload

        _global_logger.debug('Uploading files... Done')
        # start the ingest workflow
        _global_logger.debug(f'Comitting upload {organization}/{space}/{remote_dir}...')
        url = f'{self.accessmanager_url}/commit'
        url = _sanitize_url(url)

        payload = {
            'organization': organization,
            'space': space,
            'rootDir': remote_dir
        }
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }

        try:
            response = self.session.post(url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            _global_logger.info(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
        except requests.exceptions.ConnectionError as conn_err:
            _global_logger.info(f"Connection error occurred: {conn_err}")  # Handle connection errors
        except requests.exceptions.Timeout as timeout_err:
            _global_logger.info(f"Timeout error occurred: {timeout_err}")  # Handle timeout errors
        except requests.exceptions.RequestException as req_err:
            _global_logger.info(f"An error occurred: {req_err}")  # Handle all other request exceptions

        _global_logger.debug(f'Committing upload {organization}/{space}/{remote_dir}... Done')

    def _upload_file(self, organization, space, file_path, remote_dir, chunked, progress_callback):
        try:
            if chunked:
                self._upload_file_azure_chunked(organization, space, file_path=file_path, remote_dir=remote_dir, progress_callback=progress_callback)
            else:
                self._upload_file_azure(organization, space, file_path=file_path, remote_dir=remote_dir)
            _global_logger.info(f'Uploading file {file_path}... Done')
        except Exception as e:
            _global_logger.error(f"Failed to upload file {file_path}: {e}")
            raise

    def _upload_file_azure(
            self,
            organization: str,
            space: str,
            remote_dir: str,
            file_path: str
    ) -> None:
        """
        Uploads a file to Azure Blob Storage within a specified directory for a given organization and space.

        The method retrieves a SAS token for secure uploading, checks if the file already exists,
        and handles authentication errors by retrying up to a maximum number of attempts if needed.

        :param organization: The name of the organization that owns the storage.
        :param space: The name of the space within the organization where the file will be uploaded.
        :param remote_dir: The remote directory path in Azure Blob Storage where the file will be stored.
        :param file_path: The local path of the file to be uploaded.

        :raises ClientAuthenticationError: If SAS token authorization fails and cannot be refreshed.
        :raises Exception: For any other errors encountered during the upload process.
        """

        def get_blob_url():
            sas_token = self._get_storage_access_info(organization, space, reqtype='upload')
            return _sanitize_url(f'{sas_token.url}/{remote_dir}/{file_path}?{sas_token.token}')

        blob_url = get_blob_url()
        retries = 0
        max_retries = 3

        while retries < max_retries:
            with BlobClient.from_blob_url(blob_url) as blob_client:
                try:
                    if not blob_client.exists():
                        with open(file_path, "rb") as data:
                            blob_client.upload_blob(data)
                        break
                    else:
                        _global_logger.warn(f"The file already exists in the loadingzone: {file_path}")

                except ClientAuthenticationError as e:
                    error_message = str(e)
                    error_code = getattr(e, 'error_code', None)
                    retries += 1

                    if 'Signature not valid in the specified time frame' in error_message or (error_code == StorageErrorCode.AUTHENTICATION_FAILED):
                        _global_logger.debug(f"SAS token expired: {e}")
                        _global_logger.debug("Getting new SAS token and continuing upload...")
                        blob_url = get_blob_url()
                        continue  # Retry the upload
                    else:
                        _global_logger.error(f"Authentication failed: {e}")
                        raise
                except Exception as e:
                    _global_logger.error(f"An error occurred during upload: {e}")
                    raise

    def _upload_file_azure_chunked(
            self,
            organization,
            space,
            remote_dir: str,
            file_path: str,
            chunk_size: int = None,
            progress_callback=None
    ) -> None:
        """
        Uploads a large file to Azure Blob Storage in chunks.

        This method uploads a specified file to Azure Blob Storage in chunks, which helps manage large file uploads
        without exceeding memory limits. It can resume partially completed uploads by skipping already uploaded chunks.
        A progress callback function can also be provided to monitor the upload progress.

        :param organization: The name of the organization that owns the storage.
        :param space: The name of the space within the organization where the file will be uploaded.
        :param remote_dir: The remote directory path in Azure Blob Storage where the file will be stored.
        :param file_path: The local path of the file to be uploaded.
        :param chunk_size: The size of each chunk in bytes. If not provided, it is calculated based on the file size.
        :param progress_callback: A callback function that is called with the number of bytes uploaded and the total file size.
                                  The function signature should be:
                                  def progress_callback(uploaded: int, total: int) -> None:
                                  where:
                                      - uploaded: The number of bytes that have been uploaded so far.
                                      - total: The total size of the file in bytes.

        :raises ClientAuthenticationError: If SAS token authorization fails during the upload.
        :raises Exception: For other errors encountered during the upload process.
        """
        file_size = os.path.getsize(file_path)

        if not chunk_size:
            chunk_size_used = _calculate_chunk_size(file_size)
        else:
            chunk_size_used = chunk_size

        num_chunks = (file_size // chunk_size_used) + 1

        _global_logger.debug(f'uploading {num_chunks} chunks')

        def get_blob_url():
            storage_access_info = self._get_storage_access_info(organization, space, reqtype='upload')
            return _sanitize_url(f'{storage_access_info.url}/{remote_dir}/{file_path}?{storage_access_info.token}')

        blob_url = get_blob_url()

        def get_block_id(chnk_nr):
            return base64.b64encode(f"{chnk_nr:08d}".encode()).decode()

        while True:
            try:
                with BlobClient.from_blob_url(blob_url) as blob_client:
                    if not blob_client.exists():
                        block_list = []
                        uploaded_blocks = set()

                        # Get the list of already uploaded blocks (uncommitted)
                        try:
                            block_list_response = blob_client.get_block_list(block_list_type=BlockListType.UNCOMMITTED)
                            uploaded_blocks = set(block.id for block in block_list_response[1])
                            _global_logger.debug(f"Uploaded blocks: {uploaded_blocks}")
                        except Exception as e:
                            _global_logger.debug(f"No uncommitted blocks found: {e}")

                        with open(file_path, "rb") as data:
                            uploaded_size = 0
                            for chunk_number in range(num_chunks):
                                blk_id = get_block_id(chunk_number)

                                if blk_id in uploaded_blocks:
                                    _global_logger.debug(f"Chunk {chunk_number} already uploaded, skipping.")
                                    data.seek(chunk_size_used, os.SEEK_CUR)
                                    uploaded_size += min(chunk_size_used, file_size - uploaded_size)
                                    if progress_callback:
                                        progress_callback(uploaded_size, file_size)
                                    continue

                                _global_logger.debug(f"Uploading chunk {chunk_number}")
                                chunk = data.read(chunk_size_used)
                                if not chunk:
                                    break  # End of file

                                blob_client.stage_block(block_id=blk_id, data=chunk)
                                block_list.append(BlobBlock(block_id=blk_id))

                                uploaded_size += len(chunk)
                                if progress_callback:
                                    progress_callback(uploaded_size, file_size)

                        # Final commit for all staged blocks
                        if block_list:
                            # Combine uploaded blocks and new blocks
                            all_block_ids = uploaded_blocks.union(set(block.id for block in block_list))
                            # Convert to list and sort
                            all_block_ids = list(all_block_ids)
                            all_block_ids.sort(key=lambda x: int(base64.b64decode(x).decode()))
                            # Create BlobBlock objects
                            all_blocks = [BlobBlock(block_id=blk_id) for blk_id in all_block_ids]
                            # Commit the block list
                            blob_client.commit_block_list(all_blocks)
                    else:
                        _global_logger.warn(f"The file already exists in the loading zone: {file_path}")
                    break  # Upload succeeded; exit retry loop
            except ClientAuthenticationError as e:
                error_message = str(e)
                error_code = getattr(e, 'error_code', None)

                if 'Signature not valid in the specified time frame' in error_message or (error_code == StorageErrorCode.AUTHENTICATION_FAILED):
                    _global_logger.debug(f"SAS token expired: {e}")
                    _global_logger.debug("Refreshing SAS token and continuing upload...")
                    blob_url = get_blob_url()
                    continue  # Retry the upload
                else:
                    _global_logger.error(f"Authentication failed: {e}")
                    raise
            except Exception as e:
                _global_logger.error(f"An error occurred during upload: {e}")
                raise

    def storage_download_files(self, organization: str, space: str, files: List[str], local_dir: str,
                               storage_dir: str = '') -> None:
        """
        Downloads specified files from a storage directory to a local directory.
        Files can be nested in the storage and will retain their nested structure when downloaded locally.

        :param organization: The name of the organization that owns the storage.
        :param space: The specific space within the organization's storage to access.
        :param files: List of file names or relative paths to be downloaded from the storage directory.
        :param local_dir: The local directory path where the files will be downloaded.
        :param storage_dir: The directory within the storage space to locate the files. Defaults to the root directory
                            if not provided.

        Example:
        To download files 'doc1.txt' and 'folder/doc2.txt' from the 'docs' directory in storage,
        you might call the function like this:
        `storage_download_files("OrgName", "SpaceName", ["doc1.txt", "folder/doc2.txt"], "/local/path", "docs")`
        """
        return self._storage_download_files_azure(organization, space, files, local_dir, storage_dir)

    def _storage_download_files_azure(self, organization: str, space: str, files: List[str], local_dir: str,
                                      storage_dir: str = '') -> None:
        """
        Download files from Azure storage directory to local directory.

        For nested blobs, local directories are created inside the temporary directory as well.

        :param organization: organization name
        :param space: space name
        :param storage_dir: root directory inside the space to be used
        :param files: list of files to be downloaded
        :param local_dir: local directory to download the files to
        """
        if not organization:
            raise ValueError('missing organization name arg')
        if not space:
            raise ValueError('missing space name arg')
        if not files:
            raise ValueError('missing files arg')
        if not local_dir:
            raise ValueError('missing local_dir arg')

        sas_token = self._get_storage_access_info(organization, space, 'read')

        # download blobs to local directory
        for file in files:
            blob_url = _sanitize_url(f'{sas_token.url}/{storage_dir}/{file}?{sas_token.token}')
            with BlobClient.from_blob_url(blob_url) as blob_client:
                dest_file = os.path.join(local_dir, file)

                # for nested blobs, create local path as well!
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)

                with open(dest_file, "wb") as f:
                    data = blob_client.download_blob()
                    data.readinto(f)

    def storage_download_files_with_regex(self, organization: str, space: str, local_dir: str, regex: str,
                                          storage_dir: str = '') -> None:
        """
        Downloads files from a specified storage directory to a local directory based on a provided regular expression.

        This function searches for files in the storage directory that match the provided regular expression pattern.
        The full path of each file is considered during the pattern matching. Only the matching files are then downloaded
        to the specified local directory.

        :param organization: The name of the organization that owns the storage.
        :param space: The specific space within the organization's storage to search.
        :param local_dir: The local directory path where matching files will be downloaded.
        :param regex: The regular expression pattern used to filter files based on their full paths. Only files with paths matching this pattern will be
            considered for download.
        :param storage_dir: The directory within the storage space to search for files. Defaults to the root directory if not provided.

        Example:
        If we want to download all '.txt' files from the 'docs' directory in the storage,
        we might call the function like this:
        `storage_download_files_with_regex("OrgName", "SpaceName", "/local/path", r"docs/.*\.txt$")`
        """
        files = self.storage_list_blobs(organization, space)
        files_to_download = []

        for file in files:
            if storage_dir in file:
                x = re.search(regex, file)
                if x:
                    files_to_download.append(file)
        self.storage_download_files(organization, space, files_to_download, local_dir)

    def _validate_json(self, file: str) -> bool:
        """
        Validates the given json
        :param file:
            The json
        :return:
            Returns a bool, to show if the json is valid or not
        """
        url = f'https://{self._env.domain}/metadata/{self._env.api_version}/validateJson'
        payload = file
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }

        response = self.session.post(url, headers=headers, data=payload)
        if 200 <= response.status_code < 300:  # valid meta.json
            return True
        if 400 <= response.status_code < 500:  # invalid meta.json
            return False
        else:
            response.raise_for_status()

    def _get_storage_access_info(self, organization: str, space: str, reqtype: str = 'read') -> AzureStorageAccessInfo:
        """
        Retrieves a SAS token and URL for Azure Blob Storage, managing caching and renewal.

        This method uses a cache to store `AzureStorageAccessInfo` objects, which include both the SAS token and the
        URL based on a key derived from the organization, space and request type. It checks if the cached token is
        still valid or if a new one needs to be generated. If renewal is necessary, it fetches a new token and updates
        the cache. Thread-safe cache updates are ensured using a lock mechanism to handle potential concurrent access.
        """
        storage_access_info_cache_key_string = str((organization, space, reqtype))
        storage_access_info_cache_key = hashlib.md5(storage_access_info_cache_key_string.encode()).hexdigest()

        # first attempt to get the token from cache (reads are thread-safe)
        if storage_access_info_cache_key in self.storage_access_info_cache:
            storage_access_info = self.storage_access_info_cache[storage_access_info_cache_key]
            if not _storage_access_info_should_be_renewed(storage_access_info.token):
                return storage_access_info

        # acquire lock before modifying the cache
        with self.storage_access_info_cache_lock:
            # renew token
            if storage_access_info_cache_key in self.storage_access_info_cache:
                storage_access_info = self.storage_access_info_cache[storage_access_info_cache_key]
                if _storage_access_info_should_be_renewed(storage_access_info.token):
                    storage_access_info_new = self._fetch_storage_access_info(organization=organization, space=space, reqtype=reqtype)
                    self.storage_access_info_cache[storage_access_info_cache_key] = storage_access_info_new
            # generate token and cache entry
            else:
                storage_access_info = self._fetch_storage_access_info(organization=organization, space=space, reqtype=reqtype)
                self.storage_access_info_cache[storage_access_info_cache_key] = storage_access_info

        return self.storage_access_info_cache[storage_access_info_cache_key]

    def _fetch_storage_access_info(self, organization: str, space: str, reqtype: str = 'read') -> AzureStorageAccessInfo:
        """
        Fetches a new Azure Storage SAS token for the specified organization and space.

        This method communicates with the access manager to generate a SAS token for the Azure Blob Storage,
        allowing access based on the request type (e.g., read, upload, or delete). The generated token is used
        to securely access storage resources.
        """
        url = f'{self.accessmanager_url}/{reqtype}'
        url = _sanitize_url(url)

        payload = {
            'organization': organization,
            'space': space
        }
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }

        try:
            response = self.session.post(url, headers=headers, json=payload)
            response.raise_for_status()

            return AzureStorageAccessInfo.from_json(response.json())
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            raise RuntimeError(f"Failed to get SAS token: {e}")
        except ValueError as ve:
            # Handle missing token
            raise RuntimeError(f"Failed to get SAS token: {ve}")
        except Exception as ex:
            # Catch all other potential issues
            raise RuntimeError(f"An unexpected error occurred: {ex}")

    def _storage_delete_files_azure(self, organization: str, space: str, files: List[str], storage_dir: str) -> None:
        """
        Deletes files from azure
        :param organization:
        :param space:
        :param files:
        :param storage_dir:
        """
        if not organization:
            raise ValueError('missing organization name arg')
        if not space:
            raise ValueError('missing space arg')
        if not files:
            raise ValueError('missing files arg')
        if not storage_dir:
            raise ValueError('missing storage_dir arg')

        sas_token = self._get_storage_access_info(organization, space, 'delete')

        for file in files:
            blob_url = _sanitize_url(f'{sas_token.url}/{storage_dir}/{file}?{sas_token.token}')
            with BlobClient.from_blob_url(blob_url) as blob_client:
                if blob_client.exists():
                    blob_client.delete_blob()


class ClientInitializationError(Exception):
    """Exception raised for errors in the client initialization process."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
