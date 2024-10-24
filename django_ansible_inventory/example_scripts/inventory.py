#!/usr/bin/env python3

import requests
import argparse
import json
from typing import Dict, List, Any

API_BASE_URL = "http://jupiter.home.arpa/api"


def fetch_hosts() -> List[Dict[str, Any]]:
    response = requests.get(f"{API_BASE_URL}/hosts/")
    response.raise_for_status()
    return response.json()


def build_inventory(hosts: List[Dict[str, Any]]) -> Dict[str, Any]:
    inventory: Dict[str, Dict[str, Any]] = {"_meta": {"hostvars": {}}}

    for host in hosts:
        host_name = host["name"]

        # Loop through each group the host belongs to
        for group in host["groups"]:
            group_name = group["name"]
            group_vars = group["group_vars"]

            if group_name not in inventory:
                inventory[group_name] = {
                    "hosts": [],
                    "vars": group_vars,
                }

            inventory[group_name]["hosts"].append(host_name)

        # Add host variables to _meta
        inventory["_meta"]["hostvars"][host_name] = host["host_vars"]

    return inventory


def main():
    parser = argparse.ArgumentParser(
        description="Ansible Dynamic Inventory Script",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all hosts",
    )
    parser.add_argument(
        "--host",
        help="Get variables for a specific host",
    )

    args = parser.parse_args()

    hosts = fetch_hosts()

    if args.list:
        inventory = build_inventory(hosts)
        print(json.dumps(inventory, indent=4))
    elif args.host:
        # Fetch and display the variables for the specified host
        host_data = next(
            (host for host in hosts if host["name"] == args.host),
            None,
        )
        if host_data:
            print(json.dumps(host_data["host_vars"], indent=4))
        else:
            print(json.dumps({}, indent=4))
    else:
        print(json.dumps({}, indent=4))


if __name__ == "__main__":
    main()
