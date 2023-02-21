from stat import S_ISDIR, S_ISREG
import paramiko
import os
import datetime
import time


# 檔案儲存格式 (目前存放於Server: /home/eray/projectDB/中)
# Server: /home/eray/projectDB/
#         (以下為放入projectDB的專案命名格式)
#         {ex: 台塑_船隻水位(company_project)}/
#         {ex: video1~7, model, ...}/
#         {ex: img, label}/
#         {ex: frame_00001(要>=5位數).jpg, xml}


# Define Server parameters 
HostName = '192.168.33.240'
UserName = 'xxx'
PassWord = 'xxxxxx'
Port = 22


# 選擇方法 (4 methods): "upload", "download", "upload_compressed_file", "download_compressed_file"
method = "download"


# 上傳and下載 (目前存放於Server: /home/eray/projectDB/中)
# 方法一： (資料夾)
local_dir = "/home/eray/Documents/xml_2_json/專案測試"
remote_dir = "/home/eray/projectDB/專案測試"

# 方法二: (壓縮檔 ) (only support tar.xz to compress)
# 注意: 只有下載的時候 server_folder 要是資料夾路徑  ex: "/home/eray/projectDB/專案測試"
local_tar_path = "/home/eray/Documents/xml_2_json/專案測試.tar.xz"
server_folder = "/home/eray/projectDB/專案測試.tar.xz"



# Other set
# extract_target_path = '/home/user/Downloads'
# docker_container_name = 'mxic_ladder'
# run_program_in_container = 'python /home/user/mxic/test.py'
 

class SSH_Client:
    def __init__(self, host, user, password, port):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
    

    def client(self, time_out = 20):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname = self.host, port = self.port, username = self.user, 
                        password = self.password, timeout = time_out)
            
            print("Client is connected !")
            return ssh

        except Exception as e:
            print(e)
        

    def reboot(self):
        ssh_stdin, ssh_stdout, ssh_stderr = self.client().exec_command("sudo shutdown -r now")
        if ssh_stdout.channel.recv_exit_status() > 0:
            raise RuntimeError("AUT reboot failed")


    def test_reboot(self):
        self.client().exec_command('echo P@ssw0rd | sudo -S reboot')
        print("Command have been completed")


    def testCommand(self):
        stdin, stdout, stderr = self.client().exec_command('ls -l')
        # stdin, stdout, stderr = self.client().exec_command('mkdir test202205')
        # print(stdout.read().decode("utf-8"))

        for line in stdout.readlines():
            print(line)

        self.client().close()


    def run_shell(self, shell_str, time = 4):
        # shell command
        stdin, stdout, stderr = self.client(time_out = time).exec_command(shell_str)
    
        # print(stdout.read().decode("utf-8"))
        for line in stdout.readlines():
            print(line)


    def sshCommand(self, local_path, server_path):
        extract_target_path = os.path.join(server_path, "test.tar.xz")
        print("tar -C /home/user/Downloads/ -xvf " + str(extract_target_path))
        
        self.run_shell('tar -C /home/user/Downloads/ -xvf' + str(extract_target_path))
    
        # self.run_shell("docker stop mxic_ladder")
        # self.run_shell("docker start mxic_ladder")
        # self.run_shell("docker exec mxic_ladder python /home/user/mxic/test.py")
    
        self.client().close()


    def test_ssh(self):
        try:
            self.run_shell("ls -l")
            # self.run_shell("mkdir projectDB; ls -l")
            # self.run_shell("cd projectDB; ls -l")
            # self.run_shell("tree projectDB")
            # self.run_shell("tar zcvf test202205.tar.gz ./test202205; ls -l")

            # self.run_shell("cat start_docker.sh")
            # self.run_shell("rm -rf test202205; ls -l")
            # self.run_shell('python3 /home/eray/share1/2to3.py')

        except Exception as e:
            print(e)        


class SFTP_Client:
    def __init__(self, host, user, password, port):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.flag = True


    def client(self):
        try:
            t = paramiko.Transport((self.host, self.port))
            t.connect(username = self.user, password = self.password)
            sftp = paramiko.SFTPClient.from_transport(t)
            
            if self.flag:
                print("Client is connected !")

            self.flag = False
            return t, sftp

        except Exception as e:
            print(e)


    def testUpdate(self, local_path, remote_path):
        t, sftp = self.client()
        try:
            sftp.chdir(".")
            # print(sftp.getcwd())

            if remote_path not in sftp.listdir(sftp.getcwd()):
                sftp.mkdir(remote_path)
            # print(sftp.listdir(self.remote_path))

            files = os.listdir(local_path)
            # files = sftp.listdir(self.remote_path)
            for f in files:
                #'#########################################'
                #'Beginning to upload file %s ' % datetime.datetime.now()
                #'Uploading file:', os.path.join(self.local_path, f)
                # sftp.get(os.path.join(self.remote_path,f),os.path.join(self.local_path,f))
                sftp.put(os.path.join(local_path, f), os.path.join(remote_path, f))
                #'Upload file success %s ' % datetime.datetime.now()

            print("Upload Success!")
            # print("Download Success !")
            t.close()

        except Exception as e:
            print(e)
            print("Upload Fail")


    # local_tar_path = "/home/eray/Documents/xml_2_json/test_have_dirs.tar.xz"
    # server_folder = "/home/eray/projectDB/test_have_dirs.tar.xz"
    def sftpUpdate_SingleFile(self, local_path, server_path):
        # 上傳: 單檔(一般檔或壓縮檔) or 單一資料夾多檔(資料夾內不包含資料夾)
        t, sftp = self.client()
        try:
            print("正在上傳壓縮檔!")
            sftp.put(local_path, server_path)

            print("Upload Success !")
            t.close()

        except Exception as e:
            print(e)
            print("Upload Fail")


    # server_folder = "/home/eray/projectDB/test_have_dirs"
    # local_tar_path = "/home/eray/Documents/xml_2_json"
    def sftpDownload_SingleFile(self, server_path, local_path):
        # 下載: 單檔(一般檔或壓縮檔) or 單一資料夾多檔(資料夾內不包含資料夾, 多資料夾壓縮檔)
        t, sftp = self.client()
        try:
            print("正在下載壓縮檔!")
            sftp.get(server_path, local_path)

            print("Download Success !")
            t.close()

        except Exception as e:
            print(e)
            print("Download Fail")


    # local_dir = "/home/eray/Documents/xml_2_json/test202205"
    # remote_dir = "/home/eray/projectDB/test202205"
    def sftpUpdate_Folder(self, local_path, remote_path):
        # 上傳: 多層資料夾檔案
        t, sftp = self.client()

        prev_remote_dir = remote_path.replace("/"+remote_path.split("/")[-1], "")
        if remote_path.split("/")[-1] not in sftp.listdir(prev_remote_dir):
            sftp.mkdir(remote_path)

        try:
            for root, dirs, files in os.walk(local_path):
                if files:
                    for filespath in files:
                        local_file = os.path.join(root, filespath)
                        # print(local_file)
                        dir_path = local_file.replace(local_path+"/", "")
                        # print(dir_path)
            
                        remote_file = os.path.join(remote_path, dir_path)

                        try: 
                            sftp.put(local_file, remote_file)

                            print(f"Upload data:  {dir_path}")
                            print(f"Server:  {remote_file}\n")

                        except Exception as e:
                            # print(e, "\n")
                            sftp.mkdir(os.path.split(remote_file)[0])
                            sftp.put(local_file, remote_file)

                if dirs:
                    for name in dirs:
                        local_des = os.path.join(root, name)
                        des_path = local_des.replace(local_path+"/", "")
                        # print(des_path)

                        remote_route = os.path.join(remote_path, des_path)
            
                        try:
                            sftp.mkdir(remote_route)
                            # print(f"Build Server folder:  {des_path}")
                
                        except Exception as e:
                            print(e)

            print('Upload Folder Success !')
            t.close() 

        except Exception as e:
            print(e)
            print("Upload Fail")
    

    def folder_recursive(self, remote_iter_path, local_iter_path):
        # 下載遞迴器
        _, sftp = self.client()

        for path in sftp.listdir_attr(remote_iter_path):
            sftp_current_path = os.path.join(remote_iter_path, path.filename)
            local_current_path = os.path.join(local_iter_path, path.filename)
            
            mode = path.st_mode
            if S_ISREG(mode):
                sftp.get(sftp_current_path, local_current_path)
                print(f"Server:  {sftp_current_path}")
                print(f"Local download:  {local_current_path}\n")

            if S_ISDIR(mode):
                try:
                    os.mkdir(local_current_path)

                except Exception as e:
                    print(e, "\n")

                self.folder_recursive(sftp_current_path, local_current_path)
            

    # server_des = "/home/eray/projectDB/test202205"
    # local_des = "/home/eray/Documents/xml_2_json/test202205"       
    def sftpDownload_Folder(self, remote_path, local_path):
        # 下載: 多層資料夾檔案
        t, _ = self.client()
        try:
            prev_local_dir = local_path.replace("/"+local_path.split("/")[-1], "")
            
            if remote_path.split("/")[-1] not in os.listdir(prev_local_dir):
                os.mkdir(remote_path.split("/")[-1])

            self.folder_recursive(remote_path, local_path)
            
            print('Download Folder Success !')
            t.close()

        except Exception as e:
            print(e)
            print("Download Fail")  


def Update_and_Decompress(Host, User, Password, Port_, local_route, server_route):
    # upload
    SFTP_Client(Host, User, Password, Port_).sftpUpdate_SingleFile(local_route, server_route)

    # decompress
    print("正在解壓縮資料夾! 和清除壓縮檔!")
    SSH_Client(Host, User, Password, Port_).run_shell(f"cd projectDB; tar Jxvf {local_route.split('/')[-1]}")
    SSH_Client(Host, User, Password, Port_).run_shell(f"cd projectDB; rm -r {local_route.split('/')[-1]}; ls -l")


def Compress_and_Download(Host, User, Password, Port_, server_route, local_route):
    # compress
    compressed_name = server_route.split('/')[-1] + ".tar.xz"
    print("正在壓縮資料夾!")
    SSH_Client(Host, User, Password, Port_).run_shell(f"cd projectDB; tar Jcvf {compressed_name} ./{server_route.split('/')[-1]}; ls -l")

    # download
    SFTP_Client(Host, User, Password, Port_).sftpDownload_SingleFile(server_route + ".tar.xz", local_route)

        
if __name__ == "__main__":

    begin = time.time()

    # == SSH == #
    '''
    用paramiko 去執行cd指令 只會在單一exec啟作用，作用完 會回歸原本路徑
    '''
    # SSH_Client(HostName, UserName, PassWord, Port).test_ssh()
    # SSH_Client(HostName, UserName, PassWord, Port).sshCommand(local_tar_path, server_folder)
    # SSH_Client(HostName, UserName, PassWord, Port).testCommand()
    

    # == SFTP == #
    if method == "upload":
        SFTP_Client(HostName, UserName, PassWord, Port).sftpUpdate_Folder(local_dir, remote_dir)
        SSH_Client(HostName, UserName, PassWord, Port).run_shell("cd projectDB; ls-l")

    elif method == "download":
        SFTP_Client(HostName, UserName, PassWord, Port).sftpDownload_Folder(remote_dir, local_dir)
        SSH_Client(HostName, UserName, PassWord, Port).run_shell("cd projectDB; ls-l")

    elif method == "upload_compressed_file":
        Update_and_Decompress(HostName, UserName, PassWord, Port, local_tar_path, server_folder)

    elif method == "download_compressed_file":
        Compress_and_Download(HostName, UserName, PassWord, Port, server_folder, local_tar_path)


    # Other methods:
    # SFTP_Client(HostName, UserName, PassWord, Port).testUpdate(local_dir, remote_dir)
    
    end = time.time()
    print(f"\nSpent {end-begin:.2f} seconds!")

