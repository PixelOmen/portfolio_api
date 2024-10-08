import os
import time
import boto3


def verify_environment_variable(var_name):
    var = os.getenv(var_name)
    if var is None:
        print(
            f"Error: Environment variable {var_name} is not set.", flush=True)
        exit(1)
    return var


def get_ecs_task_arn(ecs_client, task_definition_arn):
    try:
        response = ecs_client.describe_task_definition(
            taskDefinition=task_definition_arn
        )
        task_arn = response['taskDefinition']['taskDefinitionArn']
    except Exception as e:
        print(f"Error finding task definition: {e}", flush=True)
        exit(1)
    return task_arn


def launch_ecs_task(ecs_client, cluster, task_arn, subnets, security_group_id):
    try:
        response = ecs_client.run_task(
            cluster=cluster,
            taskDefinition=task_arn,
            launchType='FARGATE',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': subnets,
                    'securityGroups': [security_group_id],
                    'assignPublicIp': 'DISABLED'
                }
            }
        )
    except Exception as e:
        print(f"Error launching ECS task: {e}", flush=True)
        exit(1)
    task_arn = response['tasks'][0]['taskArn']
    print(f"Task launched: {task_arn}", flush=True)
    return task_arn.split('/')[-1]  # Extract the task ID from the ARN


def check_task_status(ecs_client, cluster, task_id):
    response = ecs_client.describe_tasks(
        cluster=cluster,
        tasks=[task_id]
    )
    task = response['tasks'][0]
    status = task['lastStatus']
    exit_code = task['containers'][0].get('exitCode', None)
    if status == 'STOPPED':
        print(f"Debug response: {task}", flush=True)
    return status, exit_code


def wait_for_task_completion(ecs_client, cluster, task_id):
    while True:
        status, exit_code = check_task_status(ecs_client, cluster, task_id)
        print(f"Task status: {status}", flush=True)
        if status == 'STOPPED':
            return exit_code
        time.sleep(5)


def main():
    print("Verifying environment variables...", flush=True)
    region = verify_environment_variable("AWS_REGION")
    cluster_name = verify_environment_variable("AWS_CLUSTER_NAME")
    task_definition = verify_environment_variable("AWS_MIGRATE_TASK_DEF")
    subnet_str = verify_environment_variable("AWS_MIGRATE_SUBNETS")
    security_group_id = verify_environment_variable(
        "AWS_MIGRATE_SECURITY_GROUP")

    subnets = subnet_str.split(",")
    ecs_client = boto3.client('ecs', region_name=region)

    print("Getting ECS task arn...", flush=True)
    task_arn = get_ecs_task_arn(ecs_client, task_definition)

    print(f"Starting ECS Task", flush=True)
    task_id = launch_ecs_task(
        ecs_client,
        cluster_name,
        task_arn,
        subnets,
        security_group_id
    )

    print(f"Waiting for ECS task {task_id} to complete...", flush=True)
    exit_code = wait_for_task_completion(ecs_client, cluster_name, task_id)

    if exit_code is None:
        print("Error: ECS task did not return an exit code.", flush=True)
        exit(1)

    if exit_code != 0:
        print(f"ECS task failed with exit code {exit_code}", flush=True)
        exit(1)

    print("ECS task completed successfully.", flush=True)


if __name__ == "__main__":
    main()
