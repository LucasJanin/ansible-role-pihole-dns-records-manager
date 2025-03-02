# Ansible Role: Pi-hole DNS Records Manager

This role manages DNS records in a Pi-hole server's configuration file.

It is intended for use in a bare metal, LXC, or VM setup, not in a Docker container. This tool will populate the DNS records based on the inventory hosts. It remembers the previous execution and removes entries for hosts that have been removed from the inventory.

## Requirements

- A running Pi-hole server not in docker
- Python 3 on the control node

## Role Variables

Available variables are listed below, along with default values:

```yaml
# Action to perform (add or remove)
pihole_dns_action: "add"

# Pi-hole host to connect to
pihole_host: "pihole"

# Arrays for hostnames and IPs
dev_hostnames: []
dev_ips: []
```

## Example Playbook

```yaml
- hosts: localhost
  roles:
    - role: ansible-role-pihole-dns-reccords-manager
      vars:
        pihole_host: "pihole"
        pihole_dns_action: "add"
        dev_hostnames: 
          - "server1"
          - "server2"
        dev_ips:
          - "192.168.1.10"
          - "192.168.1.11"
```

## License

MIT

## Author Information

- Lucas Janin
- https://lucasjanin.com
- https://mastodon.social/@lucas3d