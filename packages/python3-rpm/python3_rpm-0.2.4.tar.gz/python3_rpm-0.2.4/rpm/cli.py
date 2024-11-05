import fire
from log import log
from ssh.ssh import SSHClient
from rpm.rpm import RpmService

class RPM():

    def get_service(self,rpm_name):
        rpm_service = RpmService()
        service_list = rpm_service.get_service(rpm_name)
        print("-"*30+ "    service list    " + "-"*30)
        for service in service_list:
            print(service)
        print("-"*80)
        return service_list

    def get_cmd_and_param(self,rpm_name):
        rpm_service = RpmService()
        cmd_list = rpm_service.get_cmd_and_param(rpm_name)
        print("-" * 30 + "    cmd and param list    " + "-" * 30)
        for cmd_obj in cmd_list:
            print(f"{cmd_obj['cmd']} {cmd_obj['param']}")
        print("-" * 80)
        return cmd_list


def main():
    fire.Fire(
        {
            "rpm": RPM
        }
    )

if __name__=="__main__":
    main()