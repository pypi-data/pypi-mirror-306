from typing import Optional, List

import click
import yaml
from kubernetes import config, utils
from pkg_resources import resource_filename

from tensorkube.constants import DEFAULT_NAMESPACE
from tensorkube.helpers import sanitise_name
from tensorkube.services.aws_service import get_bucket_name, get_credentials
from tensorkube.services.k8s_service import get_tensorkube_cluster_context_name, create_configmap, create_aws_secret
from tensorkube.services.knative_service import get_instance_family_from_gpu_type
from tensorkube.services.s3_service import create_s3_bucket

AXOLOTL_IMAGE = "tensorfuse/axolotl-train:v0.0.1"


def apply_training_job(job_name: str, namespace: str, yaml_file_path: str, gpus: int, gpu_type: str,
                       context_name: Optional[str] = None, secrets: List[str] = [], image_url: Optional[str] = None,
                       bucket: Optional[str] = None):
    # Load kube config
    if not context_name:
        context_name = get_tensorkube_cluster_context_name()
        if not context_name:
            return None
    k8s_api_client = config.new_client_from_config(context=context_name)

    # Read the YAML file
    with open(yaml_file_path, 'r') as f:
        yaml_content = f.read()

    image_tag = image_url.split(':')[-1]
    click.echo(f"Creating job {job_name} with {gpus} GPUs.")
    yaml_content = yaml_content.replace('${JOB_NAME}', job_name)
    yaml_content = yaml_content.replace('${GPUS}', str(gpus))
    yaml_content = yaml_content.replace('${IMAGE_URL}', image_url)
    yaml_content = yaml_content.replace('${IMAGE_TAG}', image_tag)
    yaml_content = yaml_content.replace('${NAMESPACE}', namespace)
    yaml_content = yaml_content.replace('${AXOLOTL_CONFIGMAP_NAME}', f"{job_name}-config")

    # Load the YAML content    
    yaml_dict = yaml.safe_load(yaml_content)
    if bucket:
        yaml_dict['spec']['template']['spec']['containers'][0]['env'].append(
            {'name': 'LORA_ADAPTER_BUCKET', 'value': bucket  # TODO: should we take region as well?
            })
    yaml_dict['spec']['template']['spec']['containers'][0]['env'].append({'name': 'JOB_NAME', 'value': job_name})

    if secrets:
        yaml_dict['spec']['template']['spec']['volumes'].append({'name': 'secrets',
            'projected': {'sources': [{'secret': {'name': secret_name}} for secret_name in secrets]}})

        yaml_dict['spec']['template']['spec']['containers'][0]['volumeMounts'].append(
            {'name': 'secrets', 'mountPath': '/mnt/secrets', 'readOnly': True})

    yaml_dict['spec']['template']['spec']['nodeSelector'] = {
        'karpenter.k8s.aws/instance-family': get_instance_family_from_gpu_type(gpu_type), }

    # Create the job
    utils.create_from_dict(k8s_api_client, yaml_dict)
    click.echo(f"Job {job_name} created successfully.")

def get_job_prefix_from_job_id(job_id: str) -> str:
    job_name = sanitise_name(job_id)
    job_name = f"ax-{job_name}-gpus-"
    return job_name

def get_training_id_from_job_name(job_name: str) -> str:
    return job_name.split('-gpus-')[0].split('ax-')[1]


def axolotl_train(env: str, secrets: list, gpus: int, gpu_type: str, job_id: str, config_path: str):
    if config_path is None:
        raise Exception("config_path is required")
    if job_id is None:
        raise Exception("job_id is required")

    bucket_name = get_bucket_name(env_name=env, type='train')
    create_s3_bucket(bucket_name)
    yaml_dict = None
    with open(config_path, 'r') as f:
        yaml_dict = yaml.safe_load(f)
    if yaml_dict is None or len(yaml_dict) == 0:
        raise Exception("Invalid yaml data")
    namespace = DEFAULT_NAMESPACE if not env else env
    job_name=f'{get_job_prefix_from_job_id(job_id)}{gpus}-{str(gpu_type).lower()}'
    try:
        config_name = f"{job_name}-config"
        create_configmap(config_name, namespace=namespace, data=yaml_dict, context_name=None, force=True)
    except Exception as e:
        raise Exception("Failed to create the configmap")

    yaml_file_path = resource_filename('tensorkube', 'configurations/build_configs/axolotl-train.yaml')

    try:
        create_aws_secret(get_credentials(), namespace=namespace, context_name=None)
        apply_training_job(job_name, namespace, yaml_file_path, gpus, gpu_type, secrets=secrets,
                           image_url=AXOLOTL_IMAGE, bucket=bucket_name)
    except Exception as e:
        raise Exception("Failed to create the training job")
    return
