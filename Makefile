GCP_PROJECT=kunal-scratch
GCP_REGION=us-central1
TIME_STAMP:=`env TZ=Australia/Melbourne date "+%Y%m%d-%H%M%S"`

init:
	gcloud auth application-default login --no-launch-browser
	gcloud config set project ${GCP_PROJECT}

run-local:
	python3 -m main_pipeline_job

run-df:
	pip3 install -e .; \
	echo `pip3 list`; \
	python3 -m main_pipeline_job \
		--project ${GCP_PROJECT} \
		--temp_location gs://${GCP_PROJECT}-dataflow/temp \
		--region ${GCP_REGION} \
		--runner DataflowRunner \
		--experiments=use_runner_v2 \
		--dataflow_service_options=use_runner_v2 \
		--setup_file ./setup.py
		# --pickle_library cloudpickle \
		# --save_main_session True\

deploy:
	pip3 install -e .; \
	echo `pip3 list`; \
	python3 -m main_pipeline_job \
		--runner DataflowRunner \
		--project ${GCP_PROJECT} \
		--staging_location gs://${GCP_PROJECT}-dataflow/staging \
		--temp_location gs://${GCP_PROJECT}-dataflow/temp \
		--experiments=use_runner_v2 \
		--template_location gs://${GCP_PROJECT}-dataflow/templates/file2bq

run:
	gcloud dataflow jobs run bq-data-import-job-$(TIME_STAMP) \
		--project ${GCP_PROJECT} \
		--gcs-location gs://${GCP_PROJECT}-dataflow/templates/file2bq \
		--region ${GCP_REGION} \
		--worker-machine-type e2-standard-8 \
		--max-workers 32 \
		--num-workers 16 \
		--service-account-email="dataflow-sa@kunal-scratch.iam.gserviceaccount.com"
