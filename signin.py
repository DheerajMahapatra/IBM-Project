from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import sqlite3

#Functionality Part

def forget_pass():
    def change_password():
        if user_entry.get()=='' or newpass_entry.get()=='' or confirmpass_entry.get()=='':
            messagebox.showerror('Error','All Fields Are Required',parent=window)
            
        elif newpass_entry.get()!=confirmpass_entry.get():
            messagebox.showerror('Error','Password And Confirm Password Are not Matching',parent=window)
            
        else:
            try:
                con=sqlite3.connect('userdata.db')
                mycursor=con.cursor()
                
                query='SELECT * FROM data WHERE username=?'
                mycursor.execute(query,(user_entry.get(),)) 
                row=mycursor.fetchone()
            
                if row is None:
                    messagebox.showerror('Error','Incorrect Username',parent=window)
                
                else:
                    query='UPDATE data SET password=? WHERE username=?'
                    mycursor.execute(query,(newpass_entry.get(),user_entry.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo('Sucess','Password Is Reset, Please LogIn With New Password',parent=window)
                    window.destroy()
                
            except:
                messagebox.showerror('Error','Connection is not established try again',parent=window)            
    
    window=Toplevel()
    window.title('Change Password')
    window.resizable(0, 0)
    
    bgPic=ImageTk.PhotoImage(file='forget.jpg')
    bgLabel=Label(window,image=bgPic)
    bgLabel.grid()
    
    heading_label=Label(window,text='RESET PASSWORD',font=('arial',18,'bold'),bg='#e1e9fa',fg='red')
    heading_label.place(x=720,y=130)
    
    userlabel=Label(window,text='Username',font=('arial',13,'bold'),bg='#e1e9fa',fg='blue')
    userlabel.place(x=720,y=190)
    
    user_entry=Entry(window,width=30,fg='black',bg='#e1e9fa',font=('arial',11,'bold'),bd=0)
    user_entry.place(x=720,y=220)
    
    Frame(window,width=250,height=2,bg='blue').place(x=720,y=240)
    
    
    passwordlabel=Label(window,text='New Password',font=('arial',13,'bold'),bg='#e1e9fa',fg='blue')
    passwordlabel.place(x=720,y=270)
    
    newpass_entry=Entry(window,width=30,fg='black',bg='#e1e9fa',font=('arial',11,'bold'),bd=0)
    newpass_entry.place(x=720,y=300)
    
    Frame(window,width=250,height=2,bg='blue').place(x=720,y=320)
    
    confirmlabel=Label(window,text='Confirm Password',font=('arial',13,'bold'),bg='#e1e9fa',fg='blue')
    confirmlabel.place(x=720,y=350)
    
    confirmpass_entry=Entry(window,width=30,fg='black',bg='#e1e9fa',font=('arial',11,'bold'),bd=0)
    confirmpass_entry.place(x=720,y=380)
    
    Frame(window,width=250,height=2,bg='blue').place(x=720,y=400)
    
    submitButton=Button(window,text='Submit',bd=0,bg='SpringGreen4',fg='white',font=('Open Sans','16','bold'),width=19,cursor='hand2',activebackground='#e1e9fa',activeforeground='red',command=change_password)
    submitButton.place(x=720,y=450)
    
    window.mainloop()

def login_user():
    if usernameEntry.get()=='' or passwordEntry.get()=='':
        messagebox.showerror('Error','All Fields Are Required')
        
    else:
        try:
            con=sqlite3.connect('userdata.db')
            mycursor=con.cursor()
            
        except:
            messagebox.showerror('Error','Connection is not established try again')
            return
        
        
        
        query='SELECT * FROM data WHERE username=? and password=?'
        mycursor.execute(query,(usernameEntry.get(),passwordEntry.get()))
        row=mycursor.fetchone()
        
        if row is None:
            messagebox.showerror('Error','Invalid Username OR Password')
            
        else:
            messagebox.showinfo('Welcome','Login is Sucessful')
            con.close()
        
            login_window.destroy()
            import main_final
            
def signup_page():
    login_window.destroy()
    import signup

def hide():
    openeye.config(file='closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)
    
def show():
    openeye.config(file='openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)
    
def user_enter(event):
    if usernameEntry.get()=='Username':
        usernameEntry.delete(0,END)
        
def password_enter(event):
    if passwordEntry.get()=='Password':
        passwordEntry.delete(0,END)
    

#GUI Part
login_window=Tk()
login_window.geometry('990x660+50+50')
login_window.resizable(0,0)
login_window.title('Login Page')

bgImage=ImageTk.PhotoImage(file='user.jpg')
bgLabel=Label(login_window,image=bgImage)
# bgLabel.grid(row=0,column=0)
bgLabel.place(x=0,y=0)

heading=Label(login_window,text='USER LOGIN',font=('Microsoft Yahie UI Light',15,'bold'),bg='white',fg='SpringGreen4')
heading.place(x=690,y=190)

usernameEntry=Entry(login_window,width=25,font=('Microsoft Yahie UI Light',10,'bold'),bd=0,fg='firebrick1')
usernameEntry.place(x=630,y=240)
usernameEntry.insert(0,'Username')

usernameEntry.bind('<FocusIn>',user_enter )

frame1=Frame(login_window,width=230,height=2,bg='SpringGreen4')
frame1.place(x=630,y=260) 

passwordEntry=Entry(login_window,width=25,font=('Microsoft Yahie UI Light',10,'bold'),bd=0,fg='firebrick1')
passwordEntry.place(x=630,y=280)
passwordEntry.insert(0,'Password')

passwordEntry.bind('<FocusIn>',password_enter )

frame2=Frame(login_window,width=230,height=2,bg='SpringGreen4')
frame2.place(x=630,y=300) 

openeye=PhotoImage(file='openeye.png')
eyeButton=Button(login_window,image=openeye,bd=0,bg='white',activebackground='white',cursor='hand2',command=hide)
eyeButton.place(x=830,y=270)

forgetButton = Button(login_window, text='Forget password?', bd=0, bg='white', activebackground='white', cursor='hand2',font=('Microsoft Yahie UI Light',10,'bold'),fg='firebrick1',activeforeground='SpringGreen4',command=forget_pass)
forgetButton.place(x=750, y=310)

loginButton=Button(login_window,text='Login',font=('Open Sans',16,'bold'),fg='white',bg='SpringGreen4',activeforeground='white',activebackground='SpringGreen4',cursor='hand2',bd=0,width=18,command=login_user)
loginButton.place(x=630,y=350)

orlabel=Label(login_window,text='--------------------------OR----------------------------',font=('Open Sans',10),fg='firebrick1',bg='white')
orlabel.place(x=630,y=390)

facebook_logo=PhotoImage(file='facebook.png')
fblable=Label(login_window,image=facebook_logo,bg='white')
fblable.place(x=660,y=410)

google_logo=PhotoImage(file='google.png')
fblable=Label(login_window,image=google_logo,bg='white')
fblable.place(x=730,y=410)

twitter_logo=PhotoImage(file='twitter.png')
fblable=Label(login_window,image=twitter_logo,bg='white')
fblable.place(x=800,y=410)

signuplabel=Label(login_window,text="Don't have an account?",bd=0,font=('Open Sans',10,'bold'),fg='firebrick1',bg='white')
signuplabel.place(x=630,y=450)

newaccountButton=Button(login_window,text='Create new one',font=('Open Sans',9,'bold underline'),fg='blue',bg='white',activeforeground='SpringGreen4',activebackground='white',cursor='hand2',bd=0,command=signup_page)
newaccountButton.place(x=780,y=450)


login_window.mainloop() 