#IAM #ToExpand 

An IAM policy is a set of one or more permissions used to control the access to one or more ressources.

IMA policies can be attached to single [[IAM users]], or [[IAM user groups]].

It is recommended to follow the _[[Principle of least privilege]]_ when creating and managing the policies.

There a few type of policies :
1. *Managed policies* : standalone policies created and managed by AWS, meant to cover most use cases
2. *Customer managed policies*: standalone policies created and managed at the customer account level
3. *Inline policies*: policies embedded in an IAM identity (a [[IAM users|user]], [[IAM user groups|group]], or [[IAM roles|role]]).