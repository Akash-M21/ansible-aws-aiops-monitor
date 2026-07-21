#!/usr/bin/env python3
import boto3
import logging
from typing import List

logger = logging.getLogger(__name__)

def reboot_instances_by_ip(ip_addresses: List[str], region: str = "ap-south-1") -> List[str]:
    if not ip_addresses:
        return []

    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_instances(
        Filters=[
            {"Name": "ip-address", "Values": ip_addresses},
            {"Name": "instance-state-name", "Values": ["running"]}
        ]
    )

    instance_ids = [
        instance["InstanceId"]
        for reservation in response.get("Reservations", [])
        for instance in reservation.get("Instances", [])
    ]

    if not instance_ids:
        logger.warning(f"No running instances found for IPs: {ip_addresses}")
        return []

    ec2.reboot_instances(InstanceIds=instance_ids)
    logger.info(f"Rebooted instances: {instance_ids}")
    return instance_ids
