# Pi-hole DNS Records Manager - Example

This example demonstrates how to use the ⁠ansible-role-pihole-dns-reccords-manager role to automatically configure DNS records in Pi-hole based on your Ansible inventory.

## Overview
The example consists of:
- A playbook that dynamically discovers hosts from your inventory
- An inventory file with various host groups (servers, LXC containers, VMs)

## Files
- ⁠playbooks/pihole-dns-reccords-manager.yml: The main playbook
- ⁠inventory: Example inventory file

## How It Works
The playbook automatically:
1.	Collects all hostnames from your inventory
2.	Maps them to their corresponding IP addresses
3.	Adds these as DNS records to your Pi-hole server

## Usage
Run the playbook with:
ansible-playbook -i inventory playbooks/pihole-dns-reccords-manager.yml

## Playbook Details
```yaml
# File: playbooks/pihole-dns-reccords-manager.yml
# Description: Ansible playbook for managing PiHole DNS records
# Author: Lucas Janin
# Date: 2025-03-03

- name: Auto setup hosts on PiHole
  hosts: all
  become: true
  become_method: sudo
  vars:
    # Dynamic discovery variables
    dev_hostnames: "{{ ansible_play_hosts_all }}"
    dev_ips: "{{ ansible_play_hosts_all | map('extract', hostvars, 'ansible_host') | list }}"

  tasks:
    - name: ansible-role-pihole-dns-reccords-manager
      include_role:
        name: ansible-role-pihole-dns-reccords-manager
      run_once: true
```

## The key components are:

- ⁠hosts: all: Targets all hosts in your inventory
- ⁠dev_hostnames: Dynamically populated with all hostnames
- ⁠dev_ips: Extracts the IP addresses from the inventory
- ⁠run_once: true: Ensures the role only runs once, not for each host

## Inventory Example

The inventory file organizes hosts into different groups:

- ⁠server: Physical servers
- ⁠lxc: LXC containers
- ⁠vm: Virtual machines

Each group has its own variables for SSH access and Python interpreter.

## Customization

You can customize this example by:
- Adding more hosts to the inventory
- Setting Pi-hole specific variables like ⁠pihole_host
- Changing the DNS action with ⁠pihole_dns_action

##  Requirements

- Ansible 2.9 or higher
- SSH access to all hosts in the inventory
- A running Pi-hole instance
- The ⁠ansible-role-pihole-dns-reccords-manager role installed

## Notes

- This example assumes your Pi-hole server is accessible from the Ansible controller
- The role will be executed on the Ansible controller, not on the Pi-hole server
- Make sure to set ⁠pihole_host to point to your Pi-hole server if not using the default

For more details about the role itself, please refer to the role's README.