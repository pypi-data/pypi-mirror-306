import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def get_proxy_certificate_location(proxy_endpoint):
    # Configure Proxy Certificate
    home_dir = Path.home()
    azure_config_dir = os.path.join(home_dir, ".localstack/azure")
    if not os.path.exists(azure_config_dir):
        Path(azure_config_dir).mkdir(parents=True, exist_ok=True)
    certificate_path = os.path.join(azure_config_dir, "ca.crt")
    if not os.path.exists(certificate_path):
        with urllib.request.urlopen(f"{proxy_endpoint}/_localstack/certs/ca/LocalStack_LOCAL_Root_CA.crt") as cert:
            Path(certificate_path).write_bytes(cert.read())
    return certificate_path


def check_proxy_is_running(proxy_endpoint: str):
    try:
        assert urllib.request.urlopen(f"{proxy_endpoint}/_localstack/health").status == 200
    except (AssertionError, urllib.error.URLError) as e:
        raise Exception("Make sure LocalStack is running")
