# type: ignore
"""!! Temporary pytest conftest file !!

This will be removed once the issue is fixed!
https://github.com/ansible-community/pytest-ansible/issues/135
"""
import pytest
from pytest_ansible.host_manager import get_host_manager


def initialize_workaround(self, config=None, request=None, **kwargs):
    """Return an initialized Ansible Host Manager instance."""
    ansible_cfg = {}
    # merge command-line configuration options
    if config is not None:
        ansible_cfg.update(self._load_ansible_config(config))
        if "extra_inventory" in ansible_cfg and not ansible_cfg["extra_inventory"]:
            del ansible_cfg["extra_inventory"]
    # merge pytest request configuration options
    if request is not None:
        ansible_cfg.update(self._load_request_config(request))
    # merge in provided kwargs
    ansible_cfg.update(kwargs)
    return get_host_manager(**ansible_cfg)


@pytest.fixture
def ansible_adhoc(request):
    """Return an inventory initialization method."""
    plugin = request.config.pluginmanager.getplugin("ansible")
    plugin.initialize = initialize_workaround.__get__(plugin)

    def init_host_mgr(**kwargs):
        return plugin.initialize(request.config, request, **kwargs)

    return init_host_mgr


@pytest.fixture
def ansible_module(ansible_adhoc):
    host_mgr = ansible_adhoc()
    return getattr(host_mgr, host_mgr.options["host_pattern"])
