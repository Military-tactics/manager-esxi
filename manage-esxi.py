from pyVim import Connect, connect
from pyVmomi import vim
import pyVim.task

def connect_to_vcenter(vcenter_ip, vcenter_user, vcenter_password):
    try:
        si = connect.SmartConnect(host=vcenter_ip, user=vcenter_user, pwd=vcenter_password)
        si.Disconnect()
        return si
    except Exception as e:
        print(f"Could not connect to vCenter: {e}")
        sys.exit(-1)

def get_esxi_hosts(si):
    content = si.RetrieveContent()
    esxi_hosts = content.hostFolder.childEntity
    return esxi_hosts

def start_vm(si, vm):
    try:
        task = vm.PowerOn()
        wait_for_tasks(si, [task])
    except Exception as e:
        print(f"Could not start VM {vm.name}: {e}")

def stop_vm(si, vm):
    try:
        task = vm.PowerOff()
        wait_for_tasks(si, [task])
    except Exception as e:
        print(f"Could not stop VM {vm.name}: {e}")

def wait_for_tasks(si, tasks):
    for task in tasks:
        pyVim.task.WaitForTask(task, si.RetrieveContent())

def main():
    vcenter_ip = 'vcenter_ip_address'
    vcenter_user = 'vcenter_username'
    vcenter_password = 'vcenter_password'

    si = connect_to_vcenter(vcenter_ip, vcenter_user, vcenter_password)

    esxi_hosts = get_esxi_hosts(si)
    for host in esxi_hosts:
        if isinstance(host, vim.HostSystem):
            print(f"ESXi Host: {host.name}")
            print(f"  IP Address: {host.network.ipConfig.ipAddress[0]}")
            print(f"  Version: {host.summary.config.product.version}")
            print(f"  Status: {host.summary.runtime.connectionState}")
            print("\n")

            # 这里可以添加更多的操作，例如启动/停止虚拟机
            # 例如，启动所有已停止的虚拟机
            powered_off_vms = [vm for vm in host.vm if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOff]
            for vm in powered_off_vms:
                start_vm(si, vm)

            powered_on_vms = [vm for vm in host.vm if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn]
            for vm in powered_on_vms:
                stop_vm(si, vm)

    si.Disconnect()

if __name__ == "__main__":
    main()

#在这个脚本中添加了异常处理来捕获并报告连接错误或其他操作错误。涉及获取ESXi主机信息，以及启动和停止虚拟机等操作

