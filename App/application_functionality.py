import paramiko

class TransferFiles:
    def __init__(self,host_name, ip_device, ssh_key_file_path,target_dir, books_dict):
        self.ip_device = ip_device
        self.host_name = host_name
        self.ssh_key_file_path = ssh_key_file_path
        self.target_dir=target_dir
        self.books=books_dict
  
    def uploadFileSSH(self):
        session = paramiko.SSHClient()

        # auto add host key 
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 

        key_file = paramiko.ECDSAKey.from_private_key_file(self.ssh_key_file_path)

        session.connect(
            hostname=self.ip_device,
            username=self.host_name,
            password=None,
            port=2222,
            pkey=key_file
        )
        print("start file upload")
        ftp_client = session.open_sftp()
        
        for key,value in self.books.items():
            local_file_path=value
            remote_file_path = self.target_dir + '/' + key
            try:
                print(f"Uploading file {key}")
                ftp_client.put(local_file_path,remote_file_path)
                print(f"File {key} uploaded successfully")
            except FileNotFoundError as err:
                print(f"Error {err}" )

        ftp_client.close()
        session.close()

def run_application_functionality(host_name, ip_device, ssh_key_file_path,target_dir, books_dict):
    connect1 = TransferFiles(host_name, ip_device, ssh_key_file_path,target_dir, books_dict)
    connect1.uploadFileSSH()