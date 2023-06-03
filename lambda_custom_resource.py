import ipaddress
import math
import boto3


def split_cidr(cidr, num_networks):
    """
    Splits a CIDR block into a specified number of subnets.

    :param cidr: CIDR block to be split
    :type cidr: str
    :param num_networks: Number of subnets to split the block into
    :type num_networks: int
    :return: List of subnets
    """
    try:
        # Convert CIDR to IP network object
        network = ipaddress.ip_network(cidr)

        # We can only split a CIDR block into a power of 2
        #  For example, if we split a network into 5 parts we need 3 additional bits, as 2^2 = 4 < 5 < 2^3 = 8
        additional_bits = math.ceil(math.log(num_networks, 2))
        new_prefix_length = network.prefixlen + additional_bits

        # Generate all subnets of the desired size
        subnets = list(network.subnets(new_prefix=new_prefix_length))

        if len(subnets) > num_networks:
            subnets = subnets[:num_networks]

        return [str(net) for net in subnets]

    except ValueError as e:
        print("Error:", e)


def lambda_handler(event, context):
    """
    Lambda handler function.

    :param event: AWS Lambda event
    :param context: AWS Lambda context
    :return: None
    """
    print("Received event:", event)

    cidr = event["ResourceProperties"]["CidrBlock"]
    vpc = event["ResourceProperties"]["VpcId"]
    ec2 = boto3.client("ec2", region_name=region_name)
    response = ec2.describe_availability_zones()

    num_networks = len(response["AvailabilityZones"])

    subnets_cidrs = split_cidr(cidr, num_networks)
    subnet = []
    for az in response["AvailabilityZones"]:
        subnet = ec2.create_subnet(
            CidrBlock=subnets_cidrs.pop(), VpcId=vpc, AvailabilityZone=az["ZoneName"]
        )
        subnets.append(subnet["Subnet"]["SubnetId"])
        print("Created subnet:", subnet)

    # Split the CIDR block into the specified number of subnets

    ec2 = boto3.client("ec2", region_name=region_name)
    response = ec2.describe_availability_zones()

    # Return the subnets in the response
    response_data = {"Subnets": subnets}
    response = {
        "Status": "SUCCESS",
        "PhysicalResourceId": context.log_stream_name,
        "StackId": event["StackId"],
        "RequestId": event["RequestId"],
        "LogicalResourceId": event["LogicalResourceId"],
        "Data": response_data,
    }

    print("Returning response:", response)
    return response
