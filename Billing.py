from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import random

import pymysql

window=Tk()
window.title("Billing Software")
window.geometry("900x600")

#======================================================Database=============================================================================================
try:
    conn=pymysql.connect(host='localhost', user='root',password='Awine@23',database='retail_management')
    mycursor=conn.cursor()

except:
    messagebox.showerror('Error','Connection Failed, Please Try Again')
try:
    query='select DrugName from drugs'
    mycursor.execute(query)
    data=mycursor.fetchall()
except:
    messagebox.showerror('Error','Invalid')

global l, q
q=[]
l = []
c_me=StringVar()
phone_no=StringVar()
pn=StringVar()
pr=DoubleVar()
pq=IntVar()

#======================================================FUNCTIONS=============================================================================================
def Home():
    textarea.delete(1.0,END)
    textarea.insert(END,"\t    BC BENCYN PHARMACY LIMITED")
    textarea.insert(END,"\n \t\t      P.O BOX 176")
    textarea.insert(END,"\n \t           0207529669 / 0551393568")
    textarea.insert(END,"\n \t\t       POS INVOICE\n")
    textarea.insert(END,f'\n User : \t{c_me.get()}\t\t\t      Bill No : \t{phone_no.get()}\n')
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%d-%m-%Y")
    datetime_str = f" Date: {current_date}\t\t\t\t      Time: {current_time}"
    textarea.insert(END,datetime_str)
    textarea.insert(END,f"\n==============================================")
    textarea.insert(END,f'\nProduct\t\t Qty  \t   Rate\t\tAmount')
    textarea.insert(END,f"\n==============================================\n")
    textarea.config(font=('arial',10))
    c_me.set('Clinton')
    pq.set('')
    pr.set('')
    pn.set('')


def onEnter(e):
    Addbutton.invoke()

def search(e):
    typed=pn.get()
    query = "select DrugName from drugs where DrugName LIKE %s"
    mycursor.execute(query,('%'+typed+'%'))
    data=[item[0] for item in mycursor.fetchall()]
    Pname_entry['values']=data

def displayanext(e):
    selected=pn.get()
    query='select DrugPrice from drugs where DrugName=%s'
    mycursor.execute(query,selected)
    result= mycursor.fetchone()

    if result:
        Prate_entry.delete(0,END)
        Prate_entry.insert(0,result[0])


def add():
    if pn.get()=='':
        messagebox.showerror("Error","Please All Fields Are Required")
    elif pr.get()==0 or pq.get()==0:
        messagebox.showerror('Error','Invalid Entry')
    else:
        m=pr.get()*pq.get()
        l.append(m)
        q.append(pq.get())
        textarea.insert(END,f'{pn.get()}\t\t {pq.get()}  \t  {pr.get():.2f}\t\t{m:.2f} \n')
        pq.set('')
        pr.set('')
        pn.set('')

def clear():
    l.clear()
    q.clear()
    phone_no.set('')
    x = random.randint(1000, 9999)
    phone_no.set(str(x))
    Home()

def tbill():
    lt=sum(l)
    totalq=sum(q)
    textarea.insert(END,f"\n==============================================")
    textarea.insert(END,f"\n \tTotal : \t{totalq} \t\t\t${lt:.2f}")
    textarea.insert(END,f"\n==============================================\n")
    query = 'insert into bills(Bill_Id,TotalQty,TotalAmt,DayDte) values (%s,%s,%s,%s)'
    mycursor.execute(query, (phone_no.get(),totalq,lt,))
    conn.commit()
    conn.close()



title_frame=Frame(window)
title_frame.pack(fill="x")

title_label=Label(title_frame,bg="cyan",text="Billing Software",font=("arial",18,"bold"),bd=5,relief=GROOVE)
title_label.pack(fill="x")

#======================================================CUSTOMER DETAILS=============================================================================================

wrapper1=LabelFrame(window,text="Customer Details",bg="cyan",bd=5,relief=GROOVE)
wrapper1.pack(fill="both",pady=5)

customer_name=Label(wrapper1,text="User",font=("arial",10,"bold"),bg="cyan",)
customer_name.pack(side="left")

customer_entry=Entry(wrapper1,font=("arial",9,"bold"),bd=3,relief=GROOVE,textvariable=c_me)
customer_entry.pack(side="left")

phone_label=Label(wrapper1,text="Bill No",font=("arial",10,"bold"),bg="cyan")
phone_label.place(x=350,y=0)

phone_entry=Entry(wrapper1,font=("arial",9,"bold"),bd=3,relief=GROOVE,textvariable=phone_no)
phone_entry.place(x=450,y=0)

#======================================================PRODUCTS DETAILS=============================================================================================
wrapper2=LabelFrame(window,text="Product Details",bg="cyan",bd=5,relief=GROOVE)
wrapper2.place(x=15,y=120,width=400,height=400)

Pname=Label(wrapper2,text="Product Name",font=("arial",10,"bold"),bg="cyan")
Pname.place(x=45,y=30)

Pname_entry=ttk.Combobox(wrapper2,font=("arial",9,"bold"),width=24,textvariable=pn,values=[row[0] for row in data])
Pname_entry.place(x=190,y=30)

Prate=Label(wrapper2,text="Product Rate",font=("arial",10,"bold"),bg="cyan")
Prate.place(x=45,y=80)

Prate_entry=Entry(wrapper2,font=("arial",9,"bold"),bd=3,relief=GROOVE,width=26,textvariable=pr)
Prate_entry.place(x=190,y=80)

Pquantity=Label(wrapper2,text="Product Quantity",font=("arial",10,"bold"),bg="cyan",)
Pquantity.place(x=45,y=130)

Pquantity_entry=Entry(wrapper2,font=("arial",9,"bold"),bd=3,relief=GROOVE,width=26,textvariable=pq)
Pquantity_entry.place(x=190,y=130)

#======================================================BUTTONS=============================================================================================

Addbutton=Button(wrapper2,text="Add",font=("arial",9,"bold"),width=10,command=add)
Addbutton.place(x=45,y=270)

Clearbutton=Button(wrapper2,text="Clear",font=("arial",9,"bold"),width=10, command=clear)
Clearbutton.place(x=170,y=270)

Billbutton=Button(wrapper2,text="TBill",font=("arial",9,"bold"),width=10,command=tbill)
Billbutton.place(x=296,y=270)

Pname_entry.bind('<<ComboboxSelected>>',displayanext)
Pname_entry.bind('<KeyRelease>',search)

Pquantity_entry.bind('<Return>',onEnter)

#======================================================BILLS SECTION=============================================================================================
bills=Frame(window,bd=5,relief=GROOVE,bg="white")
bills.place(x=480,y=120,width=400,height=400)

title=Label(bills,text="Bill Area",font=("arial",12,"bold"),bd=3,relief=GROOVE)
title.pack(fill="x")

yscroll=Scrollbar(bills,orient=VERTICAL)
textarea=Text(bills,yscrollcommand=yscroll)
yscroll.pack(side=RIGHT,fill=Y)
yscroll.config(command=textarea.yview())
textarea.pack()
Home()

window.mainloop()