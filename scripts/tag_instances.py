#!/usr/bin/env python3
import functools
import logging
import sys
from typing import List, Dict, Any
import boto3
from botocore.exceptions import BotoCoreError, ClientError

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)

def handle_aws_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (BotoCoreError, ClientError) as error:
            logger.error(f"AWS API Error in '{func.__name__}': {error}")
            sys.exit(1)
    return wrapper

@handle_aws_errors
def fetch_target_instances(ec2_client, environment: str = "dev") -> List[Dict[str, Any]]:
    response = ec2_client.describe_instances(
        Filters=[
            {"Name": "tag:Environment", "Values": [environment]},
            {"Name": "instance-state-name", "Values": ["running"]}
        ]
    )
    instances = [inst for res in response.get("Reservations", []) for inst in res.get("Instances", [])]
    instances.sort(key=lambda x: x["LaunchTime"])
    return instances

@handle_aws_errors
def tag_instances_sequentially(ec2_client, instances: List[Dict[str, Any]], name_prefix: str = "web") -> None:
    for index, instance in enumerate(instances, start=1):
        formatted_name = f"{name_prefix}-{index:02d}"
        ec2_client.create_tags(Resources=[instance["InstanceId"]], Tags=[{"Key": "Name", "Value": formatted_name}])
        logger.info(f"Tagged {instance['InstanceId']} as {formatted_name}")

def main():
    ec2_client = boto3.client("ec2", region_name="ap-south-1")
    instances = fetch_target_instances(ec2_client, environment="dev")
    tag_instances_sequentially(ec2_client, instances, name_prefix="web")

if __name__ == "__main__":
    main()
