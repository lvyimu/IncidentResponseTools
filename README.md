# Linux Security Response Tool

A versatile security monitoring and incident response utility for Linux systems.

## Overview

This tool provides various security monitoring and response capabilities for Linux systems, including:

- SSH brute force attack detection and IP blocking
- Webshell detection across multiple web technologies
- Log analysis for suspicious activities
- Crontab inspection for malicious scheduled tasks
- IP address search across system files

The tool is designed to assist system administrators in monitoring, detecting, and responding to potential security threats.

## Features

### 🔒 SSH Brute Force Protection

Monitors authentication logs for failed login attempts and automatically blocks IPs that exceed the threshold by adding them to `/etc/hosts.deny`.

### 🔍 Webshell Detection

Searches for common webshell signatures in web application files:

- PHP files with `eval()` or `base64_decode()` functions
- JSP files with `exec()` calls
- ASP files with `execute()` calls
- ASPX files with `eval()` functions

### 📊 Log Analysis

Analyzes various system and web server logs for suspicious IP addresses or activities:

- Apache/Nginx access and error logs
- Authentication logs
- SSH secure logs

### ⏱️ Scheduled Task Inspection

Examines crontab entries and startup scripts for potentially malicious scheduled tasks.

### 🔎 IP Address Search

Searches for IP addresses across system files to identify potential security issues or unauthorized configurations.

## Installation

Clone the repository to your local system:

```bash
git clone https://github.com/yourusername/linux-security-response-tool.git
cd linux-security-response-tool
```

No additional dependencies are required beyond standard Python 3 libraries.

## Usage

```
usage: security_tool.py [-h] [-m] [-w] [-l [IP]] [-c] [-i] [-d DIRECTORIES [DIRECTORIES ...]] [-p PATTERNS [PATTERNS ...]]

Linux Security Response Tool

options:
  -h, --help            show this help message and exit
  -m, --monitor         Monitor SSH login failures and block suspicious IPs
  -w, --webshell        Scan for potential webshells in web application files
  -l [IP], --log [IP]   Analyze logs for suspicious activities, optionally focusing on a specific IP
  -c, --crontab         Check scheduled tasks for suspicious entries
  -i, --ip-search       Search for lines containing IP addresses in system files
  -d DIRECTORIES [DIRECTORIES ...], --directories DIRECTORIES [DIRECTORIES ...]
                        Specify directories to search (default: /var/log and /etc)
  -p PATTERNS [PATTERNS ...], --patterns PATTERNS [PATTERNS ...]
                        Specify file patterns to search (default: *.log, *.conf, and hosts*)
```

### Examples

Monitor SSH login attempts and automatically block suspicious IPs:

```bash
sudo python3 security_tool.py --monitor
```

Scan web directories for potential webshells:

```bash
sudo python3 security_tool.py --webshell
```

Analyze logs for a specific suspicious IP:

```bash
sudo python3 security_tool.py --log 192.168.1.100
```

Check for suspicious scheduled tasks:

```bash
sudo python3 security_tool.py --crontab
```

Search for IP addresses in custom directories and file patterns:

```bash
sudo python3 security_tool.py --ip-search --directories /opt /home --patterns *.conf *.ini
```

## Configuration

The tool uses the following default configurations:

- SSH log file: `/var/log/secure`
- Monitored web log files:
  - `/var/log/apache2/access.log`, `/var/log/apache2/error.log`
  - `/var/log/httpd/access_log`, `/var/log/httpd/error_log`
  - `/var/log/nginx/access.log`, `/var/log/nginx/error.log`
  - `/var/log/auth.log`, `/var/log/auth.log.1`
- Hosts deny file: `/etc/hosts.deny`
- Default blocking threshold: 10 failed attempts

You can modify these settings by editing the configuration variables at the top of the script.

## Requirements

- Python 3.x
- Root/sudo access for some features (monitoring log files, accessing protected files)
- Linux-based operating system

## Security Notes

- This tool requires appropriate permissions to access system logs and modify system files.
- Some functions may require root/sudo privileges to work properly.
- Always review changes before applying them in production environments.

## License

[Specify your chosen license here, e.g., MIT, GPL, etc.]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Disclaimer

This tool is provided for legitimate security monitoring and incident response purposes. Users are responsible for ensuring they have appropriate authorization to monitor and modify the systems where this tool is deployed.