from typing import List, Tuple

import traceback

import logging

import ast
import base64
import time
import warnings
import pyspark.sql.functions as F
from pyspark.sql import DataFrame

from pyflare.sdk.config import constants
from pyflare.sdk.config.constants import S3_ICEBERG_FILE_IO
from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.utils import pyflare_logger, generic_utils
from pyflare.sdk.writers.file_writer import FileOutputWriter
from pyspark.sql.readwriter import DataFrameWriterV2

warnings.filterwarnings("ignore", message=".*version-hint.text.*")


def _generate_iceberg_catalog_conf(catalog_name: str, depot_base_path: str) -> List[Tuple[str, str]]:
    """
    Generates a list of key-value pairs for the Iceberg configuration.

    :param catalog_name: The catalog name for the configuration.
    :param depot_base_path: The base path for the warehouse.
    :return: List of tuples with configuration keys and values.
    """
    return [
        (f"spark.sql.catalog.{catalog_name}", "org.apache.iceberg.spark.SparkCatalog"),
        (f"spark.sql.catalog.{catalog_name}.type", "hadoop"),
        (f"spark.sql.catalog.{catalog_name}.warehouse", depot_base_path)
    ]


class IcebergOutputWriter(FileOutputWriter):
    """
        A class for writing data to the iceberg format using PySpark.
    """

    def __init__(self, write_config: WriteConfig):
        super().__init__(write_config)
        self.log = pyflare_logger.get_pyflare_logger(name=__name__)
        self.depot_suffix = "_" + str(int(time.time() * 1e6))

    def write(self, df: DataFrame):
        """
        Writes the given DataFrame to the iceberg format. If the "merge" option is specified in the
        write_config's extra_options, the DataFrame is merged into an existing table using a temporary view.
        Otherwise, the DataFrame is written to the iceberg format with the given options.

        Parameters:
            df (DataFrame): The DataFrame to write.

        Returns:
            None
        """
        try:
            self.temp_spark_conf()
            if "merge" in self.write_config.extra_options.keys():
                # we add _temp to use catalog properties temporarily and later remove it from spark conf
                depot = self.write_config.depot_details.get("depot") + self.depot_suffix
                collection = self.write_config.depot_details.get("collection")
                dataset = self.write_config.depot_details.get("dataset")
                view_name = f"{depot}_{collection}_{dataset}_{int(time.time() * 1e9)}"
                df.createOrReplaceTempView(view_name)
                self.spark.sql(self.__merge_into_query(view_name, depot, collection, dataset))
            else:
                spark_options = self.write_config.spark_options
                table_properties = self.write_config.extra_options.get("table_properties", {})
                io_format = self.write_config.io_format
                dataset_path = generic_utils.get_dataset_path(self.write_config, self.depot_suffix)
                df_writer = df.writeTo(dataset_path).using(io_format)
                if spark_options:
                    df_writer = df_writer.options(**spark_options)
                if table_properties:
                    df_writer = df_writer.tableProperty(**table_properties)
                df_writer = self.__process_partition_conf(df_writer)
                self.__write_mode(df_writer)
        except Exception:
            logging.error("Error writing dataframe to iceberg table: %s", traceback.format_exc())
        finally:
            self.cleanup_temp_spark_conf()
            logging.debug("iceberg catalog conf cleanup successful")

    def write_stream(self):
        """
            Writes the given DataFrame to the iceberg format in streaming mode.

            :return: None
        """
        pass

    def get_conf(self):
        """
            Returns spark configuration required for iceberg as per underlying filesystem.

            :return: Spark configuration required for iceberg as per underlying filesystem.
            :rtype: list of tuples
        """
        return getattr(self, f"_{self.write_config.depot_type()}_{self.write_config.io_format}")()

    def _abfss_iceberg(self):
        """
            Returns spark configuration required for iceberg on Azure Blob Storage.

            :return: Spark configuration required for iceberg on Azure Blob Storage.
            :rtype: list of tuples
        """
        iceberg_conf = []
        iceberg_conf.extend(generic_utils.get_abfss_spark_conf(self.write_config))
        return iceberg_conf

    def _s3_iceberg(self):
        """
            Returns spark configuration required for iceberg on AWS S3.

            :return: Spark configuration required for iceberg on AWS S3.
            :rtype: list of tuples
        """
        iceberg_conf = [S3_ICEBERG_FILE_IO]
        iceberg_conf.extend(generic_utils.get_s3_spark_conf(self.write_config))
        return iceberg_conf

    def _gcs_iceberg(self):
        """
            Returns spark configuration required for iceberg on Google Cloud Storage.

            :return: Spark configuration required for iceberg on Google Cloud Storage.
            :rtype: list of tuples
        """
        iceberg_conf = []
        iceberg_conf.extend(generic_utils.get_gcs_spark_conf(self.write_config))
        return iceberg_conf

    def __process_partition_conf(self, df_writer: DataFrameWriterV2) -> DataFrameWriterV2:
        """
            Processes the partition configuration for the given DataFrameWriterV2 instance.

            :param df_writer: The DataFrameWriterV2 instance to process.
            :type df_writer: DataFrameWriterV2
            :return: The processed DataFrameWriterV2 instance.
            :rtype: DataFrameWriterV2
        """
        partition_column_list = []
        for temp_dict in self.write_config.extra_options.get("partition", []):
            partition_scheme: str = temp_dict.get("type", "")
            partition_column: str = temp_dict.get("column", "")
            if partition_scheme.casefold() in ["year", "month", "day", "hour"]:
                self.log.info(f"partition scheme: {partition_scheme}, partition column: {partition_column}")
                partition_column_list.append(getattr(F, f"{partition_scheme}s")(partition_column))
            elif partition_scheme.casefold() == "bucket":
                bucket_count: int = temp_dict.get("bucket_count", 8)
                self.log.info(
                    f"partition scheme: {partition_scheme}, partition column: {partition_column}, "
                    f"bucket_count: {bucket_count}")
                self.log.info(f"F.bucket({bucket_count}, {partition_column}")
                partition_column_list.append(getattr(F, f"{partition_scheme}")(bucket_count, F.col(partition_column)))
            elif partition_scheme.casefold() == "identity":
                self.log.info(f"partition column: {partition_column}")
                partition_column_list.append(F.col(partition_column))
            else:
                self.log.warn(f"Invalid partition scheme: {partition_scheme}")
        if partition_column_list:
            df_writer = df_writer.partitionedBy(*partition_column_list)
        return df_writer

    def __write_mode(self, df: DataFrameWriterV2):
        """
            Sets the write mode for the given DataFrameWriterV2 instance based on the write_config's mode.

            :param df: The DataFrameWriterV2 instance to set the write mode for.
            :type df: DataFrameWriterV2
        """
        if self.write_config.mode in ["create", "overwrite", "write"]:
            df.createOrReplace()
        elif self.write_config.mode in ['overwriteByPartition']:
            df.overwritePartitions()
        else:
            df.append()

    def __merge_into_query(self, source_view: str, depot, collection, dataset):
        """
        Generates a merge query for merging the given source view into the specified dataset.

        :param source_view: The name of the source view to merge.
        :type source_view: str
        :param depot: The name of the depot.
        :type depot: str
        :param collection: The name of the collection.
        :type collection: str
        :param dataset: The name of the dataset.
        :type dataset: str
        :return: The merge query.
        :rtype: str
        """
        merge_clauses = self.write_config.extra_options.get("merge", {})

        query = f"MERGE INTO {depot}.{collection}.{dataset} as target \n"
        query += f"USING (select * from {source_view}) as source \n"
        query += f"ON {merge_clauses.get('onClause', '')} \n"
        query += f"{merge_clauses.get('whenClause', '')} \n"
        return query

    def temp_spark_conf(self):
        """
        Generates a temporary Spark configuration for iceberg.

        :return: The temporary Spark configuration.
        :rtype: list of tuples
        """
        dataset_absolute_path = self.write_config.depot_absolute_path()
        iceberg_conf = _generate_iceberg_catalog_conf(self.write_config.depot_name() +
                                                      self.depot_suffix, dataset_absolute_path)
        for key, value in iceberg_conf:
            self.spark.conf.set(key, value)
        return iceberg_conf

    def cleanup_temp_spark_conf(self):
        """
            Cleans up the temporary Spark configuration for iceberg.

            :return: None
        """
        dataset_absolute_path = self.write_config.depot_absolute_path()
        iceberg_conf = _generate_iceberg_catalog_conf(self.write_config.depot_name() + self.depot_suffix,
                                                      dataset_absolute_path)
        for key, _ in iceberg_conf:
            self.spark.conf.unset(key)
