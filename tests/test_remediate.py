import os
import pytest
import boto3
from moto import mock_aws
from scripts.remediate import reboot_instances_by_ip

@pytest.fixture(autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture
def ec2_setup():
    with mock_aws():
        ec2_client = boto3.client("ec2", region_name="ap-south-1")
        reservation = ec2_client.run_instances(
            ImageId="ami-12345678", MinCount=1, MaxCount=1, InstanceType="t2.micro"
        )
        instance_id = reservation["Instances"][0]["InstanceId"]
        yield {"client": ec2_client, "id": instance_id}

def test_reboot_valid_ip(ec2_setup):
    ec2_client = ec2_setup["client"]
    target_id = ec2_setup["id"]
    inst_info = ec2_client.describe_instances(InstanceIds=[target_id])
    target_ip = inst_info["Reservations"][0]["Instances"][0]["PublicIpAddress"]

    rebooted = reboot_instances_by_ip([target_ip], region="ap-south-1")
    assert len(rebooted) == 1
    assert target_id in rebooted
