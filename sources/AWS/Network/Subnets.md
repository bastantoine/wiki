#Network

A subnet is a range of IPs inside a [[VPC]]. It is bound to a specific [[AZ|AZ]] of the [[Region|region]] of their VPC.

It is assigned a range of IP addresses from the VPC's [[CIDR]]. In this range, 5 IPs are reserved (for example with a CIDR block `10.0.0.0/24`) :
- First of the range (ex: `10.0.0.0`): Network address
- Second of the range (ex: `10.0.0.1`): Reserved by AWS for the VPC router
- Third of the range (ex: `10.0.0.2`):  Reserved by AWS for the IP address of the DNS server
- Fourth of the range (ex: `10.0.0.3`): Reserved by AWS for future usage
- Last of the range (ex: `10.0.0.255`): Network broadcast address, though not supported in a VPC

There are two kinds of subnets:
- Public subnets
- Private subnets


## Public subnets
A public subnet is a subnet that can reach the internet, and can be reach from the internet.
It requires 3 components :
1. An [[Internet gateway|internet gateway]] created in the VPC
2. A [[Route table|route table]] configured to route all outbound traffic meant for the outside of the VPC to the internet gateway
3. A public IP address(es)

## Private subnets
If a subnet doesn't contain at least one of the element above, it is considered private, and thus cannot be reached from the outside of its
VPC.