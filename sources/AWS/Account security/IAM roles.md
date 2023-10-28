#IAM #ToExpand 

An IAM role is an [[Principal|IAM principal]] that is created in an account and is given specific permissions. They act as temporary credentials to access and/or perform operations on ressources.

- Providing access across AWS accounts
- Provide access to non AWS workloads ([[IAM Anywhere]])
- Provide access to IAM users in AWS accounts owned by third parties
- Provide access for services offered by AWS to AWS resources (service roles)
- Provide access for externally authenticated users (identity federation)

## Role assumption

*role assumption* is the action of authenticating using a given role. It happens in 3 steps:
1. The user that wants to assume the role (IAM user, federated user or AWS service) makes an API call to [[STS]] to assume the given role
2. STS then returns temporary credentials
3. The user can then use those credentials to authenticate to AWS and perform operation on resources

![[aws-role-assumption.png]]