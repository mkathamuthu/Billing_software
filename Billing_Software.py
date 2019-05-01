from tkinter import *              
from tkinter import font  as tkfont 
from fuzzywuzzy import process
import datetime
import sqlite3
import win32api
import win32print
now = datetime.datetime.now()

class SampleApp(Tk):

    def __init__(self):
        
        Tk.__init__(self)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.content_font = tkfont.Font(family='Helvetica', size=14, slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, BillingCentral,DataEntry,Dashboard,Add_New_Item,Update_QTY_Price,new_user,new_vendor):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        for i in range(0,7):
            Label(self,text="   ", width = 20).grid(row = 0 ,column =i, sticky = "E",ipady = 46) 
            Label(self,text="   ", width = 10).grid(row = i ,column =0, sticky = "E",ipady = 10)
        
        Label(self, text = "Welcome to AIMS Billing Software", font = controller.title_font,fg = "black",justify = "center").grid(row = 4,column =3)
        
        Button(self, text = "Login",bg = "white",fg = "black",borderwidth=4,command=lambda: self.check()).grid(row = 7,column =3)
        self.username = Entry(self)
        self.username.insert(0,'username')
        self.username.grid(row = 5,column=3,columnspan=1)
        self.password = Entry(self)
        self.password.insert(0,'Password')
        self.password.grid(row = 6,column=3,columnspan=1)
        
    def check(self):
        if("admin" == self.username.get() and "admin"==self.password.get()):
         
            self.controller.show_frame("PageOne")

   
        
class new_user(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        top = Frame(self,width = 1350 ,height = 100, bd = 2,relief = "raised")
        top.pack(side = TOP)
        left = Frame(self,width = 450,height = 490,bd = 0,relief = "raised")
        left.pack(side = LEFT)
        right = Frame(self,width = 450,height = 490,bd = 0,relief = "raised")
        right.pack(side = RIGHT)
        centre =Frame(self,width = 450,height = 100,bd = 0,relief = "raised")
        centre.pack(side = RIGHT)
        centre_top =Frame(centre,width = 450,height = 100,bd = 0,relief = "raised")
        centre_top.pack(side = TOP)
        centre_mid =Frame(centre,width = 450,height = 100,bd = 0,relief = "raised")
        centre_mid.pack(side = TOP)
        centre_bottom =Frame(centre,width = 450,height = 100,bd = 0,relief = "raised")
        centre_bottom.pack(side = TOP)		
        centre_button =Frame(centre,width = 450,height = 90,bd = 0,relief = "raised")
        centre_button.pack(side = TOP)
        #bottom_frame = Frame(self,width = 1350 ,height = 100, bd = 2,relief = "raised")
        #bottom_frame.pack(side = BOTTOM)
        Label(centre_top, text="Customer name", font=controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 10,ipady = 30,padx = 15)
        self.customer_name_label = Entry(centre_top)
        self.customer_name_label.pack(side =RIGHT,padx = 10,ipadx =10,ipady =5)
        Label(centre_mid, text="Address", font=controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 10,ipady = 30,padx = 15)
        self.Address_label = Entry(centre_mid)
        self.Address_label.pack(side =RIGHT,padx = 10,ipadx =10,ipady =5)
        Label(centre_bottom, text="Phone number", font=controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 10,ipady = 30,padx = 15)
        self.Phonenumber_label = Entry(centre_bottom)
        self.Phonenumber_label.pack(side =RIGHT,padx = 10,ipadx =10,ipady =5)
        update_button = Button(centre_button, text="Add user",command=self.update)
        update_button.pack(side = LEFT,fill = X,expand = 1,ipadx = 10 ,padx =10,pady =10)
        cancel_button = Button(centre_button, text="cancel",command=lambda:self.controller.show_frame("BillingCentral"))
        cancel_button.pack(side =RIGHT,fill = X,expand = 1,ipadx = 10 ,padx =10,pady =10)
       
    def update(self):
        self.customer_value = self.customer_name_label.get()
        self.address_value = self.Address_label .get()
        self.Phonenumber_value = self.Phonenumber_label .get()        
        self.dbconnect()

    def dbconnect(self):
        db = sqlite3.connect('billing.db')
        cursor = db.cursor()
        sql = "SELECT max(customerID) FROM customer_detail"
        cursor.execute(sql)
        output = cursor.fetchone()
        if output[0] is None:
            a = 0
        else:    
            a = int(output[0])
        
        sql = "INSERT INTO customer_detail(customerID,customer_name,Address,phonenumber,balance) VALUES ('%d', '%s', '%s', '%d','%d')" % (int(a+1),self.customer_value, self.address_value, int(self.Phonenumber_value),0 )
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("something wrong")

        db.close()
        
        self.customer_name_label.delete(first = 0 , last =END)
        self.Address_label.delete(first = 0 , last =END)
        self.Phonenumber_label.delete(first = 0 , last =END)
        self.controller.show_frame("BillingCentral")

class new_vendor(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        top = Frame(self,width = 1350 ,height = 100, bd = 2,relief = "raised")
        top.pack(side = TOP)
        left = Frame(self,width = 450,height = 490,bd = 0,relief = "raised")
        left.pack(side = LEFT)
        right = Frame(self,width = 450,height = 490,bd = 0,relief = "raised")
        right.pack(side = RIGHT)
        centre =Frame(self,width = 450,height = 100,bd = 0,relief = "raised")
        centre.pack(side = RIGHT)
        centre_top =Frame(centre,width = 450,height = 100,bd = 0,relief = "raised")
        centre_top.pack(side = TOP)
        centre_mid =Frame(centre,width = 450,height = 100,bd = 0,relief = "raised")
        centre_mid.pack(side = TOP)
        centre_bottom =Frame(centre,width = 450,height = 100,bd = 0,relief = "raised")
        centre_bottom.pack(side = TOP)		
        centre_button =Frame(centre,width = 450,height = 90,bd = 0,relief = "raised")
        centre_button.pack(side = TOP)
        #bottom_frame = Frame(self,width = 1350 ,height = 100, bd = 2,relief = "raised")
        #bottom_frame.pack(side = BOTTOM)
        Label(centre_top, text="Vendor name", font=controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 10,ipady = 30,padx = 15)
        self.customer_name_label = Entry(centre_top)
        self.customer_name_label.pack(side =RIGHT,padx = 10,ipadx =10,ipady =5)
        Label(centre_mid, text="Address", font=controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 10,ipady = 30,padx = 15)
        self.Address_label = Entry(centre_mid)
        self.Address_label.pack(side =RIGHT,padx = 10,ipadx =10,ipady =5)
        Label(centre_bottom, text="Phone number", font=controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 10,ipady = 30,padx = 15)
        self.Phonenumber_label = Entry(centre_bottom)
        self.Phonenumber_label.pack(side =RIGHT,padx = 10,ipadx =10,ipady =5)
        update_button = Button(centre_button, text="Add vendor",command=self.update)
        update_button.pack(side = LEFT,fill = X,expand = 1,ipadx = 10 ,padx =10,pady =10)
        cancel_button = Button(centre_button, text="cancel",command=lambda:self.controller.show_frame("BillingCentral"))
        cancel_button.pack(side =RIGHT,fill = X,expand = 1,ipadx = 10 ,padx =10,pady =10)
       
    def update(self):
        self.vendor_value = self.customer_name_label.get()
        self.v_address_value = self.Address_label .get()
        self.v_Phonenumber_value = self.Phonenumber_label .get()        
        self.dbconnect()

    def dbconnect(self):
        db = sqlite3.connect('billing.db')
        cursor = db.cursor()
        sql = "SELECT max(vendorID) FROM vendor_detail"
        cursor.execute(sql)
        output = cursor.fetchone()
        if output[0] is None:
            a = 0
        else:    
            a = int(output[0])
        
        sql = "INSERT INTO vendor_detail(vendorID,vendor_name,Phone_number,address) VALUES ('%d', '%s', '%s', '%s')" % (int(a+1),self.vendor_value, str(self.v_Phonenumber_value),self.v_address_value,  )
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("something wrong")

        db.close()
        
        self.customer_name_label.delete(first = 0 , last =END)
        self.Address_label.delete(first = 0 , last =END)
        self.Phonenumber_label.delete(first = 0 , last =END)
        self.controller.show_frame("Add_New_Item")


class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        for i in range(0,7):
            Label(self,text="   ", bg = "grey64",width = 20).grid(row = i ,column =0 , sticky = "E",ipady = 46) 
        Button(self, text="Billing Central",
                           command=lambda: controller.show_frame("BillingCentral")).grid(row = 1,column = 0,ipadx = 10)
        Button(self, text="Data Entry",
                           command=lambda: controller.show_frame("DataEntry")).grid(row = 2,column = 0,ipadx = 20)
        Button(self, text="Dashboard",
                           command=lambda: controller.show_frame("Dashboard")).grid(row = 3,column = 0,ipadx = 20)
        #Button(self, text="Exit",
                           #command=quit).grid(row = 4,column = 0,ipadx = 38)

class BillingCentral(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.Profit_total =0
        self.total = 0
        self.discount_d= 0
        self.credits= 0	
        self.discount_1= []
        self.Products_purchased = []
        self.product_name =[]
        self.qty_price = []
        self.qty_purchased =[]
        self.qty_orginal = []
        self.bill_temp_total=[]
        top = Frame(self,width = 1350 ,height = 100, bd = 2,relief = "raised")
        top.pack(side = TOP)
        left = Frame(self,width = 900,height = 590,bd = 2,relief = "raised")
        left.pack(side = LEFT)
        right = Frame(self,width = 450,height = 390,bd = 2,relief = "raised")
        right.pack(side = RIGHT)

        right_bottom = Frame(right,width = 450, height = 100,bd = 2,relief = "raised")
        right_bottom.pack(side = BOTTOM)
        right_amid = Frame(right,width = 450,height = 100,bd = 2,relief = "raised")
        right_amid.pack(side = BOTTOM)
        right_mid = Frame(right,width = 450,height = 100,bd = 2,relief = "raised")
        right_mid.pack(side = BOTTOM)

        top_label = Label(top, text = "SALES INVOICE",font = controller.title_font)
        top_label.pack(fill = X,expand = 1,ipadx = 1000,ipady = 25)	
        left_customer = Frame(left,width = 890,height = 70,bd = 2, relief = "raised")
        left_customer.pack(side = TOP)
        left_product = Frame(left,width = 890,height = 70,bd = 2, relief = "raised")
        left_product.pack(side = TOP)
        left_product_1 = Frame(left_product,width = 445,height = 70,bd = 2, relief = "raised")
        left_product_1.pack(side =LEFT)
        left_product_2 = Frame(left_product,width = 445,height = 70,bd = 2, relief = "raised")
        left_product_2.pack(side = RIGHT)
        left_detail = Frame(left,width = 890,height = 70,bd = 2, relief = "raised")
        left_detail.pack(side = TOP)
        left_detail_QTY = Frame( left_detail,width = 222,height = 70,bd = 2, relief = "raised")
        left_detail_QTY.pack(side = LEFT)
        left_detail_UNIT = Frame(left_detail,width = 222,height = 70,bd = 2, relief = "raised")
        left_detail_UNIT.pack(side = LEFT)
        left_detail_DIS = Frame(left_detail,width = 222,height = 70,bd = 2, relief = "raised")
        left_detail_DIS.pack(side = LEFT)
        left_detail_button= Frame(left_detail,width = 222,height = 70,bd = 2, relief = "raised")
        left_detail_button.pack(side = LEFT)
        left_bill = Frame(left,width = 890,height = 330,bd = 2, relief = "raised")
        left_bill.pack(side = TOP)
        left_amount = Frame(left,width = 890,height = 50,bd = 2, relief = "raised")
        left_amount.pack(side = TOP)
        Label(left_customer, text = "Customer Name",font = controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 40,ipady = 13)
        self.customer_name = Entry(left_customer)
        self.customer_name.bind('<Key>',self.getcustomerdetail)
        self.customer_name.pack(side = LEFT,fill = X,expand = 1,ipadx = 110,padx = 50,)
        Button(left_customer, text = "Add user",command = lambda: controller.show_frame("new_user"),fg = "black",borderwidth=4).pack(fill = X,expand = 1,padx = 58,ipadx = 15)
        Label(left_product_1, text = "Product Name",font = controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 45,ipady = 13)
        self.Product_name_bill = Entry(left_product_2)
        self.Product_name_bill.bind('<Key>',self.getvalue)
        self.Product_name_bill.pack(side = LEFT,fill = X,expand = 1,ipadx = 160,padx = 105, pady = 17)
        Label( left_detail_QTY, text = "QTY",font = controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 10,ipady = 13)
        self.QTY_bill = Entry( left_detail_QTY)
        self.QTY_bill.pack(side = LEFT,fill = X,expand = 1,ipadx = 0,padx = 6, pady = 23)
        Label(left_detail_UNIT, text = "UNIT",font = controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 10,ipady = 13)
        self.UNIT_bill = Entry(left_detail_UNIT)
        self.UNIT_bill.pack(side = LEFT,fill = X,expand = 1,ipadx = 0,padx = 6, pady = 23)
        Label( left_detail_DIS, text = "Discount",font = controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 10,ipady = 13)
        self.dis_bill = Entry( left_detail_DIS)
        self.dis_bill.pack(side = LEFT,fill = X,expand = 1,ipadx = 0,padx = 6, pady = 23)
        Button(left_detail_button, text = "Add Item",command = self.display,fg = "black",borderwidth=4).pack(fill = X,expand = 1,padx = 62,ipadx = 15,ipady = 4,pady = 13)
        self.textreceipt_product_name = Listbox( left_bill, font = controller.content_font,height = 15,width = 50 )
        self.textreceipt_product_name.pack(side = LEFT)
        self.textreceipt_product_name.insert(END,"Product Name\n\n")
        self.textreceipt_product_name.bind('<<ListboxSelect>>',self.delete_select) 
        self.textreceipt_QTY = Listbox( left_bill, font = controller.content_font,height = 15,width = 9 ,justify =RIGHT)
        self.textreceipt_QTY.pack(side = LEFT)
        self.textreceipt_QTY.insert(END,"QTY\n\n")
        self.textreceipt_Dis = Listbox( left_bill, font = controller.content_font,height = 15,width = 9 ,justify =RIGHT)
        self.textreceipt_Dis.pack(side = LEFT)
        self.textreceipt_Dis.insert(END,"Discount\n\n")     
        self.textreceipt_price = Listbox( left_bill, font = controller.content_font,height = 15,width = 11 ,justify =RIGHT)
        self.textreceipt_price.pack(side = LEFT)
        self.textreceipt_price.insert(END,"Price\n\n") 
        Label( left_amount, text = "Amount saved ",font = controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 80,ipady = 13)
        self.dis_amount = Label( left_amount,text = "0000000.00",font = controller.content_font)
        self.dis_amount.pack(side = LEFT,fill = X,expand = 1,ipadx = 21,ipady = 13)
        s = ' '
        self.amount_label = Label( left_amount,text = "0000000.00",font = controller.content_font)
        self.amount_label.pack(side = RIGHT,fill = X,expand = 1,ipadx = 22,ipady = 13)
        Label( left_amount, text = "Total Amount",font = controller.content_font).pack(side = RIGHT,fill = X,expand = 1,ipadx = 80,ipady = 13)

        self.mylistbox_search = Listbox(right,font = ('times',13))
        self.mylistbox_search.pack(side = TOP,ipadx = 200,ipady =150)
        self.mylistbox_search.bind('<<ListboxSelect>>',self.CurSelect)     
        Label(right, text = "Discount",font = controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 15,ipady = 13)
        Button(right, text = "Apply",command = self.total_dis,fg = "black",borderwidth=4).pack(side = RIGHT,fill = X,expand = 1,padx = 4,ipadx = 5,ipady = 4,pady = 10)
        self.Total_discount = Entry(right)
        self.Total_discount.pack(side =RIGHT,fill = X,expand = 1,ipadx = 10,padx = 10, pady = 17)
        self.Total_discount.insert(0,0)

        Label(right_mid, text = "amount_paid",font = controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 79,ipady = 13)
        self.amount_paid = Entry(right_mid)
        self.amount_paid.pack(side =RIGHT,fill = X,expand = 1,ipadx = 10,padx = 10, pady = 17)
        self.amount_paid.insert(0,0)
        self.amount_paid.bind('<Key>',self.credit_check)
        Label(right_amid, text = "credit balance",font = controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 72,ipady = 13)
        self.credit_balance_e = Entry(right_amid)
        self.credit_balance_e.pack(side =RIGHT,fill = X,expand = 1,ipadx = 15,padx = 10, pady = 17)
        self.credit_balance_e.insert(0,0)
        search_scroll = Scrollbar(self.mylistbox_search,orient = "vertical")
        search_scroll.config(command=self.mylistbox_search.yview)
        search_scroll.pack(side="right", fill="y")
		
        Button(right_bottom, text = "Print Bill",command = lambda:self.update_db(1),fg = "black",borderwidth=4).pack(side = RIGHT,fill = X,expand = 1,padx = 27,ipadx = 15,ipady = 4,pady = 13)
        Button(right_bottom, text = "Print GST Bill",command = lambda:self.update_db(0),fg = "black",borderwidth=4).pack(side = RIGHT,fill = X,expand = 1,padx = 27,ipadx = 15,ipady = 4,pady = 13)		
        Button(right_bottom, text = "Cancel",command = self.gotopageone,fg = "black",borderwidth=4).pack(side = RIGHT,fill = X,expand = 1,padx = 27,ipadx = 15,ipady = 4,pady = 13)

    def credit_check(self,event):
        self.credits= float(self.amount_paid.get())	- self.total
        self.credit_balance_e.delete(first = 0,last =END)
        self.credit_balance_e.insert(0,self.credits)
		
    def delete_select(self,event):
        value =((self.textreceipt_product_name.get(self.textreceipt_product_name.curselection())))
        i = 0

        for x in  self.product_name:
            
            if x == value:
                self.total = float(self.total)-(float(self.qty_price[i])*float(self.qty_purchased[i]))+(float(self.discount_1[i]))
                self.discount_d = float(self.discount_d)-(float(self.discount_1[i]))
                del self.product_name[i]
                del self.qty_purchased[i] 
                del self.qty_price[i]
                del self.Products_purchased[i] 	
                del self.qty_orginal[i]  
                del self.discount_1[i]				

                s = ' '
                a = (str(round(self.total,2))+ str(s *(10 - len(str(self.total)))))
                print(a)				
                self.amount_label.configure(text = a) 
                self.dis_amount.configure(text = str(round(self.discount_d,2))+ str(s *(10 - len(str(round(self.discount_d,2))))))
        				
            i = i+1
        selection = self.textreceipt_product_name.curselection()
        self.textreceipt_product_name.delete(selection[0]) 
        self.textreceipt_QTY.delete(selection[0])
        self.textreceipt_Dis.delete(selection[0]) 
        self.textreceipt_price.delete(selection[0]) 			
		
    def total_dis(self):
        #print("its here")
        self.discount_d = float(self.discount_d)+(float(self.total)*float(float(self.Total_discount.get())/100))
        self.total = float(self.total)-(float(self.total)*(float(self.Total_discount.get())/100))

        s = ' '
        a = (str(round(self.total,2))+ str(s *(10 - len(str(self.total)))))
        self.amount_label.configure(text = a)
        self.dis_amount.configure(text = str(round(self.discount_d,2))+ str(s *(10 - len(str(round(self.discount_d,2))))))
		
    def display(self):
        self.vqty_1 = self.QTY_bill.get()
        self.vdis_1 = self.dis_bill.get()
        self.temp_total = (float(self.vsp_1[self.index_2]) * float(self.vqty_1))-((float(self.vsp_1[self.index_2]) * float(self.vqty_1))*(float(self.vdis_1)/100))
        self.temp_profit_total =  (float(self.vcp_1[self.index_2]) * float(self.vqty_1))

        self.discount_Temp = ((float(self.vsp_1[self.index_2]) * float(self.vqty_1))*(float(self.vdis_1)/100))
        self.qty_price.append(float(self.vsp_1[self.index_2]))
        self.textreceipt_product_name.insert(END,self.vProduct_name[self.index_2])
        self.Products_purchased.append(self.vProduct_id[self.index_2])
        self.product_name.append(self.vProduct_name[self.index_2])
        self.qty_purchased.append(self.vqty_1)
        self.qty_orginal.append(self.vQTY_No[self.index_2])
        #self.textreceipt_product_name.insert(END,"\n")
        self.textreceipt_QTY.insert(END,self.vqty_1)    
        #self.textreceipt_QTY.insert(END,"\n")      
        self.textreceipt_Dis.insert(END,round(self.discount_Temp,2))
        #self.textreceipt_Dis.insert(END,"\n")
        self.textreceipt_price.insert(END,self.temp_total) 
        #self.textreceipt_price.insert(END,"\n") 
        self.total = float(self.total) + self.temp_total
        self.Profit_total = float(self.Profit_total) + self.temp_profit_total
        #self.total = float(self.total)-(float(self.total)*(float(self.Total_discount.get())/100))
        self.discount_d = float(self.discount_d)+float(self.discount_Temp)
        self.discount_1.append(self.discount_d)
        s = ' '
        self.bill_temp_total.append(self.temp_total)
        a = (str(round(self.total,2))+ str(s *(10 - len(str(self.total)))))
        self.amount_label.configure(text = a)
        self.dis_amount.configure(text = str(round(self.discount_d,2))+ str(s *(10 - len(str(round(self.discount_d,2))))))
        self.discount_Temp=0
        self.temp_total = 0 
        self.temp_profit_total = 0 
        self.dis_bill.delete(first = 0 , last =END)
        self.dis_bill.insert(0,0)	
        self.Product_name_bill.delete(first =0,last = 20)	
        self.QTY_bill.delete(first =0,last =END)
        self.QTY_bill.insert(0,1)		
        #self.new_invoice = []

    def update_db(self,check):
        db = sqlite3.connect('billing.db')
        cursor = db.cursor()
        sql = "SELECT max(invocieID) FROM invoice"
        cursor.execute(sql)
        output = cursor.fetchone()
        if output[0] is None:
            a = 0
        else:    
            a = int(output[0])
        self.invoice_no=a+1
        i = 0
        for tem in self.Products_purchased:
            sql = "UPDATE master_table SET QTY = %d WHERE Product_ID = %d " % (int(self.qty_orginal[i])-int( self.qty_purchased[i]),int(tem))
            sql1  = "INSERT INTO invoice(Product_ID ,invocieID ,Price,prod_qty) VALUES ('%d','%d', '%d', '%d')" % (int(tem),a+1,self.qty_price[i]*int( self.qty_purchased[i]),int( self.qty_purchased[i]))
            i = i +1
            try:
                cursor.execute(sql)
                cursor.execute(sql1)
                db.commit()
            except:
                db.rollback()
                print("something wrong")
        db.close()
        self.customer_name.delete(first = 0,last= 20)
        self.Product_name_bill.delete(first =0,last = 20)
        self.UNIT_bill.delete(first =0,last = 20)
        self.dis_bill.delete(first = 0 , last =END)
        self.dis_bill.insert(0,0)
        self.QTY_bill.delete(first =0,last =END)
        self.QTY_bill.insert(0,1)
        self.textreceipt_product_name.delete(1,END)
        self.textreceipt_QTY.delete(1,END)
        self.textreceipt_Dis.delete(1,END)
        self.textreceipt_price.delete(1,END)
        self.amount_label.configure(text = 0)
        self.dis_amount.configure(text = 0)	
        self.credit_balance_e.delete(first =0,last = 20)
        self.amount_paid.delete(first =0,last = 20)
        self.Total_discount.delete(first =0,last = 20)
        self.Total_discount.insert(0,0)
        print(check)	
        if int(check) == 0:
            self.bill_creation(0)
        else:
            self.bill_creation(1)

    def bill_creation(self,a):
        self.lineadd='\n\n\n'
        #a = "1"
        #name = "selvan"
        self.lineadd+="===============================================\n"  
        self.lineadd+="                                                                       BILL No :%s\n\n" % self.invoice_no
        self.lineadd+="                                  MSR STORE\n"
        self.lineadd+="                             N.VAIRAVANPATTI\n"
        self.lineadd+="                  Ph: 8825655109 , 9976093574\n"
        print(a)
        if int(a) == 0:
            self.lineadd+="                  GSTINO: 33EWGPS3786D1Z8\n"
        self.lineadd+="                                                                       Date:%s\n" % now.strftime("%x")   
        self.lineadd+="------------------------------------------------------------------\n"
        self.lineadd+="Name: %s\n" % self.customer_bill_value
        self.lineadd+="------------------------------------------------------------------\n"
    
        self.lineadd+="Product                     	                           Qty.        Price\n"
     
        self.lineadd+="------------------------------------------------------------------\n"
        i = 0
        for tem in self.Products_purchased:
            s1 = " "
            s1=(self.product_name[i]) + (s1 * (48-len(self.product_name[i]))) +self.qty_purchased[i]+ s1*(3-len(self.qty_purchased[i])) + s1*10+ s1*(15-len(str(self.bill_temp_total[i]))) +str(self.bill_temp_total[i])+ '\n'
            #print(s1[2])            
            self.lineadd+=s1
            i = i +1
       
        self.lineadd+="------------------------------------------------------------------\n"
        self.lineadd+="                                                                   Sub Total: %s\n"   % (self.total + self.discount_d)
        self.lineadd+="                                                                    Discount: %s\n"   % self.discount_d
        self.lineadd+="                                                                       Total: %s\n"   % self.total
        self.lineadd+="------------------------------------------------------------------\n"

		
        self.lineadd+="For MSR Store:______________________________\n"
   
        self.lineadd+="===============================================\n"
        self.Profit_total = self.total - self.Profit_total
        bill=open('bill.txt','w')

        bill.write(self.lineadd)
   
        bill.close()
        db = sqlite3.connect('billing.db')
        cursor = db.cursor()
        sql = "INSERT INTO invoice_detail(invocieID,invoice_price,customerID,date,week,month,year,profit) VALUES ('%d','%f','%d','%s','%s','%s','%s','%f')" % (self.invoice_no,float(self.total),int(self.customer_id_selected),str(now.strftime("%x")),str(now.strftime("%W")),str(now.strftime("%m")),str(now.strftime("%Y")),float(self.Profit_total))
        cursor.execute(sql)        
        try:
            
            db.commit()
        except:
            db.rollback()
            print("something wrong")
        sql = "select balance from customer_detail where customerID = %d"%(int(self.customer_id_selected))
        cursor.execute(sql)  
        old_balance = cursor.fetchone()
        #print(old_balance[0]+self.cre)
        #print(self.credits)
        sql = "update customer_detail set balance = %d where customerID = %d" % ((float(old_balance[0])+float(self.credits)),int(self.customer_id_selected))
        cursor.execute(sql)        
        try:
            
            db.commit()
        except:
            db.rollback()
            print("something wrong")
        db.close()
        lineadd = " "
        del self.vProduct_name[:]
        del self.vProduct_name_qty[:]
        del self.vProduct_id[:]
        del self.vBatch_No[:]
        del self.vQTY_No[:]
        del self.vcp_1[:]
        del self.vsp_1[:]
        del self.vunit[:]
        del self.vcustomer_name[:]
        del self.customer_ID[:]
        del self.Products_purchased[:]
        del self.product_name[:]
        del self.qty_price[:]
        del self.qty_purchased[:]
        del self.qty_orginal[:]
        del self.discount_1[:]
        del self.bill_temp_total[:]
        self.Profit_total = 0		
        self.total = 0
        self.discount_d= 0
        self.creidts= 0	
        del self.Products_purchased[:]
        del self.product_name[:]
        del self.qty_price[:]
        del self.qty_purchased[:]
        del self.qty_orginal[:]
        self.printbill()

    def printbill(self):
    
        win32api.ShellExecute (0,"print",'bill.txt','/d:"%s"' % win32print.GetDefaultPrinter (),".",0)
        self.controller.show_frame("PageOne")

    def gotopageone(self):
        self.customer_name.delete(first = 0,last= 20)
        self.Product_name_bill.delete(first =0,last = 20)
        self.UNIT_bill.delete(first =0,last = 20)
        self.dis_bill.delete(first = 0 , last =END)
        self.dis_bill.insert(0,0)
        self.QTY_bill.delete(first =0,last =END)
        self.textreceipt_product_name.delete(1,END)
        self.textreceipt_QTY.delete(1,END)
        self.textreceipt_Dis.delete(1,END)
        self.textreceipt_price.delete(1,END)
        self.amount_label.configure(text = 0)
        self.dis_amount.configure(text = 0)
        self.credit_balance_e.delete(first =0,last = 20)
        self.amount_paid.delete(first =0,last = 20)
        self.Total_discount.delete(first =0,last = 20)
        self.Total_discount.insert(0,0)
        del self.vProduct_name[:]
        del self.vProduct_name_qty[:]
        del self.vProduct_id[:]
        del self.vBatch_No[:]
        del self.vQTY_No[:]
        del self.vcp_1[:]
        del self.vsp_1[:]
        del self.vunit[:]
        del self.vcustomer_name[:]
        del self.customer_ID[:]
        del self.Products_purchased[:]
        del self.product_name[:]
        del self.qty_price[:]
        del self.qty_purchased[:]
        del self.qty_orginal[:]
        del self.discount_1[:]
        del self.bill_temp_total[:]
        self.Profit_total = 0		
        self.total = 0
        self.discount_d= 0
        self.creidts= 0	
        del self.Products_purchased[:]
        del self.product_name[:]
        del self.qty_price[:]
        del self.qty_purchased[:]
        del self.qty_orginal[:]
        self.controller.show_frame("PageOne")

    def CurSelect(self,event):
        value =((self.mylistbox_search.get(self.mylistbox_search.curselection())))
        #self.label.configure(text = value) 
        self.Product_name_bill.delete(first =0,last = 20)
        self.UNIT_bill.delete(first =0,last = 20)
        self.dis_bill.delete(first = 0 , last =END)
        self.dis_bill.insert(0,0)
        self.QTY_bill.delete(first =0,last =END)
        self.QTY_bill.insert(0,1)
        self.index_1 = 0
        i =0
        if value in self.vcustomer_name:
            for res in self.vcustomer_name:
                if res == value:
                    self.customer_id_selected = self.customer_ID[i] 
                i = i+1
            self.customer_bill_value =((self.mylistbox_search.get(self.mylistbox_search.curselection())))
            self.customer_name.delete(first =0,last =20)
            self.customer_name.insert(0,self.customer_bill_value)		
        else:
            for ans in self.vProduct_name:
             #print(ans)
            #print(value[0])
                if str(ans) == str(value[0]):
                    #print("success")
                    self.index_2 = self.index_1
                self.index_1  = self.index_1+1
        
            self.Product_name_bill.insert(0, self.vProduct_name[self.index_2])
        #self.Product_id_label.configure(text = self.vProduct_id[self.index_2])
            self.UNIT_bill.insert(0, self.vunit[self.index_2])
    
    def getvalue(self,event):
        #print("getvalue")
        self.master_dbconnect()
        value = str(self.Product_name_bill.get()) 
        self.mylistbox_search.delete(0,END)
        results = process.extract(value,self.vProduct_name,limit=50) 
        for items in results:
            if items[1] > 50 :
                for its in self.vProduct_name_qty:
                    if items[0] == its[0]:
                        self.mylistbox_search.insert(END,its)

#def CurSelect_customer(self,event):
  #      self.customer_bill_value =((self.mylistbox_search.get(self.mylistbox_search.curselection())))
    ##    self.customer_name.delete(first =0,last =20)
        #self.customer_name.insert(0,self.customer_bill_value)
        #self.Product_name_bill.insert(0, self.vProduct_name[self.index_2])
        #self.Product_id_label.configure(text = self.vProduct_id[self.index_2])
        #self.UNIT_bill.insert(0, self.vunit[self.index_2])"""
    
    def getcustomerdetail(self,event):
        self.master_dbconnect()
        value = str(self.customer_name.get()) 
        self.mylistbox_search.delete(0,END)
        results = process.extract(value,self.vcustomer_name,limit = 50)
        for items in results:           
            self.mylistbox_search.insert(END,items[0])

    def master_dbconnect(self):
        self.vProduct_name = []
        self.vProduct_name_qty = []
        self.vProduct_id = []
        self.vBatch_No = []
        self.vQTY_No = []
        self.vcp_1 = []
        self.vsp_1 = []
        self.vunit = []
        self.vcustomer_name = []
        self.customer_ID = []
        db = sqlite3.connect('billing.db')
        cursor = db.cursor()
        sql = "SELECT * FROM master_table"
        cursor.execute(sql)
        self.results_1 = cursor.fetchall()
        for res in self.results_1:
            self.vProduct_name.append(res[4])
            self.vProduct_id.append(res[2])
            self.vBatch_No.append(res[3])
            self.vQTY_No.append(res[5])
            self.vcp_1.append(res[7])
            self.vsp_1.append(res[8])
            self.vunit.append(res[6])
            self.vProduct_name_qty.append((res[4],res[5]))
        sql = "SELECT * FROM customer_detail"
        cursor.execute(sql)
        self.results_1 = cursor.fetchall()
        for res in self.results_1:
            self.vcustomer_name.append(res[1])
            self.customer_ID.append(res[0])
            
        db.close()


class DataEntry(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        #Label(self, text="This is Data Entry Page", font=controller.title_font).grid(row = 1,column =5, sticky ="N",ipady = 10)
        for i in range(0,7):
            Label(self,text="   ", bg = "grey64",width = 20).grid(row = i ,column =0 , sticky = "E",ipady = 46) 
        Button(self, text="Billing Central",
                           command=lambda: controller.show_frame("BillingCentral")).grid(row = 1,column = 0,ipadx = 10)
        Button(self, text="Data Entry",
                           command=lambda: controller.show_frame("DataEntry")).grid(row = 2,column = 0,ipadx = 20)
        Button(self, text="Dashboard",
                           command=lambda: controller.show_frame("Dashboard")).grid(row = 3,column = 0,ipadx = 20)
        #Button(self, text="Exit",
                           #command=quit).grid(row = 4,column = 0,ipadx = 38)
        for i in range(0,11):
            Label(self,text="   ", bg = "grey64",width = 20).grid(row = 0 ,column =i , sticky = "W",ipady = 45) 
        Button(self, text="Add New Item",
                           command=lambda: controller.show_frame("Add_New_Item")).grid(row = 0,column = 3,ipadx = 10)
        Button(self, text="Update QTY/Price",
                           command=lambda: controller.show_frame("Update_QTY_Price")).grid(row = 0,column = 4,ipadx = 20)    
        


class Dashboard(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        top = Frame(self,width = 1350 ,height = 50, bd = 2,relief = "raised")
        top.pack(side = TOP)
        sales = Frame(self,width = 1350,height = 170,bd = 2,relief = "raised")
        sales.pack(side = TOP)
        item_ava = Frame(self,width = 1350,height = 193,bd = 2,relief = "raised")
        item_ava.pack(side = TOP)
        cust = Frame(self,width = 1350,height = 193,bd = 2,relief = "raised")
        cust.pack(side = TOP)
        top_label = Frame(top,width = 1000 ,height = 50, bd = 2,relief = "raised")
        top_label.pack(side = LEFT)  
        top_button = Frame(top,width = 350 ,height = 50, bd = 2,relief = "raised")
        top_button.pack(side = RIGHT)        

        top_label = Label(top_label, text = "DASHBOARD",font = controller.title_font)
        top_label.pack(fill = X,expand = 1,ipadx = 500,pady = 10)
        Button(top_button, text="Main Page",
                           command=lambda: controller.show_frame("PageOne")).pack(side = LEFT,expand =1,padx = 15,pady =5)
        Button(top_button, text="Refresh",command = lambda:self.getvalue()).pack(side = RIGHT,expand =1,padx = 15,pady =5)
        weeks = Frame(sales,width = 337,height = 150,bd = 2,relief = "raised")
        weeks.pack(side = LEFT)
        weekp = Frame(sales,width = 337,height = 150,bd = 2,relief = "raised")
        weekp.pack(side = LEFT)
        months = Frame(sales,width = 337,height = 150,bd = 2,relief = "raised")
        months.pack(side = LEFT)
        monthp = Frame(sales,width = 337,height = 150,bd = 2,relief = "raised")
        monthp.pack(side = LEFT)

        item_available = Frame(item_ava,width = 675,height = 193,bd = 2,relief = "raised")
        item_available.pack(side = LEFT)
        most_bought = Frame(item_ava,width = 675,height = 193,bd = 2,relief = "raised")
        most_bought.pack(side = LEFT)
        best_customer = Frame(cust,width = 675,height = 193,bd = 2,relief = "raised")
        best_customer.pack(side = LEFT)
        items_needed = Frame(cust,width = 675,height = 193,bd = 2,relief = "raised")
        items_needed.pack(side = LEFT)
        Label(weeks, text = "Weekly Sales",font = controller.title_font).pack(side = TOP,fill = X,expand = 1,ipadx = 89,pady = 10)
        Label(weekp, text = "Weekly Profit",font = controller.title_font).pack(side = TOP,fill = X,expand = 1,ipadx = 87,pady = 10)
        Label(months, text = "monthly Sales",font = controller.title_font).pack(side = TOP,fill = X,expand = 1,ipadx = 87,pady = 10)
        Label(monthp, text = "monthly Profit",font = controller.title_font).pack(side = TOP,fill = X,expand = 1,ipadx = 85,pady = 10)
        self.week_sales_value = Entry(weeks,font = controller.title_font)
        self.week_sales_value.pack(side = TOP,fill = X,expand = 1,ipadx = 35,ipady = 20)
        self.week_profit_value = Entry(weekp,font = controller.title_font)
        self.week_profit_value.pack(side = TOP,fill = X,expand = 1,ipadx = 35,ipady = 20)
        self.month_sales_value = Entry(months,font = controller.title_font)
        self.month_sales_value.pack(side = TOP,fill = X,expand = 1,ipadx = 35,ipady = 20)
        self.month_profit_value = Entry(monthp,font = controller.title_font)
        self.month_profit_value.pack(side = TOP,fill = X,expand = 1,ipadx = 35,ipady = 20)		
        #self.mylistbox_C_brief = Listbox(item_available,font = ('times',13))
        #self.mylistbox_C_brief.pack(side = LEFT,fill = X,expand = 1,ipadx = 325,ipady = 62)
        Label(item_available, text = "Best customer",font = controller.content_font).pack(side = TOP,fill = X,expand = 1,ipadx = 0,pady = 20)
        Label(most_bought, text = "Products Available",font = controller.content_font).pack(side = TOP,fill = X,expand = 1,ipadx = 0,pady = 20)
        Label(best_customer, text = "Most Bought Product",font = controller.content_font).pack(side = TOP,fill = X,expand = 1,ipadx = 0,pady = 20)		
        self.mylistbox_M_brief = Text( best_customer, font = controller.content_font,height = 50,width = 50 )
        self.mylistbox_M_brief.pack(side = LEFT,ipadx = 325,ipady = 62)
        self.mylistbox_C_brief = Text( item_available, font = controller.content_font,height = 50,width = 50 )
        self.mylistbox_C_brief.pack(side = LEFT,ipadx = 325,ipady = 62)
        #self.mylistbox_C_brief.insert(END,"Best Customer\nCustomer Name,Total Sales,Credit balance\n")
        self.mylistbox_P_brief = Text( most_bought, font = controller.content_font,height = 50,width = 50 )
        self.mylistbox_P_brief.pack(side = LEFT,ipadx = 325,ipady = 62)
        #self.mylistbox_P_brief.insert(END,"Product Name,Qty,Unit,Cost Price,Selling price\n")
        customer_scroll = Scrollbar(self.mylistbox_C_brief,orient = "vertical")
        customer_scroll.config(command=self.mylistbox_C_brief.yview)
        customer_scroll.pack(side="right", fill="y")
        product_scroll = Scrollbar(self.mylistbox_P_brief,orient = "vertical")
        product_scroll.config(command=self.mylistbox_P_brief.yview)
        product_scroll.pack(side="right", fill="y")
        customer_scroll_1 = Scrollbar(self.mylistbox_M_brief,orient = "vertical")
        customer_scroll_1.config(command=self.mylistbox_M_brief.yview)
        customer_scroll_1.pack(side="right", fill="y")
        self.getvalue()

    def getvalue(self):
        #print("getvalue")
        self.master_dbconnect()
        #value = str(self.entry.get()) 
        self.mylistbox_P_brief.delete('1.0',END)
        self.mylistbox_M_brief.delete('1.0',END)
        self.mylistbox_C_brief.delete('1.0',END)
        self.week_sales_value.delete(0,END)
        self.week_profit_value.delete(0,END)
        self.month_sales_value.delete(0,END)
        self.month_profit_value.delete(0,END)		
        #results = process.extract(value,self.vProduct_name,limit = 4) 
        self.week_sales_value.insert(0,str(self.weekly_sales[0]))
        self.week_profit_value.insert(0,str(self.weekly_sales[1]))
        self.month_sales_value.insert(0,str(self.monthly_sales[0]))
        self.month_profit_value.insert(0,str(self.monthly_sales[1]))
        self.mylistbox_C_brief.insert(END,"Customer Name,Total Sales,Credit balance\n")
        self.mylistbox_P_brief.insert(END,"Product Name , Qty , Unit , Cost Price , Selling price\n")
        self.mylistbox_M_brief.insert(END,"Product Name , Cost Price, Selling Price, count\n")		
        for items in self.vout:
            self.mylistbox_P_brief.insert(END,items)
            self.mylistbox_P_brief.insert(END,"\n")
        for items in self.vout_1:
            self.mylistbox_C_brief.insert(END,items)
            self.mylistbox_C_brief.insert(END,"\n")
        for items in self.mostout:
            self.mylistbox_M_brief.insert(END,items)
            self.mylistbox_M_brief.insert(END,"\n")

    def master_dbconnect(self):
        self.vout = []
        self.mostout = []
        self.vout_1 = []
        self.weekly_sales = 0
        self.monthly_sales = 0
        db = sqlite3.connect('billing.db')
        cursor = db.cursor()
        sql = "SELECT * FROM master_table"
        cursor.execute(sql)
        self.results_1 = cursor.fetchall()
        for res in self.results_1:
            self.vout.append((res[4],",",res[5],",",res[6],",",res[7],",",res[8]))
        sql = "SELECT Product_name,CP,SP,count(b.Product_ID	) FROM master_table a inner join invoice b on a.Product_ID = b.Product_ID group by b.Product_ID Order by count(b.Product_ID) Desc"
        cursor.execute(sql)
        self.results_1 = cursor.fetchall()
        for res in self.results_1:
            self.mostout.append((res[0],",",res[1],",",res[2],",",res[3]))
        sql = "select customer_name,sum(b.invoice_price),balance from customer_detail a inner join invoice_detail b on a.customerID=b.customerID group by a.customerID order by sum(b.invoice_price) desc"
        cursor.execute(sql)
        self.results_2 = cursor.fetchall()
        for res in self.results_2:
            self.vout_1.append((res[0],",",res[1],",",res[2]))
        current_week = now.strftime("%W")
        current_year = now.strftime("%Y")
        sql = "SELECT sum(invoice_price), sum(profit)FROM invoice_detail where week = '%s' and year ='%s' " % (str(current_week),str(current_year))
        cursor.execute(sql)
        self.weekly_sales = cursor.fetchone()
        current_month = now.strftime("%m")
        sql = "SELECT sum(invoice_price), sum(profit)FROM invoice_detail where month = '%s' and year ='%s' " % (str(current_month),str(current_year))
        cursor.execute(sql)
        self.monthly_sales = cursor.fetchone()
		
        db.close()


class Add_New_Item(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        top = Frame(self,width = 1350 ,height = 100, bd = 2,relief = "raised")
        top.pack(side = TOP)
        left = Frame(self,width = 900,height = 590,bd = 2,relief = "raised")
        left.pack(side = LEFT)
        right = Frame(self,width = 450,height = 590,bd = 2,relief = "raised")
        right.pack(side = RIGHT)
        right_top = Frame(right,width = 450,height = 495,bd = 2,relief = "raised")
        right_top.pack(side = TOP)
        right_bottom = Frame(right,width = 450,height = 95,bd = 1,relief = "raised")
        right_bottom.pack(side = BOTTOM)
        left_product_id = Frame(left,width = 900,height = 98,bd = 1,relief = "raised")
        left_product_id.pack(side = TOP)
        left_product_name = Frame(left,width = 900,height =98,bd = 1,relief = "raised")
        left_product_name.pack(side = TOP)
        left_product_QTY = Frame(left,width = 900,height = 99,bd = 1,relief = "raised")
        left_product_QTY.pack(side = TOP)
        left_product_price = Frame(left,width = 900,height = 98,bd = 1,relief = "raised")
        left_product_price.pack(side = TOP)
        left_vendor = Frame(left,width = 900,height = 98,bd = 1,relief = "raised")
        left_vendor.pack(side = TOP)
        left_button = Frame(left,width = 900,height = 98,bd = 1,relief = "raised")
        left_button.pack(side = TOP)
        top_label = Label(top, text = "UPDATE QTY/PRICE",font = controller.title_font)
        top_label.pack(fill = X,expand = 1,ipadx = 1000,ipady = 25)	
        Label(left_product_id, text="Product ID", font=controller.content_font).pack(side = LEFT,padx = 50,pady =30)
        self.Product_id_label = Entry(left_product_id)
        self.Product_id_label.pack(side = LEFT,fill = X,expand = 1,ipadx = 15,ipady = 5,padx = 50)
        self.Batch_no_label = Entry(left_product_id)
        self.Batch_no_label.pack(side = RIGHT,fill = X,expand = 1,ipadx = 15,ipady = 5,padx =50,pady = 35)
        Label(left_product_id, text="Batch_No", font=controller.content_font).pack(side = RIGHT,padx = 50)
        Label(left_product_name, text="Product name", font=controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 10,ipady = 30,padx = 15)
        self.Product_name_label = Entry(left_product_name)
        self.Product_name_label.pack(side =LEFT,padx = 147,ipadx =150,ipady =5)
        Label(left_product_QTY, text="QTY", font=controller.content_font).pack(side = LEFT,padx = 50,pady =30)
        self.QTY = Entry(left_product_QTY)
        self.QTY.pack(side = LEFT,fill = X,expand = 1,ipadx = 15,ipady = 5,padx = 75)
        self.UNIT_label = Entry(left_product_QTY)
        self.UNIT_label.pack(side = RIGHT,fill = X,expand = 1,ipadx = 15,ipady = 5,padx =77,pady = 35)
        Label(left_product_QTY, text="unit", font=controller.content_font).pack(side = RIGHT,padx = 50)
        Label(left_product_price, text="Cost price", font=controller.content_font).pack(side = LEFT,padx = 50,pady =30)
        self.CP = Entry(left_product_price)
        self.CP.pack(side = LEFT,fill = X,expand = 1,ipadx = 40,ipady = 5,padx = 20)
        self.SP = Entry(left_product_price)
        self.SP.pack(side = RIGHT,fill = X,expand = 1,ipadx = 40,ipady = 5,padx =20,pady = 35)
        Label(left_product_price, text="Selling price", font=controller.content_font).pack(side = RIGHT,padx = 50)
        Label(left_vendor, text="vendor name", font=controller.content_font).pack(side = LEFT,padx = 20,pady =30)
        self.vendor_name = Entry(left_vendor)
        self.vendor_name.bind('<Key>',self.getvalue)
        self.vendor_name.pack(side = LEFT,fill = X,expand = 1,ipadx = 20,ipady = 5,padx = 30)
        update_button = Button(left_vendor, text="Add vendor",command=lambda:controller.show_frame("new_vendor"))
        update_button.pack(side = RIGHT,fill = X,expand = 1,ipadx = 10 ,padx =10,pady =10) 
        self.phone_number = Entry(left_vendor)
        self.phone_number.pack(side = RIGHT,fill = X,expand = 1,ipadx = 20,ipady = 5,padx =30,pady = 35)
        Label(left_vendor, text="Phone_number", font=controller.content_font).pack(side = RIGHT,padx = 20)

        update_button = Button(left_button, text="Add Item",command=self.update)
        update_button.pack(fill = X,expand = 1,ipadx = 50 ,padx =367,pady =27)
       
        #self.label = Label(right)
        #self.label.grid(row =4,column =0)
        self.mylistbox = Listbox(right_top,font = ('times',13))
        self.mylistbox.pack(side = TOP,fill = X,expand = 1,ipadx = 200,ipady = 80)

        self.mylistbox.bind('<<ListboxSelect>>',self.CurSelect)
        Button(right_bottom, text="cancel",command=lambda:controller.show_frame("PageOne")).pack(side = BOTTOM,fill = X,expand = 1,ipadx = 10 ,padx =190,pady =80)
       
        db = sqlite3.connect('billing.db')
        cursor = db.cursor()
        sql = "SELECT max(Product_ID) FROM master_table"
        cursor.execute(sql)
        output = cursor.fetchone()
        if output[0] is None:
            a = 0
        else:    
            a = int(output[0])
        
        self.Product_id_label.insert(0,a+1)

    def getvalue(self,event):
        #print("getvalue")
        self.master_dbconnect()
        value = str(self.vendor_name.get()) 
        self.mylistbox.delete(0,END)
        results = process.extract(value,self.vvendor_name,limit = 50) 
        for items in results:
            if items[1] > 50 :
                self.mylistbox.insert(END,items[0])

		
    def update(self):
        self.Product_id_value = self.Product_id_label.get()
        self.Batch_no_value = self.Batch_no_label.get()
        self.Product_name_value = self.Product_name_label.get()
        self.QTY_value = self.QTY.get()
        self.UNIT_value = self.UNIT_label.get()
        self.CP_value = self.CP.get()
        self.SP_value = self.SP.get()
        #self.vendor_name_value = self.vendor_name.get()
        #self.phone_number_value = self.phone_number.get()
        self.dbconnect()

    def CurSelect(self,event):
        value =str((self.mylistbox.get(self.mylistbox.curselection())))
        #self.label.configure(text = value) 
        i =0
        for res in self.vvendor_name:
            if res == value:
                self.vendor_name_selected = self.vvendor_name[i] 
                self.vendor_id_selected = self.vvendor_id[i] 
                self.vendor_Phone_number_selected = self.vvendor_Phone_number[i] 
            i = i+1

        self.vendor_name.delete(first =0,last =20)
        self.vendor_name.insert(0,self.vendor_name_selected)		
        self.phone_number.delete(first =0,last =20)
        self.phone_number.insert(0,self.vendor_Phone_number_selected)		
		
    def dbconnect(self):
        db = sqlite3.connect('billing.db')
        cursor = db.cursor()
        sql = "INSERT INTO master_table(vendorID,Product_ID,Batch_No,Product_name,QTY, Unit,CP,SP) VALUES ('%d','%d', '%s', '%s', '%d', '%s','%f','%f' )" % (int(self.vendor_id_selected),int(self.Product_id_value), self.Batch_no_value,self.Product_name_value,int(self.QTY_value),self.UNIT_value,float(self.CP_value),float(self.SP_value) )
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("something wrong")
        self.Product_id_label.delete(first = 0 , last =END)
        sql = "SELECT max(Product_ID) FROM master_table"
        cursor.execute(sql)
        output = cursor.fetchone()
        a = output[0]
        self.Product_id_label.insert(0,a+1)
        db.close()
        #self.Product_id.delete(first = 0 , last =END)
        self.Batch_no_label.delete(first = 0 , last =END)
        self.Product_name_label.delete(first = 0 , last =END)
        self.QTY.delete(first = 0 , last =END)
        self.UNIT_label.delete(first = 0 , last =END)
        self.CP.delete(first = 0 , last =END)
        self.SP.delete(first = 0 , last =END)
        self.vendor_name.delete(first = 0 , last =END)
        self.phone_number.delete(first = 0 , last =END)

        self.controller.show_frame("PageOne")

    def master_dbconnect(self):
        self.vvendor_name = []
        self.vvendor_id = []
        self.vvendor_Phone_number = []
        
        db = sqlite3.connect('billing.db')
        cursor = db.cursor()
        sql = "SELECT vendorID,vendor_name,Phone_number FROM vendor_detail"
        cursor.execute(sql)
        self.results_1 = cursor.fetchall()
        for res in self.results_1:
            self.vvendor_name.append(res[1])
            self.vvendor_id.append(res[0])
            self.vvendor_Phone_number .append(res[2])


        db.close()
		


class Update_QTY_Price(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        top = Frame(self,width = 1350 ,height = 100, bd = 2,relief = "raised")
        top.pack(side = TOP)
        left = Frame(self,width = 900,height = 590,bd = 2,relief = "raised")
        left.pack(side = LEFT)
        right = Frame(self,width = 450,height = 590,bd = 2,relief = "raised")
        right.pack(side = RIGHT)
        right_top = Frame(right,width = 450,height = 495,bd = 2,relief = "raised")
        right_top.pack(side = TOP)
        right_bottom = Frame(right,width = 450,height = 95,bd = 1,relief = "raised")
        right_bottom.pack(side = BOTTOM)
        left_product_id = Frame(left,width = 900,height = 98,bd = 1,relief = "raised")
        left_product_id.pack(side = TOP)
        left_product_name = Frame(left,width = 900,height =98,bd = 1,relief = "raised")
        left_product_name.pack(side = TOP)
        left_product_QTY = Frame(left,width = 900,height = 99,bd = 1,relief = "raised")
        left_product_QTY.pack(side = TOP)
        left_product_price = Frame(left,width = 900,height = 98,bd = 1,relief = "raised")
        left_product_price.pack(side = TOP)
        left_vendor = Frame(left,width = 900,height = 98,bd = 1,relief = "raised")
        left_vendor.pack(side = TOP)
        left_button = Frame(left,width = 900,height = 98,bd = 1,relief = "raised")
        left_button.pack(side = TOP)
        top_label = Label(top, text = "UPDATE QTY/PRICE",font = controller.title_font)
        top_label.pack(fill = X,expand = 1,ipadx = 1000,ipady = 25)	
        Label(left_product_id, text="Product ID", font=controller.content_font).pack(side = LEFT,padx = 50,pady =30)
        self.Product_id_label = Entry(left_product_id)
        self.Product_id_label.pack(side = LEFT,fill = X,expand = 1,ipadx = 15,ipady = 5,padx = 50)
        self.Batch_no_label = Entry(left_product_id)
        self.Batch_no_label.pack(side = RIGHT,fill = X,expand = 1,ipadx = 15,ipady = 5,padx =50,pady = 35)
        Label(left_product_id, text="Batch_No", font=controller.content_font).pack(side = RIGHT,padx = 50)
        Label(left_product_name, text="Product name", font=controller.content_font).pack(side = LEFT,fill = X,expand = 1,ipadx = 10,ipady = 30,padx = 15)
        self.Product_name_label = Entry(left_product_name)
        self.Product_name_label.pack(side =LEFT,padx = 147,ipadx =150,ipady =5)
        Label(left_product_QTY, text="QTY", font=controller.content_font).pack(side = LEFT,padx = 50,pady =30)
        self.QTY = Entry(left_product_QTY)
        self.QTY.pack(side = LEFT,fill = X,expand = 1,ipadx = 15,ipady = 5,padx = 75)
        self.UNIT_label = Entry(left_product_QTY)
        self.UNIT_label.pack(side = RIGHT,fill = X,expand = 1,ipadx = 15,ipady = 5,padx =77,pady = 35)
        Label(left_product_QTY, text="unit", font=controller.content_font).pack(side = RIGHT,padx = 50)
        Label(left_product_price, text="Cost price", font=controller.content_font).pack(side = LEFT,padx = 50,pady =30)
        self.CP = Entry(left_product_price)
        self.CP.pack(side = LEFT,fill = X,expand = 1,ipadx = 25,ipady = 5,padx = 35)
        self.SP = Entry(left_product_price)
        self.SP.pack(side = RIGHT,fill = X,expand = 1,ipadx = 25,ipady = 5,padx =35,pady = 35)
        Label(left_product_price, text="Selling price", font=controller.content_font).pack(side = RIGHT,padx = 50)
        Label(left_vendor, text="vendor name", font=controller.content_font).pack(side = LEFT,padx = 20,pady =30)
        self.vendor_name = Entry(left_vendor)
        self.vendor_name.pack(side = LEFT,fill = X,expand = 1,ipadx = 15,ipady = 5,padx = 62)
        self.phone_number = Entry(left_vendor)
        self.phone_number.pack(side = RIGHT,fill = X,expand = 1,ipadx = 15,ipady = 5,padx =61,pady = 35)
        Label(left_vendor, text="Phone_number", font=controller.content_font).pack(side = RIGHT,padx = 20)
      
        update_button = Button(left_button, text="Update Item",command=self.update)
        update_button.pack(fill = X,expand = 1,ipadx = 50 ,padx =360,pady =27)

        Label(right_top, text="Search Product", font=controller.content_font).pack(side = TOP,padx = 20)        
        self.entry = Entry(right_top)
        self.entry.bind('<Key>',self.getvalue)
        self.entry.pack(side = TOP,fill = X,expand = 1,ipadx = 200,ipady = 2)
       
        #self.label = Label(right)
        #self.label.grid(row =4,column =0)
        self.mylistbox = Listbox(right_top,font = ('times',13))
        self.mylistbox.pack(side = TOP,fill = X,expand = 1,ipadx = 200,ipady = 70)

        self.mylistbox.bind('<<ListboxSelect>>',self.CurSelect)
        Button(right_bottom, text="cancel",command=lambda:controller.show_frame("PageOne")).pack(side = BOTTOM,fill = X,expand = 1,ipadx = 10 ,padx =190,pady =80)

    def CurSelect(self,event):
        value =str((self.mylistbox.get(self.mylistbox.curselection())))
        #self.label.configure(text = value) 
        self.index_1 = 0
        self.Product_name_label.delete(first = 0 , last =END)
        self.UNIT_label.delete(first = 0 , last =END)
        self.Product_id_label .delete(first = 0 , last =END)

        for ans in self.vProduct_name:
            if ans == value:
                self.index_2 = self.index_1
                temp = self.mvendor_id[self.index_2]
                i = 0 
                #print(float(temp)) 
                for x in self.vvendor_id:
                    #print(str(x))
                    if float(temp) == float(x):
                        self.vendor_name.insert(0,self.vvendor_name[i])
                        self.phone_number.insert(0,self.vvendor_number[i])
                    i = i+1    
            self.index_1  = self.index_1+1
        
        self.Product_name_label.insert(0,self.vProduct_name[self.index_2])
        self.Product_id_label.insert(0,self.vProduct_id[self.index_2])
        self.UNIT_label.insert(0,self.vunit[self.index_2])
        #self.vendor_name.insert(0,self.vvendor_name[self.index_2])
        #elf.phone_number.insert(0,self.vvendor_number[self.index_2])



    def update(self):
        self.Batch_no_value = self.Batch_no_label.get()
        self.QTY_value = self.QTY.get()
        self.CP_value = self.CP.get()
        self.SP_value = self.SP.get()
        self.update_dbconnect()		

    def update_dbconnect(self):
        db = sqlite3.connect('billing.db')
        cursor = db.cursor()
        temp = int(self.QTY_value)+int(self.vQTY_No[self.index_2])
        sql = "UPDATE master_table SET QTY = %d,CP = %f,SP=%f WHERE Product_ID = %d " % (int(temp),float(self.CP_value),float(self.SP_value) ,int(self.vProduct_id[self.index_2]))
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("something wrong")
        db.close()
        #self.Product_id_label .delete(first = 0 , last =END)
        self.Batch_no_label.delete(first = 0 , last =END)
        self.Product_name_label.delete(first = 0 , last =END)
        self.QTY.delete(first = 0 , last =END)
        self.UNIT_label.delete(first = 0 , last =END)
        self.CP.delete(first = 0 , last =END)
        self.SP.delete(first = 0 , last =END)
        self.vendor_name.delete(first = 0 , last =END)
        self.phone_number.delete(first = 0 , last =END)
        self.controller.show_frame("PageOne")

    def getvalue(self,event):
        #print("getvalue")
        self.master_dbconnect()
        value = str(self.entry.get()) 
        self.mylistbox.delete(0,END)
        results = process.extract(value,self.vProduct_name,limit = 50) 
        for items in results:
            if items[1] > 50 :
                self.mylistbox.insert(END,items[0])

    def master_dbconnect(self):
        self.vProduct_name = []
        self.vProduct_id = []
        self.vBatch_No = []
        self.vQTY_No = []
        self.vcp_1 = []
        self.vsp_1 = []
        self.vunit = []
        self.mvendor_id=[]
        self.vvendor_id = []
        self.vvendor_name = []
        self.vvendor_number = []
        db = sqlite3.connect('billing.db')
        cursor = db.cursor()
        sql = "SELECT * FROM master_table"
        cursor.execute(sql)
        self.results_1 = cursor.fetchall()
        for res in self.results_1:
            self.vProduct_name.append(res[4])
            self.vProduct_id.append(res[2])
            self.vBatch_No.append(res[3])
            self.vQTY_No.append(res[5])
            self.vcp_1.append(res[7])
            self.vsp_1.append(res[8])
            self.vunit.append(res[6])
            self.mvendor_id.append(res[1])
        sql = "SELECT vendorID,vendor_name,Phone_number  FROM vendor_detail"
        cursor.execute(sql)
        self.results_1 = cursor.fetchall()
        for res in self.results_1:
            self.vvendor_name.append(res[1])
            self.vvendor_number.append(res[2])
            self.vvendor_id.append(res[0])

        db.close()

if __name__ == "__main__":
    app = SampleApp()
    app.title("Billing Software")
    app.geometry("1350x690") # size of the window width:- 500, height:- 375
    app.resizable(0, 0)
    #app.attributes("-fullscreen", True)
    app.wm_iconbitmap('favicon.ico')
    app.mainloop()
