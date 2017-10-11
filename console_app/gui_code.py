
import Tkinter
from tkFileDialog import *
from classify import *
import os
import shutil
import platform
import subprocess

max_numberoffiles = 5000 #### maximumnumber of files at a time

class gui_classify(Tkinter.Frame):
    def __init__(self,master):
        Tkinter.Frame.__init__(self,master)
        self.master = master
        self.initUI()
        self.master.geometry("620x530")
        self.master.resizable(0,0)

#------------------- scroll functionality and canvas,frames -------------------------#
        
    def AuxscrollFunction(self,event):
        #set a max size for myframe. Otherwise, it will grow as needed, and scrollbar do not act
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=600,height=500)
        
        
    def initUI(self):
        self.master.title("Document Feature Identification")
        self.frameOne = Tkinter.Frame(self.master)
        self.frameOne.grid(row=0,column=0)
        
        self.myframe =Tkinter. Frame(self.master)
        self.myframe.grid(row=1, column=0,sticky='nsew')

        #Creating of a new frame, inside of "myframe" to the objects to be inserted
        #Creating a scrollbar

        #The reason for this, is to attach the scrollbar to "myframe", and when the size of frame "ListFrame" exceed the size of myframe, the scrollbar acts
        self.canvas=Tkinter.Canvas(self.myframe)
        self.listFrame=Tkinter.Frame(self.canvas)
        self.scrollb=Tkinter.Scrollbar(self.master, orient="vertical",command=self.canvas.yview)
        self.scrollb.grid(row=1, column=1, sticky='nsew')  #grid scrollbar in master, but
        self.canvas['yscrollcommand'] = self.scrollb.set   #attach scrollbar to myframe

        self.canvas.create_window((0,0),window=self.listFrame,anchor='nw')
        self.listFrame.bind("<Configure>", self.AuxscrollFunction)

        self.canvas.pack(side="left")

        self.text1 = Tkinter.Label(self.frameOne, text = " Classify your Files :) ", justify="center")
        self.text1.grid(row=1, column=0)

#-----------------canvas and scrollbar code ends----------------------#
        

#----------------------------------------adding main gui----------------------------------#
    
        self.filename=""
        self.file_path={}
        self.file_list=[]
        self.filepath_label={}
        self.result_label={}
        self.remove_button={}
        self.view_button={}
        self.filegenre_label={}
        self.genre={}
        self.targetDirectory={}
        self.count=0
        self.rownumber=0
        self.dictionary =load_dict()

        
        self.entryVariable = Tkinter.StringVar()
        self.input_file_entry = Tkinter.Entry(self.listFrame,textvariable=self.entryVariable)
        self.input_file_entry.grid(column=0,row=0,columnspan=1, sticky="ew")

        self.input_file_entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set("")

        button = Tkinter.Button(self.listFrame,text="Browse",
                                command=self.OnBrowse_ButtonClick)
        button.grid(column=1,row=0)
        add_button = Tkinter.Button(self.listFrame,text="add",
                                command=self.OnAdd_ButtonClick)
        add_button.grid(column=0,row=1,columnspan=1)

        labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self.listFrame,textvariable=labelVariable,
                              anchor="w")
        label.grid(column=0,row=2,columnspan=2,sticky='EW')
        labelVariable.set(u"List of Files !")
        self.rownumber=5
        self.classify_button = Tkinter.Button(self.listFrame,text=u"Classify",
                                command=self.OnClassify_ButtonClick)
        
        self.grid_columnconfigure(0,weight=1)
        self.update()

        self.input_file_entry.focus_set()
        self.input_file_entry.selection_range(0, Tkinter.END)

#-------------------on clicking classify button-------------------------#
    def OnClassify_ButtonClick(self):
        
        self.rownumber=max_numberoffiles+5
        self.addtable()
        
        for file_x in self.file_list :
            self.genre[file_x] = classify_file(file_x, self.dictionary)
            print (file_x,self.genre[file_x])
            self.targetDirectory[file_x] = r'./categorized/{}'.format(self.genre[file_x])

            check_existence = os.path.join(self.targetDirectory[file_x], os.path.basename(file_x))
            if os.path.exists(check_existence):
                os.remove(check_existence)
            self.ensure_dir(self.targetDirectory[file_x])
            
            shutil.move(file_x, self.targetDirectory[file_x])
            #shutil.copy(file_x, self.targetDirectory[file_x])   #switch to this if u want to copy instead of moving

        self.addRows()

#------------------ ensuring that categorized folders are present-------------------#        
    def ensure_dir(self,f):
        if not os.path.isdir(f):
            os.makedirs(f)

#------------------- starting of output ---------------------------------#       
    def addtable(self):
        
        Titleoftable = Tkinter.StringVar()
        label1 = Tkinter.Label(self.listFrame,textvariable=Titleoftable,
                              anchor="w")
        label1.grid(row= self.rownumber,column=0, pady=(20))
        Titleoftable.set(u"________RESULT________\n\nThe following files are classified into following categories ") 
        self.rownumber = self.rownumber + 1            


#-----------------------output of genre at each row-------------------#
        
    def addRows(self):
             
        i=  self.rownumber
        for file_x in self.file_list:
            a= Tkinter.StringVar()
            label2 = Tkinter.Label(self.listFrame,textvariable=a,anchor="w")
            label2.grid(row= self.rownumber,column=0,columnspan=1,sticky='EW', pady=(10))
            a.set(file_x)
            
            temp= Tkinter.StringVar()
            self.filegenre_label[file_x] = Tkinter.Label(self.listFrame,textvariable=temp,anchor="w")
            self.filegenre_label[file_x].grid(column=1,row=(self.rownumber),columnspan=1,sticky='EW')
            temp.set(self.genre[file_x])

            self.view_button[file_x] = Tkinter.Button(self.listFrame,text=u"View",
                                command= lambda i = file_x: self.OnView_ButtonClick(i))
            self.view_button[file_x].grid(row= (self.rownumber),column=3)

            self.rownumber+=1

#--------------- View the destination --------------------#
    def open_file(self,path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        
    def OnView_ButtonClick(self,i):
        print (self.targetDirectory[i])
        self.open_file(self.targetDirectory[i]+"")
             
             
#------------------------------ on clicking add button--------------------#             
    def OnAdd_ButtonClick(self):

        if (self.filename != '' and (self.filename not in self.file_list) ) :
            self.file_list.append(self.filename)
            self.count += 1
            self.file_path[self.filename] = Tkinter.StringVar()
            self.filepath_label[self.filename] = Tkinter.Label(self.listFrame,textvariable=self.file_path[self.filename],
                              anchor="w")
            self.filepath_label[self.filename].grid(column=0,row=(self.rownumber),columnspan=2,sticky='EW')
            self.file_path[self.filename].set(self.filename)

            self.remove_button[self.filename] = Tkinter.Button(self.listFrame,text=u"Remove",
                                command= lambda i = self.filename: self.OnRemove_ButtonClick(i))
            self.remove_button[self.filename].grid(column=4,row= (self.rownumber),sticky='W')
            self.rownumber +=1
        #adding view table and classify button below list
            self.classify_button.grid(row=max_numberoffiles)
            self.entryVariable.set("")
            

#------------------------------ on clicking remove button--------------------#             
        
    def OnRemove_ButtonClick(self,i):
        self.file_list.remove(i)
        del self.file_path[i]
        self.filepath_label[i].destroy()
        self.remove_button[i].destroy()

        print (self.file_list)

#------------------------------ on clicking browse button or pressing enter button--------------------#             

    def OnBrowse_ButtonClick(self):
        self.filename = askopenfilename()
        self.entryVariable.set(self.filename)
        self.input_file_entry.focus_set()
        self.input_file_entry.selection_range(0, Tkinter.END)

    def OnPressEnter(self,event):
        self.OnAdd_ButtonClick()


######################  main code ################################################

if __name__ == "__main__":
    root= Tkinter.Tk()
    app = gui_classify(root)
    #app.pack(side="top", fill="both", expand=True)
    app.mainloop()

##################  code ends  ###############################
