import re
import os
from log import log
from ssh.ssh import SSHClient
from chatgpt.chatgpt import ChatGPT


class RpmService():
    def get_service(self, rpm_name):
        log.info(f"begin to get service list for {rpm_name}...")
        ssh = SSHClient(ip=os.environ.get("SERVER_IP", "127.0.0.1"), port=os.environ.get("SERVER_PORT", 22),
                        username=os.environ.get("SERVER_USERNAME", "root"),
                        password=os.environ.get("SERVER_PASSWORD", "root@123"))
        ssh.exec(f"dnf install -y {rpm_name}", timeout=1200)
        output = ssh.exec("rpm -ql " + rpm_name + " | grep -E 'service$'|grep -v @|awk -F / '{print $NF}'",
                          timeout=20).stdout.strip()
        service_list = [elem.strip() for elem in output.split("\n") if ".service" in elem]
        log.info(f"total {len(service_verify_list)} service list. They are:")
        return service_list

    def service_only_need_start_once(self,service):
        log.info(f"begin to get service {service} whether is only start once...")
        ssh = SSHClient(ip=os.environ.get("SERVER_IP", "127.0.0.1"), port=os.environ.get("SERVER_PORT", 22),
                        username=os.environ.get("SERVER_USERNAME", "root"),
                        password=os.environ.get("SERVER_PASSWORD", "root@123"))
        output = ssh.exec(f"find /usr/ /etc/ -name {service_name}|head -n 1|xargs cat|grep Type=oneshot").stdout
        if "Type=oneshot" in output:
            log.info(f"service {service_name} only need to start once.")
            return True
        else:
            log.info(f"service {service_name} can start more than once.")
            return False

    # def get_sub_command_list(self, command):
    #     chatgpt = ChatGPT(base_url=os.environ.get("OPENAI_BASE_URL","http://127.0.0.1"),api_key=os.environ.get("OPENAI_API_KEY","xxx"))
    #     sub_commands = []
    #     question = f"请列出 {command} 命令的子命令列表，只需要列出子命令列表，无需其他任何多余的解释，如果没有子命令，则直接返回空字符串"
    #     rs = chatgpt.ask(question)
    #     rs = rs.strip().replace("-", "").strip()
    #     for elem in rs.split("\n"):
    #         temp = re.search("([a-zA-Z]+)", elem)
    #         if temp:
    #             sub_command = temp.group(1)
    #             if sub_command != command:
    #                 sub_commands.append(temp.group(1))
    #     return sub_commands

    def get_sub_command_list(self,ssh,cmd):
        sub_commands=[]
        output = ssh.exec(
            cmd + " --help 2>&1|grep -E '^( {2,4})[a-zA-Z][^: =\.]* -* {1,8}[a-zA-Z\-]+' |awk -F ' ' '{print $1}'",
            timeout=60).stdout.strip()
        if output.strip():
            for line in output.strip().split("\n"):
                if line.strip not in sub_commands:
                    sub_commands.append(line.strip())
        return sub_commands

    def get_param_list(self,cmd):
        ssh = SSHClient(ip=os.environ.get("SERVER_IP", "127.0.0.1"), port=os.environ.get("SERVER_PORT", 22),
                        username=os.environ.get("SERVER_USERNAME", "root"),
                        password=os.environ.get("SERVER_PASSWORD", "root@123"))
        params = []
        output = ssh.exec(
                cmd + " --help 2>&1 |grep -Ei '^ *-+[-a-zA-Z]'",
                timeout=120).stdout.strip()
        for line in output.split("\n"):
            temp = re.search("^\s*(-\w+)\#*", line)
            if temp:
                param = temp.group(1)
                if param not in params:
                    params.append(param)
            temp = re.search("^\s*(--[\w\-]+)", line)
            if temp:
                param = temp.group(1)
                if param not in params:
                    params.append(param)
            temp = re.search("^\s*-\S+,\s*(--[\w\-]+)", line)
            if temp:
                param = temp.group(1)
                if param not in params:
                    params.append(param)
            temp = re.search("^\s*-\w+\s*\|\s*(--[\w\-]+)", line)
            if temp:
                param = temp.group(1)
                if param not in params:
                    params.append(param)
        return params


    def get_cmd_and_param(self, rpm_name):
        log.info(f"begin to get cmd and param for {rpm_name}...")
        ssh = SSHClient(ip=os.environ.get("SERVER_IP", "127.0.0.1"), port=os.environ.get("SERVER_PORT", 22),
                        username=os.environ.get("SERVER_USERNAME", "root"),
                        password=os.environ.get("SERVER_PASSWORD", "root@123"))
        ssh.exec(f"dnf install -y {rpm_name}", timeout=1200)
        output = ssh.exec("rpm -ql " + rpm_name + " | grep /usr/bin | awk -F'/' '{print $NF}'",
                          timeout=10).stdout.strip()
        cmd_temp_list = [line.strip() for line in output.split("\n") if line.strip()]
        cmds=[]
        for cmd in cmd_temp_list:
            rs=ssh.exec(f"command -v {cmd}", timeout=1200)
            if rs.exit_status_code == 0:
                cmds.append(cmd)
        cmds_list = []
        for cmd in cmds:
            sub_commands = self.get_sub_command_list(ssh,cmd)
            if sub_commands:
                for sub_command in sub_commands:
                    if sub_command and sub_command != cmd:
                        new_command = f"{cmd} {sub_command}"
                    else:
                        new_command = cmd
                    if new_command not in cmds_list:
                        cmds_list.append(new_command)
            else:
                cmds_list.append(cmd)
        cmd_params_list=[]
        for cmd in cmds_list:
            params = self.get_param_list(cmd)
            for param in params:
                tmp={
                    "cmd":cmd,
                    "param":param
                }
                cmd_params_list.append(tmp)
        return cmd_params_list


