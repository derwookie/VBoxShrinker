import os
import subprocess
import pyperclip
import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedTk as themedtk
from tkinter.messagebox import showinfo

class GUI(themedtk):
    def __init__(self):
        super().__init__()
        self.set_theme("breeze")
        self.path = os.path.dirname(__file__)
        self.defineGUI()

    def defineGUI(self):
        print("self.defineGUI()")
        #windowconf
        self.title("VBoxShrinker v0.1-beta")
        self.iconbitmap(os.path.join(os.path.dirname(__file__), "icon.ico"))
        #self.geometry("1280x768")
        
        #gridconf
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=2)
        self.columnconfigure(3, weight=2)
        self.columnconfigure(4, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        #widgetsconf
        #row 0
        self.pathLabel = ttk.Label(self, text="Path to .vdi-Files")
        self.pathLabel.grid(column=0, row=0, padx=5, pady=5)

        self.wd = tk.StringVar(value=str(os.getcwd()))
        self.pathEntry = ttk.Entry(self, textvariable=self.wd)
        self.pathEntry.grid(column=1, row=0, columnspan=3, padx=5, pady=5, sticky="WE")
        self.pathEntry.bind("<Return>", self.setPathFromEntry)
        self.pathEntry.bind("<Control-c>", self.copyPath)
        self.pathEntry.bind("<Control-v>", self.pastePath)
        self.pathEntry.bind("<Control-o>", self.openPathTxt)

        self.openPath = ttk.Button(self, text="Directory Dialog", command=self.setPath)
        self.openPath.grid(column=4, row=0, padx=5, pady=5)

        #row 1
        self.listLabel = ttk.Label(self, text="List of .vdi-Files")
        self.listLabel.grid(column=0, row=1, padx=5, pady=5)

        treecontent = ("file", "dir", "size")
        self.listTreeview = ttk.Treeview(self, columns=treecontent, show='headings')
        self.listTreeview.heading('file', text="File")
        self.listTreeview.heading('dir', text="Directory")
        self.listTreeview.heading('size', text="Size")
        scrollbar = ttk.Scrollbar(self.listTreeview, orient=tk.VERTICAL, command=self.listTreeview.yview)
        self.listTreeview.configure(yscroll=scrollbar.set)
        self.listTreeview.column('file', minwidth=20, stretch=0)
        self.listTreeview.column('dir', minwidth=200, stretch=1)
        self.listTreeview.column('size', minwidth=5, stretch=0, anchor=tk.E)
        self.listTreeview.grid(column=1, row=1, columnspan=4, padx=5, pady=5, sticky="NSWE")
        
        #row 2
        self.shrinkingProgressBar = ttk.Progressbar(self, orient='horizontal', mode='indeterminate')
        self.shrinkingProgressBar.grid(column=0, row=2, padx=5, pady=5, columnspan=5, sticky="NSWE")

        #row 3
        self.savePathButton = ttk.Button(self, text="Save the Path", command=self.savePath)
        self.savePathButton.grid(column=0, row=3, padx=5, pady=5, sticky="SE")

        self.shrinkOneButton = ttk.Button(self, text="Choose one and shrink it", command=self.shrinkOne)
        self.shrinkOneButton.grid(column=1, row=3, padx=5, pady=5, sticky="SE")

        self.shrinkAllButton = ttk.Button(self, text="Shrink All", command=self.shrinkAll)
        self.shrinkAllButton.grid(column=2, row=3, padx=5, pady=5, sticky="SE")

        self.shrinkSelectedButton = ttk.Button(self, text="Shrink Selected", command=self.shrinkSelected)
        self.shrinkSelectedButton.grid(column=3, row=3, padx=5, pady=5, sticky="SE")

        self.exitButton = ttk.Button(self, text="Close Program", command=lambda: self.quit())
        self.exitButton.grid(column=4, row=3, padx=5, pady=5, sticky="SE")


        #self.listTemp = self.getVDIs()
        #self.refreshList()
        
        self.mainloop()

    def refreshList(self):
        print("self.refreshList()")
        for i in range(0,len(self.listTemp)-1):
            #self.listTemp[1] = self.listTemp[1].split("/")
            print(self.listTemp[i])
            print(1)
            self.listTreeview.insert('', tk.END, values=self.listTemp[i])

    def getVDIs(self):
        print("self.getVDIs()")
        for item in self.listTreeview.get_children():
            self.listTreeview.delete(item)
        files = []
        size = 0
        for r, d, f in os.walk(self.path):
            for file in f:
                if '.vdi' in file:
                    filepath = os.path.join(r, file)
                    size = float(os.path.getsize(filepath))
                    counter = 0
                    while True:
                        if size >= 3072:
                            counter += 1
                            size = size / 1024
                        else:
                            break
                    suf = ""
                    if counter == 1:
                        suf = "kB"
                    elif counter == 2:
                        suf = "MB"
                    elif counter == 3:
                        suf = "GB"
                    files.append((file, r, str(round(size, 3)) + suf))
        #for i in range(0, len(files)):
        #    print(files[i])
        return files

    def savePath(self):
        print("self.savePath()")
        p = os.path.dirname(__file__)
        print(p)
        try:
            os.remove(os.path.join(p, "Path.txt"))
        except:
            pass
        with open(os.path.join(p, "Path.txt"), "w") as file:
            file.write(self.wd.get())

    def openPathTxt(self, some):
        print("self.openPathTxt()")
        p = os.path.dirname(__file__)
        with open(os.path.join(p, "Path.txt"), "r") as file:
            self.wd.set(file.read)
        self.refreshList()
        print("Accessed self.refreshList from self.openPathTxt")

    def shrinkSelected(self):
        print("self.shrinkSelected()")
        self.getFileSizes()
        chose = self.listTreeview.selection()
        chosen = []
        temp2 = []
        out = []

        for i in range(0, len(chose)):
            temp = chose[i]
            temp = temp.replace("I", "")
            chosen.append(int(temp))
        for i in range(0, len(chosen)):
            temp2.append(self.getVDIs()[chosen[i]-1])
            print("Accessed self.getVDIs from self.shrinkSelected")
        for i in range(0, len(temp2)):
            out.append([temp2[i][0], temp2[i][1]])
        #print(out)
        showinfo(title="Information", message="To see the output, look at the console in the background.")
        self.shrinkingProgressBar.start()
        for i in range(0, len(out)):
            self.shrink(os.path.join(out[i][1],out[i][0]))
            print("Accessed self.shrink from self.shrinkSelected")
        self.shrinkingProgressBar.stop()
        showinfo(title="Information", message=f"Shrinking is finished, you can close the program now.")
        self.getFileSizes()
        print("Accessed self.getFileSizes from self.shrinkSelected")
        #sys.exit

    def shrinkAll(self):
        print("self.shrinkAll()")
        files = self.getVDIs()
        print("Accessed self.getVDIs from self.shrinkAll")
        #print(type(files))
        #print(2)
        showinfo(title="Information", message="To see the output, look at the console in the background.")
        self.shrinkingProgressBar.start()
        for i in range(0, len(files)):
            vdi = files[i][1] + "\\" + files[i][0]
            #print(vdi)
            self.shrink(vdi)
            print("Accessed self.shrink from line 171")
            #print(3)
        self.shrinkingProgressBar.stop()
        showinfo(title="Information", message=f"Shrinking is finished, you can close the program now.")

    def shrinkOne(self):
        print("self.shrinkOne()")
        from tkinter import filedialog
        vdi = filedialog.askopenfilename(title="Open a VM-File", filetypes=(('Virtual-Disk-Images', 'vdi'),))
        #print(type(vdi))
        #print(4)
        #print(f"\n{vdi}\n")
        #print(5)
        showinfo(title="Information", message="To see the output, look at the console in the background.")
        self.shrinkingProgressBar.start()
        self.shrink(vdi)
        print("Accessed self.shrink from self.shrinkOne")
        self.shrinkingProgressBar.stop()
        showinfo(title="Information", message=f"Shrinking is finished, you can close the program now.")


    def shrink(self, whattoshrink):
        print("self.shrink()")
        print(f"Shrinking {whattoshrink} now:")
        #print(6)
        #print(f"VBoxManage modifyhd \"{whattoshrink}\" --compact")
        #print(7)
        
        # Since VBoxManage seems to not give any output through stdout, the only option to monitor is to 
        # open a shell in the background and watch that instead of the GUI
        # I'll include the necessary code for capturing the output in case oracle change their mind :)
        # Until then, my variable "output" will contain just a string with a space
        output = subprocess.check_output(f"VBoxManage modifymedium disk \"{whattoshrink}\" --compact", shell=True)
        #print(type(t))
        output = output.decode('utf-8')
        #print(type(t))
        print(output)

        print(8)
        print("Done\n")
        print(9)

    def setPath(self):
        print("self.setPath()")
        from tkinter import filedialog
        self.path = filedialog.askdirectory()
        self.wd.set(self.path)
        self.listTemp = self.getVDIs()
        print("Accessed self.getVDIs from self.setPath")
        self.refreshList()
        print("Accessed self.refreshList from self.setPath")

    def setPathFromEntry(self, event):
        print("self.setPathFromEntry()")
        self.path = self.wd.get()
        print(self.path)
        print(10)
        self.listTemp = self.getVDIs()
        print("Accessed self.getVDIs from self.setPathFromEntry")
        self.refreshList()
        print("Accessed self.refreshList from self.setPathFromEntry")

    def copyPath(self, some):
        print("self.copyPath()")
        pyperclip.copy(self.wd.get())
        print(f"Wrote {self.wd.get()} to clipboard")

    def pastePath(self, some):
        print("Self.pastePath()")
        self.wd.set(pyperclip.paste())
        print(f"Pasted{pyperclip.paste()} from clipboard")

    def getFileSizes(self):
        print("self.getFileSizes()")
        size = 0
        for r, d, f in os.walk(self.path):
            for file in f:
                if '.vdi' in file:
                    filepath = os.path.join(r, file)
                    #print("VM: " + self.convertFileSize(float(os.path.getsize(filepath))))
                    size = size + float(os.path.getsize(filepath))
                    #print("Zwischen: " + self.convertFileSize(float(size)))
        #print("Gesamt: " + self.convertFileSize(float(size)))
        return size

    def convertFileSize(self, size: float):
        print("self.convertFileSize()")
        out = size
        suf = ""
        counter = 0
        while True:
            if out > 2048:
                counter += 1
                out = out / 1024
            else:
                break
        out = round(out, 3)
        if counter == 0:
            suf = "B"
        elif counter == 1:
            suf = "kiB"
        elif counter == 2:
            suf = "MiB"
        elif counter == 3:
            suf = "GiB"
        elif counter == 4:
            suf = "TiB"
        
        return str(out) + suf
        


if __name__ == '__main__':
    GUI()