# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import re
import subprocess
import time
import os
import argparse
import glob

# 配置项
logfile = "/var/log/secure"
web_logfiles = [
    "/var/log/apache2/access.log", "/var/log/apache2/error.log",
    "/var/log/httpd/access_log", "/var/log/httpd/error_log",
    "/var/log/auth.log", "/var/log/auth.log.1",
    "/var/log/secure",
    "/var/log/nginx/access.log", "/var/log/nginx/error.log"
]
hostdeny = "/etc/hosts.deny"
num = 10  # 封禁阈值

# 统计密码错误次数
errordict = {}

commands_webshell = [
    'find ./ -type f -name "*.jsp" | xargs grep "exec("',
    'find ./ -type f -name "*.php" | xargs grep "eval("',
    'find ./ -type f -name "*.asp" | xargs grep "execute("',
    'find ./ -type f -name "*.aspx" | xargs grep "eval("',
    'find ./ -type f -name "*.php" | xargs grep "base64_decode"'
]


def getdenies():
    """获取已封禁 IP"""
    denieddict = {}
    if os.path.exists(hostdeny):
        with open(hostdeny, "r") as f:
            for line in f:
                match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if match:
                    denieddict[match.group(1)] = 1
    return denieddict


def monitor():
    """监控 SSH 登录失败日志并封禁可疑 IP"""
    denieddict = getdenies()
    with subprocess.Popen(['tail', '-F', logfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as popen:
        print(f"监控 {logfile} ...")
        while True:
            time.sleep(0.1)
            line = popen.stdout.readline().strip()
            if not line:
                continue

            # 将 bytes 转换为 string
            line_str = line.decode('utf-8', errors='ignore')

            match_invalid = re.search(r'Invalid user \w+ from (\d+\.\d+\.\d+\.\d+)', line_str)
            match_failed = re.search(r'Failed password for \w+ from (\d+\.\d+\.\d+\.\d+)', line_str)

            if match_invalid:
                ip = match_invalid.group(1)
            elif match_failed:
                ip = match_failed.group(1)
                errordict[ip] = errordict.get(ip, 0) + 1
                if errordict[ip] < num:
                    continue
            else:
                continue

            if ip not in denieddict:
                subprocess.call(f"echo 'sshd:{ip}' >> {hostdeny}", shell=True)
                denieddict[ip] = 1
                print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 封禁 IP: {ip}")
                errordict.pop(ip, None)


def Investigation():
    """排查 Webshell"""
    for cmd in commands_webshell:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        # 确保输出是字符串
        stdout_str = stdout.decode('utf-8', errors='ignore') if stdout else ""
        stderr_str = stderr.decode('utf-8', errors='ignore') if stderr else ""

        if "Permission denied" in stderr_str:
            print(f"权限不足，尝试 sudo 运行: {cmd}")
            run_command(cmd, use_sudo=True)
        else:
            print(stdout_str or "无匹配项")
            if stderr_str:
                print(f"错误:\n{stderr_str}")


def run_command(cmd, use_sudo=False):
    """执行命令"""
    if use_sudo:
        cmd = f"sudo {cmd}"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # 确保输出是字符串
    stdout_str = stdout.decode('utf-8', errors='ignore') if stdout else ""
    stderr_str = stderr.decode('utf-8', errors='ignore') if stderr else ""

    if stdout_str:
        print(stdout_str)
    if stderr_str:
        print(f"错误:\n{stderr_str}")


def log_analysis(ip=None):
    """日志分析"""

    def grep_logs(files, keyword):
        for log_file in files:
            if os.path.exists(log_file):
                print(f"\n搜索 {keyword} 关键字于: {log_file}")
                cmd = f'grep "{keyword}" {log_file}'
                run_command(cmd)

    if ip:
        print(f"\n分析日志中 IP: {ip}")
        grep_logs(web_logfiles, ip)
    else:
        print("未提供 IP，默认检查 hosts.deny 封禁的 IP")
        denied_ips = getdenies()  # 获取 hosts.deny 里的 IP
        if not denied_ips:
            print("未找到封禁的 IP，跳过分析。")
        else:
            for ip in denied_ips:
                grep_logs(web_logfiles, ip)


def search_ip_in_files(search_dirs=None, file_patterns=None):
    """搜索包含IP地址的行并打印出来（包括文件名）"""
    # 默认搜索目录
    if search_dirs is None:
        search_dirs = ['/var/log', '/etc']

    # 默认文件模式
    if file_patterns is None:
        file_patterns = ['*.log', '*.conf', 'hosts*']

    # IP地址的正则表达式模式
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

    # 文件计数器
    file_count = 0
    line_count = 0

    print(f"开始搜索IP地址...\n")
    print(f"搜索目录: {', '.join(search_dirs)}")
    print(f"文件模式: {', '.join(file_patterns)}")
    print("-" * 80)

    # 遍历每个目录和文件模式
    try:
        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                print(f"警告: 目录不存在 - {search_dir}")
                continue

            for pattern in file_patterns:
                # 构建搜索路径
                search_path = os.path.join(search_dir, '**', pattern)

                # 使用glob递归搜索所有匹配的文件
                for filepath in glob.glob(search_path, recursive=True):
                    if not os.path.isfile(filepath):
                        continue

                    file_count += 1

                    try:
                        with open(filepath, 'r', errors='ignore') as file:
                            for line_num, line in enumerate(file, 1):
                                if ip_pattern.search(line):
                                    line_count += 1
                                    # 删除多余空白字符并限制长度
                                    clean_line = ' '.join(line.strip().split())
                                    if len(clean_line) > 200:
                                        clean_line = clean_line[:197] + '...'
                                    print(f"{filepath}:{line_num}: {clean_line}")
                    except (PermissionError, IOError) as e:
                        print(f"无法读取文件 {filepath}: {e}")
    except Exception as e:
        print(f"搜索过程中出错: {e}")

    print("-" * 80)
    print(f"搜索完成。检查了 {file_count} 个文件，发现 {line_count} 行包含IP地址。")


def crontab_check():
    """检查计划任务"""
    file_path = "/etc/rc.local"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            print(file.read())
    else:
        print(f"文件 {file_path} 不存在。")

    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, check=True)
        print(result.stdout.decode('utf-8', errors='ignore'))
    except AttributeError:
        # 对于较旧的 Python 版本，capture_output 可能不存在
        result = subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode('utf-8', errors='ignore'))
    finally:
        print("\n检查计划任务完成")


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="应急响应工具")
    parser.add_argument("-m", "--monitor", action="store_true", help="监控 SSH 登录失败")
    parser.add_argument("-w", "--webshell", action="store_true", help="排查 Webshell")
    parser.add_argument("-l", "--log", metavar="keywards", nargs="?", const="default",
                        help="执行日志分析，不带参数则使用默认路径文件的ip，带参数则使用指定的关键词")
    parser.add_argument("-c", "--crontab", action="store_true", help="检查计划任务")
    parser.add_argument("-i", "--ip-search", action="store_true",
                        help="搜索包含IP地址格式的行")
    parser.add_argument("-d", "--directories", nargs="+",
                        help="指定要搜索的目录，默认为 /var/log 和 /etc")
    parser.add_argument("-p", "--patterns", nargs="+",
                        help="指定要搜索的文件模式，默认为 *.log、*.conf 和 hosts*")
    return parser.parse_args()


def main():
    """主程序入口"""
    args = parse_args()

    if args.monitor:
        monitor()
    elif args.webshell:
        Investigation()
    elif args.log is not None:
        if args.log == "default":
            log_analysis()
        else:
            log_analysis(args.log)
    elif args.crontab:
        crontab_check()
    elif args.ip_search:
        search_ip_in_files(args.directories, args.patterns)
    else:
        print("请提供正确的参数，使用 -h 获取帮助。")


if __name__ == '__main__':
    main()