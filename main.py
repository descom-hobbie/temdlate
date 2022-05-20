from tkinter import *
from tkinter import font , filedialog
from markdown2 import Markdown
from tkhtmlview import HTMLLabel
from tkinter import messagebox as mbox
from md2pdf.core import md2pdf

header = open("template/header.html").read()
footer = open("template/footer.html").read()
style = "template/style.css"

lastfilename = ""
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.myfont = font.Font(family="Helvetica", size=18)
        self.init_window()

    def init_window(self):
        self.master.title("Temdlate")
        self.pack(fill=BOTH, expand=1)

        self.inputeditor = Text(self, width="1", font=self.myfont)
        self.inputeditor.pack(fill=BOTH, expand=1, side=LEFT, padx=20, pady=20)

        self.outputbox = HTMLLabel(self, width="1", background="white", html="<h1>Welcome</h1>")
        self.outputbox.pack(fill=BOTH, expand=1, side=RIGHT)
        self.outputbox.fit_height()

        self.inputeditor.bind("<<Modified>>", self.onInputChange)

        self.mainmenu = Menu(self)
        self.filemenu = Menu(self.mainmenu, tearoff=False)
        self.filemenu.add_command(label="Open", command=self.openfile)
        self.filemenu.add_command(label="Save", command=self.quicksave, accelerator="Ctrl+S")
        self.filemenu.add_command(label="Save as", command=self.savefile)
        self.filemenu.add_command(label="Export to PDF", command=self.exportfile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit, accelerator="Ctrl+Q")
        self.mainmenu.add_cascade(label="File", menu=self.filemenu)
        self.master.config(menu=self.mainmenu)

        self.bind_all("<Control-q>", lambda event: self.quit())
        self.bind_all("<Control-s>", lambda event: self.quicksave())

    def onInputChange(self , event):
        self.inputeditor.edit_modified(0)
        md2html = Markdown()
        self.outputbox.set_html(md2html.convert(self.inputeditor.get("1.0" , END)))

    def openfile(self):
        openfilename = filedialog.askopenfilename(filetypes=(("Markdown File", "*.md , *.mdown , *.markdown"), ("Text File", "*.txt"), ("All Files", "*.*")))
        if openfilename:
            try:
                self.inputeditor.delete(1.0, END)
                self.inputeditor.insert(END , open(openfilename).read())
            except:
                mbox.showerror("Error Opening Selected File" , "Oops!, The file you selected : {} can not be opened!".format(openfilename))

    def savefile(self):
        global lastfilename

        filedata = self.inputeditor.get("1.0" , END)
        savefilename = filedialog.asksaveasfilename(filetypes = (("Markdown File", "*.md"), ("Text File", "*.txt")) , title="Save Markdown File")
        lastfilename = savefilename
        if savefilename:
            try:
                f = open(savefilename , "w")
                f.write(filedata)
            except:
                mbox.showerror("Error Saving File" , "Oops!, The File : {} can not be saved!".format(savefilename))

    def quicksave(self):
        global lastfilename

        filedata = self.inputeditor.get("1.0" , END)
        savefilename = lastfilename

        if savefilename == "":
            self.savefile()
            return

        if savefilename:
            try:
                f = open(savefilename , "w")
                f.write(filedata)
            except:
                mbox.showerror("Error Saving File" , "Oops!, The File : {} can not be saved!".format(savefilename))

    def exportfile(self):
        filedata = header + self.inputeditor.get("1.0" , END) + footer
        exportfilename = filedialog.asksaveasfilename(filetypes = (("PDF file", "*.pdf"),), defaultextension='.pdf' , title="Export PDF file")
        if exportfilename:
            try:
                md2pdf(exportfilename, md_content=filedata, css_file_path=style)
            except:
                mbox.showerror("Error Saving File" , "Oops!, The File : {} can not be saved!".format(exportfilename))

root = Tk()
root.geometry("960x720")
app = Window(root)
app.mainloop()
