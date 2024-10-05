from tkinter import*
from tkinter import messagebox
from PIL import ImageTk
import sqlite3

def clear():
    emailEntry.delete(0,END)
    usernameEntry.delete(0,END)
    passwordEntry.delete(0,END)
    confirmEntry.delete(0,END)
    check.set(0)

def connect_database():
    if emailEntry.get()=='' or usernameEntry.get()=='' or passwordEntry.get()=='' or confirmEntry.get()=='':
        messagebox.showerror('Error','All Fields Are Required')
        
    elif passwordEntry.get()!=confirmEntry.get(): 
        messagebox.showerror('Error','Password Mismatch')
        
    elif check.get()==0:
        messagebox.showerror('Error','Please Accept Term & Conditions')
        
    else:
        try:
            con=sqlite3.connect('userdata.db')
            mycursor=con.cursor()
            
            query = 'CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY AUTOINCREMENT, email VARCHAR(50), username VARCHAR(100), password VARCHAR(20))'
            mycursor.execute(query)
            
            
            query='SELECT * FROM data WHERE username=?'
            mycursor.execute(query,(usernameEntry.get(),))
            row=mycursor.fetchone()
        
            if row is not None:
                messagebox.showerror('Error','Username Already Exists')
                
            else:
                query='INSERT INTO data(email,username,password)values(?,?,?)'
                mycursor.execute(query,(emailEntry.get(),usernameEntry.get(),passwordEntry.get()))
                
                con.commit()
                con.close()
                
                messagebox.showinfo('Success', 'Registration is Successfully')
                
                clear()   
                
                signup_window.destroy()
                import signin
            
        except:
            messagebox.showerror('Error','Database Connectivity Issue, Please Try Again')
            return
          

def login_page():
    signup_window.destroy()
    import signin

signup_window=Tk()
signup_window.title('Signup Page')
signup_window.resizable(False,False)

background=ImageTk.PhotoImage(file='create.jpg')

bgLabel=Label(signup_window,image=background)
bgLabel.grid()

#frame=Frame(signup_window,width=50,height=20,bg='red')
frame=Frame(signup_window,bg='white')
frame.place(x=683,y=68)

heading=Label(frame,text='CREATE AN ACCOUNT',font=('Microsoft Yahie UI Light',19,'bold underline'),bg='white',fg='SpringGreen4')
heading.grid(row=0,column=0,padx=23,pady=10)

emailLable=Label(frame,text='Email',font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
emailLable.grid(row=1,column=0,sticky='w',padx=23,pady=(10,0))

emailEntry=Entry(frame,width=33,font=('Microsoft Yahei UI Light',10,'bold'),fg='black',bg='SpringGreen4')
emailEntry.grid(row=2,column=0,sticky='w',padx=23)

usernameLable=Label(frame,text='Username',font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
usernameLable.grid(row=3,column=0,sticky='w',padx=23,pady=(10,0))

usernameEntry=Entry(frame,width=33,font=('Microsoft Yahei UI Light',10,'bold'),fg='black',bg='SpringGreen4')
usernameEntry.grid(row=4,column=0,sticky='w',padx=23)

passwordLable=Label(frame,text='Password',font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
passwordLable.grid(row=5,column=0,sticky='w',padx=23,pady=(10,0))

passwordEntry=Entry(frame,width=33,font=('Microsoft Yahei UI Light',10,'bold'),fg='black',bg='SpringGreen4')
passwordEntry.grid(row=6,column=0,sticky='w',padx=23)

confirmLable=Label(frame,text='Confirm Password',font=('Microsoft Yahei UI Light',10,'bold'),bg='white',fg='firebrick1')
confirmLable.grid(row=7,column=0,sticky='w',padx=23,pady=(10,0))

confirmEntry=Entry(frame,width=33,font=('Microsoft Yahei UI Light',10,'bold'),fg='black',bg='SpringGreen4')
confirmEntry.grid(row=8,column=0,sticky='w',padx=23)

check=IntVar()
termsandcondition=Checkbutton(frame,text='I agree to the Term & Conditions',font=('Microsoft Yahei UI Light',10,'bold'),fg='firebrick1',bg='white',activebackground='white',activeforeground='SpringGreen4',cursor='hand2',variable=check)
termsandcondition.grid(row=9,column=0,sticky='w',padx=23,pady=30)

signupButton=Button(frame,text='SignUp',font=('Open Sans',19,'bold'),bd=0,cursor='hand2',bg='firebrick1',fg='white',activebackground='white',activeforeground='SpringGreen4',width=15,command=connect_database)
signupButton.grid(row=10,column=0,pady=10)

alreadyaccounts=Label(frame,text="Don't have an account?",font=('Open Sans','12','bold'),bg='white',fg='firebrick1')
alreadyaccounts.grid(row=11,column=0,sticky='w',padx=25,pady=20)

loginButton=Button(frame,text='Log In',font=('Open Sans',12,'bold underline'),bg='white',fg='blue',bd=0,cursor='hand2',activebackground='white',activeforeground='SpringGreen4',command=login_page)
loginButton.place(x=220,y=466)

signup_window.mainloop()