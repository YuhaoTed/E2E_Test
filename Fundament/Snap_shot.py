import paramiko
import scpclient
from scp import SCPClient
import time
class Snap_Shot:

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    scpclient = None
    ssh_session = None
    shell = None
    Flag = True
    def Connect(self):
        try:
            self.ssh.connect(hostname='192.168.1.4', port=22, username = 'root',password='root')

            self.scpclient = SCPClient(self.ssh.get_transport(),socket_timeout=15.0)

            self.ssh_session = self.ssh.get_transport().open_session()
            self.shell = self.ssh.invoke_shell()
        except Exception as ex:
            print("连接发送失败")
            return False
        return True
    def Get_png(self):
        if self.Flag:
            #第一次输入
            self.shell.send("ash -lc 'tsd.system.displaymanager.mib3.app.test-client-dsi'\n")
            self.Flag = False
        time.sleep(0.5)
        try:
            self.shell.send("screenshot /tmp/1.png\n")
            time.sleep(1)
            self.scpclient.get('/tmp/1.png', local_path='D:\\software\\pythonProject\\SC')
            time.sleep(0.5)
        except Exception as ex:
            #print("截图失败")
            return False
        #print("截图成功")
        return True
