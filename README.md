# Ansible On Clouds "AoC" Tests/Test Scenarios

A repository demonstrating Ansible On Clouds automated tests/test scenarios
using the pytest framework.

This repository is currently a **proof of concept** and is still under
implementation. The initial intention is to provide a baseline/example
structure/standard for developing new tests. Tests can range from
unit/feature/system/e2e tests.

You may find items missing currently as it is still under construction, such as:

* Accessing an AAP instance deployed
* Passing in additional parameters/data to tests
* Implementing correct operation commands for AoC deployments

All of these will be coming soon!

## Quickstart

The code block below provides you with the necessary commands to try out
the existing tests.

```shell
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Prior to running tests, ensure podman service is running, else it will fail
podman system service -t 0 &

# Set the necessary environment variables required by the tests
export AOC_OPS_IMAGE_REGISTRY_USERNAME=<username>
export AOC_OPS_IMAGE_REGISTRY_PASSWORD=<password>

# Change directories into tests/
cd tests

# Test AoC AWS backup operation
pytest -v -s --ansible-host-pattern=localhost operations/backup -m aoc_aws_backup --junitxml="aoc_aws_backup_results.xml"

# Test AoC GCP backup operation
pytest -v -s --ansible-host-pattern=localhost operations/backup -m aoc_gcp_backup --junitxml="aoc_gcp_backup_results.xml"

# Test AoC AWS restore operation
pytest -v -s --ansible-host-pattern=localhost operations/restore -m aoc_aws_restore --junitxml="aoc_aws_restore_results.xml"

# Test AoC GCP restore operation
pytest -v -s --ansible-host-pattern=localhost operations/backup -m aoc_gcp_restore --junitxml="aoc_gcp_restore_results.xml"
```
