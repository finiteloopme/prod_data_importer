import logging
import argparse
import os
import sys

# def checkIfFileImported(readableFile):
#     from google.cloud import storage
#     from apache_beam.io.gcp import gcsfilesystem
    
#     file = readableFile.path
#     gcs_client = storage.Client()
#     gcs = gcsfilesystem.gcsio.GcsIO(storage_client=gcs_client)

#     return not gcs.exists(path=file)

# def createFile(readableFile):
#     from google.cloud import storage
#     from apache_beam.io.gcp import gcsfilesystem

#     file = readableFile.path + ".loaded"
#     gcs_client = storage.Client()
#     gcs = gcsfilesystem.gcsio.GcsIO(storage_client=gcs_client)
#     gcs.open(file, mode="w").close()

#     return [file]

def run(argv=None):

    from handlers.product_loader import LoadProduct
    from handlers.rating_loader import LoadRating

    import apache_beam as beam
    from apache_beam.io import fileio
    from apache_beam.io.gcp import gcsfilesystem
    from apache_beam.options.pipeline_options import PipelineOptions
    from apache_beam.options.pipeline_options import SetupOptions
    import google.auth

    NUM_LINES_PER_READ=500000
    BQ_DATASET_ID="kunal-scratch.product_ratings_raw"
    BQ_PROUDCT_TABLE="PRODUCT_INFO"
    BQ_RATINGS_TABLE="RATINGS_INFO"

    parser = argparse.ArgumentParser()
    args, beam_args = parser.parse_known_args(argv)
    beam_options = PipelineOptions(beam_args,
        dataflow_service_options=["use_runner_v2"])
    beam_options.view_as(SetupOptions).setup_file = "./setup.py"

    # file_name = "gs://kunal-scratch/product-ratings-raw/AMAZON_FASHION_5.json.gz"
    with beam.Pipeline(options=beam_options) as pipeline:
        import_into_bq=True
        imported_file_ext=".loaded"
        prod_files = (
            pipeline
            | "Find the product files" >> fileio.MatchFiles('gs://kunal-scratch/product-ratings-raw/*json.gz')
            | "Filter out imported file[json]" >> beam.Filter(lambda file: not gcsfilesystem.GCSFileSystem(pipeline_options=beam_options).exists(file.path + imported_file_ext))
            # | "Filter out imported file[json]" >> beam.Filter(checkIfFileImported)
            | "Aid parallel processing of products" >> beam.Reshuffle()
            # | "DEBUG Prod filename" >> beam.ParDo(lambda file: logging.info(file.path))
            | "Load product file" >> beam.ParDo(LoadProduct(num_lines=NUM_LINES_PER_READ, table_name=BQ_PROUDCT_TABLE, import_into_bq=import_into_bq))
            # | "DEBUG processed filename" >> beam.ParDo(logging.info)
            # | "Mark the product file as processed" >> beam.Map(createFile)
            | "Mark the product file as processed" >> beam.ParDo(
                lambda file: gcsfilesystem.GCSFileSystem(pipeline_options=beam_options)
                    .create(path=file + imported_file_ext).close()
                # lambda file: createFile(path=file + imported_file_ext)
                )
        )
        ratings_files = (
            pipeline
            | "Find the ratings files" >> fileio.MatchFiles('gs://kunal-scratch/product-ratings-raw/*.csv')
            | "Filter out imported file[csv]" >> beam.Filter(
                lambda file: not gcsfilesystem.GCSFileSystem(pipeline_options=beam_options)
                    .exists(file.path + imported_file_ext)
                # lambda file: not doesFileExist(file.path + imported_file_ext)
                )
            | "Aid parallel processing[csv]" >> beam.Reshuffle()
            # | "DEBUG Rating filename" >> beam.ParDo(lambda file: logging.info(file.path))
            | "Load rating file" >> beam.ParDo(LoadRating(num_lines=NUM_LINES_PER_READ, table_name=BQ_RATINGS_TABLE, import_into_bq=import_into_bq))
            # # | "DEBUG processed filename" >> beam.ParDo(logging.info)
            | "Mark the rating file as processed" >> beam.ParDo(
                lambda file: gcsfilesystem.GCSFileSystem(pipeline_options=beam_options)
                    .create(path=file + imported_file_ext).close()
                # lambda file: createFile(path=file + imported_file_ext)
                )
        )

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()