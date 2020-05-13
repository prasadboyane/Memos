from tkinter import *
from tkinter import ttk
from MEMO_Project import *

class login_cls:

    user = 'admin'
    passw ='admin'

    def __init__(self,root):
        self.root = root
        self.root.title('LOGIN TO MEMO')
        
        rows = 0
        while rows<10:
            self.root.rowconfigure(rows, weight=1)
            self.root.columnconfigure(rows, weight=1)
            rows+=1

        frame = LabelFrame(self.root, text=' Login ')
        frame.grid(row = 1,column = 1,columnspan=10,rowspan=10)

        Label(frame, text = ' Usename ').grid(row = 2, column = 1, sticky = W)
        self.username = Entry(frame)
        self.username.grid(row = 2,column = 2, padx=(10, 10),pady=(5, 5))

        Label(frame, text = ' Password ').grid(row = 5, column = 1, sticky = W)
        self.password = Entry(frame, show='*')
        self.password.grid(row = 5, column = 2, padx=(10, 10),pady=(5, 5))

        ttk.Button(frame, text = 'LOGIN',command = self.login_user).grid(row=7,column=2, padx=(10, 10),pady=(5, 5))
        
        self.message = Label(text = '',fg = 'Red')
        self.message.grid(row=9,column=6)

    def login_user(self):
        
        '''check in database if creds are correct or not '''
        
        config = {
            'host': 'localhost',
            'user': 'root',
            'passwd': 'root',
            'host': 'localhost',
            'database': 'memos',
            'autocommit': True
        }

        #mydb= mysql.connector.connect(host="localhost",user='root',passwd='root',database ='memos',autocommit= True)
        mydb= mysql.connector.connect(**config)
        mycr= mydb.cursor(buffered=True)
        
        query="select * from users where username='{}' and password='{}'".format(self.username.get(),self.password.get())
        mycr.execute(query)
        cnt = mycr.rowcount
        mycr.close()
        mydb.close()
        
        '''Check username and password entered are correct'''
        if cnt != 0 or (self.username.get() == 'admin' and self.password.get()== "admin"):
            
            curr_usr = self.username.get()
            #Destroy the current window
            root.destroy()
            
            #Open new window
            newroot = Tk()
            application = Memo_window(newroot,curr_usr)
            newroot.mainloop()

        else:

            '''Prompt user that either id or password is wrong'''
            self.message['text'] = 'Username or Password incorrect. Try again!'


        


if __name__ == '__main__':

    root = Tk()
    root.geometry('425x225')
    application = login_cls(root)
    root.mainloop()
