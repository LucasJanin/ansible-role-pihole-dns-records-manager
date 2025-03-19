# Ansible Role: Pi-hole DNS Records

This role manages DNS records in Pi-hole 6, supporting both standard and Docker-based installations. Pi-hole 5 is not supported due to its different configuration files.

## Features

- Adds DNS records in Pi-hole while preserving existing configuration
- Works with both standard Pi-hole installations and Docker-based setups
- Preserves previous host configurations for cleanup
- Uses a Python script to modify the Pi-hole configuration file directly
- Process completed on the Ansible localhost
- Preserves original file permissions and ownership
- Creates a backup of the pihole.toml file (just in case :-)

## Role Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `pihole_host` | Host where Pi-hole is installed | `pihole` |
| `pihole_toml_file` | Path to Pi-hole configuration file on the remote host | `/etc/pihole/pihole.toml` |
| `pihole_local_storage_dir` | Local directory for temporary files | `/tmp/pihole-dns-records-manager` |
| `pihole_config_file` | Local path to the fetched config file | `{{ pihole_local_storage_dir }}/pihole.toml` |
| `pihole_hosts_save_file` | File to save previous hosts for cleanup | `{{ pihole_local_storage_dir }}/previous_hosts.json` |
| `pihole_docker_mode` | Whether Pi-hole is installed via Docker | `false` |
| `pihole_docker_container_name` | Name of the Pi-hole Docker container | `pihole` |

## Example Usage

```yaml
# Standard Pi-hole Installation
- hosts: localhost
  roles:
    - role: pihole_dns_records

# Docker-based Pi-hole Installation
- hosts: localhost
  roles:
    - role: pihole_dns_records
      vars:
        pihole_host: pihole
        pihole_docker_mode: true
        pihole_docker_container_name: pihole

```

## Example Playbook

Check the [examples](examples/) directory for sample playbooks.

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/my-new-feature`)
5. Create a new Pull Request

## Author Information

Lucas Janin
- Mastodon: [https://mastodon.social/@lucas3d](https://mastodon.social/@lucas3d)
- Website: [https://www.lucasjanin.com](https://www.lucasjanin.com)
- GitHub: [github.com/lucasjanin](https://github.com/lucasjanin)
- LinkedIn: [linkedin.com/in/lucasjanin](https://linkedin.com/in/lucasjanin)