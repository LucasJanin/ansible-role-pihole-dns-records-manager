#!/usr/bin/env python3
# manage_pihole_dns_records.py
# Script to add or remove DNS records from Pi-hole's TOML configuration file while preserving comments and formatting

import sys
import os
import re
import json
import argparse

def main():
    # Create a parser with a more detailed description
    parser = argparse.ArgumentParser(
        description='Manage Pi-hole DNS records in the TOML configuration file.',
        epilog='''
Examples:
  # Add a single DNS record
  python3 manage_pihole_dns_records.py --action add --hostnames "toto" --ips "192.168.1.11"
  
  # Add multiple DNS records
  python3 manage_pihole_dns_records.py --action add --hostnames '["toto", "server1"]' --ips '["192.168.1.11", "192.168.1.12"]'
  
  # Remove a single DNS record by hostname
  python3 manage_pihole_dns_records.py --action remove --hostnames "toto"
  
  # Remove multiple DNS records by hostname
  python3 manage_pihole_dns_records.py --action remove --hostnames '["toto", "server1"]'
  
  # Specify a different config file path
  python3 manage_pihole_dns_records.py --action add --hostnames "toto" --ips "192.168.1.11" --config "/path/to/pihole.toml"
''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--action', choices=['add', 'remove'], default='add', 
                        help='Action to perform: add new DNS records or remove existing ones')
    parser.add_argument('--hostnames', required=True, 
                        help='JSON array of hostnames or a single hostname (e.g., "toto" or ["toto", "server1"])')
    parser.add_argument('--ips', 
                        help='JSON array of IPs or a single IP (required for add action, e.g., "192.168.1.11" or ["192.168.1.11", "192.168.1.12"])')
    parser.add_argument('--config', default='/tmp/pihole.toml', 
                        help='Path to Pi-hole TOML config file (default: /tmp/pihole.toml)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.action == 'add' and not args.ips:
        print("Error: --ips is required for add action")
        parser.print_help()
        sys.exit(1)
    
    # Parse hostnames
    try:
        hostnames = json.loads(args.hostnames)
        if not isinstance(hostnames, list):
            hostnames = [hostnames]
    except json.JSONDecodeError:
        # If JSON parsing fails, assume it's a single hostname
        hostnames = [args.hostnames]
    
    # Parse IPs if provided
    ips = None
    if args.ips:
        try:
            ips = json.loads(args.ips)
            if not isinstance(ips, list):
                ips = [ips]
        except json.JSONDecodeError:
            # If JSON parsing fails, assume it's a single IP
            ips = [args.ips]
        
        # Validate that hostnames and IPs have the same length for add action
        if args.action == 'add' and len(hostnames) != len(ips):
            print("Error: The lists of hostnames and IPs must have the same length")
            sys.exit(1)
    
    # Path to Pi-hole configuration file
    pihole_config_path = args.config
    
    # Check if the file exists
    if not os.path.exists(pihole_config_path):
        print(f"Error: {pihole_config_path} does not exist")
        sys.exit(1)
    
    try:
        # Read the file content
        with open(pihole_config_path, 'r') as f:
            lines = f.readlines()
        
        # Find the real hosts array (not in comments)
        hosts_line_index = -1
        for i, line in enumerate(lines):
            # Skip commented lines (those starting with #)
            if line.strip().startswith('#'):
                continue
            
            # Look for the actual hosts = [ line
            if re.search(r'^\s*hosts\s*=\s*\[', line.strip()):
                hosts_line_index = i
                break
        
        if hosts_line_index == -1:
            print("Error: 'hosts' array not found in the configuration file")
            sys.exit(1)
        
        # Determine the indentation style from the existing content
        indent = None
        for i in range(hosts_line_index + 1, len(lines)):
            if '"' in lines[i] and not lines[i].strip().startswith('#'):
                indent_match = re.match(r'(\s+)"', lines[i])
                if indent_match:
                    indent = indent_match.group(1)
                    break
        
        if indent is None:
            # If no existing entries with indentation found, use default
            indent = '    '
        
        if args.action == 'add':
            # Create a mapping of hostname to IP for the new records
            hostname_to_ip = {hostname: ip for hostname, ip in zip(hostnames, ips)}
            
            # First, remove any existing records with the same hostnames but different IPs
            existing_records = {}
            lines_to_remove = []
            
            for i, line in enumerate(lines):
                if i <= hosts_line_index:
                    continue
                
                # Skip commented lines
                if line.strip().startswith('#'):
                    continue
                
                # Look for DNS record entries
                match = re.search(r'"([0-9.]+)\s+([^"]+)"', line)
                if match:
                    ip = match.group(1)
                    hostname = match.group(2)
                    
                    # Check if this hostname is in our list to add
                    if hostname in hostname_to_ip and hostname_to_ip[hostname] != ip:
                        lines_to_remove.append(i)
                        existing_records[hostname] = ip
            
            # Remove lines from bottom to top to avoid index shifting
            removed_records = []
            for i in sorted(lines_to_remove, reverse=True):
                line = lines.pop(i)
                match = re.search(r'"([^"]+)"', line)
                if match:
                    removed_records.append(match.group(1))
            
            # Now add the new records
            new_records = [f"{ip} {hostname}" for hostname, ip in hostname_to_ip.items()]
            new_lines = []
            records_added = 0
            
            for new_record in new_records:
                # Check if the exact record already exists (should not happen after removals)
                record_exists = False
                for line in lines:
                    if f'"{new_record}"' in line or f"'{new_record}'" in line:
                        record_exists = True
                        break
                
                if not record_exists:
                    new_lines.append(f'{indent}"{new_record}",\n')
                    records_added += 1
            
            # Insert the new records after the hosts = [ line
            for i, new_line in enumerate(new_lines):
                lines.insert(hosts_line_index + 1 + i, new_line)
            
            # Write the updated content back to the file
            with open(pihole_config_path, 'w') as f:
                f.writelines(lines)
            
            # Print summary
            if len(removed_records) > 0:
                print(f"Removed {len(removed_records)} existing records with different IPs:")
                for record in removed_records:
                    print(f"  - {record}")
            
            if records_added > 0:
                print(f"Added {records_added} new records:")
                for record in new_records:
                    print(f"  - {record}")
            
            if len(removed_records) == 0 and records_added == 0:
                print("All records already exist with the correct IPs, no changes made")
            
            sys.exit(0)
            
        elif args.action == 'remove':
            # Remove records that match the hostnames
            records_removed = 0
            removed_records = []
            new_lines = []
            
            # Keep track of which lines to keep
            for i, line in enumerate(lines):
                keep_line = True
                
                # Check if this line contains a record to remove
                for hostname in hostnames:
                    # Match either "IP hostname" or just "hostname" in the line
                    if (f' {hostname}"' in line or f' {hostname},' in line or 
                        line.strip() == f'"{hostname}"' or line.strip() == f'"{hostname}",'):
                        keep_line = False
                        records_removed += 1
                        # Extract the full record for reporting
                        match = re.search(r'"([^"]+)"', line)
                        if match:
                            removed_records.append(match.group(1))
                        break
                
                if keep_line:
                    new_lines.append(line)
            
            if records_removed == 0:
                print("No matching records found, no changes made")
                sys.exit(0)
            
            # Write the updated content back to the file
            with open(pihole_config_path, 'w') as f:
                f.writelines(new_lines)
            
            print(f"Removed {records_removed} records successfully while preserving formatting")
            for record in removed_records:
                print(f"  - {record}")
            sys.exit(0)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
