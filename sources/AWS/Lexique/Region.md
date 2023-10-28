#Network

A region is a cluster of [[AZ]] in a geographical area. Each AZ inside a region is completely independent of the others AZs.

Some ressources are tied to a given region.

Some regions also include [[Local zones|local zones]] and/or [[Edge locations|edge locations]].

There are 27 regions across the globe.

Link to the [AWS page on infrastructure](https://aws.amazon.com/fr/about-aws/global-infrastructure/regions_az/).

## Partitions

^66238c

The regions are separated in partitions. There's currently 3 partitions:
- `aws` : all regions available for regular customers
- `aws-cn`: regions in China dedicated to the chinese customers
- `aws-us-gov`: regions dedicted to [AWS GovCloud](https://aws.amazon.com/govcloud-us/) in the US