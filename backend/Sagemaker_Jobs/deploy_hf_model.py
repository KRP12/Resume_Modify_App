import boto3
import sagemaker
from sagemaker.huggingface import HuggingFaceModel

sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()
hub_model_id = "google/flan-t5-base"

huggingface_model = HuggingFaceModel(
    env={'HF_MODEL_ID': hub_model_id, 'HF_TASK': "text2text-generation"},
    role=role,
    transformers_version="4.26.0",
    pytorch_version="1.13.1",
    py_version="py39",
    sagemaker_session=sagemaker_session
)

predictor = huggingface_model.deploy(
    initial_instance_count=1,
    instance_type="ml.g5.xlarge",
    endpoint_name="resume-improver-t5-endpoint"
)
