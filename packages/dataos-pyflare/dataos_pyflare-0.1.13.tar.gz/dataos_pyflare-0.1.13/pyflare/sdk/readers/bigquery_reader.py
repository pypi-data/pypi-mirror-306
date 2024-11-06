import base64
import json
import tempfile

from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.readers.file_reader import Reader
from pyflare.sdk.utils import pyflare_logger, generic_utils


class BigqueryInputReader(Reader):

    def __init__(self, read_config: ReadConfig):
        super().__init__(read_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)

    def read(self):
        spark_options = self.read_config.spark_options
        io_format = self.read_config.io_format
        dataset_path = "{}.{}.{}".format(self.read_config.spark_options.get("parentProject", ""),
                                         self.read_config.collection(), self.read_config.dataset_name())
        if spark_options:
            df = self.spark.read.options(**spark_options).format(io_format).load(dataset_path)
        else:
            df = self.spark.read.format(io_format).load(dataset_path)
        return df

    def read_stream(self):
        pass

    def get_conf(self):
        # depot_name = self.read_config.depot_details['depot']
        # secret_file_path = f"{depot_name}_secrets_file_path"
        # keyfile_path = self.read_config.depot_details.get("secrets", {}).get(secret_file_path, "")

        connection_details = self.read_config.depot_details.get("connection", {})
        secrets = self.read_config.depot_details.get("secrets", {})
        gcp_secrets_content = json.dumps(secrets)
        with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_secrets_file:
            temp_secrets_file.write(gcp_secrets_content)
            temp_secrets_file_path = temp_secrets_file.name
        bigquery_spark_option = {
            "parentProject": connection_details.get("project", "")
        }
        self.read_config.spark_options = bigquery_spark_option
        bigquery_conf = [
            ("spark.hadoop.google.cloud.auth.service.account.json.keyfile", temp_secrets_file_path),
            ("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem"),
            ("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
        ]
        return bigquery_conf
