import tempfile

import base64
import json

from pyflare.sdk.config.constants import GCS_TEMP_BUCKET
from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.utils import pyflare_logger
from pyflare.sdk.writers.writer import Writer


class BigqueryOutputWriter(Writer):

    def __init__(self, write_config: WriteConfig):
        super().__init__(write_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)

    def write(self, df):
        # self.resolve_write_format()
        if self.write_config.is_stream:
            return self.write_stream()
        spark_options = self.write_config.spark_options
        dataset_path = "{}.{}.{}".format(self.write_config.spark_options.get("parentProject", ""),
                                         self.write_config.collection(), self.write_config.dataset_name())
        df.write.options(**spark_options).format("bigquery").mode(self.write_config.mode).save(dataset_path)

    def write_stream(self):
        pass

    def get_conf(self):
        connection_details = self.write_config.depot_details.get("connection", {})
        secrets = self.write_config.depot_details.get("secrets", {})
        gcp_secrets_content = json.dumps(secrets)
        with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_secrets_file:
            temp_secrets_file.write(gcp_secrets_content)
            temp_secrets_file_path = temp_secrets_file.name
        bigquery_spark_option = {
            "parentProject": connection_details.get("project", ""),
            "temporaryGcsBucket": GCS_TEMP_BUCKET
        }
        self.write_config.spark_options = bigquery_spark_option
        bigquery_conf = [
            ("spark.hadoop.google.cloud.auth.service.account.json.keyfile", temp_secrets_file_path),
            ("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem"),
            ("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
        ]
        return bigquery_conf
