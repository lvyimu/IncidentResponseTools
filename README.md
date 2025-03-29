# Linux安全响应工具

一个多功能的Linux系统安全监控和应急响应实用工具。

## 概述

该工具为Linux系统提供了各种安全监控和响应功能，包括：

- SSH暴力破解攻击检测和IP封禁
- 多种Web技术下的Webshell检测
- 可疑活动的日志分析
- 恶意计划任务检查
- 系统文件中的IP地址搜索

此工具旨在帮助系统管理员监控、检测和应对潜在的安全威胁。

## 功能特性

### 🔒 SSH暴力破解防护

监控认证日志中的登录失败尝试，并自动将超过阈值的IP添加到`/etc/hosts.deny`中进行封禁。

### 🔍 Webshell检测

在Web应用程序文件中搜索常见的Webshell特征：

- 包含`eval()`或`base64_decode()`函数的PHP文件
- 包含`exec()`调用的JSP文件
- 包含`execute()`调用的ASP文件
- 包含`eval()`函数的ASPX文件

### 📊 日志分析

分析各种系统和Web服务器日志，寻找可疑IP地址或活动：

- Apache/Nginx访问和错误日志
- 认证日志
- SSH安全日志

### ⏱️ 计划任务检查

检查crontab条目和启动脚本，寻找潜在的恶意计划任务。

### 🔎 IP地址搜索

在系统文件中搜索IP地址，以识别潜在的安全问题或未授权的配置。

## 安装

将仓库克隆到本地系统：

```bash
git clone https://github.com/lvyimu/IncidentResponseTools.git
cd IncidentResponseTools
```

除标准Python 3库外，无需其他依赖项。

## 使用方法

```
usage: main.py [-h] [-m] [-w] [-l [keywards]] [-c] [-i]
               [-d DIRECTORIES [DIRECTORIES ...]] [-p PATTERNS [PATTERNS ...]]

应急响应工具

optional arguments:
  -h, --help            show this help message and exit
  -m, --monitor         监控 SSH 登录失败
  -w, --webshell        排查 Webshell
  -l [keywards], --log [keywards]
                        执行日志分析，不带参数则使用默认路径文件的ip，带参数则使用指定的关键词
  -c, --crontab         检查计划任务
  -i, --ip-search       搜索包含IP地址格式的行
  -d DIRECTORIES [DIRECTORIES ...], --directories DIRECTORIES [DIRECTORIES ...]
                        指定要搜索的目录，默认为 /var/log 和 /etc
  -p PATTERNS [PATTERNS ...], --patterns PATTERNS [PATTERNS ...]
                        指定要搜索的文件模式，默认为 *.log、*.conf 和 hosts*              
```

### 示例

监控SSH登录尝试并自动封禁可疑IP：

```bash
sudo python3 main.py --monitor
```

扫描Web目录中的潜在Webshell：

```bash
sudo python3 main.py --webshell
```

分析特定可疑IP的日志：

```bash
sudo python3 main.py --log 192.168.1.100
```

检查可疑的计划任务：

```bash
sudo python3 main.py --crontab
```

在自定义目录和文件模式中搜索IP地址：

```bash
sudo python3 main.py --ip-search --directories /opt /home --patterns *.conf *.ini
```

## 配置

该工具使用以下默认配置：

- SSH日志文件：`/var/log/secure`
- 监控的Web日志文件：
  - `/var/log/apache2/access.log`、`/var/log/apache2/error.log`
  - `/var/log/httpd/access_log`、`/var/log/httpd/error_log`
  - `/var/log/nginx/access.log`、`/var/log/nginx/error.log`
  - `/var/log/auth.log`、`/var/log/auth.log.1`
- 主机拒绝文件：`/etc/hosts.deny`
- 默认封禁阈值：10次失败尝试

您可以通过编辑脚本顶部的配置变量来修改这些设置。

## 系统要求

- Python 3.x
- 某些功能需要root/sudo访问权限（监控日志文件、访问受保护文件）
- 基于Linux的操作系统

## 安全注意事项

- 此工具需要适当的权限来访问系统日志和修改系统文件。
- 某些功能可能需要root/sudo权限才能正常工作。
- 在生产环境中应用更改前，请始终进行审查。

## 免责声明

本工具提供用于合法的安全监控和应急响应目的。用户有责任确保他们有适当的授权来监控和修改部署此工具的系统。


# IncidentResponseTools

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
git clone https://github.com/lvyimu/IncidentResponseTools.git
cd IncidentResponseTools
```

No additional dependencies are required beyond standard Python 3 libraries.

## Usage

```
usage: main.py [-h] [-m] [-w] [-l [keywards]] [-c] [-i]
               [-d DIRECTORIES [DIRECTORIES ...]] [-p PATTERNS [PATTERNS ...]]

应急响应工具

optional arguments:
  -h, --help            show this help message and exit
  -m, --monitor         监控 SSH 登录失败
  -w, --webshell        排查 Webshell
  -l [keywards], --log [keywards]
                        执行日志分析，不带参数则使用默认路径文件的ip，带参数则使用指定的关键词
  -c, --crontab         检查计划任务
  -i, --ip-search       搜索包含IP地址格式的行
  -d DIRECTORIES [DIRECTORIES ...], --directories DIRECTORIES [DIRECTORIES ...]
                        指定要搜索的目录，默认为 /var/log 和 /etc
  -p PATTERNS [PATTERNS ...], --patterns PATTERNS [PATTERNS ...]
                        指定要搜索的文件模式，默认为 *.log、*.conf 和 hosts*
```

### Examples

Monitor SSH login attempts and automatically block suspicious IPs:

```bash
sudo python3 main.py --monitor
```

Scan web directories for potential webshells:

```bash
sudo python3 main.py --webshell
```

Analyze logs for a specific suspicious IP:

```bash
sudo python3 main.py --log 192.168.1.100
```

Check for suspicious scheduled tasks:

```bash
sudo python3 main.py --crontab
```

Search for IP addresses in custom directories and file patterns:

```bash
sudo python3 main.py --ip-search --directories /opt /home --patterns *.conf *.ini
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


## Disclaimer

This tool is provided for legitimate security monitoring and incident response purposes. Users are responsible for ensuring they have appropriate authorization to monitor and modify the systems where this tool is deployed.
