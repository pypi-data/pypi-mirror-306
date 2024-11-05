![PyPI - License](https://img.shields.io/pypi/l/superb-data-klient)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/superb-data-klient)
![PyPI](https://img.shields.io/pypi/v/superb-data-klient?label=version)
![PyPI - Downloads](https://img.shields.io/pypi/dm/superb-data-klient)


# superb-data-klient


**superb-data-klient** offers a streamlined interface to access various services of the *Superb Data Kraken platform* (**SDK**). With the library, you can
effortlessly fetch and index data, manage indices, spaces and organizations on the **SDK**.

Designed primarily for a Jupyter Hub environment within the platform, it's versatile enough to be set up in other environments too.


## Installation and Supported Versions

```console
$ python -m pip install superb-data-klient
```

## Usage


### Authentication


To begin, authenticate against the SDK's OIDC provider. This is achieved when instantiating the client object:

1. **System Environment Variables** (recommended for Jupyter environments):
    ```python
    import superbdataklient as sdk
    client = sdk.SDKClient()
    ```
   This approach leverages environment variables **SDK_ACCESS_TOKEN** and **SDK_REFRESH_TOKEN**.


2. **Login Credentials**:
    ``` python
    import superbdataklient as sdk
    sdk.SDKClient(username='hasslethehoff', password='lookingforfreedom')
    ```

3. **Authentication Code Flow**:

   If none of the above mentioned authentication methods fit, authentication is fulfilled via code-flow.

   **CAUTION** Beware that this method only works in a browser-environment.

**NOTE:** If your user account was linked from an external identity provider, your account in the SDK identity provider (Keycloak) does not have a password by default. To enable login via basic authentication, you need to set a password through self-service first.

Follow these steps to set your password:

1. Go to the self-service portal for your environment:
   - [https://{domain}/auth/realms/{realm}/account/](https://{domain}/auth/realms/{realm}/account/).
   - e.g. [https://app.sdk-cloud.de/auth/realms/efs-sdk/account/](https://app.sdk-cloud.de/auth/realms/efs-sdk/account/).
2. Set a password for your account.
3. Once the password is set, you can log in using basic authentication (option 2).

### Configuration


While the default settings cater to the standard SDK instance, configurations for various other instances are also available.


#### Setting Environment

``` python
import superbdataklient as sdk
client = sdk.SDKClient(env='sdk-dev')
client = sdk.SDKClient(env='sdk')
```

#### Overwriting Settings

``` python
client = sdk.SDKClient(domain='mydomain.ai', realm='my-realm', client_id='my-client-id', api_version='v13.37')
```


#### Proxy
To use the SDK Client behind a company proxy a user might add the following config parameters to the constructor.  
**NOTE**: The environment Variables "http_proxy" and "https_proxy" will overwrite the settings in the SDKClient. 
So remove them before configuring the SDKClient.
```python
client = SDKClient(username='hasslethehoff', 
                   password='lookingforfreedom', 
                   proxy_http="http://proxy.example.com:8080", 
                   proxy_https="https://proxy.example.com:8080", 
                   proxy_user="proxyusername", 
                   proxy_pass="proxyuserpassword")
```

#### Logging
Our flexible logging-functionality allows you to pass a user-defined logger. This makes it easier to integrate the log output of the class into an existing logging framework.
The logger can be passed as an argument during the initialization of the `SDKClient` instance. If this is the case, log messages are automatically forwarded to this logger in the various methods - otherwise logging will be printed to `stdout` / `stderr`.

```python
import logging
from superbdataklient import SDKClient

# Logger konfigurieren
my_logger = logging.getLogger('sdk_logger')
my_logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
my_logger.addHandler(console_handler)

# Logger an SDKClient übergeben
client = SDKClient(logger=my_logger)
```

---
### Examples


#### Organizations


Get details of all organizations, or retrieve by ID or name:

``` python
client.organization_get_all()
client.organization_get_by_id(1337)
client.organization_get_by_name('my-organization')
```

#### Spaces


To retrieve spaces related to an organization:

``` python
organization_id = 1234
client.space_get_all(organization_id)
client.space_get_by_id(organization_id, space_id)
client.space_get_by_name(organization_id, space)
```

#### Index


<!--
TODO: implement after search service works without all_access ()

List all accessible indices:

``` python
indices = client.index_get_all()
```
-->

Retrieve a specific document:

``` python
document = client.index_get_document(index_name, doc_id)
``` 

Fetch all documents within an index:

``` python
documents = client.index_get_all_documents("index_name")
```

Iterate through documents using a generator:

``` python
documents = client.index_get_documents("index-name")
for document in documents:
   print(document)
```

Index multiple documents:

``` python
documents = [
   {"_id": 123, "name": "document01", "value": "value"},
   {"_id": 1337, "name": "document02", "value": "value"}
]
index_name = "index"
client.index_documents(documents, index_name)
``` 

Note: The optional **_id** field is used as the document ID for indexing in OpenSearch.

Filter indices by organization, space, and type:

``` python
client.index_filter_by_space("my-organization", "my-space", "index-type")
```

For all spaces in an organization, use `*` instead of a space name. Available **index_type** values are **ANALYSIS** or **MEASUREMENTS**.

Create an application index:

``` python
mapping = {
   ...
}
client.application_index_create("my-application-index", "my-organization", "my-space", mapping)
```

Remove an application index by its name:

``` python
client.application_index_delete("my-organization_my-space_analysis_my-application-index")
```

#### Storage


List files in Storage:

``` python
files = client.storage_list_blobs("my-organization", "space")
```

Download specific files from Storage:

``` python
files = ['file01.txt', 'directory/file02.json']
client.storage_download_files(organization='my-organization', space='my-space', files=files, local_dir='tmp')
```

Use regex patterns for file downloads:

``` python
files = ['file01.txt', 'directory/file02.json']
client.storage_download_files_with_regex(organization='my-organization', space='my-space', files=files, local_dir='tmp', regex=r'.*json$')
```

Upload files from a local directory. Ensure the presence of a valid `meta.json` if the `metadataGenerate` property on the space is not set to `true`:

``` python
files = ['meta.json', 'file01.txt', 'file02.txt']
client.storage_upload_files(organization='my-organization', space='my-space', files=files, local_dir='tmp')
```

If you want to monitor the status of the upload, you can pass a `progress_callback` function with the following function-signature:

``` python
def progress_callback(uploaded: int, total: int) -> None:
```

where:
- `uploaded`: The number of bytes that have been uploaded so far.
- `total`: The total size of the file in bytes.

``` python
def progress_callback(uploaded, total):
    # do something to update the progress-bar

files = ['meta.json', 'file01.txt', 'file02.txt']
client.storage_upload_files(organization='my-organization', space='my-space', files=files, local_dir='tmp', progress_callback=progress_callback)
```
