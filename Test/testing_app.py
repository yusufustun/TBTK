import shutil

class TransferMockFiles:
    def __init__(self,books_dict):
        self.target_dir="Test/Test Directory"
        self.books=books_dict
  
    def uploadMockFiles(self):
        for key,value in self.books.items():
            
            local_file_path=value
            remote_file_path = self.target_dir + '/' + key

            try:
                print(f"Uploading file {key}")
                shutil.copy(local_file_path,remote_file_path)
                print(f"File {key} uploaded successfully")
            except FileNotFoundError as err:
                print(f"Error {err}" )

def run_test_functionality(books_dict):
    connect1 = TransferMockFiles(books_dict)
    connect1.uploadMockFiles()
    