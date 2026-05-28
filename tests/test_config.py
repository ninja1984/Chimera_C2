import yaml
import os

def test_config_exists():
    """Verify that the core configuration file is present."""
    assert os.path.exists("config/settings.yaml"), "Config file is missing!"

def test_config_structure():
    """Verify that the config file has the required root keys."""
    with open("config/settings.yaml", "r") as f:
        config = yaml.safe_load(f)
    assert "orchestrator" in config
    assert "c2_server" in config
    assert "agents" in config
