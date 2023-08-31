# Ansible On Clouds "AoC" Tests/Test Scenarios

A repository demonstrating Ansible On Clouds automated tests/test scenarios
using the pytest framework.

This repository is currently a **proof of concept** and is still under
implementation. The initial intention is to provide a baseline/example
structure/standard for developing new tests. Tests can range from
unit/feature/system/e2e tests.

You may find items missing currently as it is still under construction, such as:

* Implementing correct operation commands for AoC operations

All of these will be coming soon!

## Quickstart

Run the following commands below to setup your environment to run any tests:

```shell
# Setup (creates python virtual environment, installs packages)
make setup

# Set the necessary environment variables required by the tests
export AOC_OPS_CONTAINER_IMAGE_REGISTRY_USERNAME=<username>
export AOC_OPS_CONTAINER_IMAGE_REGISTRY_PASSWORD=<password>
```

Once you have completed the initial setup commands, you can run tests
by invoking pytest either from your terminal or IDE.

Each test accepts input in either of the following form:

* Pytest cli options
* Environment variables

You can view these options by running the following pytest command against the
directory where the test modules reside. The examples below will present you
with the cli options you can provide to pytest or the alternative environment
variables you can set.

```shell
# View available aoc aws backup operation options
pytest tests/aoc/aws/operations --help | grep "Custom options" -A 20

# View available aoc gcp backup operation options
pytest tests/aoc/gcp/operations --help | grep "Custom options" -A 20
```

When each test is run, if any option is unset. Messages will be logged
for you to see what needs to be set.

Below demonstrates calling pytest command to run aoc aws backup operation
test case:

```shell
# !!Replace <string> with correct values prior to running

# Set options via pytest cli options
pytest --ansible-host-pattern=localhost \
--aoc-stack-deployment-name=<stack-name> \
--aoc-aws-credentials-path=~/.aws/credentials \
--aoc-aws-backup-iam-role-arn=<iam-role-arn> \
--aoc-aws-backup-prefix=<backup-prefix> \
--aoc-aws-backup-s3-bucket=<s3-bucket-name> \
--aoc-aws-backup-ssm-bucket-name=<s3-ssm-bucket-name> \
--aoc-aws-region=<aws-region> \
--junitxml=aoc_aws_backup_results.xml \
-m aoc_aws_backup \
tests/aoc/aws/operations

# Set options via environment variables
export AOC_STACK_DEPLOYMENT_NAME=<stack-name>
export AOC_AWS_CREDENTIALS_PATH=~/.aws/credentials
export AOC_AWS_BACKUP_IAM_ROLE_ARN=<iam-role-arn>
export AOC_AWS_BACKUP_PREFIX=<backup-prefix>
export AOC_AWS_BACKUP_S3_BUCKET=<s3-bucket-name>
export AOC_AWS_BACKUP_SSM_BUCKET_NAME=<s3-ssm-bucket-name>
export AOC_AWS_REGION=<aws-region>
pytest --ansible-host-pattern=localhost \
--junitxml=aoc_aws_backup_results.xml \
-m aoc_aws_backup \
tests/aoc/aws/operations
```
