import paramiko
from tkinter import messagebox 

class TransferFiles:
    def __init__(self,host_name, ip_device, port, ssh_key_file_path,target_dir, books_dict):
        self.ip_device = ip_device
        self.port = port
        self.host_name = host_name
        self.ssh_key_file_path = ssh_key_file_path
        self.target_dir=target_dir
        self.books=books_dict
  
    def uploadFileSSH(self):
        try:
            session = paramiko.SSHClient()
            # auto add host key 
            session.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 

            key_file = paramiko.ECDSAKey.from_private_key_file(self.ssh_key_file_path)

            session.connect(
                hostname=self.ip_device,
                username=self.host_name,
                password=None,
                port=self.port,
                pkey=key_file,
                timeout=8.0
            )
            ftp_client = session.open_sftp()
            
            for key,value in self.books.items():
                local_file_path=value
                remote_file_path = self.target_dir + '/' + key
                try:
                    ftp_client.put(local_file_path,remote_file_path)
                    messagebox.showinfo("showinfo", f"Uploaded file {key}")
                except FileNotFoundError as e:
                    messagebox.showerror("showerror",f"File {key} not found")
                except IOError or OSError as e:
                    messagebox.showerror("showerror",f"File {key} operation failed on SFTP server due to path issues")
                except PermissionError as e:
                    messagebox.showerror("showerror",f"Permission denied on file {key}")
            ftp_client.close()
        except paramiko.AuthenticationException as e:
            messagebox.showerror("showerror", "SSH authentication failed due to incorrect credentials")
        except paramiko.SSHException as e:
            messagebox.showerror("showerror", "Failed SSH2 protocol negotiation")
        except Exception as e:
            messagebox.showerror("showerror", f"Exception: {e}")
        finally:
            session.close()

def run_application_functionality(host_name, ip_device, port ,ssh_key_file_path,target_dir, books_dict):
    connect1 = TransferFiles(host_name, ip_device, port,ssh_key_file_path,target_dir, books_dict)
    connect1.uploadFileSSH() if len(books_dict) > 0 else messagebox.showinfo("showinfo","Add files to upload")