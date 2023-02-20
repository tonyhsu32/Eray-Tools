import paramiko
import os
import datetime

hostname = '192.168.220.27'
username = 'user'
password = 'Fongcon123456'
port = 22

local_dir = '/home/eray/myImageTool/ftp/test'
remote_dir = '/home/user/test202110'

code_tar_path= "/home/eray/share1/fix_cant_stop"
target_folder= "/home/user/Downloads"
extract_target_path= '/home/user/Downloads'
docker_container_name= 'mxic_ladder'
run_program_in_container= 'python /home/user/mxic/test.py'
 
# def reboot():
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(hostname=DEVICE_IP, username=DEVICE_USERNAME, password=DEVICE_PASSWORD)
#     ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo shutdown -r now")
#     if ssh_stdout.channel.recv_exit_status() > 0:
#         raise RuntimeError("AUT reboot failed")

# def test():
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     client.connect(ip, port=22, username=username, password=password, timeout=20)
#     client.exec_command('echo P@ssw0rd | sudo -S reboot')
#     print("Command have been completed")
        
def testCommand(hostname, username, password, port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username=username, password=password, timeout=4)
    
    #stdin, stdout, stderr = client.exec_command('ls -l')
    stdin, stdout, stderr = client.exec_command('mkdir test202110')
    #print(stdout.read())
    for line in stdout.readlines():
        print(line)
    client.close()
    
def testUpdate(hostname, username, password, port, local_dir, remote_dir):
    
    try:
        
        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        #        files=sftp.listdir(dir_path)
        files = os.listdir(local_dir)
        for f in files:
            #'#########################################'
            #'Beginning to upload file %s ' % datetime.datetime.now()
            #'Uploading file:', os.path.join(local_dir, f)
            # sftp.get(os.path.join(dir_path,f),os.path.join(local_path,f))
            sftp.put(os.path.join(local_dir, f), os.path.join(remote_dir, f))
            #'Upload file success %s ' % datetime.datetime.now()
        t.close()
    except:
        print("upload fail")
        
def sftpUpdate_SingleFile(hostname, username, password, port, code_tar_path, target_folder):
    
    t = paramiko.Transport((hostname, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    
    sftp.put(code_tar_path,  os.path.join(target_folder, "test.tar.xz"))
        
    t.close()
    
def sftpUpdate_Folder(hostname, username, password, port, local_dir, remote_dir):
    
    t = paramiko.Transport((hostname, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    
    #sftp.put(code_tar_path,  os.path.join(target_folder, "test.tar.xz"))   
    #t.close()
    
    for root, dirs, files in os.walk(local_dir):
        for filespath in files:
            local_file = os.path.join(root, filespath)
            a = local_file.replace(local_dir, "")
            remote_file = os.path.join(remote_dir, a)
            
            try:
                sftp.put(local_file, remote_file)
            except Exception as e:
                sftp.mkdir(os.path.split(remote_file)[0])
                sftp.put(local_file, remote_file)
    
        for name in dirs:
            local_path = os.path.join(root, name)
            a = local_path.replace(local_dir, "")
            remote_path = os.path.join(remote_dir, a)
            try:
                sftp.mkdir(remote_path)
            except Exception as e:
                print(e)
    
    print('upload folder success')
    t.close()    
    
    
def run_shell(client, shell_str):
    
    stdin, stdout, stderr = client.exec_command(shell_str)
        
    #print(stdout.read())
    for line in stdout.readlines():
        print(line)
        
def sshCommand(hostname, username, password, port, code_tar_path, target_folder):
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username=username, password=password, timeout=4)
    
    extract_target_path = os.path.join(target_folder, "test.tar.xz")
    print ("tar -C /home/user/Downloads/ -xvf " + str(extract_target_path))
    run_shell(client, 'tar -C /home/user/Downloads/ -xvf' + str(extract_target_path))
    
    run_shell(client, "docker stop mxic_ladder")
    run_shell(client, "docker start mxic_ladder")
    run_shell(client, "docker exec mxic_ladder python /home/user/mxic/test.py")
    
    
    client.close()

def test(hostname, username, password, port):
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username=username, password=password, timeout=4)
    #run_shell(client, 'python3 /home/eray/share1/2to3.py')
    
        
if __name__ == "__main__":
    
    test("192.168.33.139", "eray", "80661707", 22)
    #sftpUpdate("192.168.33.240", "eray", "80661707", 22, code_tar_path, target_folder)
    '''
    用paramiko 去執行cd指令 只會在單一exec啟作用，作用完 會回歸原本路徑
    '''
    #sftpUpdate(hostname, username, password, port, code_tar_path, target_folder)
    #sshCommand(hostname, username, password, port, code_tar_path, target_folder)
    
    #testUpdate(hostname, username, password, port, local_dir, remote_dir)
    #testCommand(hostname, username, password, port)
