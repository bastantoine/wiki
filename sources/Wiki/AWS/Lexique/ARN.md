#IAM 

ARN: *Amazon Resource Name*

The ARN is a unique identifier for a resource that is used in the [[IAM policies]] to grant permissions on some resources.

It has the following format:

arn:*`partition`*:*`service`*:*`region`*:*`account`*:*`resource`*

Where:

- `partition` identifies the [[Region#^66238c|partition]] for the resource.
- `service` identifies the AWS product.
- `region` identifies the [[Region|region]] of the resource. Ressources which are global across all regions have this field blank.
- `account` specifies the AWS account ID with no hyphens.
-  `resource` identifies the specific resource by name.

It is possible to use widlcards (`*`) in the `resource` portion of the ARN to match multiple resources at once.