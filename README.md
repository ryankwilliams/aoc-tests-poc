# AoC QE Tests

This repository is a proof of concept for the Ansible On Clouds QE team
to demonstrate creating tests using the pytest framework.

This project has many parts that still need implementation, it is meant
to provide a baseline for developing tests. Items missing about providing
access to the AAP instance deployed, passing in additional parameters per
operation playbook, implementing the correct commands to run the playbooks
within the operations container, etc. As of now it is providing a baseline
to build upon.

## Quickstart

```shell
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Prior to running tests, ensure podman service is running, else it will fail
podman system service -t 0 &

# Test AoC AWS backup operation
export AOC_OPS_IMAGE_REGISTRY_USERNAME=<username>
export AOC_OPS_IMAGE_REGISTRY_PASSWORD=<password>
cd tests
pytest -v -s --ansible-host-pattern=localhost operations/backup -m aoc_aws_backup --junitxml="aoc_aws_backup_results.xml"

# Test AoC GCP backup operation
export AOC_OPS_IMAGE_REGISTRY_USERNAME=<username>
export AOC_OPS_IMAGE_REGISTRY_PASSWORD=<password>
cd tests
pytest -v -s --ansible-host-pattern=localhost operations/backup -m aoc_gcp_backup --junitxml="aoc_gcp_backup_results.xml"

# Test AoC AWS restore operation
export AOC_OPS_IMAGE_REGISTRY_USERNAME=<username>
export AOC_OPS_IMAGE_REGISTRY_PASSWORD=<password>
cd tests
pytest -v -s --ansible-host-pattern=localhost operations/restore -m aoc_aws_restore --junitxml="aoc_aws_restore_results.xml"

# Test AoC GCP restore operation
export AOC_OPS_IMAGE_REGISTRY_USERNAME=<username>
export AOC_OPS_IMAGE_REGISTRY_PASSWORD=<password>
cd tests
pytest -v -s --ansible-host-pattern=localhost operations/backup -m aoc_gcp_restore --junitxml="aoc_gcp_restore_results.xml"
```
