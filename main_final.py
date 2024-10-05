from tkinter import*
import tkinter as tk
from PIL import ImageTk,Image
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from PIL import ImageTk
import customtkinter
import sqlite3
import datetime

# Main window
main_window = tk.Tk()
main_window.geometry("1540x810+0+0")
main_window.resizable(0, 0)
main_window.title('Hospital Management System')

# Background Image
bg_image = ImageTk.PhotoImage(file='main_back_final.jpg')
bg_label = tk.Label(main_window, image=bg_image)
bg_label.place(x=0, y=0)

# Clear entry fields

def clear_fields():
    patient_name_entry.delete(0, tk.END)
    patient_age_entry.delete(0, tk.END)
    patient_id_entry.delete(0, tk.END)
    patient_dob_entry.delete(0, tk.END)
    patient_phno_entry.delete(0, tk.END)
    patient_addr_entry.delete(0, tk.END)
    patient_bloodgroup.set('')#delete(0, tk.END)
    patient_symptoms.set('')#delete(0, tk.END)
    patient_other_entry.delete(0, tk.END)
    doctor_name.set('')#delete(0, tk.END)
    patient_doa_entry.delete(0, tk.END)
    patient_ward.set('')#delete(0, tk.END)
    patient_bed.set('')#delete(0, tk.END)
    patient_status.set('')


# Database connection

def connect_database():
    # Retrieve data from entry fields
    name = patient_name_entry.get()
    age = patient_age_entry.get()
    patient_id = patient_id_entry.get()
    dob = patient_dob_entry.get()
    phno = patient_phno_entry.get()
    address = patient_addr_entry.get()
    
    blood = patient_bloodgroup.get()
    symptoms = patient_symptoms.get()
    other = patient_other_entry.get()
    doctor = doctor_name.get()
    doa = patient_doa_entry.get()
    ward = patient_ward.get()
    bed = patient_bed.get()
    status = patient_status.get()


    #spc=['~','`','!','@','#','$','%','^','&','*','(',')','+','-','=','"',',','<','>',';']
    # spc="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
    # spc=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T'
    #      ,'U','V','W','X','Y','Z',]

    chek_bed=['','G1','G2','G3','G4','G5','G6','G7','G8','G9','P1','P2','P3','P4','I1','I2','I3','CC1','CC2','N1','N2','E1','E2','E3','E4','G10','G11','G12','G13','G14']
    # Check if all fields are filled
    if '' in (name, age, patient_id, dob, phno, address, blood, symptoms, other, doctor, doa, ward, bed, status):
        messagebox.showerror('Error', 'All Fields Are Required')
        return
    
    #Check Name
    elif not name.isalpha():
        messagebox.showerror('Error', 'Name should contain only alphabetic characters')
        return
    
    # elif name not in spc:
    #     messagebox.showerror('Error', 'Name should contain only alphabetic characters')
    #     return
    
    
    
    #Check age
    elif not age.isdigit() or int(age) <= 0 or int(age) > 100:
        messagebox.showerror('Error', 'Invalid Age')
        return

    #Check phono is digit or not or more than 10 digit
    elif len(phno) != 10 or not phno.isdigit():
        messagebox.showerror('Error', 'Invalid Phone Number')
        return
    
    #Check ward_bed
    elif bed not in chek_bed:
        messagebox.showerror('Error', 'Invalid Bed')
        return
    
    else:
        try:
            # Connect to the database
            con = sqlite3.connect('admit.db')
            mycursor = con.cursor()

            # Create table if not exists
            mycursor.execute('''CREATE TABLE IF NOT EXISTS patients(
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            name TEXT, 
                            age INTEGER, 
                            patient_id TEXT, 
                            dob DATE,
                            phno INTEGER,
                            address TEXT,
                            blood TEXT,
                            symptoms TEXT,
                            other TEXT,
                            doctor TEXT,
                            doa DATE,
                            ward TEXT,
                            bed TEXT,
                            status TEXT
                            )''')

            # Check if patient exists
            mycursor.execute('SELECT * FROM patients WHERE patient_id=?', (patient_id,))
            row = mycursor.fetchone()

            if row is not None:
                messagebox.showerror('Error', 'Patient Already Exists')
                
            else:
                # Check if bed is already assigned
                mycursor.execute('SELECT * FROM patients WHERE bed=?', (bed,))
                assigned_bed = mycursor.fetchone()
                if assigned_bed:
                    messagebox.showerror('Error', 'Bed Already Assigned to Another Patient')
                else:
                    # Insert patient data into the table
                    mycursor.execute('INSERT INTO patients(name, age, patient_id, dob, phno, address,  blood, symptoms, other, doctor, doa, ward, bed, status) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                    (name, age, patient_id, dob, phno, address, blood, symptoms, other, doctor, doa, ward, bed, status))
                    con.commit()
                    con.close()
                    messagebox.showinfo('Success', 'Patient Details saved Successfully')
                    clear_fields()
        
        except :
            messagebox.showerror('Error','Database Error')

   

# Function to admit a patient

def admit_patient():
    def admit_detail():
        admit_window = tk.Toplevel()
        admit_window.geometry("1280x880+0+0")
        admit_window.title('ADMIT PATIENT')
        admit_window.resizable(0, 0)

        # Background Image
        bg_image = ImageTk.PhotoImage(file='admit2.jpg')
        bg_label = tk.Label(admit_window, image=bg_image)
        bg_label.image = bg_image
        bg_label.grid()
        
     
        
        bg_image = ImageTk.PhotoImage(file='logo_hm.jpg')
        bg_label = tk.Label(admit_window, image=bg_image,)
        bg_label.image = bg_image
        #bg_label.grid()
        bg_label.place(x=550,y=100)

        # Patient Details Label
        tk.Label(admit_window, text='PATIENT DETAILS', font=('Arial', 20, 'bold'), bg='#d5eef6', fg='SpringGreen4').place(x=520, y=20)
        tk.Frame(admit_window, width=320, height=2, bg='springgreen4').place(x=490, y=50)

        # Patient Name
        tk.Label(admit_window, text='Patient Name:', font=('Arial', 15, 'bold'), bg='#d5eef6', fg='blue').place(x=40, y=70)
        global patient_name_entry
        patient_name_entry = tk.Entry(admit_window, width=30, fg='black', bg='#d5eef6', font=('Arial', 15, 'bold'), bd=0)
        patient_name_entry.place(x=40, y=93)
        tk.Frame(admit_window, width=352, height=2, bg='blue').place(x=40, y=120)

        # Patient Age
        tk.Label(admit_window, text='Patient Age:', font=('Arial', 15, 'bold'), bg='#d5eef6', fg='blue').place(x=40, y=165)
        global patient_age_entry
        patient_age_entry = tk.Entry(admit_window, width=30, fg='black', bg='#d5eef6', font=('Arial', 15, 'bold'), bd=0)
        patient_age_entry.place(x=40, y=193)
        tk.Frame(admit_window, width=352, height=2, bg='blue').place(x=40, y=220)

        # Patient ID
        tk.Label(admit_window, text='Patient ID:', font=('Arial', 15, 'bold'), bg='#d5eef6', fg='blue').place(x=40, y=265)
        global patient_id_entry
        patient_id_entry = tk.Entry(admit_window, width=30, fg='black', bg='#d5eef6', font=('Arial', 15, 'bold'), bd=0)
        patient_id_entry.place(x=40, y=293)
        tk.Frame(admit_window, width=352, height=2, bg='blue').place(x=40, y=320)

        # Patient DOB
        tk.Label(admit_window, text='Patient DOB:', font=('Arial', 15, 'bold'), bg='#d5eef6', fg='blue', cursor='hand2').place(x=40, y=365)
        global patient_dob_entry
        current_date = datetime.datetime.now().date()
        patient_dob_entry = DateEntry(admit_window, width=30, bg='#d5eef6', font=('Arial', 15, 'bold'), bd=0)
        patient_dob_entry.set_date(current_date)
        patient_dob_entry.place(x=40, y=393)
        tk.Frame(admit_window, width=352, height=2, bg='blue').place(x=40, y=422)

        #Patient Phno.
        tk.Label(admit_window, text='Patient Phone No:', font=('Arial', 15, 'bold'), bg='#d5eef6', fg='blue').place(x=40, y=465)
        global patient_phno_entry
        patient_phno_entry = tk.Entry(admit_window, width=30, fg='black', bg='#d5eef6', font=('Arial', 15, 'bold'), bd=0)
        patient_phno_entry.place(x=40, y=493)
        tk.Frame(admit_window, width=352, height=2, bg='blue').place(x=40, y=520)


        # Patient Address
        tk.Label(admit_window, text='Patient Address:', font=('Arial', 15, 'bold'), bg='#d5eef6', fg='blue').place(x=40, y=565)
        global patient_addr_entry
        patient_addr_entry = tk.Entry(admit_window, width=30, fg='black', bg='#d5eef6', font=('Arial', 15, 'bold'), bd=0)
        patient_addr_entry.place(x=40, y=593)
        tk.Frame(admit_window, width=352, height=2, bg='blue').place(x=40, y=620)
        

        #Patient Status
        global patient_status
        tk.Label(admit_window, text='Patient Status:', font=('Arial', 15, 'bold'), bg='#d5eef6', fg='blue', cursor='hand2').place(x=40, y=665)
        patient_status=ttk.Combobox(admit_window,state='readonly',font=('Arial', 15, 'bold'),width=30)
        patient_status['value']=('',"Admit")
        patient_status.current(0)
        patient_status.place(x=40,y=693)
        tk.Frame(admit_window, width=352, height=2, bg='blue').place(x=40, y=720)


        #Patient Blood Group
        global patient_bloodgroup
        tk.Label(admit_window, text='Patient Blood Group:', font=('Arial', 15, 'bold'), bg='#d5eef6', fg='blue', cursor='hand2').place(x=920, y=62)
        patient_bloodgroup=ttk.Combobox(admit_window,state='readonly',font=('Arial', 15, 'bold'),width=30)
        patient_bloodgroup['value']=('',"A+","A-","B+","B-","O+","O-","AB+","AB-")
        patient_bloodgroup.current(0)
        patient_bloodgroup.place(x=920,y=91)
        tk.Frame(admit_window, width=352, height=2, bg='blue').place(x=920, y=120)
        
        
        #Patient Symptoms
        global patient_symptoms
        tk.Label(admit_window, text='Patient Symptoms:', font=('Arial', 15, 'bold'), bg='#d5eef6', fg='blue', cursor='hand2').place(x=920, y=162)
        patient_symptoms=ttk.Combobox(admit_window,state='readonly',font=('Arial', 15, 'bold'),width=30)
        patient_symptoms['value']=('',"Memory disturbances","Taste or smell disturbances","Chest Pain","Shortness of Breath","Fatigue","Fast or Uneven Heartbeat","Skin Hives and Redness","Nausea or Vomiting","Itchy Eyes","Feeling or Being Sick","Headaches","Aches and Pains","Frequent Infections","Night Sweats","Unexplained Weight Loss","Pregnancy","Unexplained Bleeding or Bruising","Unexplained Pain or Ache","Unusual Lump or Swelling anywhere","Decrease in Vision","Eye Pain or Redness","Dryness or Excessive Tearing","Trouble Waking your Child","Sharp or Constant Belly Pain","Burning when your Child Pees","Blood in their Urine","Digestive Issues","Chronic Fatigue","Persistent Pain","Fever")
        patient_symptoms.current(0)
        patient_symptoms.place(x=920,y=191)
        tk.Frame(admit_window, width=352, height=2, bg='blue').place(x=920, y=220)
        
        # Patient Other Info
        global patient_other_entry
        tk.Label(admit_window, text='Other:', font=('Arial', 15, 'bold'), bg='#d5eef6', fg='blue').place(x=920, y=262)
        patient_other_entry = tk.Entry(admit_window, width=30, fg='black', bg='#d5eef6', font=('Arial', 15, 'bold'), bd=0)
        patient_other_entry.place(x=920, y=291)
        tk.Frame(admit_window, width=352, height=2, bg='blue').place(x=920, y=320)
        
        #Doctor Name
        global doctor_name
        tk.Label(admit_window, text='Doctor Name:', font=('Arial', 15, 'bold'), bg='#d5eef6', fg='blue', cursor='hand2').place(x=920, y=362)
        doctor_name=ttk.Combobox(admit_window,state='readonly',font=('Arial', 15, 'bold'),width=30)
        doctor_name['value']=('',"DR. NITISH KUMAR","DR. VIKAS SINGH","DR. SHARAD JAIN","DR. ANJALI SINGH","DR. MUNNA BHAI","DR. VEENA BHATT","DR. K S GOPINATH","DR. ARJUN KUMAR SINGH","DR. ASHIT KUMAR","DR. SHIV ANKAR")
        doctor_name.current(0)
        doctor_name.place(x=920,y=391)
        tk.Frame(admit_window, width=352, height=2, bg='blue').place(x=920, y=420)
        
        # Patient Date of admit
        global patient_doa_entry
        tk.Label(admit_window, text='Patient Date of Admit:', font=('Arial', 15, 'bold'), bg='#d5eef6', fg='blue', cursor='hand2').place(x=920, y=465)
        current_date = datetime.datetime.now().date()
        patient_doa_entry = DateEntry(admit_window, width=30, bg='#d5eef6', font=('Arial', 15, 'bold'), bd=0)
        patient_doa_entry.set_date(current_date)
        patient_doa_entry.place(x=920, y=493)
        tk.Frame(admit_window, width=352, height=2, bg='blue').place(x=920, y=522)
        
        #Patient Ward
        global patient_ward
        tk.Label(admit_window, text='Patient Ward Type:', font=('Arial', 15, 'bold'), bg='#d5eef6', fg='blue', cursor='hand2').place(x=920, y=565)
        patient_ward=ttk.Combobox(admit_window,state='readonly',font=('Arial', 15, 'bold'),width=30)
        patient_ward['value']=('',"General Ward","Private Cabin","I.C.U","I.C.C.U","N.I.C.U","Emergengy Ward")
        patient_ward.current(0)
        patient_ward.place(x=920,y=593)
        tk.Frame(admit_window, width=352, height=2, bg='blue').place(x=920, y=622)
        
        #Patient Bed No.
        global patient_bed
        tk.Label(admit_window, text='Patient Bed No.:', font=('Arial', 15, 'bold'), bg='#d5eef6', fg='blue', cursor='hand2').place(x=920, y=665)
        patient_bed=ttk.Combobox(admit_window,state='write',font=('Arial', 15, 'bold'),width=30)
        patient_bed['value']=('','G1','G2','G3','G4','G5','G6','G7','G8','G9','P1','P2','P3','P4','I1','I2','I3','CC1','CC2','N1','N2','E1','E2','E3','E4','G10','G11','G12','G13','G14')
        patient_bed.current(0)
        patient_bed.place(x=920,y=693)
        tk.Frame(admit_window, width=352, height=2, bg='blue').place(x=920, y=722)




        # Save Button
        tk.Button(admit_window, text='ADMIT', font=('Open Sans', 19, 'bold'), bd=0, cursor='hand2', bg='firebrick1',
                  fg='white', activebackground='white', activeforeground='SpringGreen4', width=15,
                  command=connect_database).place(x=550, y=750)
        admit_window.grab_set()
        
        

   

    # admit_frame=Frame(main_window,bg='#DEEDF4')
    # admit_frame.place(x=125,y=400)
    # button=customtkinter.CTkButton(admit_frame,text="ADMIT PATIENT",height=80,width=200,corner_radius=30,font=('Helvetica',34),cursor='hand2',fg_color='medium sea green',command=admit_detail)
    # button.grid(row=1,column=0)
    
    #ADMIT PATIENT BUTTON
    admit_frame=Frame(main_window,bg='#DEEDF4')
    admit_frame.place(x=125,y=400)
    pic1=customtkinter.CTkImage(Image.open('buttonAdmitPatient.png'),size=(165,165))
    button=customtkinter.CTkButton(admit_frame,text='',image=pic1,cursor='hand2',command=admit_detail,corner_radius=100,hover_color='navy blue',fg_color='#DEEDF4',bg_color='#DEEDF4')
    admit_frame.image=pic1
    button.grid(row=1,column=0)
    
    
# Discharge Patient Button


def discharge_patient():
    
    def discharge():
        #Create Window
        discharge_window = tk.Toplevel()
        discharge_window.geometry("900x728+50+50")
        discharge_window.title('DISCHARGE PATIENT')
        discharge_window.resizable(0, 0)
        
        #Background Image
        bg_image = ImageTk.PhotoImage(file='charge.jpg')
        bg_label = tk.Label(discharge_window, image=bg_image)
        bg_label.image = bg_image
        bg_label.grid()
        
        #Entry Point
        tk.Label(discharge_window, text='Patient ID:', font=('Arial', 15, 'bold'),bg='#fed1df').place(x=50, y=80)
        patient_id_entry = tk.Entry(discharge_window, width=10, font=('Arial', 15, 'bold'),bg='#fed1df',bd=0,fg='black',background='#fed1df')
        patient_id_entry.place(x=170, y=80)
        tk.Frame(discharge_window, width=100, height=2, bg='black').place(x=170, y=108)
    
           
        # Patient Date of Discharge
        global patient_dod
        tk.Label(discharge_window, text='Date of Discharge:', font=('Arial', 15, 'bold'), bg='#fed1df').place(x=50, y=140)
        current_date = datetime.datetime.now().date()
        patient_dod = DateEntry(discharge_window, width=7, bg='#fed1df', font=('Arial', 15, 'bold'),cursor='hand2', bd=0)
        patient_dod.set_date(current_date)
        patient_dod.place(x=240, y=140)
        tk.Frame(discharge_window, width=100, height=2, bg='black').place(x=240, y=168)

        #Entry Point
        tk.Label(discharge_window, text='Patient Name:', font=('Arial', 15, 'bold'),bg='#fed1df').place(x=500, y=80)
        patient_name_entry = tk.Entry(discharge_window, width=15, font=('Arial', 15, 'bold'),bg='#fed1df',bd=0,fg='black',background='#fed1df')
        patient_name_entry.place(x=650, y=80)
        tk.Frame(discharge_window, width=130, height=2, bg='black').place(x=650, y=108)
        
        #Entry Point
        tk.Label(discharge_window, text='Patient No:', font=('Arial', 15, 'bold'),bg='#fed1df').place(x=500, y=140)
        patient_no_entry = tk.Entry(discharge_window, width=15, font=('Arial', 15, 'bold'),bg='#fed1df',bd=0,fg='black',background='#fed1df')
        patient_no_entry.place(x=620, y=140)
        tk.Frame(discharge_window, width=130, height=2, bg='black').place(x=620, y=168)
        
        #Update DataBase 
        def discharge_from_database():
            patient_id = patient_id_entry.get()
            dod = patient_dod.get()
            name1 = patient_name_entry.get()
            num = patient_no_entry.get()

            #Check Empty Field
            if patient_id == '' or name1=='':
                messagebox.showerror('Error', 'All Fields Are Required')
                return
            
            #Check Name
            elif not name1.isalpha():
                messagebox.showerror('Error', 'Name should contain only alphabetic characters')
                return
            
                #Check phono is digit or not or more than 10 digit
            elif len(num) != 10 or not num.isdigit():
                messagebox.showerror('Error', 'Invalid Phone Number')
                return

            else:
                try:
                    # Connect to the admit.db database
                    con_admit = sqlite3.connect('admit.db')
                    mycursor_admit = con_admit.cursor()

                    mycursor_admit.execute('SELECT * FROM patients WHERE patient_id=?', (patient_id,))
                    patient_data = mycursor_admit.fetchone()
                    
                    

                    if patient_data:
                        # Update status, patient ID, and bed in admit.db
                        mycursor_admit.execute('UPDATE patients SET status=? WHERE patient_id=?', ('Discharge', patient_id))
                        mycursor_admit.execute('UPDATE patients SET patient_id=? WHERE patient_id=?', ('', patient_id))
                        mycursor_admit.execute('UPDATE patients SET bed=? WHERE bed=?', ('', patient_data[13]))
                        con_admit.commit()
                        con_admit.close()
                        
                        
                        

                        # Connect to the discharge.db database
                        con_discharge = sqlite3.connect('discharge.db')
                        mycursor_discharge = con_discharge.cursor()

                        # Create table if not exists
                        mycursor_discharge.execute('''CREATE TABLE IF NOT EXISTS discharge(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,  
                            patient_id TEXT, 
                            dod DATE,
                            name1 TEXT,
                            num INTEGER
                            )''')

                        # Insert patient data into the discharge table
                        mycursor_discharge.execute('INSERT INTO discharge(patient_id, dod, name1, num) VALUES(?, ?, ? ,?)', (patient_id, dod, name1, num))
                        con_discharge.commit()
                        con_discharge.close()

                        messagebox.showwarning('Warning', 'Discharging Patient')
                        clear_fields()

                    else:
                        messagebox.showerror('Error', 'Patient ID not found')
                        

                except :
                    messagebox.showinfo('Success', 'Patient Discharged')

                patient_id_entry.delete(0, 'end')

            
        #Heading Discharge Information
        heading_label=Label(discharge_window,text='DISCHARGE PATIENT',font=('arial',18,'bold underline'),bg='#fed1df',fg='red')
        heading_label.place(x=320,y=20)

        #Create Discharge Button
    
        discharge_button = tk.Button(discharge_window, text="Discharge", font=('Arial', 15, 'bold'), bg='red',fg='white',bd=0, activebackground='red',cursor='hand2',command=discharge_from_database)
        discharge_button.place(x=380, y=200)
        
    
    #Dischare Button In Main Window
    # discharge_frame=Frame(main_window,bg='#DEEDF4')
    # discharge_frame.place(x=600,y=400)
    # button=customtkinter.CTkButton(discharge_frame,text="DISCHARGE",height=80,width=200,corner_radius=30,font=('Helvetica',34),cursor='hand2',fg_color='medium sea green',command=discharge)
    # button.grid(row=1,column=2)
    
    discharge_frame=Frame(main_window,bg='#DEEDF4')
    discharge_frame.place(x=600,y=400)
    pic1=customtkinter.CTkImage(Image.open('buttonDischarge.png'),size=(165,165))
    button=customtkinter.CTkButton(discharge_frame,text='',image=pic1,cursor='hand2',corner_radius=100,hover_color='navy blue',fg_color='#DEEDF4',bg_color='#DEEDF4',command=discharge)
    discharge_frame.image=pic1
    button.grid(row=1,column=2)


# Nurse Details Button

def nurse_detail():
    
    #def nurse_detail():
    def nurse_login():
        window=Toplevel()
        window.geometry("1280x800+0+0")
        window.title('NURSE INFORMATION')

        #Background Image
        bg_image = ImageTk.PhotoImage(file='detail.jpg')
        bg_label = tk.Label(window, image=bg_image)
        bg_label.image = bg_image
        bg_label.grid()

        def reshmi():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Ms. RESHMI DETAILS')
            bgImage=ImageTk.PhotoImage(file='BGnurse.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #label for nurse info
            data=Label(window,bg='white')
            data.place(x=55,y=240)
            
            designation=Label(data,text="Name: Ms. RESHMI JAIN\nDesignation: BSc in NURSING\nNURSE ID: TCHNUR123",font=('Courier New',24),borderwidth=0,bg='white')
            designation.grid(row=0,column=0)


        def sumitra():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Ms. SUMITRA DETAILS')
            bgImage=ImageTk.PhotoImage(file='BGnurse.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #label for nurse info
            data=Label(window,bg='white')
            data.place(x=55,y=240)
            
            designation=Label(data,text="Name: Ms. SUMITRA KUMARI\nDesignation: MSc in NURSING\nNURSE ID: TCHNUR345",font=('Courier New',24),borderwidth=0,bg='white')
            designation.grid(row=0,column=0)


        def naina():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Ms. NAINA DETAILS')
            bgImage=ImageTk.PhotoImage(file='BGnurse.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #label for nurse info
            data=Label(window,bg='white')
            data.place(x=55,y=240)
            
            designation=Label(data,text="Name: Ms. NAINA MATHUR\nDesignation: BSc in NURSING\nNURSE ID: TCHNUR167",font=('Courier New',24),borderwidth=0,bg='white')
            designation.grid(row=0,column=0)


        def priti():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Ms. PRITI DETAILS')
            bgImage=ImageTk.PhotoImage(file='BGnurse.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #label for nurse info
            data=Label(window,bg='white')
            data.place(x=55,y=240)
            
            designation=Label(data,text="Name: Ms. PRITI AGARWAL\nDesignation: BSc in NURSING\nNURSE ID: TCHNUR987",font=('Courier New',24),borderwidth=0,bg='white')
            designation.grid(row=0,column=0)

        def harshita():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Ms.HARSHITA DETAILS')
            bgImage=ImageTk.PhotoImage(file='BGnurse.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #label for nurse info
            data=Label(window,bg='white')
            data.place(x=55,y=240)
            
            designation=Label(data,text="Name: Ms. HARSHITA AGARWAL\nDesignation: BSc in NURSING\nNURSE ID: TCHNUR098",font=('Courier New',24),borderwidth=0,bg='white')
            designation.grid(row=0,column=0)

        def archana():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Ms.ARCHANA DETAILS')
            bgImage=ImageTk.PhotoImage(file='BGnurse.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #label for nurse info
            data=Label(window,bg='white')
            data.place(x=55,y=240)
            
            designation=Label(data,text="Name: Ms. ARCHANA SINGH\nDesignation: MSc in NURSING\nNURSE ID: TCHNUR056",font=('Courier New',24),borderwidth=0,bg='white')
            designation.grid(row=0,column=0)

        def aditi():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Ms.ADITI DETAILS')
            bgImage=ImageTk.PhotoImage(file='BGnurse.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #label for nurse info
            data=Label(window,bg='white')
            data.place(x=55,y=240)
            
            designation=Label(data,text="Name: Ms. ADITI SEN\nDesignation: BSc in NURSING\nNURSE ID: TCHNUR133",font=('Courier New',24),borderwidth=0,bg='white')
            designation.grid(row=0,column=0)

        def rashi():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Ms.RASHI DETAILS')
            bgImage=ImageTk.PhotoImage(file='BGnurse.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #label for nurse info
            data=Label(window,bg='white')
            data.place(x=55,y=240)
            
            designation=Label(data,text="Name: Ms. RASHI KHANNA\nDesignation: MSc in NURSING\nNURSE ID: TCHNUR134",font=('Courier New',24),borderwidth=0,bg='white')
            designation.grid(row=0,column=0)

        def kriti():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Ms.KRITI DETAILS')
            bgImage=ImageTk.PhotoImage(file='BGnurse.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #label for nurse info
            data=Label(window,bg='white')
            data.place(x=55,y=240)
            
            designation=Label(data,text="Name: Ms. KRITI SINGH\nDesignation: BSc in NURSING\nNURSE ID: TCHNUR007",font=('Courier New',24),borderwidth=0,bg='white')
            designation.grid(row=0,column=0)

        def nidhi():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Ms.NIDHI DETAILS')
            bgImage=ImageTk.PhotoImage(file='BGnurse.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #label for nurse info
            data=Label(window,bg='white')
            data.place(x=55,y=240)
            
            designation=Label(data,text="Name: Ms. NIDHI GURGAIN\nDesignation: BSc in NURSING\nNURSE ID: TCHNUR565",font=('Courier New',24),borderwidth=0,bg='white')
            designation.grid(row=0,column=0)
        

        #heading
        head=Label(window,text="NURSE INFORMATION",font=('Courier New',34,'bold underline'),bg='#e8e7e7',fg='firebrick3')
        head.place(x=350,y=35)

        #Nurse image
        bg_image = ImageTk.PhotoImage(file='nurseIcon.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=60,y=150)

        newaccountButton1=Button(window,text='Ms. HARSHITA AGARWAL',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=harshita)
        newaccountButton1.place(x=140,y=150)

        #Nurse image
        bg_image = ImageTk.PhotoImage(file='nurseIcon.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=60,y=250)

        newaccountButton2=Button(window,text='Ms. SUMITRA KUMARI',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=sumitra)
        newaccountButton2.place(x=140,y=250)

        #Nurse image
        bg_image = ImageTk.PhotoImage(file='nurseIcon.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=60,y=350)

        newaccountButton3=Button(window,text='Ms. NAINA MATHUR',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=naina)
        newaccountButton3.place(x=140,y=350)

        #Nurse image
        bg_image = ImageTk.PhotoImage(file='nurseIcon.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=60,y=450)

        newaccountButton4=Button(window,text='Ms. PRITI AGARWAL',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=priti)
        newaccountButton4.place(x=140,y=450)

        #Nurse image
        bg_image = ImageTk.PhotoImage(file='nurseIcon.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=60,y=550)

        newaccountButton5=Button(window,text='Ms. RESHMI JAIN',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=reshmi)
        newaccountButton5.place(x=140,y=550)

        #Nurse image
        bg_image = ImageTk.PhotoImage(file='nurseIcon.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=880,y=150)

        newaccountButton6=Button(window,text='Ms. ARCHANA SINGH',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=archana)
        newaccountButton6.place(x=940,y=150)

        #Nurse image
        bg_image = ImageTk.PhotoImage(file='nurseIcon.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=880,y=250)

        newaccountButton7=Button(window,text='Ms. ADITI SEN',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=aditi)
        newaccountButton7.place(x=940,y=250)

        #Nurse image
        bg_image = ImageTk.PhotoImage(file='nurseIcon.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=880,y=350)

        newaccountButton8=Button(window,text='Ms. RASHI KHANNA',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=rashi)
        newaccountButton8.place(x=940,y=350)

        #Nurse image
        bg_image = ImageTk.PhotoImage(file='nurseIcon.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=880,y=450)

        newaccountButton9=Button(window,text='Ms. KRITI SINGH',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=kriti)
        newaccountButton9.place(x=940,y=450)

        #Nurse image
        bg_image = ImageTk.PhotoImage(file='nurseIcon.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=880,y=550)

        newaccountButton10=Button(window,text='Ms. NIDHI GURGAIN',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=nidhi)
        newaccountButton10.place(x=940,y=550)


    #Nurse Info Button
    # nurse_frame=Frame(main_window,bg='#DEEDF4')
    # nurse_frame.place(x=125,y=600)
    # button=customtkinter.CTkButton(nurse_frame,text="NURSE INFO",height=80,width=200,corner_radius=30,font=('Helvetica',34),cursor='hand2',fg_color='medium sea green',command=nurse_login)
    # button.grid(row=0,column=1)
    
    nurse_frame=Frame(main_window,bg='#DEEDF4')
    nurse_frame.place(x=125,y=600)
    pic1=customtkinter.CTkImage(Image.open('button2Nurse.png'),size=(165,165))
    button=customtkinter.CTkButton(nurse_frame,text='',image=pic1,cursor='hand2',command=nurse_login,corner_radius=100,hover_color='navy blue',fg_color='#DEEDF4',bg_color='#DEEDF4')
    nurse_frame.image=pic1
    button.grid(row=0,column=1)
    

# Doctor Details Button

def doctor_detail():
    def doctor_login():
        window=Toplevel()
        window.geometry("1280x800+0+0")
        window.title('DOCTOR INFORMATION')
        window.resizable(0,0)
       
        #Background Image
        bg_image = ImageTk.PhotoImage(file='detail.jpg')
        bg_label = tk.Label(window, image=bg_image)
        bg_label.image = bg_image
        bg_label.grid()
        
        def nitish():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Dr. NITISH DETAILS')
            bgImage=ImageTk.PhotoImage(file='doctor_nurseBg.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #showing enlarged image
            imageLabel=Label(window)
            imageLabel.place(x=650, y=200)
            doctor1=ImageTk.PhotoImage(file='drNitish.jpg')#.resize((480,350))
            #docNitish= ImageTk.PhotoImage(doctor1)
            window.resizable(0,0)
            docLabel = tk.Label(imageLabel, image=doctor1)
            docLabel.image = doctor1#docNitish
            docLabel.grid(row=0,column=1)

            #label for doc info
            data=Label(window,bg='#DEEDF4',background='#aee6fc')
            data.place(x=90,y=240)
            
            designation=Label(data,text="Name: DR. NITISH KUMAR\nDesignation: NEUROLOGIST\nDoctor ID: TCHDOC231\nPhone Number: 9031558214\nAddress: JAMSHEDPUR",font=('Courier New',28),bg='#aee6fc',borderwidth=0)
            designation.grid(row=0,column=0)


        def vikas():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Dr. VIKAS DETAILS')
            bgImage=ImageTk.PhotoImage(file='doctor_nurseBg.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #showing enlarged image
            imageLabel=Label(window)
            imageLabel.place(x=650, y=200)
            doctor1=ImageTk.PhotoImage(file='drVikas.jpg')#.resize((480,350))
            #docVikas= ImageTk.PhotoImage(doctor1)
            window.resizable(0,0)
            docLabel = tk.Label(imageLabel, image=doctor1)
            docLabel.image = doctor1
            docLabel.grid(row=0,column=1)
            
            #label for doc info
            data=Label(window,bg='#DEEDF4',background='#aee6fc')
            data.place(x=75,y=240)
            
            designation=Label(data,text="Name: Dr. VIKAS SINGH\nDesignation: CARDIOLOGIST\nDoctor ID: TCHDOC432\nPhone Number: 9031558214\nAddress: JAMSHEDPUR",font=('Courier New',28),bg='#aee6fc')
            designation.grid(row=0,column=0)
            
        def sharad():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Dr. SHARAD DETAILS')
            bgImage=ImageTk.PhotoImage(file='doctor_nurseBg.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #showing enlarged image
            imageLabel=Label(window)
            imageLabel.place(x=650, y=200)
            doctor1=ImageTk.PhotoImage(file='drSharad.jpg')#.resize((480,350))
            #doc= ImageTk.PhotoImage(doctor1)
            window.resizable(0,0)
            docLabel = tk.Label(imageLabel, image=doctor1)
            docLabel.image = doctor1
            docLabel.grid(row=0,column=1)
            
            #label for doc info
            data=Label(window,bg='#DEEDF4',background='#aee6fc')
            data.place(x=75,y=240)
            
            designation=Label(data,text="Name: Dr. SHARAD JAIN\nDesignation: IMMUNOLOGIST\nDoctor ID: TCHDOC546\nPhone Number: 9031558214\nAddress: JAMSHEDPUR",font=('Courier New',28),bg='#aee6fc')
            designation.grid(row=0,column=0)

        def anjali():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Dr. ANJALI DETAILS')
            bgImage=ImageTk.PhotoImage(file='doctor_nurseBg.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #showing enlarged image
            imageLabel=Label(window)
            imageLabel.place(x=720, y=200)
            doctor1=ImageTk.PhotoImage(file='drAnjali.jpg')#.resize((480,350))
            #doc= ImageTk.PhotoImage(doctor1)
            window.resizable(0,0)
            docLabel = tk.Label(imageLabel, image=doctor1)
            docLabel.image = doctor1
            docLabel.grid(row=0,column=1)
            
            #label for doc info
            data=Label(window,bg='#DEEDF4',background='#aee6fc')
            data.place(x=70,y=240)
            
            designation=Label(data,text="Name: Dr. ANJALI SINGH\nDesignation: ANESTHESIOLOGIST\nDoctor ID: TCHDOC343\nPhone Number: 9031558214\nAddress: JAMSHEDPUR",font=('Courier New',28),bg='#aee6fc')
            designation.grid(row=0,column=0)

        def munna():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Dr. MUNNA DETAILS')
            bgImage=ImageTk.PhotoImage(file='doctor_nurseBg.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #showing enlarged image
            imageLabel=Label(window)
            imageLabel.place(x=650, y=200)
            doctor1=ImageTk.PhotoImage(file='drMunna2.jpg')#.resize((480,350))
            #doc= ImageTk.PhotoImage(doctor1)
            window.resizable(0,0)
            docLabel = tk.Label(imageLabel, image=doctor1)
            docLabel.image = doctor1
            docLabel.grid(row=0,column=1)
            
            #label for doc info
            data=Label(window,bg='#DEEDF4',background='#aee6fc')
            data.place(x=70,y=240)
            
            designation=Label(data,text="Name: Dr. MUNNA BHAI\nDesignation: HEMATOLOGIST\nDoctor ID: TCHDOC556\nPhone Number: 9031558214\nAddress: JAMSHEDPUR",font=('Courier New',28),bg='#aee6fc')
            designation.grid(row=0,column=0)

        def venna():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Dr. VEENA DETAILS')
            bgImage=ImageTk.PhotoImage(file='doctor_nurseBg.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #showing enlarged image
            imageLabel=Label(window)
            imageLabel.place(x=650, y=200)
            doctor1=ImageTk.PhotoImage(file='drVenna.jpg')#.resize((480,350))
            #doc= ImageTk.PhotoImage(doctor1)
            window.resizable(0,0)
            docLabel = tk.Label(imageLabel, image=doctor1)
            docLabel.image = doctor1
            docLabel.grid(row=0,column=1)
            
            #label for doc info
            data=Label(window,bg='#DEEDF4',background='#aee6fc')
            data.place(x=70,y=240)
            
            designation=Label(data,text="Name: Dr. VENNA BHATT\nDesignation: GYNECOLOGIST\nDoctor ID: TCHDOC768\nPhone Number: 9031558214\nAddress: JAMSHEDPUR",font=('Courier New',28),bg='#aee6fc')
            designation.grid(row=0,column=0)

        def salunkhe():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Dr. SALUNKHE DETAILS')
            bgImage=ImageTk.PhotoImage(file='doctor_nurseBg.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #showing enlarged image
            imageLabel=Label(window)
            imageLabel.place(x=750, y=200)
            doctor1=ImageTk.PhotoImage(file='drSalunkhe.jpg')#.resize((480,350))
            #doc= ImageTk.PhotoImage(doctor1)
            window.resizable(0,0)
            docLabel = tk.Label(imageLabel, image=doctor1)
            docLabel.image = doctor1
            docLabel.grid(row=0,column=1)
            
            #label for doc info
            data=Label(window,bg='#DEEDF4',background='#aee6fc')
            data.place(x=70,y=240)
            
            designation=Label(data,text="Name: Dr. R.P.SALUNKHE\nDesignation: FORENSIC EXPERT\nDoctor ID: TCHDOC098\nPhone Number: 9031558214\nAddress: JAMSHEDPUR",font=('Courier New',28),bg='#aee6fc')
            designation.grid(row=0,column=0)

        def arjun():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Dr. ARJUN DETAILS')
            bgImage=ImageTk.PhotoImage(file='doctor_nurseBg.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #showing enlarged image
            imageLabel=Label(window)
            imageLabel.place(x=750, y=200)
            doctor1=ImageTk.PhotoImage(file='drArjun.jpg')#.resize((480,350))
            #doc= ImageTk.PhotoImage(doctor1)
            window.resizable(0,0)
            docLabel = tk.Label(imageLabel, image=doctor1)
            docLabel.image = doctor1
            docLabel.grid(row=0,column=1)
            
            #label for doc info
            data=Label(window,bg='#DEEDF4',background='#aee6fc')
            data.place(x=60,y=240)
            
            designation=Label(data,text="Name: Dr. ARJUN KUMAR SINGH\nDesignation: OPHTHALMOLOGIST\nDoctor ID: TCHDOC254\nPhone Number: 9031558214\nAddress: JAMSHEDPUR",font=('Courier New',28),bg='#aee6fc')
            designation.grid(row=0,column=0)

        def ashit():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Dr. ASHIT DETAILS')
            bgImage=ImageTk.PhotoImage(file='doctor_nurseBg.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #showing enlarged image
            imageLabel=Label(window)
            imageLabel.place(x=750, y=200)
            doctor1=ImageTk.PhotoImage(file='drAshit.jpg')#.resize((370,390))
            #doc= ImageTk.PhotoImage(doctor1)
            window.resizable(0,0)
            docLabel = tk.Label(imageLabel, image=doctor1)
            docLabel.image = doctor1
            docLabel.grid(row=0,column=1)
            
            #label for doc info
            data=Label(window,bg='#DEEDF4',background='#aee6fc')
            data.place(x=70,y=240)
            
            designation=Label(data,text="Name: Dr. ASHIT KUMAR\nDesignation: GENERAL PHYSICIAN\nDoctor ID: TCHDOC2242\nPhone Number: 9031558214\nAddress: JAMSHEDPUR",font=('Courier New',28),bg='#aee6fc')
            designation.grid(row=0,column=0)

        def shiv():
            window=Toplevel()
            window.geometry("1280x800+0+0")
            window.title(' Dr. SHIV DETAILS')
            bgImage=ImageTk.PhotoImage(file='doctor_nurseBg.jpg')

            bgLabel=tk.Label(window,image=bgImage)
            bgLabel.image=bgImage
            bgLabel.grid()

            #showing enlarged image
            imageLabel=Label(window)
            imageLabel.place(x=730, y=200)
            doctor1=ImageTk.PhotoImage(file='drShiv.jpg')#.resize((480,350))
            #doc= ImageTk.PhotoImage(doctor1)
            window.resizable(0,0)
            docLabel = tk.Label(imageLabel, image=doctor1)
            docLabel.image = doctor1
            docLabel.grid(row=0,column=1)
            
            #label for doc info
            data=Label(window,bg='#DEEDF4',background='#aee6fc')
            data.place(x=70,y=240)
            
            designation=Label(data,text="Name: Dr. SHIV ANKAR\nDesignation: PEDIATRICIAN\nDoctor ID: TCHDOC389\nPhone Number: 9031558214\nAddress: JAMSHEDPUR",font=('Courier New',28),bg='#aee6fc')
            designation.grid(row=0,column=0)
        
        #heading
        head=Label(window,text="DOCTOR INFORMATION",font=('Courier New',34,'bold underline'),bg='#e8e7e7',fg='firebrick3')
        head.place(x=350,y=35)

        #Doctor image
        bg_image = ImageTk.PhotoImage(file='photo.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=60,y=150)

        newaccountButton1=Button(window,text='Dr. NITISH',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=nitish)
        newaccountButton1.place(x=140,y=150)

        bg_image = ImageTk.PhotoImage(file='photo.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=60,y=250)

        newaccountButton2=Button(window,text='Dr. VIKAS',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=vikas)
        newaccountButton2.place(x=140,y=250)
        
        bg_image = ImageTk.PhotoImage(file='photo.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=60,y=350)

        newaccountButton3=Button(window,text='Dr. SHARAD',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=sharad)
        newaccountButton3.place(x=140,y=350)

        bg_image = ImageTk.PhotoImage(file='doc_Icon.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=60,y=450)

        newaccountButton4=Button(window,text='Dr. ANJALI',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=anjali)
        newaccountButton4.place(x=140,y=450)

        bg_image = ImageTk.PhotoImage(file='photo.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=60,y=550)

        newaccountButton5=Button(window,text='Dr. MUNNA',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=munna)
        newaccountButton5.place(x=140,y=550)
        
        bg_image = ImageTk.PhotoImage(file='doc_Icon.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=900,y=150)

        newaccountButton6=Button(window,text='Dr. VEENA',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=venna)
        newaccountButton6.place(x=980,y=150)

        bg_image = ImageTk.PhotoImage(file='photo.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=900,y=250)

        newaccountButton7=Button(window,text='Dr. SALUNKHE',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=salunkhe)
        newaccountButton7.place(x=980,y=250)

        bg_image = ImageTk.PhotoImage(file='photo.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=900,y=350)

        newaccountButton8=Button(window,text='Dr. ARJUN',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=arjun)
        newaccountButton8.place(x=980,y=350)

        bg_image = ImageTk.PhotoImage(file='photo.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=900,y=450)

        newaccountButton9=Button(window,text='Dr. ASHIT',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=ashit)
        newaccountButton9.place(x=980,y=450)

        bg_image = ImageTk.PhotoImage(file='photo.jpg')
        bg_label = tk.Label(window, image=bg_image,)
        bg_label.image = bg_image
        bg_label.place(x=900,y=550)

        newaccountButton10=Button(window,text='Dr. SHIV',font=('Helvetica',20,'bold underline'),fg='black',bg='#e8e7e7',activeforeground='#e8e7e7',activebackground='#e8e7e7',cursor='hand2',bd=0,command=shiv)
        newaccountButton10.place(x=980,y=550)
    
    #Doctor Info Button
    # doctor_frame=Frame(main_window,bg='#DEEDF4')
    # doctor_frame.place(x=125,y=200)
    # button=customtkinter.CTkButton(doctor_frame,text="DOCTOR INFO",height=80,width=200,corner_radius=30,font=('Helvetica',34),cursor='hand2',command=doctor_login,fg_color='medium sea green')
    # button.grid(row=0,column=1)    
    
    doctor_frame=Frame(main_window,bg='#DEEDF4')
    doctor_frame.place(x=125,y=200)
    pic1=customtkinter.CTkImage(Image.open('button1Doc.png'),size=(165,165))
    button=customtkinter.CTkButton(doctor_frame,text='',image=pic1,cursor='hand2',command=doctor_login,corner_radius=100,hover_color='navy blue',fg_color='#DEEDF4',bg_color='#DEEDF4')
    doctor_frame.image=pic1
    button.grid(row=0,column=1)
        
        

# Patient Details Button

def patient_detail():

    def patient():
        patient_window = tk.Toplevel()
        patient_window.geometry("700x500+50+50")
        patient_window.title('PATIENT INFORMATION')
        patient_window.resizable(0, 0)
    
        #Background image    
        bg_image = ImageTk.PhotoImage(file='search.jpg')
        bg_label = tk.Label(patient_window, image=bg_image)
        bg_label.image = bg_image
        bg_label.grid()
    
    

        # Patient Info search bar
        global patient_info_entry
        tk.Label(patient_window, text='Patient ID:', font=('Arial', 15, 'bold'), bg='#e8ecf4', fg='blue').place(x=278, y=50)
        patient_info_entry = tk.Entry(patient_window, width=19, fg='black', bg='#e8ecf4', font=('Arial', 20, 'bold'), bd=0)
        patient_info_entry.place(x=280, y=80)
        tk.Frame(patient_window, width=120, height=2, bg='blue').place(x=280, y=112)


        #Heading Search Patient
        heading_label=Label(patient_window,text='SEARCH PATIENT',font=('arial',18,'bold underline'),bg='#e8ecf4',fg='red')
        heading_label.place(x=250,y=10)
        
        # Function to search for patient information
        def search_patient():
            # Get the patient ID from the entry field
            patient_id = patient_info_entry.get()
            
            if patient_id=='':
                messagebox.showerror('Info', 'Patient ID not found')
                
            else:
                try:
                    # Connect to the database
                    con = sqlite3.connect('admit.db')
                    mycursor = con.cursor()

                    # Retrieve patient information based on ID
                    mycursor.execute('SELECT * FROM patients WHERE patient_id=?', (patient_id,))
                    patient_data = mycursor.fetchall()

                    if len(patient_data)>0:
                
                        patient_window = tk.Toplevel()
                        patient_window.geometry("900x700+50+50")
                        patient_window.title('Patient Information')
                        patient_window.resizable(0, 0)
                        
                        #Background image    
                        bg_image = ImageTk.PhotoImage(file='patient_detail.jpg')
                        bg_label = tk.Label(patient_window, image=bg_image)
                        bg_label.image = bg_image
                        bg_label.grid()
                        

                    
                        
                        Dataframe=Frame(patient_window,bd=20,relief=RIDGE,bg='SpringGreen4')
                        Dataframe.place(x=30,y=140,width=550,height=480)
                        
                        # #patation image
                        # bgImage=ImageTk.PhotoImage(file='pat_icon.jpg')
                        # bgLabel=Label(patient_window,image=bgImage)
                        # bgLabel.place(x=800,y=50)
                        

                        
                        tk.Label(patient_window, text='PATIENT INFORMATION', font=('Arial', 25, 'bold'), bg='#8acddd', fg='SpringGreen4').place(x=280, y=15)
                        tk.Frame(patient_window, width=420, height=2, bg='SpringGreen4').place(x=260, y=52)
                        tk.Label(patient_window, text=f'Name: {patient_data[0][1]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=80,y=170)
                        tk.Label(patient_window, text=f'Age: {patient_data[0][2]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=80,y=200)
                        tk.Label(patient_window, text=f'ID: {patient_data[0][3]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=80,y=230)
                        tk.Label(patient_window, text=f'D.O.B: {patient_data[0][4]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=80,y=260)
                        tk.Label(patient_window, text=f'Phone No.: {patient_data[0][5]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=80,y=290)
                        tk.Label(patient_window, text=f'Address: {patient_data[0][6]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=80,y=320)
                        tk.Label(patient_window, text=f'Blood Group: {patient_data[0][7]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=80,y=350)
                        tk.Label(patient_window, text=f'Symptoms: {patient_data[0][8]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=80,y=380)
                        tk.Label(patient_window, text=f'Other: {patient_data[0][9]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=80,y=410)
                        tk.Label(patient_window, text=f"Doctor's Name: {patient_data[0][10]}", font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=80,y=440)
                        tk.Label(patient_window, text=f'D.O.A: {patient_data[0][11]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=80,y=470)
                        tk.Label(patient_window, text=f'Ward: {patient_data[0][12]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=80,y=500)
                        tk.Label(patient_window, text=f'Bed: {patient_data[0][13]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=80,y=530)
                        tk.Label(patient_window, text=f'Status: {patient_data[0][14]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=80,y=560)
                    else:
                        messagebox.showerror('Info', 'Patient ID not found')
                    
                    con.close()
                except :
                    messagebox.showerror('Error', 'Connectivity Issue')
                
            
                patient_info_entry.delete(0, tk.END)

        #Search Button for search patient by ID
        search_button = tk.Button(patient_window, text="🔍", font=('Arial',30, 'bold'), bg='#e8ecf4', fg='black', activebackground='#e8ecf4', bd=0,cursor='hand2', command=search_patient)
        search_button.place(x=380, y=50)
    
            
     #Patient Info Button           
    # patient_frame=Frame(main_window,bg='#DEEDF4')
    # patient_frame.place(x=600,y=200)
    # button=customtkinter.CTkButton(patient_frame,text="PATIENT INFO",height=80,width=200,corner_radius=30,font=('Helvetica',34),cursor='hand2',fg_color='medium sea green',command=patient)
    # button.grid(row=0,column=2)
    
    patient_frame=Frame(main_window,bg='#DEEDF4')
    patient_frame.place(x=600,y=200)
    pic1=customtkinter.CTkImage(Image.open('button3Patient.png'),size=(165,165))
    button=customtkinter.CTkButton(patient_frame,text='',image=pic1,cursor='hand2',corner_radius=100,hover_color='navy blue',fg_color='#DEEDF4',bg_color='#DEEDF4',command=patient)
    patient_frame.image=pic1
    button.grid(row=0,column=2)


#Ambulance

def ambulance():
    
    def info():
        #Create Window
        info_window=tk.Toplevel()
        info_window.geometry("900x628+400+150")
        info_window.title('Detail')
        info_window.resizable(0,0)
        
        #Background Image
        bg_image = ImageTk.PhotoImage(file='info2.jpg')
        bg_label = tk.Label(info_window, image=bg_image)
        bg_label.image = bg_image
        bg_label.grid()
        
        bg_image = ImageTk.PhotoImage(file='driver.jpg')
        bg_label = tk.Label(info_window, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(x=610,y=60)
    
    
        #Heading Ambulance Information
        heading_label=Label(info_window,text='Name:SHYAM KUMAR SONI \n Address:Ghamariya,Lal Building \n ID:AD001 \n Blood Group:A+ \n B.O.B:12.12.2004 \n Marital Status:Searching Her',font=('arial',15,'bold'),bg='#ffffff',fg='red')
        heading_label.place(x=550,y=300)
    
    def detail():
    
        #Create Window
        ambulance_window = tk.Toplevel()
        ambulance_window.geometry("626x417+200+200")
        ambulance_window.title('AMBULANCE')
        ambulance_window.resizable(0, 0)
        
        #Background Image
        bg_image = ImageTk.PhotoImage(file='amb3.jpg')
        bg_label = tk.Label(ambulance_window, image=bg_image)
        bg_label.image = bg_image
        bg_label.grid()
        
        
        #Heading Ambulance Information
        heading_label=Label(ambulance_window,text='108',font=('arial',20,'bold underline'),bg='#dbf0f5',fg='red')
        heading_label.place(x=480,y=110)
        
        #Heading Emergency Contact
        heading_label=Label(ambulance_window,text='Emergency Contact:',font=('arial',16,'bold underline'),bg='#ffffff',fg='red')
        heading_label.place(x=20,y=350)
        
        #Contact Button
        contactButton=Button(ambulance_window,text='8877471116',font=('Open Sans',16,'bold'),fg='red',bg='#ffffff',activebackground='#ffffff',activeforeground='SpringGreen4',cursor='hand2',bd=0, command=info)
        contactButton.place(x=230,y=348)
        
        
    #Ambulance Button
    ambulanceButton=Button(main_window,text='AMBULANCE',font=('Open Sans',15,'bold underline'),fg='red',bg='#d9e9f6',activebackground='#d9e9f6',activeforeground='SpringGreen4',cursor='hand2',bd=0,command=detail)
    ambulanceButton.place(x=1350,y=85)



#Admin Button,
def admin():
    
    
    def sad():
        #Create Window
        admin_window = tk.Toplevel()
        admin_window.geometry("880x550+200+200")
        admin_window.title('ADMIN LOGIN')
        admin_window.resizable(0, 0)
            
        #Background Image
        bg_image = ImageTk.PhotoImage(file='admin.jpg')
        bg_label = tk.Label(admin_window, image=bg_image)
        bg_label.image = bg_image
        bg_label.grid()
            
            
        #Heading Ambulance Information
        heading_label=Label(admin_window,text='ADMIN LOGIN',font=('arial',20,'bold underline'),bg='#f7f6f1',fg='red')
        heading_label.place(x=370,y=10)
        
        #Entry Point ADMIN ID
        tk.Label(admin_window, text='ID:', font=('Arial', 15, 'bold'),bg='#f7f6f1').place(x=395, y=345)
        admin_id = tk.Entry(admin_window, width=10, font=('Arial', 15, 'bold'),bg='#f7f6f1',bd=0,fg='black',background='#f7f6f1')
        admin_id.place(x=430, y=345)
        tk.Frame(admin_window, width=100, height=2, bg='black').place(x=430, y=371)
        
        #Entry Point ADMIN PASSWORD
        tk.Label(admin_window, text='PASSWORD:', font=('Arial', 15, 'bold'),bg='#f7f6f1').place(x=300, y=400)
        admin_password = tk.Entry(admin_window, width=10, font=('Arial', 15, 'bold'),bg='#f7f6f1',bd=0,fg='black',background='#f7f6f1')
        admin_password.place(x=430, y=400)
        tk.Frame(admin_window, width=100, height=2, bg='black').place(x=430, y=425)

        def admin_login():
            
            #Check Id PASSWORD
            id=admin_id.get()
            password=admin_password.get()
        
            if id=='SAD' and password=='2029':
                        
                #Create Window
                admin_window = tk.Toplevel()
                admin_window.geometry("880x550+150+150")
                admin_window.title('ADMIN ACCESS')
                admin_window.resizable(0, 0)
                        
                #Background Image
                bg_image = ImageTk.PhotoImage(file='AdminPage.jpg')
                bg_label = tk.Label(admin_window, image=bg_image)
                bg_label.image = bg_image
                bg_label.grid()
                        
                        
                #Heading Ambulance Information
                # heading_label=Label(admin_window,text='ADMIN',font=('arial',20,'bold underline'),bg='#f7f6f1',fg='red')
                # heading_label.place(x=360,y=10)
                
                
                def show_user():
                    
                    #Create Window
                    user_window = tk.Toplevel()
                    user_window.geometry("880x550+150+150")
                    user_window.title('SHOW USER')
                    user_window.resizable(0, 0)
                            
                    #Background Image
                    bg_image = ImageTk.PhotoImage(file='findUser.jpg')
                    bg_label = tk.Label(user_window, image=bg_image)
                    bg_label.image = bg_image
                    bg_label.grid()
                    
                    #Entry username
                    tk.Label(user_window, text='USER NAME:', font=('Arial', 15, 'bold'),bg='#e2e9fb').place(x=290, y=50)
                    user_id_entry = tk.Entry(user_window, width=20, font=('Arial', 15, 'bold'),bg='#e2e9fb',bd=0,fg='black',background='#e2e9fb')
                    user_id_entry.place(x=425, y=50)
                    tk.Frame(user_window, width=220, height=2, bg='black').place(x=425, y=74)
                    
                    
                    
                    def user_data():
                        # Get the patient ID from the entry field
                        user_id = user_id_entry.get()
                        
                        if user_id_entry=='':
                            messagebox.showerror('Error', 'All Fields Are Required')
                            
                        else:
                            try:
                                # Connect to the database
                                con = sqlite3.connect('userdata.db')
                                mycursor = con.cursor()

                                # Retrieve patient information based on ID
                                mycursor.execute('SELECT * FROM data WHERE username=?', (user_id,))
                                user_data = mycursor.fetchall()

                                if len(user_data)>0:
                            
                                    user2_window = tk.Toplevel()
                                    user2_window.geometry("880x550+50+50")
                                    user2_window.title('USER Information')
                                    user2_window.resizable(0, 0)
                                    
                                    # #Background image    
                                    bg_image = ImageTk.PhotoImage(file='UserInfo.jpg')
                                    bg_label = tk.Label(user2_window, image=bg_image)
                                    bg_label.image = bg_image
                                    bg_label.grid()
                                    

                                
                                    
                                    Dataframe=Frame(user2_window,bd=15,relief=RIDGE,bg='SpringGreen4')
                                    Dataframe.place(x=30,y=130,width=390,height=180)
                                    
                
                                    
                                    # tk.Label(user2_window, text='USER INFORMATION', font=('Arial', 25, 'bold'), bg='#8acddd', fg='SpringGreen4').place(x=280, y=15)
                                    # tk.Frame(user2_window, width=420, height=2, bg='SpringGreen4').place(x=260, y=52)
                                    tk.Label(user2_window, text=f'Email: {user_data[0][1]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=65,y=170)
                                    tk.Label(user2_window, text=f'USER NAME: {user_data[0][2]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=65,y=200)
                                    tk.Label(user2_window, text=f'PASSWORD: {user_data[0][3]}', font=('Arial', 17,'bold'),fg='white',bg='SpringGreen4').place(x=65,y=230)
                                    
                               
                                else:
                                    messagebox.showerror('Error', 'USER ID not found')
                                
                                con.close()
                            except :
                                messagebox.showerror('Error', 'Connectivity Issue')
                            
                        
                            #patient_info_entry.delete(0, tk.END)
                            user_id_entry.delete(0,tk.END)
                    
                    
                    #SEARCH USER Button
                    admin_login_Button=Button(user_window,text='🔍',font=('Open Sans',20,'bold'),fg='black',bg='#e2e9fb',activebackground='#e2e9fb',activeforeground='SpringGreen4',cursor='hand2',bd=0,command=user_data)
                    admin_login_Button.place(x=600,y=30)
                
                
                
                def del_user():
                    
                    #Create Window
                    del_user_window = tk.Toplevel()
                    del_user_window.geometry("880x550+150+150")
                    del_user_window.title('SHOW USER')
                    del_user_window.resizable(0, 0)
                            
                    #Background Image
                    bg_image = ImageTk.PhotoImage(file='DelteUser.jpg')
                    bg_label = tk.Label(del_user_window, image=bg_image)
                    bg_label.image = bg_image
                    bg_label.grid()
                    
                    #Entry username
                    tk.Label(del_user_window, text='USER NAME:', font=('Arial', 15, 'bold'),bg='#e7e7e7').place(x=290, y=50)
                    user_id_entry = tk.Entry(del_user_window, width=20, font=('Arial', 15, 'bold'),bg='#e7e7e7',bd=0,fg='black',background='#e7e7e7')
                    user_id_entry.place(x=425, y=50)
                    tk.Frame(del_user_window, width=220, height=2, bg='black').place(x=425, y=74)
                
                    #Update DataBase 
                    def remove():
                        user_id = user_id_entry.get()
                        

                        if user_id == '':
                            messagebox.showerror('Error', 'All Fields Are Required')
                            return

                        else:
                            try:
                                # Connect to the admit.db database
                                con_user = sqlite3.connect('userdata.db')
                                mycursor_user = con_user.cursor()

                                mycursor_user.execute('SELECT * FROM data WHERE username=?', (user_id,))
                                user_data = mycursor_user.fetchone()

                                if user_data:
                                    # Update status, patient ID, and bed in admit.db
                                    mycursor_user.execute('UPDATE data SET username=? WHERE username=?', ('REMOVED', user_id))
                                    
                                    con_user.commit()
                                    con_user.close()


                                    messagebox.showwarning('Warning', 'USER REMOVED')
                                    messagebox.showinfo('Success', 'USER REMOVED')
                                    

                                else:
                                    messagebox.showerror('Error', 'USER ID not found')

                            except :
                                messagebox.showerror('Error', 'Database Connectivity Error')

                            user_id_entry.delete(0,tk.END)
                   
                    
                    
                    #SEARCH USER Button
                    admin_login_Button=Button(del_user_window,text='🔍',font=('Open Sans',20,'bold'),fg='black',bg='#e7e7e7',activebackground='#e7e7e7',activeforeground='SpringGreen4',cursor='hand2',bd=0,command=remove)
                    admin_login_Button.place(x=600,y=30)
                
                
                
                #SHOW USER Button
                admin_login_Button=Button(admin_window,text='SHOW USER',font=('Open Sans',15,'bold underline'),fg='red',bg='#b7ddf4',activebackground='#b7ddf4',activeforeground='SpringGreen4',cursor='hand2',bd=0,command=show_user)
                admin_login_Button.place(x=50,y=445) 
                
                #DELETE USER Button
                admin_login_Button=Button(admin_window,text='DELETE USER',font=('Open Sans',15,'bold underline'),fg='red',bg='#b7ddf4',activebackground='#b7ddf4',activeforeground='SpringGreen4',cursor='hand2',bd=0,command=del_user)
                admin_login_Button.place(x=680,y=445) 
                
                
                admin_id.delete(0,tk.END)
                admin_password.delete(0,tk.END)
                
                
                
            else:
                messagebox.showerror('Error', 'ADMIN NOT FOUND')
                
                
            
            
    
        #ADMIN LOGIN Button
        admin_login_Button=Button(admin_window,text='LOGIN',font=('Open Sans',15,'bold'),fg='red',bg='#f7f6f1',activebackground='#f7f6f1',activeforeground='SpringGreen4',cursor='hand2',bd=0,command=admin_login)
        admin_login_Button.place(x=425,y=445)                
    
    #ADMIN Button
    adminButton=Button(main_window,text='ADMIN',font=('Open Sans',15,'bold underline'),fg='red',bg='#d9e9f6',activebackground='#d9e9f6',activeforeground='SpringGreen4',cursor='hand2',bd=0,command=sad)
    adminButton.place(x=1190,y=85)



# Call the functions to create buttons and labels
doctor_detail()
patient_detail()
discharge_patient()
admit_patient()
nurse_detail()
admin()
ambulance()
main_window.mainloop()
