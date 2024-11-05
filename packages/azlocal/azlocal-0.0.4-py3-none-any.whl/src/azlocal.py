#!/usr/bin/env python

"""
Thin wrapper around the "az" command line interface (CLI) for use
with LocalStack.

The "azlocal" CLI allows you to easily interact with your local Azure services
without having to configure anything.

Example:
Instead of the following command ...
HTTPS_PROXY=... REQUESTS_CA_BUNDLE=... az storage account list
... you can simply use this:
azlocal storage account list

Options:
  Run "azlocal help" for more details on the Azure CLI subcommands.
"""

import os
import sys

from .shared import check_proxy_is_running, get_proxy_certificate_location


def usage():
    print(__doc__.strip())


def run(cmd, env):
    """
    Replaces this process with the AZ CLI process, with the given command and environment
    """
    os.execvpe(cmd[0], cmd, env)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        return usage()
    run_as_separate_process()


def prepare_environment(proxy_endpoint: str):

    certificate_path = get_proxy_certificate_location(proxy_endpoint)

    # prepare env vars
    env_dict = os.environ.copy()

    env_dict['HTTP_PROXY'] = proxy_endpoint
    env_dict['HTTPS_PROXY'] = proxy_endpoint
    env_dict['REQUESTS_CA_BUNDLE'] = certificate_path

    # update environment variables in the current process
    os.environ.update(env_dict)

    return env_dict


def run_as_separate_process():
    """
    Constructs a command line string and calls "az" as an external process.
    """

    cmd_args = list(sys.argv)
    cmd_args[0] = 'az'
    if ("--help" in cmd_args) or ("--version" in cmd_args):
        # Early exit - if we only want to know the version/help, we don't need LS to be running
        run(cmd_args, None)
        return

    proxy_endpoint = os.environ.get("HTTP_PROXY") or os.environ.get("HTTPS_PROXY") or 'http://localhost:4566'
    check_proxy_is_running(proxy_endpoint)

    env_dict = prepare_environment(proxy_endpoint)

    # Hijack the login command to automatically login
    if len(cmd_args) > 1 and cmd_args[1] == "login" and "--help" not in cmd_args:
        cmd_args = ["az", "login", "--service-principal", "-u", "any-app", "-p", "any-pass", "--tenant", "any-tenant"]

    # run the command
    run(cmd_args, env_dict)


if __name__ == '__main__':
    main()
