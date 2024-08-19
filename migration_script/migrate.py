import os
import time
import boto3


def verify_environment_variable(var_name):
    if var_name not in os.environ:
        print(f"Error: Environment variable {var_name} is not set.")
        exit(1)
    return os.environ[var_name]


def check_task_status(ecs_client, cluster, task_id):
    response = ecs_client.describe_tasks(
        cluster=cluster,
        tasks=[task_id]
    )
    task = response['tasks'][0]
    return task['lastStatus'], task['containers'][0].get('exitCode', None)


def wait_for_task_completion(ecs_client, cluster, task_id):
    while True:
        status, exit_code = check_task_status(ecs_client, cluster, task_id)
        print(f"Task status: {status}")
        if status == 'STOPPED':
            return exit_code
        time.sleep(5)


def main():
    print('Failing the migration')
    exit(1)
    # print("Verifying environment variables...")
    # region = verify_environment_variable("REGION")
    # cluster_name = verify_environment_variable("CLUSTER_NAME")
    # task_id = verify_environment_variable("TASK_ID")
    # ecs_client = boto3.client('ecs', region_name=region)

    # print(f"Waiting for ECS task {task_id} to complete...")
    # exit_code = wait_for_task_completion(ecs_client, cluster_name, task_id)

    # if exit_code is None:
    #     print("Error: ECS task did not return an exit code.")
    #     exit(1)

    # if exit_code != 0:
    #     print(f"ECS task failed with exit code {exit_code}")
    #     exit(1)

    # print("ECS task completed successfully.")


if __name__ == "__main__":
    main()
