#necessary modules
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import ttkbootstrap as ttb
from tkinter.font import Font
from PIL import Image,ImageTk,ImageDraw
from datetime import date
from tkinter import filedialog as fd
import os.path 
import sqlite3
import shutil
import re
import cv2
from functools import partial
win_man=[]

def db_creation():      
    conn = sqlite3.connect('mydb.db') 
    cursor = conn.cursor()
    
    create_table_query = '''
    CREATE TABLE Users (   
    email TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    qualification TEXT NOT NULL,
    gender TEXT NOT NULL,
    image BLOB  NULL,
    description TEXT NULL
    )
    '''
    
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()
    
if(os.path.isfile("mydb.db")):
    pass
else:
    db_creation()

conn = sqlite3.connect('mydb.db') 
cursor = conn.cursor()

def insert_data(*userDetails):
    for dat in userDetails:
        
        if dat == "":
            mb.showwarning(title="Crud Application",message="Enter values in all the filed",parent=cwin)
            return False
    
    if userDetails[0] == "example@mail.com" or userDetails[1] == "Example" or userDetails[2] == "Password" :
         mb.showerror(title="Crud Application",message="The default details can't be stored",parent=cwin)
         return False
    try:
        
        insert_query = '''
        INSERT INTO Users (email, name, password, date_of_birth, qualification, gender)
        VALUES (?, ?, ?, ?, ?, ?)'''
        
        cursor.execute(insert_query,userDetails)
        conn.commit()
        mb.showinfo(title="Crud Application",message="Data has been stored",parent=cwin)
        
        go_back()
        win_man[-1].state("deiconify")
    
    except sqlite3.IntegrityError :
        mb.showerror(title="Crud Application",message="Mail-Id already registered",parent=cwin)
        return False

def read_data(mail,pwd):
    if mail == "" or pwd == "":
        mb.showerror("Crud Application","Enter values in the field")
        return False
    
    if mail == "example@gmail.com" or pwd == "password" :
        mb.showerror("Crud Application","This is the default value please enter somevalues")
        return False
    
    query = '''SELECT * FROM Users WHERE email=? '''
    cursor.execute(query,(mail,))
    res = cursor.fetchall()

    if (len(res) == 0):
        mb.showerror("Crud Application","invalid mail id")
    else:
        if(res[0][2] == pwd):
            read(res)
        else:
            mb.showerror("Crud Application","Invalid Password")

def fetch_data_for_update(mail):
    
    if mail == "":
        mb.showerror(title="Crud Application",message="invalid mail id",parent=uwin)
        return False
    
    query = '''SELECT * FROM Users WHERE email=? '''
    cursor.execute(query,(mail,))
    res = cursor.fetchall()
    
    if (len(res) == 0):
        mb.showerror(title="Crud Application",message="invalid mail id",parent=uwin)
    else :
        up_update(res)

def fetch_data_for_delete(dmail):
    
    if dmail == '':
        mb.showerror(title="Crud Application",message="Enter value in field",parent = dwin)
    else:
        delete_query = '''
        DELETE FROM Users
        WHERE email = ?
        '''
        
        cursor.execute("SELECT * from Users where email=?;",(dmail,))
        a = cursor.fetchall()
        
        if len(a) != 0:
            if mb.askyesno(title="Crud Application",message="Are you sure want to delete your profile",parent = dwin):
                cursor.execute(delete_query, (dmail,))
                mb.showinfo(title="Crud Application",message="Your Data has been deleted",parent = dwin)
                conn.commit()
            else:
                pass
        else :
            mb.showerror(title="Crud Application",message="Invalid Mail-Id",parent = dwin)
        
def update_data(*data):
    
    for d in data:
        if d == "":
            mb.showerror(title="Crud Application",message="Enter values in all the field",parent=uwin) 
            return False
    
    update_query = '''
    UPDATE Users
    SET name = ?,date_of_birth=?, qualification = ?,gender=?
    WHERE email = ?
    '''
    cursor.execute(update_query,data)
    conn.commit()
    mb.showinfo("Crud Application","Data Updated Successfully")

def up_update(data):
    Label(uFrame,text="Enter name:",font=labelfont).place(x=600,y=350)
    Label(uFrame,text="Enter Date-Of-Birth:",font=labelfont).place(x=600,y=450)
    Label(uFrame,text="Select Qualification:",font=labelfont).place(x=600,y=550)
    Label(uFrame,text="Select Gender:",font=labelfont).place(x=600,y=650)
    
    name_ent = ttb.Entry(uFrame,bootstyle="secondary", width=50)
    name_ent.place(x= 1000,y=350,height=50)
    
    date_ent=ttb.DateEntry(uFrame,bootstyle='dark',width = 50)
    date_ent.place(x=1000,y=450,height=50)
    
    combo = ttb.Combobox(uFrame,bootstyle='primary',values=('PG','UG','XII','X','Below X'),width=50)
    combo.place(x=1000,y=550)
    
    gen=StringVar()
    
    ttb.Radiobutton(uFrame,text="Male",variable=gen,bootstyle='success',value="male").place(x=1000,y=650)
    ttb.Radiobutton(uFrame,text="Female",variable=gen,bootstyle='danger',value="female").place(x=1100,y=650)
    
    com_dict = {"PG":0,"UG":1,"XII":2,"X":3,"Below X":4}
    
    name_ent.insert(0,data[0][1])
    date_ent.entry.delete(0, 'end')
    date_ent.entry.insert(0,data[0][3])
    combo.current(com_dict[data[0][4]])
    gen.set(data[0][5])
    
    ttb.Button(uFrame,text='Update',bootstyle="info-outline",width=50,command= lambda : update_data(name_ent.get(),date_ent.entry.get(),combo.get(),gen.get(),uEmail_ent.get())).place(x=800,y=750,height=50)
        
def upadate_image(file_name,mail):
    update_query = '''
    UPDATE Users
    SET image=?
    WHERE email = ?
    '''
    cursor.execute(update_query,(file_name,mail))
    conn.commit()
    mb.showinfo(title="Crud Application",message="Image Updated Successfully",parent = rwin)

def round_image(image_path, size):
    image = Image.open(image_path)
    image = image.resize((size, size), resample=Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    rounded_image = Image.new("RGBA", (size, size))
    rounded_image.paste(image, (0, 0), mask=mask)
    photo = ImageTk.PhotoImage(rounded_image)
    return photo

def add_image(mail):
    win.destroy()
    global profile_img
    global img_label
    global profile_img
    
    dest_file = "images/"
    
    f_types = [('Jpg Files', '*.jpg'),('Png Files', '*.png'),('All files','*.*')]
    file_loc = fd.askopenfilename(parent = rwin,title='Open a Image file',filetypes=f_types)
    file_name = os.path.basename(file_loc)
    dest_file+=file_name
    shutil.copyfile(file_loc,dest_file)
    upadate_image(dest_file,mail)
    add_p_btn.configure(text="+ Edit Profile")
    
    cursor.execute("SELECT image from Users where email=?",(mail,))
    img_file = cursor.fetchone()
    profile_img = round_image(img_file[0], 200)
    img_label.configure(image=profile_img)

def update_desc(data,mail):
    u_q = '''
    UPDATE Users
    SET description=?
    WHERE email = ?
    '''
    
    cursor.execute(u_q,(data,mail))
    conn.commit()
    desc_ent.destroy()
    desc_sub_btn.destroy()
    mb.showinfo(title="Crud Application",message="Description Updated Successfully",parent = rwin)
    
    cursor.execute("SELECT description from Users where email=?",(mail,))
    a = cursor.fetchone()
    if a[0]=="":
        desc_label.configure(text="Add a description")
    else:
        desc_label.configure(text=a[0])

def add_desc(mail):
    global desc_ent
    global desc_sub_btn
    
    desc_ent = ttb.Text(rFrame)
    desc_ent.place(x=800,y=120,width=900,height=150)
    
    cursor.execute("SELECT description from Users where email=?",(mail,))
    a = cursor.fetchone()
    
    if a[0] is None:
        pass
    else:
        desc_ent.insert("1.0",a[0])
    desc_sub_btn=ttb.Button(rFrame,text='Submit',bootstyle="info-outline",command= lambda : update_desc(desc_ent.get("1.0", "end-1c"),mail))
    desc_sub_btn.place(x=1200,y=280)

def go_back():
    global win_man
    
    if len(win_man) != 1 :
        win_man[-1].destroy()
        win_man.pop()
    else:
        if mb.askyesno('Crud Application',"Do You want to exit ?") :
            win_man[-1].destroy()
            win_man.pop()

def validate_email(mail):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern,mail):
        return True
    else:
        return False

def open_camera(name,mail):
    global img_name
    global profile_img
    win.destroy()
    cam = cv2.VideoCapture(0)
    img_counter = 0
    while True: 
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Press Space to capture image", frame)

        k = cv2.waitKey(1)
        
        if k%256 == 27:
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            img_name = f"images/{name}.png"
            cv2.imwrite(img_name, frame)
            img_counter += 1
            break

    cam.release()
    cv2.destroyAllWindows()
    
    upadate_image(img_name,mail)
    add_p_btn.configure(text="+ Edit Profile")
    cursor.execute("SELECT image from Users where email=?",(mail,))
    img_file = cursor.fetchone()
    profile_img = round_image(img_file[0], 200)
    img_label.configure(image=profile_img)

def open_image(name,mail):
    global win
    win = Toplevel()
    win.geometry("400x200")
    win.title("Crud Application")
    ttb.Button(win,text='Open File',bootstyle="secondary",width=20,command = lambda : add_image(mail)).pack(side=LEFT,padx=10)
    ttb.Button(win,text='Open Camera',bootstyle="secondary-ttl",width=20,command = lambda : open_camera(name,mail)).pack(side=RIGHT,padx=10)
    
def create():  
    global cwin
    
    cwin=Toplevel()
    win_man.append(cwin)
    
    cwin.geometry("2000x2000")
    cwin.state("zoomed")
    cwin.title("Crud Application")
    
    cFrame = Frame(cwin)
    cFrame.place(width=2000,height=2000)
    
    cwin.iconphoto(False,icon)
    
    menubar=Menu(cwin)
    opt=Menu(menubar,tearoff=0,font=("cambria",15))
    menubar.add_cascade(label="Options",menu=opt)
    opt.add_command(label="Create",command=create)
    opt.add_command(label="Read",command=read,state=DISABLED)
    opt.add_command(label="Update",command = update)
    opt.add_command(label="Delete",command=delete)
    opt.add_command(label="Close",command=root.destroy)
    cwin.config(menu=menubar)
        
    Button(cFrame,image=back,command = go_back).place(x=10,y=10)
    
    ttb.Separator(cFrame,bootstyle="warning",orient="horizontal").place(x=450,y=950,width=1100)
    ttb.Separator(cFrame,bootstyle="warning",orient="vertical").place(x=450,y=200,height=750)
    ttb.Separator(cFrame,bootstyle="warning",orient="horizontal").place(x=450,y=200,width=1100)
    ttb.Separator(cFrame,bootstyle="warning",orient="vertical").place(x=1550,y=200,height=750)
    
    Label(cFrame,text="Register your profile",font=titfont).place(x=470,y=30)
    Label(cFrame,text="Enter Mail id:",font=labelfont).place(x=600,y=250)
    Label(cFrame,text="Enter Name:",font=labelfont).place(x=600,y=350)
    Label(cFrame,text="Enter Password:",font=labelfont).place(x=600,y=450)
    Label(cFrame,text="Enter Date-Of-Birth:",font=labelfont).place(x=600,y=550)
    Label(cFrame,text="Select Qualification:",font=labelfont).place(x=600,y=650)
    Label(cFrame,text="Select Gender:",font=labelfont).place(x=600,y=750)
    
    gender = StringVar()
    
    mail_ent = ttb.Entry(cFrame,bootstyle="primary", width=50)
    mail_ent.place(x= 1000,y=250,height=50)
    
    name_ent = ttb.Entry(cFrame,bootstyle="secondary", width=50)
    name_ent.place(x= 1000,y=350,height=50)
    
    pass_ent = ttb.Entry(cFrame,bootstyle="info",width=50)
    pass_ent.place(x= 1000,y=450,height=50)
    
    date_ent=ttb.DateEntry(cFrame,bootstyle='dark',startdate=date(2003,5,14),width = 50)
    date_ent.place(x=1000,y=550,height=50)
    
    combo_ent=ttb.Combobox(cFrame,bootstyle='primary',values=('PG','UG','XII','X','Below X'),width=50)
    combo_ent.place(x=1000,y=650)
    
    ttb.Radiobutton(cFrame,text="Male",bootstyle='success',variable=gender,value="male").place(x=1000,y=750)
    ttb.Radiobutton(cFrame,text="Female",bootstyle='danger',variable=gender,value="female").place(x=1100,y=750)
    
    ttb.Button(cFrame,text='Submit',bootstyle="info-outline",width=100,command = lambda : insert_data(mail_ent.get(),name_ent.get(),pass_ent.get(),date_ent.entry.get(),combo_ent.get(),gender.get())).place(x=600,y=850,height=50)
    
    mail_ent.insert(0,"example@mail.com")
    name_ent.insert(0,"Example")
    pass_ent.insert(0,"Password")
    
    mail_err_lab = ttb.Label(cFrame,font=('Microsoft Yahei UI Light', 10, 'bold'),bootstyle="danger")
    mail_err_lab.place(x=1000,y=300)
    name_err_lab = ttb.Label(cFrame,font=('Microsoft Yahei UI Light', 10, 'bold'),bootstyle="danger")
    name_err_lab.place(x=1000,y=400)
    pass_err_lab = ttb.Label(cFrame,font=('Microsoft Yahei UI Light', 10, 'bold'),bootstyle="danger")
    pass_err_lab.place(x=1200,y=500)
    
    def pass_show():
        if(cbval.get()==1):
            pass_ent.config(show="")
        else:
            pass_ent.config(show="*")

    cbval=IntVar(value=0)
    checkb= ttb.Checkbutton(cwin,text='Show Password',variable=cbval,onvalue=1,offvalue=0,command=pass_show)
    checkb.place(x=1000,y=500)
    
    def mail_ent_enter(a):
        if(mail_ent.get() == 'example@mail.com'):
            mail_ent.delete(0, 'end')
    mail_ent.bind("<FocusIn>",mail_ent_enter)

    def mail_ent_leave(a):
        if mail_ent.get() == "":
            mail_err_lab.configure(text="Maild-Id can't be null")
            mail_ent.insert(0,"example@mail.com")
        else:
            mail_err_lab.configure(text="")
            if validate_email(mail_ent.get()):
                pass
            else:
                mail_err_lab.configure(text="Invalid Maild-ID")
    mail_ent.bind("<FocusOut>",mail_ent_leave)
    
    def name_ent_enter(a):
        if(name_ent.get() == 'Example'):
            name_ent.delete(0, 'end')
    name_ent.bind("<FocusIn>",name_ent_enter)

    def name_ent_leave(a):
        if name_ent.get() == "":
            name_err_lab.configure(text="Name can't be null")
            name_ent.insert(0,"Example")
        else:
            name_err_lab.configure(text="")
    name_ent.bind("<FocusOut>",name_ent_leave)
    
    def pass_ent_enter(a):
        if(pass_ent.get() == 'Password'):
            pass_ent.delete(0, 'end')
            pass_ent.configure(show="*")
    pass_ent.bind("<FocusIn>",pass_ent_enter)

    def pass_ent_leave(a):
        if pass_ent.get() == "":
            pass_err_lab.configure(text="Password can't be null")
            pass_ent.insert(0,"Password")
            pass_ent.configure(show="")
        else:
            pass_err_lab.configure(text="")
    pass_ent.bind("<FocusOut>",pass_ent_leave)
    
def read(res):
    global profile_img
    global img_label
    global rwin
    global add_p_btn
    global plus
    global desc_label
    global rFrame
    global descFrame
    
    rwin=Toplevel()
    win_man.append(rwin)
    
    rwin.geometry("2000x2000")
    rwin.state("zoomed")
    rwin.title("Crud Application")
    
    rFrame = Frame(rwin)
    rFrame.place(width=2000,height=2000)
    rwin.iconphoto(False,icon)
    
    Button(rFrame,image=back,command = go_back).place(x=10,y=10)
    
    menubar=Menu(rwin)
    opt=Menu(menubar,tearoff=0,font=("cambria",15))
    menubar.add_cascade(label="Options",menu=opt)
    opt.add_command(label="Create",command=create)
    opt.add_command(label="Read",command=read,state=DISABLED)
    opt.add_command(label="Update",command = update)
    opt.add_command(label="Delete",command=delete)
    opt.add_command(label="Close",command=root.destroy)
    rwin.config(menu=menubar)
    	
    ttb.Separator(rFrame,bootstyle="warning",orient="horizontal").place(x=280,y=950,width=1500)
    ttb.Separator(rFrame,bootstyle="warning",orient="vertical").place(x=280,y=50,height=900)
    ttb.Separator(rFrame,bootstyle="warning",orient="horizontal").place(x=280,y=50,width=1500)
    ttb.Separator(rFrame,bootstyle="warning",orient="vertical").place(x=1780,y=50,height=900)
    
    if res[0][6] is None:
        profile_img = round_image('profile.jpg', 200)
        img_label = Label(rFrame, image = profile_img,)
        img_label.place(x= 420 , y = 100)
        prof_btn_txt = "+ Add Profile"
    else:
        if os.path.isfile(res[0][6]):    
            profile_img = round_image(res[0][6], 200)
            img_label = Label(rFrame, image = profile_img,)
            img_label.place(x= 420 , y = 100)
            prof_btn_txt = "+ Edit Profile"
        else:
            profile_img = round_image('profile.jpg', 200)
            img_label = Label(rFrame, image = profile_img,)
            img_label.place(x= 420 , y = 100)
            prof_btn_txt = "+ Edit Profile"
            mb.showinfo(title="Crud Application",message="Your Image file was deleted kindly reupload it",parent=rwin)
            
    add_p_btn= ttb.Button(rFrame,text=prof_btn_txt,bootstyle="light-outline-toolbutton",width=40,command=lambda:open_image(res[0][1],res[0][0]))
    add_p_btn.place(x=350,y=330,height=50)
    
    ffont = Font(family="georgia",size=30,underline=1)
    
    desc="Add a description"
    descFrame = LabelFrame(rFrame,text="-Description:-",font=("geogia",20),bg="#121212")
    descFrame.place(x=800,y=120 ,width=900,height=200)
    
    plus = PhotoImage(file = 'plus.png')
    
    if res[0][7] is None:
        desc_label=Label(descFrame,text=desc,font=("courier",13))
        desc_label.grid(row=1,column=1,padx=10,pady=5)
        ttb.Button(rFrame,image=plus,command=lambda:add_desc(res[0][0]),bootstyle="dark").place(x=1700,y=200)
    
    else:
        desc_label=Label(descFrame,text=res[0][7],font=("courier",13))
        desc_label.grid(row=1,column=1,padx=10,pady=5)
        ttb.Button(rFrame,image=plus,command=lambda:add_desc(res[0][0]),bootstyle="dark").place(x=1700,y=200)
       
    Label(rFrame,text="Welcome back",font=("geogia",30)).place(x=800,y=350)
    Label(rFrame,text=res[0][1],font=ffont,fg="gold").place(x=1150,y=350)
    
    Label(rFrame,text="Mail-Id",font=labelfont).place(x=600,y=500)
    Label(rFrame,text="Phone Number",font=labelfont).place(x=600,y=600)
    Label(rFrame,text="Qualification",font=labelfont).place(x=600,y=700)
    Label(rFrame,text="Gender",font=labelfont).place(x=600,y=800)
    
    Label(rFrame,text=f":\t{res[0][0]}",font=labelfont,foreground="gold").place(x=950,y=500)
    Label(rFrame,text=f":\t{res[0][3]}",font=labelfont,fg="gold").place(x=950,y=600)
    Label(rFrame,text=f":\t{res[0][4]}",font=labelfont,fg="gold").place(x=950,y=700)
    Label(rFrame,text=f":\t{res[0][5]}",font=labelfont,fg="gold").place(x=950,y=800)
    

def update():
    global uwin
    global uFrame
    global uEmail_ent
    
    uwin=Toplevel()
    win_man.append(uwin)
    
    uwin.geometry("2000x2000")
    uwin.state("zoomed")
    uwin.title("Crud Application")
    
    uFrame = Frame(uwin)
    uFrame.place(width=2000,height=2000)
    
    uwin.iconphoto(False,icon)
    
    Button(uFrame,image=back,command = go_back).place(x=10,y=10)
    
    menubar=Menu(uwin)
    opt=Menu(menubar,tearoff=0,font=("cambria",15))
    menubar.add_cascade(label="Options",menu=opt)
    opt.add_command(label="Create",command=create)
    opt.add_command(label="Read",command=read,state=DISABLED)
    opt.add_command(label="Update",command = update)
    opt.add_command(label="Delete",command=delete)
    opt.add_command(label="Close",command=root.destroy)
    uwin.config(menu=menubar)
    	
    ttb.Separator(uFrame,bootstyle="warning",orient="horizontal").place(x=280,y=950,width=1500)
    ttb.Separator(uFrame,bootstyle="warning",orient="vertical").place(x=280,y=50,height=900)
    ttb.Separator(uFrame,bootstyle="warning",orient="horizontal").place(x=280,y=50,width=1500)
    ttb.Separator(uFrame,bootstyle="warning",orient="vertical").place(x=1780,y=50,height=900)
    
    Label(uFrame,text="Update your profile",font=titfont).place(x=470,y=100)
    Label(uFrame,text="Enter Mail:",font=labelfont).place(x=500,y=250)

    uEmail_ent = ttb.Entry(uFrame,bootstyle="secondary", width=50)
    uEmail_ent.place(x= 740,y=250,height=50)

    ttb.Button(uFrame,text='Search',bootstyle="info-outline",width=30,command= lambda : fetch_data_for_update(uEmail_ent.get())).place(x=1240,y=250,height=50)


def delete():
    global dwin
    global dFrame
    global uEmail_ent
    
    dwin=Toplevel()
    win_man.append(dwin)
    
    dwin.geometry("2000x2000")
    dwin.state("zoomed")
    dwin.title("Crud Application")
    
    dFrame = Frame(dwin)
    dFrame.place(width=2000,height=2000)
    
    dwin.iconphoto(False,icon)
    
    Button(dFrame,image=back,command = go_back).place(x=10,y=10)
    
    menubar=Menu(dwin)
    opt=Menu(menubar,tearoff=0,font=("cambria",15))
    menubar.add_cascade(label="Options",menu=opt)
    opt.add_command(label="Create",command=create)
    opt.add_command(label="Read",command=read,state=DISABLED)
    opt.add_command(label="Update",command = update)
    opt.add_command(label="Delete",command=delete)
    opt.add_command(label="Close",command=root.destroy)
    dwin.config(menu=menubar)
    	
    ttb.Separator(dFrame,bootstyle="warning",orient="horizontal").place(x=450,y=850,width=1000)
    ttb.Separator(dFrame,bootstyle="warning",orient="vertical").place(x=450,y=150,height=700)
    ttb.Separator(dFrame,bootstyle="warning",orient="horizontal").place(x=450,y=150,width=1000)
    ttb.Separator(dFrame,bootstyle="warning",orient="vertical").place(x=1450,y=150,height=700)
    
    Label(dFrame,text="Delete your profile",font=titfont).place(x=500,y=200)
    Label(dFrame,text="Enter Mail:",font=labelfont).place(x=600,y=400)
    
    dEmail_ent = ttb.Entry(dFrame,bootstyle="secondary", width=70)
    dEmail_ent.place(x= 820,y=400,height=50)
    
    ttb.Button(dFrame,text='Search',bootstyle="info-outline",width=90,command= lambda : fetch_data_for_delete(dEmail_ent.get())).place(x=630,y=500,height=50)




root = ttb.Window(themename="cyborg")
win_man.append(root)

root.geometry("2000x2000")
root.state("zoomed")
root.title("Crud Application")

menubar=Menu(root)
opt=Menu(menubar,tearoff=0,font=("cambria",15))
menubar.add_cascade(label="Options",menu=opt)
opt.add_command(label="Create",command=create)
opt.add_command(label="Read",command=read,state=DISABLED)
opt.add_command(label="Update",command = update)
opt.add_command(label="Delete",command=delete)
opt.add_command(label="Close",command=root.destroy)
root.config(menu=menubar)

frontFrame = Frame(root)
frontFrame.place(width=2000,height=2000)

icon = PhotoImage(file = 'cat.png')

root.iconphoto(False,icon)

titfont = Font(family="algerian",underline=1,weight="bold",size=50,slant="italic")
labelfont = Font(family="cambria",size=20)
bfont = Font(size=10)

back = PhotoImage(file='back.png')
Button(frontFrame,image=back,command=go_back).place(x=10,y=10)

Label(frontFrame,text="Crud Application ",font=titfont).place(x=650,y=100)
Label(frontFrame,text="Enter Mail id:",font=labelfont).place(x=600,y=300)
Label(frontFrame,text="Enter Password:",font=labelfont).place(x=600,y=450)

mail_ent = ttb.Entry(frontFrame,bootstyle="primary", width=100)
mail_ent.place(x= 600,y=370,height=50)
mail_ent.insert(0,"example@mail.com")

pw_ent = ttb.Entry(frontFrame,bootstyle="primary", width=100)
pw_ent.place(x= 600,y=520,height=50)
pw_ent.insert(0,"password")

def pw_show():
    if(cbval.get()==1):
        pw_ent.config(show="")
    else:
        pw_ent.config(show="*")

cbval=IntVar(value=0)
checkb= ttb.Checkbutton(root,text='Show Password',variable=cbval,onvalue=1,offvalue=0,command=pw_show)
checkb.place(x=600,y=580)

ttb.Separator(frontFrame,bootstyle="warning",orient="horizontal").place(x=450,y=900,width=1150)
ttb.Separator(frontFrame,bootstyle="warning",orient="vertical").place(x=450,y=50,height=850)
ttb.Separator(frontFrame,bootstyle="warning",orient="horizontal").place(x=450,y=50,width=1150)
ttb.Separator(frontFrame,bootstyle="warning",orient="vertical").place(x=1600,y=50,height=850)

ttb.Button(frontFrame,text = 'Login',width=100,bootstyle="info-outline",command=lambda : read_data(mail_ent.get(),pw_ent.get())).place(x=600,y=650,height=50)

Label(frontFrame,text="Don't have an account",font=labelfont).place(x=700,y=750)
ttb.Button(frontFrame,text = 'Register',width=30,bootstyle="info-link",command = create).place(x=1020,y=750,height=50)

def mail_ent_enter(a):
    if(mail_ent.get() == 'example@mail.com'):
        mail_ent.delete(0, 'end')
mail_ent.bind("<FocusIn>",mail_ent_enter)

def mail_ent_leave(a):
    if mail_ent.get() == "":
        mail_ent.insert(0,"example@mail.com")

mail_ent.bind("<FocusOut>",mail_ent_leave)

def pw_ent_enter(a):
    if(pw_ent.get() == 'password'):
        pw_ent.delete(0, 'end')
        pw_ent.configure(show="*")
pw_ent.bind("<FocusIn>",pw_ent_enter)

def pw_ent_leave(a):
    if pw_ent.get() == "":
        pw_ent.insert(0,"password")
        pw_ent.config(show="")
pw_ent.bind("<FocusOut>",pw_ent_leave)

mail_ent.bind("<Return>",lambda event:read_data(mail_ent.get(),pw_ent.get()))
pw_ent.bind("<Return>",lambda event:read_data(mail_ent.get(),pw_ent.get()))


root.mainloop()