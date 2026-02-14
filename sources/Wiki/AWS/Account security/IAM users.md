#IAM 

A IAM user is a user within an AWS account.

By default they are not allowed to do, access or view anything. They must be granted specific permissions.

They have their own credentials to login and perfom operations.

A IAM user can have two types of credentials :
1. Access key : allows programatic access for the SDKs and APIs
2. Password : allows access to the management console

It is recommended to follow the *[[Principle of least privilege]]* when configuring the credentials that a given user can use.

By default, IAM users arent allowed to do, view or access any ressource. They must be granted permissions using [[IAM policies]] directly assigned to them, 

or by being a member of an [[IAM user groups]].