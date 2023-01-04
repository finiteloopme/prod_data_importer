
import logging
import os
import pandas as pd

import apache_beam as beam

from .load_into_bq import LoadIntoBQ

class LoadRating(beam.DoFn):
    def __init__(self, num_lines=500000, table_name="RATINGS_INFO", import_into_bq=False) -> None:
        super().__init__()
        self.import_into_bq = import_into_bq
        self.num_lines = num_lines
        self.table_name=table_name

    # If TRUE load chunks in to the table
    # Returns URI for the file that was read
    def process(self, element):
        gcs_filepath = element.path
        # df = pd.DataFrame()
        reader = pd.read_csv(gcs_filepath, 
                            header=None, 
                            names=["item","user", "rating", "timestamp"], 
                            chunksize=self.num_lines)
        file_name = os.path.basename(gcs_filepath)
        bq_loader = LoadIntoBQ(dataset_id="kunal-scratch.product_ratings_raw",table_id=self.table_name)
        for chunk in reader:
            logging.info("Processing: " + file_name)
            if self.import_into_bq and chunk is not None:
                bq_loader.writeToBQ(element=chunk)
            # df = chunk

        return [gcs_filepath]