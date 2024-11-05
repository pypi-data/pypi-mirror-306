# Data utilities for EO4EU

This package provides classes and functions that help with common tasks involving:

- Reading data from configMaps and secrets
- Uploading to and downloading from S3 buckets
- Configuring components in general

## Installation

`eo4eu-data-utils` is published on [PyPI](https://pypi.org/project/eo4eu-data-utils/) and can be installed with `pip` anywhere. You can look for the latest version and pin that in your `requirements.txt` or what-have-you.

## Usage

For example usage of this package, you may refer to [post-pro](https://git.apps.eo4eu.eu/eo4eu/eo4eu-provision-handler/post-pro), [jupyter-openfaas](https://git.apps.eo4eu.eu/eo4eu/eo4eu-openfaas-operations/jupyter-openfaas) or [jupyter-proxy](https://git.apps.eo4eu.eu/eo4eu/eo4eu-openfaas-operations/jupyter-proxy).

### ConfigMaps and Secrets

You can use the legacy API if you want something similar to `get_configMap` and `get_secret`:

```py
from eo4eu_data_utils.legacy import ClusterAccess

access = ClusterAccess()

BOTO_CONFIG = {
    "region_name":           access.cfgmap("s3-access", "region_name"),
    "endpoint_url":          access.cfgmap("s3-access", "endpoint_url"),
    "aws_access_key_id":     access.secret("s3-access-scr", "aws_access_key_id"),
    "aws_secret_access_key": access.secret("s3-access-scr", "aws_secret_access_key"),
}
```

It is recommended that you use `eo4eu_data_utils.config.Config` instead, which is described after S3 Access.

### S3 Access

The old `StorageUtils` class is supported:

```py
from eo4eu_data_utils.legacy import StorageUtils

ap = StorageUtils(config_boto=CONFIG_BOTO, config_cloudpath=CONFIG_CLOUD)
```

But the new one is more convenient; you specify the bucket when creating it and you don't have to keep track of it for every call:

```py
from eo4eu_data_utils.storage import Datastore

datastore = Datastore(
    config = CONFIG_BOTO,  # exactly the same config dict as before
    bucket = BUCKET_NAME
)
```

List files in bucket:

```py
files = datastore.list_files(subfolder, subsubfolder, ...)  # paths for (nested) subfolders are optional
```

Download and upload bytes:

```py
file_data = datastore.download(s3_key)
succeeded: bool = datastore.upload(other_s3_key, file_data)
```

Download and upload files:

```py
dl_succeeded: bool = datastore.download_to(s3_key, local_path)
up_succeeded: bool = datastore.upload_from(local_path, s3_key)
```

Download and upload many files at once:

```py
dl_s3_keys = ["data/d0.csv", "data/d1.csv", "data/img.tiff"]
dl_output_dir = "download_dir"
dl_result = datastore.download_many(dl_s3_keys, dl_output_dir)

up_s3_keys = ["output/result_0/meta.json", "output/result_0/r0.csv"]
up_input_dir = "output"
up_result = datastore.upload_many(up_s3_keys, up_input_dir)
```

Here the variables `dl_result` and `up_result` are of the class `eo4eu_data_utils.storage.TransferResult` and contain the succeeded and failed transfers. Example:

```py
for success in dl_result.succeeded:
    logger.info(f"Downloaded {success.src} to {success.dst}")

for failure in dl_result.failed:
    logger.warning(f"Failed to download {failure.src} to {failure.dst}")
```

You can check the number of successses/failures by way of `TransferResult.succeeded_num` and `TransferResult.failed_num`, or just get the `len` of the above lists.


### Configuration

The `Config` class allows you to define a configuration dict and fill it in different ways depending on whether you're on dev or prod. For example:

```py
from eo4eu_data_utils.config import Config, Try

unfilled_config = Config(
    boto = {
        "region_name":           Try.cfgmap("s3-access", "region_name"),
        "endpoint_url":          Try.cfgmap("s3-access", "endpoint_url"),
        "aws_access_key_id":     Try.secret("s3-access-scr", "aws_access_key_id"),
        "aws_secret_access_key": Try.secret("s3-access-scr", "aws_secret_access_key"),
    },
    eo4eu = {
        "namespace":      Try.cfgmap("eo4eu", "namespace"),
        "s3_bucket_name": Try.cfgmap("eo4eu", "s3-bucket-name"),
    },
    # ...
)
```

The values may be accessed as nested attributes or dict items:

```py
# all of these are valid
key_id = config.boto.aws_access_key_id
key_id = config.boto["aws_access_key_id"]
key_id = config["boto"].aws_access_key_id
key_id = config["boto"]["aws_access_key_id"]
```

This means that `config.boto` is *not* a python dict. If you need a dict, you can convert it like so:

```py
client = boto3.client(**config.boto.to_dict())
```

### Filling the configuration

On prod, you can fill an unfilled config from the configMaps and secrets on the cluster:

```py
config = unfilled_config.use_files().fill()
```

On dev, you can fill it from environment variables:

```py
config = unfilled_config.use_env().fill()
```

For the previous example, the environment variables must be of the form:
```sh
export CONFIGMAPS_S3_ACCESS_REGION_NAME=
export CONFIGMAPS_S3_ACCESS_ENDPOINT_URL=
export CONFIGMAPS_EO4EU_NAMESPACE=
export CONFIGMAPS_EO4EU_S3_BUCKET_NAME=

export SECRETS_S3_ACCESS_SCR_AWS_ACCESS_KEY_ID=
export SECRETS_S3_ACCESS_SCR_AWS_SECRET_ACCESS_KEY=
```

Some common configs are defined in [eo4eu_data_utils.config](https://git.apps.eo4eu.eu/eo4eu/eo4eu-provision-handler/eo4eu-data-utils/-/blob/main/eo4eu_data_utils/config/defaults.py), you may want to take a look at them.

You can automatically convert the `Try` values to different types and set default values to be used in case they are not found:

```py
from eo4eu_data_utils.config import Config, Try

unfilled_config = Config(
    # ...
    elasticsearch = {
        "username":    Try.secret("els-access-scr", "username"),
        "password":    Try.secret("els-access-scr", "password"),
        "local_dir":   Try.cfgmap("els", "local").default("els_dir").to_path(),  # i.e. pathlib.Path
        "max_retries": Try.cfgmap("els", "max_retries").default(10).to_int()
    }
)
```

In the above example, it should be noted that the order of methods matters. If `/configmaps/els/local` doesn't exist, it will be replaced with the default value `"els_dir"` and *then* converted to a path. If the order was switched, it would first try to convert the missing value to a path, fail, and then return the string `"els_dir"`. It is recommended that you put all your type converters at the end to ensure the result is of the desired type.

A third constructor for `Try` is provided: `Try.source`. This is different to `cfgmap` and `secret` in that it doesn't assume it's a file in `/configmaps` or `/secrets`. It's there to provide extra configuration, for example:

```py
from eo4eu_data_utils.config import Config, Try

unfilled_config = Config(
    # ...
    testing = {
        "raise_exceptions": Try.source("debug", "raise_exceptions").default(False).to_bool(),
        "max_retries":      Try.source("http", "max_retries").default(5).to_int(),
    },
)
```

These can be filled from environment variables:

```py
config = unfilled_config.use_env().fill()
```

With:

```sh
export DEBUG_RAISE_EXCEPTIONS=true
export HTTP_MAX_RETRIES=10
```

Or, alternatively, you can use a simple python dictionary:

```py
input = {
    "debug": {
        "raise_exceptions": True,
        "delete_output": False,  # extra keys get ignored
    },
    "http": {
        "max_retries": 10
    },
}

config = unfilled_config.use_dict(input).fill()
```

Or a JSON string:

```py
input ="""{
    "debug": {
        "raise_exceptions": true
    },
    "http": {
        "max_retries": 10
    }
}"""

config = unfilled_config.use_json(input).fill()
```

You can chain different sources of inputs, and the config will look through them until it finds a match.

```py
config = unfilled_config.use_env().use_dict(input).fill()
```

Finally, passing `raise_on_err = True` into `Config.fill` will raise a `ValueError` if a field was unable to be filled:

```py
try:
    config = unfilled_config.use_files().fill(raise_on_err = True)
except Exception as e:
    logger.error(f"Unable to fill configuration: {e}")
```
