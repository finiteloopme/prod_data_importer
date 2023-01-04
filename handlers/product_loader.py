
import logging
import os
import pandas as pd

import apache_beam as beam

from .load_into_bq import LoadIntoBQ

class LoadProduct(beam.DoFn):
    def __init__(self, num_lines=500000, table_name="PRODUCT_INFO", import_into_bq=False) -> None:
        super().__init__()
        self.import_into_bq = import_into_bq
        self.num_lines = num_lines
        self.table_name=table_name

    # If TRUE load chunks in to the table
    # Returns URI for the file that was read
    def process(self, element):
        gcs_filepath = element.path

        # df = pd.DataFrame()
        reader = pd.read_json(gcs_filepath, compression='gzip', lines=True, chunksize=self.num_lines)
        file_name = os.path.basename(gcs_filepath)
        for chunk in reader:
            chunk["vote"] = chunk["vote"].astype(str)
            logging.info("Processing: " + file_name)
            if self.import_into_bq:
                LoadIntoBQ(dataset_id="kunal-scratch.product_ratings_raw",table_id=self.table_name).writeToBQ(element=chunk)

        return [gcs_filepath]