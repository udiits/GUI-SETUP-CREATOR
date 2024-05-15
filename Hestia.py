from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import sys, os
import webbrowser as wb
##import ctypes #This import helps to fix the blurred text problem.
## 
##ctypes.windll.shcore.SetProcessDpiAwareness(1) #This line fixes the blurry text.

#Function that sorts the location issue.
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Main Application.
splash_root=Tk()
splash_root.geometry("500x300+700+400")
img = Image.open(resource_path("Project Images\\Splash_Logo_Main.png"))
img = img.resize((500,300), Image.ANTIALIAS)
photoImg1 =  ImageTk.PhotoImage(img)
splash_img=Label(splash_root, image=photoImg1)
splash_img.grid(row=1, column=0)
splash_root.overrideredirect(True)

#Variables in use
img_ref_dic={} #For storing image references.
opt=[] #Python variable for storing additional features
sql_info={} #Python Variable that stores SQL login data
code_filename="" #Python Variable to hold code file name
setup_filename="" #Python Variable to hold code file name

#Variables that store code.
widget_list=[]
var_name_list=[]

def main():
    splash_root.destroy()
    root=Tk()
    root.title("Hestia - The GUI Creator")
    root.iconbitmap(resource_path("Project Images\\Main_Logo.ico"))
    root.geometry("800x480+400+300")
    root.resizable(width=False, height=False)
    canvas=Canvas(root, bg="White",borderwidth=1, relief="solid", height=350, width=450)
    s = ttk.Style()
    s.configure('My.TFrame', background='white', borderwidth=2, relief="solid")
    s.configure('My.TLabel', background="white", foreground="black")
    s.configure('My.TRadiobutton', background="white", foreground="black")
    widget_data_frame=ttk.Frame(root, style='My.TFrame', width=200, borderwidth=5)
    menubar=Menu(root)

    img = Image.open(resource_path("Project Images\\MainBackground.png"))
    img = img.resize((800,450), Image.ANTIALIAS)
    photoImg =  ImageTk.PhotoImage(img)
    main_img=Label(root, image=photoImg)
    main_img.grid(row=1, column=0)

    #Variables in use.
    address=StringVar()#Tkinter Variable for image name
    address.set("None")
    address_p=0 #Python variable for image name
    my_image=""
    win=StringVar() #Tkinter Variable for window name
    win.set("top")
    win_title=StringVar() #Tkinter variable for window title.
    win_title.set("tk")
    win_log=StringVar()
    win_log.set("")
    win_bg=StringVar() #Tkinter Variable for window background.
    win_bg.set("")
    bg=StringVar() #Tkinter Variable for background color
    bg.set('Default')
    fg=StringVar() #Tkinter Variable for foreground color
    fg.set("Default")
    wd=StringVar() #Tkinter variable for width of widget.
    wd.set("Default")
    bd=IntVar() #Tkinter variable for border-width of widget.
    bd.set(1)
    rel_sty=StringVar()
    rel_sty.set("Default")
    wish=False
    txt=StringVar() #Tkinter variable for widget text
    var_ch=IntVar() #Tkinter variable to store value for text variable or text.
    var_ch.set(1)
    var_nam=StringVar() #Tkinter variable that stores variable name of widget.

    #General Functions
    def move(e):
        """This function helps to move the image on screen"""
        global wish, img, my_image
        try:
            if wish:
                add=address.get()
                img=PhotoImage(file=resource_path(f"Project Images\\{add}.png"))
                my_image=canvas.create_image(e.x,e.y, image=img)
            else:
                pass
        except:
            pass

    def save():
        """This function saves the co-ordinates and image object in dictionary"""
        global img,wish, my_image
        if img!=None and wish:
            img_x,img_y=canvas.coords(my_image)
            img_id=str(address.get())+str(len(img_ref_dic))
            backg=bg.get()
            foreg=fg.get()
            bdw=bd.get()
            rel=rel_sty.get().lower()
            wid=wd.get()
            text=txt.get()
            var_wish=var_ch.get()
            var_fin_name=""
            if var_wish==1:
                var_wish="No"
            elif var_wish==2:
                var_fin_name=var_nam.get()
                var_wish="Yes"    
            #The dictionary key as widget name and has data in the order:
            # Widget Photo, X-Coord, Y-Coord, Bg-Color, Fg-Color, Bd-Width,\
            # Relief, Width, Text-As-Option, Text Variable Name 
            img_ref_dic[img_id]=[img, img_x,img_y, backg, foreg, bdw, rel, wid, text,var_wish, var_fin_name]
            text_setter(address.get(),text,my_image)
            bg.set("Default")
            fg.set("Default")
            bd.set(1)
            wd.set("Default")
            rel_sty.set("Default")
            address.set("None")
            txt.set("")
            var_nam.set("")
            var_ch.set(1)
            var_opt()
            wish=False
        else:
            pass
        
    def text_setter(widget,line,image):
        fill_col=""
        outline_col="black"
        
        #The conditions below just change the background color of the box.
        if widget=="Entry":
            fill_col="#ffffff"
            outline_col="#b5b5b5"
            
        elif widget=="Label":
            fill_col="#f0f0f0"
            outline_col="#f0f0f0"
            
        elif widget=="Button":
            fill_col="#e1e1e1"
            outline_col="#b4b4b4"
            
        else:
            pass
        
        txt=canvas.create_text(canvas.coords(image), text=line,font=("TkDefaultFont"))
        points=list(canvas.bbox(txt)) #Variable that contains box coordinates of text.
        points2=canvas.bbox(image) #Variable that contains box coordinates of image.
        if points[2]-points[0]<points2[2]-points2[0]: #If Text Smaller than Box,
            points=list(points2) #Make the textbox of the size of the widget.
        points[1],points[3]=points2[1],points2[3]
        canvas.create_rectangle(points,fill=fill_col,outline=outline_col)
        canvas.tag_raise(txt)
    
    def make(l):
        """This function makes the widgets on the canvas when a setup is opened."""
        for i in l:
            add=num_rem(i)
            img=PhotoImage(file=resource_path(f"Project Images\\{add}.png"))
            my_image=canvas.create_image(l[i][0],l[i][1], image=img)
            text_setter(add,l[i][7],my_image)
            l[i].insert(0, img)

    def give(add):
        """This function makes the new widget on screen"""
        global img, wish, my_image
        address.set(add)
        img=PhotoImage(file=resource_path(f"Project Images\\{add}.png"))
        my_image=canvas.create_image(200,200, image=img)
        wish=True
        
    def resize(l_ex=0): #l_ex to extend the length of main window.
        """This function resizes the canvas and main window"""
        dimens=canv_size.get()
        if dimens!="Custom":
            w, h = dimens.split("x")
            w,h=eval(w), eval(h)
            l_ex=40
            if h==350:
                l_ex=100
            canvas.configure(height=h, width=w)
            wid_fram_w=widget_data_frame.winfo_width()
            root.geometry(f"{w+wid_fram_w+40}x{h+l_ex}")
        elif dimens=="Custom":
            custom_resize()
        else:
            pass

    def custom_resize():
        c_resize=Toplevel(root)
        c_resize.title("Custom Size")
        c_resize.iconbitmap(resource_path("Project Images\\Main_Logo.ico"))
        c_resize.resizable(width=False, height=False)
        c_resize.transient(root)
        cust_h=StringVar()
        cust_w=StringVar()
        ttk.Label(c_resize, text="Custom Size: ").grid(row=0, column=0)
        ttk.Label(c_resize, text="Enter Height: ").grid(row=1, column=0, padx=5)
        ttk.Entry(c_resize, textvariable=cust_h).grid(row=1, column=1, padx=10, pady=3)
        ttk.Label(c_resize, text="Enter Width: ").grid(row=2, column=0, padx=5)
        ttk.Entry(c_resize, textvariable=cust_w).grid(row=2, column=1, padx=10, pady=3)
        def custom_set():
            h,w=cust_h.get(), cust_w.get()
            if h and w:
                canv_size.set(f"{w}x{h}")
                resize()
                c_resize.destroy()
            else:
                messagebox.showerror("Empty Field","Please enter something in the fields.")
        ttk.Button(c_resize, text="Apply", command=custom_set).grid(row=3, column=1, pady=5)
        c_resize.mainloop()
        
    #Function for Disabling/Enabling Buttons for new widgets.
    def dis_enable_new(status):
        """This function enables/disables the canvas size and other options"""
        if status:
            menubar.entryconfigure("New Widget",state="normal")
            menubar.entryconfigure("Canvas Size",state="normal")
            menubar.entryconfigure("Add-Ons",state="normal")
            menubar.entryconfigure("Parent Window",state="normal")
        else:
            menubar.entryconfigure("New Widget",state="disabled")
            menubar.entryconfigure("Canvas Size",state="disabled")
            menubar.entryconfigure("Add-Ons",state="disabled")
            menubar.entryconfigure("Parent Window",state="disabled")

    #Functions for handling files
    def New_File(event=None):
        """This function opens a new file to start working"""
        root.title("Untitled")
        global code_filename, setup_filename
        code_filename=None
        setup_filename=None
        canvas.delete("all")
        canvas.grid(row=0,column=0, padx=10, pady=8, sticky="news")
        canvas.configure(height=350, width=450)
        widget_data_frame.grid(row=0, column=1, sticky="news", pady=8)
        main_img.grid_forget()
        img_ref_dic.clear()
        dis_enable_new(True)
        
    def Open(event=None):
        """This function opens the files with saved setup"""
        try:
            global img_ref_dic, sql_info, opt, code_filename, setup_filename
            New_File()
            f= filedialog.askopenfilename(defaultextension=".txt",
            filetypes=[("All Files", "*.*"), ("Text Documents","*.txt")])
            if f:
                root.title(os.path.basename(f) + " - Hestia")
            imgs="" #This variable holds the dictionary that will be loaded from file.
            sql_data={}
            par_win_set=[] #Variable to hold window settings.
            extra_addons=[]
            canv_size_info=""
            with open(f, "r+") as file:
                imgs=file.readline()
                sql_data=eval(file.readline())
                par_win_set=eval(file.readline())
                extra_addons=eval(file.readline())
                canv_size_info=file.readline()
            img_ref_dic=eval(imgs)
            make(img_ref_dic)
            if sql_data:
                SQL.set(1)
            sql_info=sql_data
            opt=extra_addons
            if "PIL" in opt:
                pil.set(1)
            win.set(par_win_set[0])
            win_title.set(par_win_set[1])
            win_log.set(par_win_set[2])
            canv_size.set(canv_size_info)
            setup_filename=f #Setting only setup filename to avoid confusion with code file.
            resize()
        except:
            pass

    def Save_Code(event=None):
        """This function saves code of the GUI"""
        global code_filename
        try:
            global var_name_list,opt,sql_info
            var_name_list.clear() #this line clears the already present variables in list to avoid double entry.
            opt=add_feat(opt) #This line adds features to the code.
            var_add(img_ref_dic, var_name_list) #This line adds variables to be declared to the var_name_list.
            widget_writer(img_ref_dic) #This line writes code for widgets.
            with open(code_filename, "w+") as fh:
                final_writer(fh ,opt, widget_list, var_name_list,sql_info)
            root.title(os.path.basename(code_filename) + " - Hestia")
        except:
            Save_Code_As()

    def Save_Code_As(event=None):
        """This helps to change name of the saved code file"""
        global img_ref_dic
        if len(img_ref_dic)!=0:
            try:
                if messagebox.askyesno("Write Code?","Do you want to write the code?"):
                    global var_name_list,opt,sql_info, code_filename
                    var_name_list.clear() #this line clears the already present variables in list to avoid double entry.
                    opt=add_feat(opt) #This line adds features to the code.
                    var_add(img_ref_dic, var_name_list) #This line adds variables to be declared to the var_name_list.
                    widget_writer(img_ref_dic) #This line writes code for widgets.
                    f= filedialog.asksaveasfilename(initialfile="Untitled.txt",
                    defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents","*.txt")])
                    if f:
                        with open(f, "w+") as fh:
                            final_writer(fh ,opt, widget_list, var_name_list,sql_info)
                        root.title(os.path.basename(f) + " - Hestia")
                    code_filename=f
            except:
                pass
        else:
             messagebox.showerror("No Widgets","No widgets on the canvas. : (")
        
    def Save_Setup(event=None):
        """This function saves setup of the GUI"""
        global setup_filename
        try:
            global sql_info, opt
            opt=add_feat(opt)
            temp_dic=img_ref_dic.copy() #This line creates a copy of img_ref_dic.
            for i in temp_dic:
                temp_dic[i]=temp_dic[i][1:] 
            window_data=[win.get(), win_title.get(), win_log.get()]
            canv_data=canv_size.get()
            with open(filename, "w") as fh:
                fh.write(str(temp_dic)+"\n")
                fh.write(str(sql_info)+"\n")
                fh.write(str(window_data)+"\n")
                fh.write(str(opt)+"\n")
                fh.write(str(canv_data))
            root.title(os.path.basename(setup_filename) + " - Hestia")
        except:
            Save_Setup_As()
            
    def Save_Setup_As(event=None):
        """This helps to change name of the save file"""
        if len(img_ref_dic)!=0:
            try:
                global sql_info, opt, setup_filename
                opt=add_feat(opt)
                temp_dic=img_ref_dic.copy() #This line creates a copy of img_ref_dic.
                for i in temp_dic:
                    temp_dic[i]=temp_dic[i][1:] 
                window_data=[win.get(), win_title.get(), win_log.get()]
                canv_data=canv_size.get()
                f= filedialog.asksaveasfilename(initialfile="Untitled.txt",
                defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents","*.txt")])
                with open(f, "w") as fh:
                    fh.write(str(temp_dic)+"\n")
                    fh.write(str(sql_info)+"\n")
                    fh.write(str(window_data)+"\n")
                    fh.write(str(opt)+"\n")
                    fh.write(str(canv_data))
                root.title(os.path.basename(f) + " - Hestia")
                setup_filename=f
            except:
                pass
        else:
            messagebox.showerror("No Widgets","No widgets on the canvas. : (")
            
    def num_rem(s):
        """This function removes number from key name (The key name in img_ref_dic)"""
        if s[:5] in ("Label","Entry"):
            return s[:5]
        elif s[:6]=="Button":
            return s[:6]

    #Function for adding features to the code.
    def add_feat(l):
        """This function adds extra features to the Tkinter code"""
        if TTK.get() and "tkinter.ttk" not in l:
            l.append("tkinter.ttk")
        if SQL.get() and "mysql.connector" not in l:
            l.append("mysql.connector")
        if pil.get() and "PIL" not in l:
            l.append("PIL")
        return l

    def sql_data():
        """This function takes SQL Login Credentials"""
        if SQL.get():
            sql=Toplevel(root)
            sql.title("SQL Credentials")
            sql.iconbitmap(resource_path("Project Images\\Main_Logo.ico"))
            sql.resizable(width=False, height=False)
            sql.transient(root)
            username=StringVar()
            passwd=StringVar()
            database=StringVar()
            def sql_log():
                global sql_info
                user=username.get()
                passw=passwd.get()
                datab=database.get()
                if user and passw and datab:
                    sql_info={"host":"localhost","user":user, "passwd":passw,\
                              "database":datab}
                    sql.destroy()
                else:
                    messagebox.showerror("Empty Field","Please enter something in the fields.")
            ttk.Label(sql, text="MySQL Login Data").grid(row=0, column=0, columnspan=2)
            ttk.Label(sql, text="Username: ").grid(row=1, column=0, padx=5)
            ttk.Entry(sql, textvariable=username).grid(row=1, column=1, padx=10, pady=3)
            ttk.Label(sql, text="Password: ").grid(row=2, column=0, padx=5)
            ttk.Entry(sql, textvariable=passwd).grid(row=2, column=1, padx=10, pady=3)
            ttk.Label(sql, text="Database: ").grid(row=3, column=0, padx=5)
            ttk.Entry(sql, textvariable=database).grid(row=3, column=1, padx=10, pady=3)
            ttk.Button(sql, text="Submit", command=sql_log).grid(row=4, column=1, pady=5)
            sql.mainloop()
        
    #Functions for writing code.
    def widget_writer(l):
        """This function writes the widgets to dictionary"""    
        win_name=win.get()
        line=len(widget_list) 
        key=eval(str(l.keys())[10:-1]) #This line makes the list of all the keys.
        for i in range(line, len(key)):
            line=""
            if l[key[i]][9]=="Yes":
                terms=[f'{num_rem(key[i])}',f'({win_name}', f', textvariable={l[key[i]][10]}', \
 f", bg='{l[key[i]][3]}'", f", fg='{l[key[i]][4]}'", f', borderwidth={l[key[i]][5]}', \
 f", relief='{l[key[i]][6]}'", f', width={l[key[i]][7]}',f').place(x={l[key[i]][1]}', f', y={l[key[i]][2]})\n']
                for term in terms:
                    if term.find("Default")==-1 and term.find("relief")==-1:
                        line+=term
                    elif term.find("relief")!=-1 and term.find("default")==-1: #Since relief may have 'Default' in lower case, this line 
                        line+=term                                             #checks for that. (And same with the line in second part)
                widget_list.append(line)
            else:
                terms=[f'{num_rem(key[i])}',f'({win_name}', f", text='{l[key[i]][8]}'", \
 f", bg='{l[key[i]][3]}'", f", fg='{l[key[i]][4]}'", f', borderwidth={l[key[i]][5]}', \
 f", relief='{l[key[i]][6]}'", f', width={l[key[i]][7]}',f').place(x={l[key[i]][1]}', f', y={l[key[i]][2]})\n']
                for term in terms:
                    if term.find("Default")==-1 and term.find("relief")==-1:
                        line+=term
                    elif term.find("relief")!=-1 and term.find("default")==-1:
                        line+=term
                widget_list.append(line)

    def final_writer(file,opt, widget_list, var_list,sql_info):
        """This function writes the final code on file"""
        file.write("from tkinter import *\n")
        for extra in opt:
            file.write(f"from {extra} import *\n")
        if "mysql.connector" in opt:
            file.write(f'''con=connect(host="localhost",user="{sql_info['user']}", \
passwd="{sql_info['passwd']}", database="{sql_info['database']}")\n''')
        file.writelines(["\n",f"{win.get()}=Tk()\n",\
                         f"{win.get()}.title('{win_title.get()}')\n",\
                         f"{win.get()}.iconbitmap(r'{win_log.get()}')\n"])
        file.write(f"{win.get()}.geometry('{canvas.winfo_width()}x{canvas.winfo_height()}')")
        if len(var_list)!=0:
            file.write("\n\n#Tkinter variables used in code.\n")
            code_var=[var for var in var_list]
            file.writelines(code_var)
        file.write("\n\n#Widgets\n")
        widgets=[line for line in widget_list]
        file.writelines(widgets)
        file.write(f"\n{win.get()}.mainloop()")

    #Functions for handling widgets with variables    
    def var_opt():
        """This function adds/removes the widget variable name entry"""
        if var_ch.get()==2:
            Wid_Var.grid(row=5, column=0, padx=5, pady=5)            
            Wid_Var_Ent.grid(row=5, column=1)        
        else:
            Wid_Var.grid_forget()            
            Wid_Var_Ent.grid_forget()

    def var_add(l,l2):
        """This function adds code for Tkinter variables used in code"""
        line=len(l) 
        key=eval(str(l.keys())[10:-1])
        for i in range(line):
            if l[key[i]][9]=="Yes":
                l2.append(f"{l[key[i]][10]}=StringVar()\n{l[key[i]][10]}.set('{l[key[i]][8]}')\n")
        pass
    
    def close_main(event=None):
        """This function overrides the close button to ask the user if it really wants to quit"""
        if messagebox.askyesno("Quit","Do you really want to quit?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW",close_main)

    def win_name():
        nam_win=Toplevel(root)
        nam_win.title("Window Name")
        nam_win.iconbitmap(resource_path("Project Images\\Main_Logo.ico"))
        nam_win.resizable(width=False, height=False)
        nam_win.transient(root)
        def win_set():
            win_name=win.get()
            win.set(win_name)
            nam_win.destroy()
        ttk.Label(nam_win, text="Parent Window Name: ").grid(row=0, column=0, columnspan=2, sticky="news")
        ttk.Label(nam_win, text="Name: ").grid(row=1, column=0, padx=3)
        ttk.Entry(nam_win, textvariable=win).grid(row=1, column=1, padx=5, pady=10)
        ttk.Button(nam_win, text="OK", command=win_set).grid(row=2, column=1, padx=5, pady=5)
        nam_win.mainloop()

    def win_titl():
        title_win=Toplevel(root)
        title_win.title("Window Title")
        title_win.iconbitmap(resource_path("Project Images\\Main_Logo.ico"))
        title_win.resizable(width=False, height=False)
        title_win.transient(root)
        def win_title_set():
            win_head=win_title.get()
            win_title.set(win_head)
            title_win.destroy()
        ttk.Label(title_win, text="Parent Window Title: ").grid(row=0, column=0, columnspan=2, sticky="news")
        ttk.Label(title_win, text="Title: ").grid(row=1, column=0, padx=3)
        ttk.Entry(title_win, textvariable=win_title).grid(row=1, column=1, padx=5, pady=10)
        ttk.Button(title_win, text="OK", command=win_title_set).grid(row=2, column=1, padx=5, pady=5)
        title_win.mainloop()

    def win_logo():
        f= filedialog.askopenfilename(defaultextension=".ico",filetypes=[("All Files", "*.*"), ("Icons","*.ico")])
        win_log.set(f)
        pass

    #Functions for help and docs.
    def help_window():
        help_win=Toplevel(root)
        help_win.title("About Hestia v1.0")
        help_win.iconbitmap(resource_path("Project Images\\Main_Logo.ico"))
        help_win.resizable(width=False, height=False)
        help_win.transient(root)
        img = Image.open(resource_path("Project Images\\Main_Logo_Help.png"))
        img = img.resize((110,128), Image.ANTIALIAS)
        poster =  ImageTk.PhotoImage(img)
        head=Label(help_win, image=poster)
        head.grid(row=1, column=0, pady=15)
        info=["Hestia - The GUI Creator",'Hestia is a program by which you can \n\
        create your own GUI program setup effortlessly.',"Hestia is currently being developed.",\
        "For any suggestions or bug reports,\n you can email me at udits2844@gmail.com"]
        Label(help_win, text=info[0]).grid(row=2, column=0, pady=5, padx=10)
        Label(help_win, text=info[1]).grid(row=3, column=0, pady=5, padx=10)
        Label(help_win, text=info[2]).grid(row=4, column=0, pady=5, padx=10)
        Label(help_win, text=info[3]).grid(row=5, column=0, pady=5, padx=10)
        Label(help_win, text="").grid(row=6, column=0, padx=10)
        help_win.mainloop()
        
    def hes_doc():
        wb.open(resource_path(r'Introduction to Hestia.pdf'))
        
    #Menu for file operations
    filemenu=Menu(menubar, tearoff=0)

    filemenu.add_command(label="New File", accelerator="Ctrl+N", compound=LEFT, underline=0, command=New_File)
    filemenu.add_command(label="Open Setup...", accelerator="Ctrl+O", compound=LEFT, underline=0, command=Open)
    filemenu.add_command(label="Save Code", accelerator="Ctrl+Alt+C", compound=LEFT, underline=0, command=Save_Code)
    filemenu.add_command(label="Save Code As", accelerator="Ctrl+Shift+C", command=Save_Code_As)
    filemenu.add_command(label="Save Setup", accelerator="Ctrl+S", compound=LEFT, underline=0, command=Save_Setup)
    filemenu.add_command(label="Save Setup As", accelerator="Ctrl+Shift+S", command=Save_Setup_As)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", accelerator="Alt+F4", command=close_main)

    menubar.add_cascade(label="File", menu=filemenu)

    #Menu For Widgets
    widgetmenu=Menu(menubar, tearoff=0)
    widgets=["Label","Button","Entry"]
    for i in widgets:
        widgetmenu.add_cascade(label=i, command= lambda i=i: give(i))
        
    menubar.add_cascade(label="New Widget", menu=widgetmenu)

    #Menu for Canvas size.
    canv_size_menu=Menu(menubar, tearoff=0)
    sizes=["450x350","600x450","750x500","800x600", "Custom"]
    canv_size= StringVar()
    canv_size.set("450x350")
    for x in sizes:
        canv_size_menu.add_radiobutton(label=x, variable=canv_size, command=resize)
        
    menubar.add_cascade(label="Canvas Size", menu=canv_size_menu)

    #Menu for Add-ons.
    add_ons_menu=Menu(menubar, tearoff=0)
    TTK=IntVar()
    add_ons_menu.add_checkbutton(label="ttk (Beta)", onvalue=1, offvalue=0, variable=TTK)
    SQL=IntVar()
    add_ons_menu.add_checkbutton(label="MySQL", onvalue=1, offvalue=0, variable=SQL, command=sql_data)
    pil=IntVar()
    add_ons_menu.add_checkbutton(label="PIL", onvalue=1, offvalue=0, variable=pil)
    menubar.add_cascade(label="Add-Ons", menu=add_ons_menu)

    #Menu for Parent Window options.
    par_win=Menu(menubar, tearoff=0)
    win_opt=["Name","Title","Logo"]
    for option in win_opt:
        cmd=eval("win_"+option[:4].lower())
        par_win.add_cascade(label=option, command=cmd)

    menubar.add_cascade(label="Parent Window", menu=par_win)
    

    #Menu for help in the program.
    help_menu=Menu(menubar, tearoff=0)
    help_option=["About Hestia","Hestia Docs"]
##    for option in help_option:
##        help_menu.add_cascade(label=option)
    help_menu.add_cascade(label="About Hestia", command=help_window)
    help_menu.add_cascade(label="Hestia Docs", command=hes_doc)
    menubar.add_cascade(label="Help", menu=help_menu)
    root.config(menu=menubar)
                
    #Data Frame Buttons.
    #ttk.Button(widget_data_frame, text="Thor, Hit Me", command=lambda: make(img_ref_dic)).grid(row=0, column=0)
    ttk.Label(widget_data_frame, text="Current Widget Data", style='My.TLabel').grid(row=0, column=0, columnspan=2, pady=5)            
    ttk.Label(widget_data_frame, text="Current Widget: ", style='My.TLabel').grid(row=1, column=0, pady=5)
    ttk.Label(widget_data_frame, textvariable=address, style='My.TLabel').grid(row=1, column=1)
    ttk.Label(widget_data_frame, text="Widget Text: ", style='My.TLabel').grid(row=2, column=0, padx=5, pady=5)            
    ttk.Entry(widget_data_frame, textvariable=txt).grid(row=2, column=1)
    ttk.Label(widget_data_frame, text="Set Text As: ", style='My.TLabel').grid(row=3, column=0, pady=5)
    ttk.Radiobutton(widget_data_frame,text="Text Item", variable=var_ch, value=1, style="My.TRadiobutton", command=var_opt).grid(row=3, column=1, sticky="news")
    ttk.Radiobutton(widget_data_frame,text="Text Variable", variable=var_ch, value=2, style="My.TRadiobutton", command=var_opt).grid(row=4, column=1, sticky="news")
    Wid_Var=ttk.Label(widget_data_frame, text="Variable Name: ", style='My.TLabel')
    Wid_Var_Ent=ttk.Entry(widget_data_frame, textvariable=var_nam)
    ttk.Label(widget_data_frame, text="Background Color: ", style='My.TLabel').grid(row=6, column=0, padx=5)
    bg_color=ttk.Combobox(widget_data_frame, width=17, textvariable=bg)
    bg_color['values']=("Default","White","Black","Red","Blue","Green","Yellow")
    bg_color.grid(row=6, column=1, pady=5)
    ttk.Label(widget_data_frame, text="Foreground Color: ", style='My.TLabel').grid(row=7, column=0, padx=5)
    fg_color=ttk.Combobox(widget_data_frame, width=17, textvariable=fg)
    fg_color['values']=("Default","White","Black","Red","Blue","Green","Yellow")
    fg_color.grid(row=7, column=1, pady=5)
    ttk.Label(widget_data_frame, text="Width: ", style='My.TLabel').grid(row=8, column=0, padx=5)
    w_breadth=ttk.Combobox(widget_data_frame, width=17, textvariable=wd)
    w_breadth['values']=("Default",10,12,14,16,18,20,22)
    w_breadth.grid(row=8, column=1, pady=5)
    ttk.Label(widget_data_frame, text="Border Width: ", style='My.TLabel').grid(row=9, column=0, padx=5)
    w_border=ttk.Combobox(widget_data_frame, width=17, textvariable=bd)
    w_border['values']=(1,2,3,4,5)
    w_border.grid(row=9, column=1, pady=5)
    ttk.Label(widget_data_frame, text="Relief: ", style='My.TLabel').grid(row=10, column=0, padx=5)
    w_rel=ttk.Combobox(widget_data_frame, width=17, textvariable=rel_sty)
    w_rel['values']=("Default","Solid","Sunken","Raised","Groove","Ridge")
    w_rel.grid(row=10, column=1, pady=5)
    ttk.Button(widget_data_frame, text="Place Widget", command=save).grid(row=11,column=0, columnspan=2, padx=5, pady=10)
    #ttk.Button(widget_data_frame, text="Save Code", command=lambda: widget_writer(img_ref_dic)).grid(row=11, column=1, pady=10)

    #Disabling the menu options that work only with canvas available.
    dis_enable_new(False)
    
    #Key Bindings
    canvas.bind("<B1-Motion>",move)
    root.bind("<Control-N>", New_File)
    root.bind("<Control-n>", New_File)
    root.bind("<Control-O>", Open)
    root.bind("<Control-o>", Open)
    root.bind("<Control-Alt-C>", Save_Code)
    root.bind("<Control-Alt-c>", Save_Code)
    root.bind("<Control-Shift-C>", Save_Code_As)
    root.bind("<Control-Shift-c>", Save_Code_As)
    root.bind("<Control-S>", Save_Setup)
    root.bind("<Control-s>", Save_Setup)
    root.bind("<Control-Shift-S>", Save_Setup_As)
    root.bind("<Control-Shift-s>", Save_Setup_As)
    root.bind("<Alt-F4>",close_main)
    root.mainloop()
    
splash_root.after(3000, main)
splash_root.mainloop()

#To-Do-List:
#1.  Add the text variable/text option to dictionary. - Done.
#2.  For saving a setup, you have to just save the main dictionaries in
#    a text file. - Done.
#3.  Add file dialogues for saving and opening files.-Done
#4.  Add a button to write the final code on a text file. - Done.
#5.  Add option for extra add-ons in code eg. ttk, sql connector etc. -Done.
#6.  Find more options to give in widget data options. - Done.
#7.  Figure out how to undo, redo things in this program. - Will do, maybe later
#8.  Write 'About' and 'Documentation' for the program.
#9.  Make a nice logo for the program. -Done
#10. Make a transition window as in MS Teams for this. -Done
#11. Add lines to file that declares variables.-Done
#12. PLEASE Do something for the window when it resizes, check resize function.-Done
#13. Add code that writes SQL credentials to the code file.-Done
#14. Create option for main window name, background image. -Done (Will see about background image)
#15. Create a function take_var_name , that takes the names of the currently
#    used names of the variables in the user code (Use it in opened files too).
#16. When user saves his setup , make option to save SQL and other stuff too. -Done
#17. Write code for the default settings of fg, bg etc. -Done
#18. The Save Setup function deletes the widgets on screen. - Done
#19. If the user chooses to have a widget textvariable, then initialize
#    that variable with the text given in text field. -Done
#20. Write About Hestia and Hestia Docs.
#21. When you get time , you can add an option to add menu to the user's
#    GUI program.
#22. Correct the Save function to save as filename.

#Complaints.
#1. Functions are glitchy. -Resolved
#2. Check for proper functioning of open/save/save setup etc. functions.-Done
#3. The open function does not assign the global img_ref_dic its value, look for the solution please.-Done

#Notes
#1. The last change that you made was in final writer function and
#   was about the logo of user's window.
