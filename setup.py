from setuptools import find_packages
from setuptools import setup

# import handlers.product_loader
# import handlers.rating_loader
# import handlers.load_into_bq

REQUIRED_PACKAGES = [
    "apache-beam[gcp]==2.43.0",
    "fsspec",
    "gcsfs"
]

setup(
    name="prod_data_importer",
    version="0.1",
    description="Imports product rating info into BQ",
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages()
)