import logging
from google.cloud import bigquery

class LoadIntoBQ():
    def __init__(self,dataset_id="kunal-scratch.product_ratings_raw",table_id="PRODUCT_INFO") -> None:
        super().__init__()
        self.dataset_id = dataset_id
        self.table_id = table_id

    def writeToBQ(self, element):
        # Construct a BigQuery client object.
        client = bigquery.Client()

        job_config = bigquery.LoadJobConfig(
            autodetect=True, 
            ignore_unknown_values=True, 
            create_disposition="CREATE_IF_NEEDED", 
            write_disposition="WRITE_APPEND"
        )
        
        load_job = client.load_table_from_dataframe(
            element,
            self.dataset_id+"."+self.table_id,
            location="US",  # Must match the destination dataset location.
            job_config=job_config,
        )  # Make an API request.

        load_job.result()  # Waits for the job to complete.
        destination_table = client.get_table(self.dataset_id+"."+self.table_id)
        logging.info("Loaded {} rows in table {}.".format(len(element), self.table_id))
        
        return 
