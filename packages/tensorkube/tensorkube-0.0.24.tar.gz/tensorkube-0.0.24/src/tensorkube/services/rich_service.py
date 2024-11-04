from typing import Optional, List

import click
import inquirer
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from tensorkube.constants import DEFAULT_NAMESPACE, DATASET_BUCKET_TYPE
from tensorkube.services.aws_service import get_bucket_name
from tensorkube.services.dataset_service import list_datasets
from tensorkube.services.k8s_service import start_streaming_pod, ssh_into_pod_with_podman, list_jobs, get_pods_for_jobs, \
    delete_job
from tensorkube.services.knative_service import list_deployed_services, get_knative_service, get_ready_condition, \
    get_pods_for_service, get_istio_ingress_gateway_hostname
from tensorkube.services.train import get_training_id_from_job_name


def list_tensorkube_deployments(env_name: Optional[str] = None, all: bool = False, old: bool = False):
    table = Table(title="Tensorkube Deployments")
    trees = []
    table.add_column("Name", style="magenta", no_wrap=True)
    table.add_column("Latest Ready", style="green", no_wrap=False, overflow="fold")
    table.add_column("Ready", no_wrap=False, overflow="fold")
    table.add_column("Env", no_wrap=False, overflow="fold")
    table.add_column("Reason", no_wrap=False, overflow="fold")

    elb_url = get_istio_ingress_gateway_hostname()

    deployed_services = list_deployed_services(env_name=env_name, all=all)
    if not deployed_services:
        return
    services = deployed_services['items']
    for service in services:

        ready_condition = get_ready_condition(service)
        if 'latestReadyRevisionName' in service['status']:
            latest_ready_revision = service['status']['latestReadyRevisionName'][-4:]
        else:
            latest_ready_revision = "N/A"
        if old:
            service_url = service['status']['url']
        else:
            service_url = f'http://{elb_url}/svc/{service["metadata"]["namespace"]}/{service["metadata"]["name"]}/'
        service_name = service['metadata']['name']
        service_env = service['metadata']['namespace']
        tree = Tree("[bold][bright_magenta]" + service_name)
        tree.add("[bold]env:[/] " + service_env)
        tree.add("[bold]URL:[/] [cyan]" + service_url)
        trees.append(tree)
        table.add_row(service_name, latest_ready_revision, ready_condition['status'],
                      service_env, ready_condition.get('reason', None))

    console = Console()
    console.print(table)
    for tree in trees:
        console.print(tree)


def describe_deployment(service_name: str, env_name: Optional[str] = None):
    env_namespace = env_name if env_name else DEFAULT_NAMESPACE
    deployment = get_knative_service(service_name=service_name, namespace=env_namespace)
    if deployment is None:
        click.echo(f"Service {service_name} not found in environment {env_namespace}")
        return
    ready_condition = get_ready_condition(deployment)

    if ready_condition['status'] == 'True':
        ready_status_color = "green"
    elif ready_condition['status'] == 'False':
        ready_status_color = "red"
    else:
        ready_status_color = "yellow"
    tree = Tree("[bold][bright_magenta]" + service_name)
    url = f'http://{get_istio_ingress_gateway_hostname()}/svc/{env_namespace}/{service_name}/'
    tree.add("[bold]URL:[/] [cyan]" + url)
    tree.add("[bold]Latest Created Revision:[/] " + deployment['status']['latestCreatedRevisionName'])
    tree.add("[bold]Latest Ready Revision:[/] [green]" + deployment['status']['latestReadyRevisionName'])
    tree.add(f"[bold]Ready Status:[/] [{ready_status_color}]" + ready_condition['status'])
    tree.add("[bold]Reason:[/] " + deployment['status']['conditions'][0].get('reason', ""))
    tree.add("[bold]Last Deployed At:[/] " + deployment['spec']['template']['metadata']['annotations']['deploy_time'])
    console = Console()
    console.print(tree)


def display_deployment_logs(service_name: str, namespace: str = "default"):
    services_in_namespaces = list_deployed_services(env_name=namespace)['items']
    # check if the service name is present in the namespace
    if service_name not in [service['metadata']['name'] for service in services_in_namespaces]:
        click.echo(f"Service {service_name} not found in environment {namespace}")
        return
    service_pods = get_pods_for_service(service_name=service_name, namespace=namespace)
    if service_pods is None:
        click.echo(f"Your service failed to initialise. No containers could be started. Check dockerfile or view deployment logs")
        return
    if len(service_pods.items) == 0:
        click.echo(f"No active pods found for service {service_name}.")
        return
    elif len(service_pods.items) == 1:
        pod_name = service_pods.items[0].metadata.name
    else:
        click.echo(f"Multiple pods found for service {service_name}. Please specify a pod name.")
        questions = [inquirer.List('pod', message="Please select a pod",
                                   choices=[pod.metadata.name for pod in service_pods.items], ), ]
        pod_name = inquirer.prompt(questions)['pod']

    start_streaming_pod(pod_name=pod_name, namespace=namespace, container_name="user-container")


def ssh_into_deployed_service(service_name: str, namespace: str = "default"):
    services_in_namespaces = list_deployed_services(env_name=namespace)['items']
    # check if the service name is present in the namespace
    if service_name not in [service['metadata']['name'] for service in services_in_namespaces]:
        click.echo(f"Service {service_name} not found in environment {namespace}")
        return
    service_pods = get_pods_for_service(service_name=service_name, namespace=namespace)
    if service_pods is None:
        click.echo(f"Your service failed to initialise. No containers could be started. Check dockerfile or view deployment logs")
        return
    if len(service_pods.items) == 0:
        click.echo(f"No pods found for service {service_name}")
        return
    elif len(service_pods.items) == 1:
        pod_name = service_pods.items[0].metadata.name
    else:
        click.echo(f"Multiple pods found for service {service_name}. Please specify a pod name.")
        questions = [inquirer.List('pod', message="Please select a pod",
                                   choices=[pod.metadata.name for pod in service_pods.items], ), ]
        pod_name = inquirer.prompt(questions)['pod']

    click.echo(f"SSHing into pod: {pod_name}")
    ssh_into_pod_with_podman(pod_name=pod_name, namespace=namespace)


def display_secrets(secrets, namespace: str = DEFAULT_NAMESPACE):
    if not secrets:
        click.echo(f"No secrets found in namespace {namespace}")
        return
    if namespace != DEFAULT_NAMESPACE:
        tree = Tree("[bold][bright_magenta]Secrets in env: " + namespace)
    else:
        tree = Tree("[bold][bright_magenta]Secrets")    
    for secret in secrets:
        tree.add("[bold]Name:[/] " + secret.metadata.name)
    console = Console()
    console.print(tree)


def list_tensorkube_datasets():
    # Get datasets
    datasets = list_datasets()
    if datasets is None:
        return
    if len(datasets) == 0:
        click.echo(click.style("No datasets found.", fg='yellow'))
        return

    table = Table(title="Tensorkube Datasets")
    trees = []

    # Add columns for the main table
    table.add_column("Dataset ID", style="magenta", no_wrap=True)
    table.add_column("Last Modified", style="green", no_wrap=False, overflow="fold")
    table.add_column("Size", no_wrap=False, overflow="fold")

    # Get bucket name for URL construction
    bucket_name = get_bucket_name(type=DATASET_BUCKET_TYPE)

    # Populate table and create trees for detailed view
    for dataset in datasets:
        # Skip directories
        if dataset.is_directory:
            continue

        # Remove .jsonl extension from dataset ID
        dataset_id = dataset.key.rsplit('.jsonl', 1)[0]

        # Create S3 URL
        dataset_url = f"s3://{bucket_name}/{dataset.key}"

        # Add row to main table
        table.add_row(
            dataset_id,
            dataset.last_modified,
            dataset.size
        )

        # Create detailed tree view for each dataset
        tree = Tree(f"[bold][bright_magenta]{dataset_id}")
        tree.add(f"[bold]Size:[/] {dataset.raw_size}")
        tree.add(f"[bold]Last Modified:[/] {dataset.last_modified}")
        tree.add(f"[bold]URL:[/] [cyan]{dataset_url}")
        if dataset.owner != '--':
            tree.add(f"[bold]Owner:[/] {dataset.owner}")
        trees.append(tree)

    # Print both table and trees
    console = Console()
    console.print(table)
    for tree in trees:
        console.print(tree)


def display_job_logs(job_prefix: str, namespace: str = "default"):
    """
    Displays logs from a specified job's pods

    Args:
        job_prefix: Prefix of the job name
        namespace: Kubernetes namespace where the job exists
    """
    # Get all jobs in the namespace with the prefix
    jobs_in_namespace = list_jobs(namespace=namespace, job_name_prefix=job_prefix)
    if not jobs_in_namespace or len(jobs_in_namespace.items) == 0:
        click.echo(click.style(f"No jobs with prefix '{job_prefix}' found in environment {namespace}", fg='red'))
        return

    # If multiple jobs found, ask user to select one
    if len(jobs_in_namespace.items) > 1:
        click.echo("Multiple jobs found. Please select a job.")
        questions = [
            inquirer.List(
                'job',
                message="Please select a job",
                choices=[job.metadata.name for job in jobs_in_namespace.items],
            ),
        ]
        job_name = inquirer.prompt(questions)['job']
    else:
        job_name = jobs_in_namespace.items[0].metadata.name

    # Get pods associated with the selected job
    job_pods = get_pods_for_jobs(job_name=job_name, namespace=namespace)

    if job_pods is None:
        click.echo(click.style(
            f"Your job failed to initialize. No containers could be started. Check configuration or view deployment logs",
            fg='red'
        ))
        return

    if len(job_pods.items) == 0:
        click.echo(click.style(f"No active pods found for job {job_name}.", fg='yellow'))
        return
    elif len(job_pods.items) == 1:
        pod_name = job_pods.items[0].metadata.name
    else:
        click.echo("Multiple pods found for job. Please select a pod.")
        questions = [
            inquirer.List(
                'pod',
                message="Please select a pod",
                choices=[pod.metadata.name for pod in job_pods.items],
            ),
        ]
        pod_name = inquirer.prompt(questions)['pod']

    # Stream logs from the selected pod
    start_streaming_pod(
        pod_name=pod_name,
        namespace=namespace,
        container_name="user-container"
    )


def list_tensorkube_training_jobs(namespace: Optional[str] = None, all: bool = False, job_prefix: Optional[str] = None):
    """
    Lists all jobs and their statuses with optional prefix filtering

    Args:
        namespace: Specific namespace to list jobs from
        all: If True, lists jobs from all namespaces
        job_prefix: Optional prefix to filter job names
    """
    table = Table(title="Tensorkube Jobs")
    trees = []

    # Add columns for the main table
    table.add_column("Job Id", style="magenta", no_wrap=True)
    table.add_column("Status", style="green", no_wrap=False, overflow="fold")
    table.add_column("Start Time", no_wrap=False, overflow="fold")
    table.add_column("Completion Time", no_wrap=False, overflow="fold")
    table.add_column("Env", no_wrap=False, overflow="fold")

    # Get jobs
    jobs = list_jobs(namespace=namespace, all=all, job_name_prefix=job_prefix)
    if not jobs:
        click.echo(click.style("No jobs found.", fg='yellow'))
        return

    for job in jobs.items:
        job_name = job.metadata.name
        job_namespace = job.metadata.namespace

        # Get job status information
        status = job.status
        start_time = status.start_time.strftime("%Y-%m-%d %H:%M:%S") if status.start_time else "N/A"
        completion_time = status.completion_time.strftime("%Y-%m-%d %H:%M:%S") if status.completion_time else "Running"

        # Determine job status
        if status.succeeded:
            job_status = "Succeeded"
        elif status.failed:
            job_status = f"Failed ({status.failed} attempts)"
        elif status.active:
            job_status = "Active"
        else:
            job_status = "Pending"

        # Create detailed tree view
        tree = Tree(f"[bold][bright_magenta]{get_training_id_from_job_name(job_name)}")
        tree.add(f"[bold]Namespace:[/] {job_namespace}")
        tree.add(f"[bold]Status:[/] {job_status}")
        tree.add(f"[bold]Start Time:[/] {start_time}")
        tree.add(f"[bold]Completion Time:[/] {completion_time}")

        # Add additional status details if available
        if hasattr(status, 'conditions') and status.conditions:
            conditions_tree = tree.add("[bold]Conditions")
            for condition in status.conditions:
                condition_status = f"{condition.type}: {condition.status}"
                if condition.reason:
                    condition_status += f" ({condition.reason})"
                conditions_tree.add(condition_status)

        trees.append(tree)

        # Add row to main table
        table.add_row(
            get_training_id_from_job_name(job_name),
            job_status,
            start_time,
            completion_time,
            job_namespace
        )

    # Print both table and trees
    console = Console()
    console.print(table)
    console.print()  # Add blank line between table and trees
    for tree in trees:
        console.print(tree)


def delete_tensorkube_job_by_prefix(job_prefix: str, namespace: str = "default") -> bool:
    """
    Deletes a job matching the given prefix. If multiple jobs match, asks user to select one.

    Args:
        job_prefix: Prefix of the job name to delete
        namespace: Kubernetes namespace where the job exists

    Returns:
        bool: True if deletion was successful, False otherwise
    """
    # Get all jobs in the namespace with the prefix
    jobs_in_namespace = list_jobs(namespace=namespace, job_name_prefix=job_prefix)
    if not jobs_in_namespace or len(jobs_in_namespace.items) == 0:
        click.echo(click.style(f"No jobs with prefix '{job_prefix}' found in environment {namespace}", fg='red'))
        return False

    # If multiple jobs found, ask user to select one
    if len(jobs_in_namespace.items) > 1:
        click.echo("Multiple jobs found. Please select a job to delete.")
        questions = [
            inquirer.List(
                'job',
                message="Please select a job to delete",
                choices=[job.metadata.name for job in jobs_in_namespace.items],
            ),
        ]
        job_name = inquirer.prompt(questions)['job']
    else:
        job_name = jobs_in_namespace.items[0].metadata.name

    # Confirm deletion
    if click.confirm(click.style(f"Are you sure you want to delete job '{job_name}'?", fg='yellow')):
        return delete_job(job_name, namespace)
    else:
        click.echo("Job deletion cancelled.")
        return False