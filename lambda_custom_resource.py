import ipaddress
import math


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


print(split_cidr("10.0.0.0/16", 5))
