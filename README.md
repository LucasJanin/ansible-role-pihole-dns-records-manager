# Ansible Role: Pi-hole DNS Records

This role manages DNS records in Pi-hole 6, supporting both standard and Docker-based installations. Pi-hole 5 is not supported due to its different configuration files.

## Features

- Adds or removes DNS records in Pi-hole.  
- Works with both standard Pi-hole installations and Docker-based setups.  
- Preserves previous host configurations for cleanup.  
- Uses a Python script to modify the Pi-hole configuration file directly.  
- Process completed on the Ansible localhost.  
- Creates a backup of the pihole.toml file (just in case :-)

## Role Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `pihole_host` | Host where Pi-hole is installed | `pihole` |
| `pihole_toml_file` | Path to Pi-hole configuration file on the remote host, on docker mode this need to be updated | `/etc/pihole/pihole-FTL.toml` |
| `pihole_local_storage_dir` | Local directory for temporary files | `/tmp/pihole-dns-records-manager` |
| `pihole_config_file` | Local path to the fetched config file | `{{ pihole_local_storage_dir }}/pihole-FTL.toml` |
| `pihole_hosts_save_file` | File to save previous hosts for cleanup | `{{ pihole_local_storage_dir }}/previous_hosts.json` |
| `pihole_dns_action` | Action to perform (add or remove) | `add` |
| `pihole_docker_mode` | Whether Pi-hole is installed via Docker | `false` |
| `pihole_docker_container_name` | Name of the Pi-hole Docker container | `pihole` |
| `dev_hostnames` | List of hostnames to configure | `[]` |
| `dev_ips` | List of corresponding IP addresses | `[]` |

## Example Usage

```yaml
# Standard Pi-hole Installation
- hosts: localhost
  roles:
    - role: pihole_dns_records
      vars:
        pihole_host: pihole
        dev_hostnames:
          - server1.local
          - server2.local
        dev_ips:
          - 192.168.1.10
          - 192.168.1.11

# Docker-based Pi-hole Installation
- hosts: localhost
  roles:
    - role: pihole_dns_records
      vars:
        pihole_host: pihole
        pihole_docker_mode: true
        pihole_docker_container_name: pihole
        dev_hostnames:
          - server1.local
          - server2.local
        dev_ips:
          - 192.168.1.10
          - 192.168.1.11

#Removing DNS Records
- hosts: localhost
  roles:
    - role: pihole_dns_records
      vars:
        pihole_host: pihole
        pihole_dns_action: remove
        dev_hostnames:
          - server1.local
          - server2.local
```

## License

MIT

## Author Information

- Lucas Janin
- https://lucasjanin.com
- https://mastodon.social/@lucas3d