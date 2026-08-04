#Modules
from tkinter import *
from tkinter import messagebox 

import customtkinter as ctk

from PIL import Image as PIL_Image

from tkinter import filedialog
from pathlib import Path

import json

#File
from App.application_functionality import run_application_functionality
from Test.testing_app import run_test_functionality

mock_client=True # used for testing

# Reason for using class instead of a function
#   1. Organized we know which widgets belong to which app cuz of self
#   2. Classes data holds state wheras function run, return a value and forget everything

class KindleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_default_color_theme("blue")
        self.title("TBTK")
        self.geometry("600x500")
        self.resizable(width=False,height=True)

        #Variables
        self.config_file_path = Path("App/config.json")

        #WIDGETS
        #Framing details

        self.title_frame = ctk.CTkFrame(
            master=self,
            width=500,height=100,
        )
        self.top_half_frame = ctk.CTkFrame(
            master=self,
            width=500, height=200
        )
        self.bottom_half_frame = ctk.CTkFrame(
            master=self,
            width=500, height=200
        )
        self.left_frame = ctk.CTkFrame(
            master=self.top_half_frame,
            width=250, height=250
        )
        self.right_frame = ctk.CTkFrame(
            master=self.top_half_frame,
            width=350, height=250
        )
        self.bottom_frame = ctk.CTkFrame(
            master=self.bottom_half_frame,
            width=500, height=250
        )
            # Frames for bottom file picker
        self.file_picker_title_frame = ctk.CTkFrame(
            self.bottom_frame
        )
        self.select_folder_file_frame = ctk.CTkFrame(
            self.bottom_frame
        )
        self.display_files_frame = ctk.CTkFrame(
            self.bottom_frame
        )
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.display_files_frame
        )
        # Title
        self.label = ctk.CTkLabel(self.title_frame, text="TBTK", fg_color="transparent", font=("Arial",35))
        
        self.run_img = ctk.CTkImage(
            light_image=PIL_Image.open('images/run-icon.png'),
            dark_image=PIL_Image.open('images/run-icon.png'),
            size=(30,30)
        )
        self.run_button = ctk.CTkButton(
            self.title_frame,text="",image=self.run_img,width=30,command=self.runScript
        )

        #Setting target directory
            # this is shared variable between options
            # default value is kindle_option

        self.save_config_button = ctk.CTkButton(
            master=self.left_frame,
            text="Save configurations",
            command=self.saveToConfigFile
        )
        
        self.target_dir = ctk.StringVar(value="Type target folder...")

        self.kindle_option = ctk.CTkRadioButton(
            master=self.left_frame,
            text="Kindle",
            command=self.setTargetDir,
            variable=self.target_dir,
            value="/mnt/us/documents"
        )
        self.koreader_option = ctk.CTkRadioButton(
            master=self.left_frame,
            text="Koreader",
            command=self.setTargetDir,
            variable=self.target_dir,
            value="/mnt/us/Books"
        )
        self.set_own_option = ctk.CTkRadioButton(
            master=self.left_frame,
            text="Set own target folder",
            command=self.setTargetDir,
            variable=self.target_dir,
            value="Type target folder..."
        )
        self.set_own_option_entry = ctk.CTkEntry(
            master=self.left_frame,
            placeholder_text=self.target_dir.get(),
            width=200, height=30,
        )
        #self.set_own_option_entry.configure(state="disabled")

        #Setting SSH details
        self.host_name_entry_label = ctk.CTkLabel(
            master=self.right_frame,
            text="Host name:",
            width=150, height=50
        )
        self.host_name_entry = ctk.CTkEntry(
            master=self.right_frame,
            placeholder_text="root",
            width=220, height=50,
        )

        self.ip_entry_label = ctk.CTkLabel(
            master=self.right_frame,
            text="IP of device:",
            width=150, height=50
        )
        self.ip_entry = ctk.CTkEntry(
            master=self.right_frame,
            placeholder_text="192.168.10.124",
            width=220, height=50,
        )

        self.ssh_entry_label = ctk.CTkLabel(
            master=self.right_frame,
            text="SSH key folder path:",
            width=150, height=50
        )
        self.ssh_entry = ctk.CTkEntry(
            master=self.right_frame,
            placeholder_text="/Users/username/.ssh/id_ecdsa",
            width=220, height=50,
        )

        #Choosing files/books to upload
        self.file_picker_title = ctk.CTkLabel(
            self.file_picker_title_frame, text="Select Book(s):",font=("Arial",20)
        )

            # Add if file OR iterate if directory
        self.books: dict[str,Path] = {}

        self.folder_img = ctk.CTkImage(
            light_image=PIL_Image.open('images/folder-icon.png'),
            dark_image=PIL_Image.open('images/folder-icon.png'),
            size=(50,50)
        )

        self.select_button_file = ctk.CTkButton(
            self.select_folder_file_frame, text="File",command=self.selectBooksFile,image=self.folder_img
        )
        self.select_button_dir = ctk.CTkButton(
            self.select_folder_file_frame, text="Directory",command=self.selectBooksFolder,image=self.folder_img
        )

        self.packWidgets()
        self.checkConfigFile()

    #Function - Pack wigdets
    def packWidgets(self):
        #Packing all widgets
        self.label.pack(side=LEFT,pady=10,padx=10)
        self.run_button.pack(side=RIGHT,pady=10,padx=10)

        self.title_frame.pack(fill="both",expand=True)
        self.top_half_frame.pack(fill="both",expand=True)
        self.bottom_half_frame.pack(fill="both",expand=True)

        self.left_frame.pack(side="left",fill="both",expand=True)
        self.right_frame.pack(side="right",fill="both",expand=True)
        self.bottom_frame.pack(fill="both",expand=True)

        self.save_config_button.pack(pady=10)
        self.kindle_option.pack(pady=10)
        self.koreader_option.pack(pady=10)
        self.set_own_option.pack(pady=10)
        self.set_own_option_entry.pack(pady=5)

        self.host_name_entry_label.grid(row=0,column=0,pady=5)
        self.host_name_entry.grid(row=0,column=1,pady=5)

        self.ip_entry_label.grid(row=1,column=0,pady=5)
        self.ip_entry.grid(row=1,column=1,pady=5)

        self.ssh_entry_label.grid(row=2,column=0,pady=5)
        self.ssh_entry.grid(row=2,column=1,pady=5)

        self.file_picker_title_frame.grid(row=0,column=0)
        self.select_folder_file_frame.grid(row=1,column=0)
        self.display_files_frame.grid(row=1,column=1)

        self.file_picker_title.pack()

        self.select_button_file.pack(side=LEFT,padx=5)
        self.select_button_dir.pack(side=LEFT)

        self.scroll_frame.pack(side=RIGHT)

    #Function - Check config
    def checkConfigFile(self) -> None:
        try:
            with open(self.config_file_path,"r") as f:
                configs = json.load(f)
            self.host_name_entry.insert(0,configs["host_name"])
            self.ip_entry.insert(0,configs["ip_device"])
            self.ssh_entry.insert(0,configs["ssh_key_file_path"])
            self.set_own_option_entry.insert(0,configs["target_dir"])
            f.close()
        except FileNotFoundError as err:
            # print("Config file not found: ", err)
            messagebox.showerror("showerror","Configuration file was not found")

    #Functions - Save to config file
    def saveToConfigFile(self) -> None:
        data = self.returnArguments()

        try:
            with open(self.config_file_path,"r") as f:
                configs = json.load(f)
            
            configs["host_name"] = data[0]
            configs["ip_device"] = data[1]
            configs["ssh_key_file_path"] = data[2]
            configs["target_dir"] = data[3]

            with open(self.config_file_path,"w") as f:
                json.dump(configs,f,indent=2)

            f.close()

            self.displaySavedConfigMessage()
            # print("Saved configurations")

        except FileNotFoundError as err:
            self.displaySavedConfigErrorMessage()
            # print("Config file not found: ", err)

        #displays success or error message
    def displaySavedConfigErrorMessage(self):
        template_config_file = '{"target_dir": "", "ssh_key_file_path": "", "ip_device": "", "host_name": "" }'

        # if user clicks yes we write the template of a config file, and save what they had in input boxes into config file 
        if (messagebox.askyesnocancel("askyesnocancel","Config files doesn't exist. Create a config file?")):
            f = open("App/config.json","w")
            f.write(template_config_file)
            f.close()
            self.saveToConfigFile()

    def displaySavedConfigMessage(self):
        messagebox.showinfo("showinfo","Saved configurations!")

    #Functions - Title functions

    def getTargetDir(self) -> str:
        return self.setTargetDir()
    
    def getHostName(self) -> str:
        return self.host_name_entry.get().strip()
    
    def returnArguments(self) -> tuple:
        # collect the data from boxes
        collect_target_dir = self.setTargetDir()

        collect_host_name = self.host_name_entry.get().strip()
        collect_host_name = collect_host_name or "root"

        collect_ip_device = self.ip_entry.get().strip()
        collect_ip_device = collect_ip_device or "192.168.10.19"

        collect_ssh_entry = self.ssh_entry.get().strip()
        collect_ssh_entry = collect_ssh_entry or "/Users/samiyusuf/.ssh/id_ecdsa"
        
        collect_list_books = self.books

         # return as array of arguments
        return (
            collect_host_name,
            collect_ip_device,
            collect_ssh_entry,
            collect_target_dir,
            collect_list_books
        )
    def runScript(self) -> None:
        data = self.returnArguments()
        host_name = data[0]
        ip_device = data[1]
        ssh_key_file_path = data[2]
        target_dir = data[3]
        books_dict = data[4]

        if(mock_client):
            run_test_functionality(books_dict)
        else:
            run_application_functionality(host_name, ip_device, ssh_key_file_path,target_dir, books_dict)

    #Functions - Setting target dir
    def setTargetDir(self) -> str:
        target=self.target_dir.get()
        if(target=="Type target folder..."):
            self.set_own_option_entry.configure(state="normal")
            target=self.getEntryBoxTargetDir()
        else:
            self.set_own_option_entry.configure(state="disabled")
        return target

    def getEntryBoxTargetDir(self)->str:
        entry_box = self.set_own_option_entry.get()
        return "/mnt/us/documents" if (entry_box=="") else entry_box        

    #Function - Choosing files/books to upload
    def selectBooksFile(self) -> None:
        file_path = Path(filedialog.askopenfilename())
        if(file_path!=Path(".")):
            self.addToBooks(file_path)

    def selectBooksFolder(self) -> None:
        dir_path = Path(filedialog.askdirectory(initialdir="/Users/samiyusuf/Desktop/CODE/"))
        if(dir_path!=Path(".")): # check if user has clicked cancel
            for file in dir_path.iterdir(): 
                if file.is_file(): # check file is a file 
                    self.addToBooks(file)

    def addToBooks(self, file:Path) -> None:
        book_name = str(file.name)
        book_path = file  
        self.books[book_name] = book_path
        self.addToDisplay(book_name)

    def addToDisplay(self,book_name:str) -> None:
        frame = ctk.CTkFrame(
            self.scroll_frame,border_color="red",border_width=2,height=50
        )
        label = ctk.CTkLabel(frame,text=book_name)
        button = ctk.CTkButton(
            frame,text="x",command=lambda: self.deleteBook(frame,book_name), width=10
        )
        frame.pack(pady=10)
        label.pack(side=LEFT)
        button.pack(side=RIGHT)

    def deleteBook(self, frame:ctk.CTkFrame, book_name:str) -> None:
        frame.destroy()
        self.books.pop(book_name)

#Main
def run_app_gui():
    app = KindleApp()
    app.mainloop()    