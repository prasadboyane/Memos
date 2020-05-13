''' IMPORTING NECCESARY PACKAGES'''

from tkinter import *
from tkinter import ttk
import datetime
import time
import tkinter.messagebox
import mysql.connector

''' IMPORTING SUCCESSFUL'''

''' CREATING CLASS'''


class Memo_window:

    def __init__(self, root, curr_user):
        self.root = root
        self.root.geometry('655x525+600+200')
        self.root.title('Your Memos')
        self.curr_user=curr_user

        '''Logo and Title'''

        self.photo = PhotoImage(file='memo.png')
        self.label = Label(image=self.photo)
        self.label.grid(row=0, column=0)

#        self.label1 = Label(font=('arial', 15, 'bold'), text='School Portal System', fg='dark blue')
#        self.label1.grid(row=8, column=0)

        ''' New Records '''
        frame = LabelFrame(self.root, text='Add New Memo ')
        frame.grid(row=0, column=1)

        Label(frame, text='Title:').grid(row=1, column=1, sticky=W,padx=(10, 10))
        self.title = Entry(frame)
        self.title.grid(row=1, column=2,padx=(10, 10),pady=(5, 5))

        Label(frame, text='Body:').grid(row=2, column=1, sticky=W,padx=(10, 10))
        self.body = Entry(frame)
        self.body.grid(row=2, column=2,padx=(10, 10),pady=(5, 5))

        

        '''Add Button'''
        ttk.Button(frame, text='Add Memo', command=self.add).grid(row=7, column=2,pady=(20, 20))

        '''Message Display'''
        self.message = Label(text='', fg='Red')
        self.message.grid(row=8, column=1)

        '''Database Table display box '''
        self.tree = ttk.Treeview(height=10, column=['', '', '', ''])
        self.tree.grid(row=9, column=0, columnspan=2)
        self.tree.heading('#0', text='User')
        self.tree.column('#0', width=60)
        self.tree.heading('#1', text='Title')
        self.tree.column('#1', width=100)
        self.tree.heading('#2', text='Body')
        self.tree.column('#2', width=280)
        self.tree.heading('#3', text='Create date')
        self.tree.column('#3', width=100)
        self.tree.heading('#4', text='Modified date')
        self.tree.column('#4', width=112)

        '''Time and Date'''

        def tick():
            d = datetime.datetime.now()
            today = '{:%B %d,%Y}'.format(d)

            mytime = time.strftime('%I:%M:%S%p')
            self.lblInfo.config(text=(mytime + '\t' + today))
            self.lblInfo.after(200, tick)

        self.lblInfo = Label(font=('arial', 20), fg='Dark Blue')
        self.lblInfo.grid(row=10, column=0, columnspan=2)
        tick()

        ''' Menu Bar '''
        Chooser = Menu()
        itemone = Menu()

        itemone.add_command(label='Add Record', command=self.add)
        itemone.add_command(label='Edit Record', command=self.edit)
        itemone.add_command(label='Delete Record', command=self.delet)
        itemone.add_separator()
        itemone.add_command(label='Help', command=self.help)
        itemone.add_command(label='Exit', command=self.ex)

        Chooser.add_cascade(label='File', menu=itemone)
        Chooser.add_command(label='Add', command=self.add)
        Chooser.add_command(label='Edit', command=self.edit)
        Chooser.add_command(label='Delete', command=self.delet)
        if self.curr_user=='admin':
            Chooser.add_command(label='Add user', command=self.add_user)
        Chooser.add_command(label='Help', command=self.help)
        Chooser.add_command(label='Exit', command=self.ex)

        root.config(menu=Chooser)
        self.veiwing_records()

    ''' View Database Table'''
    records=''
    def run_query(self, query):
        config = {
            'host': 'localhost',
            'user': 'root',
            'passwd': 'root',
            'host': 'localhost',
            'database': 'memos',
            'autocommit': True
        }
        mydb= mysql.connector.connect(**config)
        mycr= mydb.cursor(buffered=True)
        
        if (query.find('SELECT *') != -1): 
           mycr.execute(query)
           query_result = mycr.fetchall()
        else:
           query_result = mycr.execute(query)
           
        mycr.close()
        mydb.close()
        return query_result

    def veiwing_records(self):
         records = self.tree.get_children()
         for element in records:
             self.tree.delete(element)
         query = 'SELECT * FROM user_memo where username="{}"'.format(self.curr_user)
         db_table = self.run_query(query)
         for data in db_table:
            self.tree.insert('', 1000, text=data[0], values=data[1:])

    ''' Add New Record '''

    def validation(self):
         return len(self.title.get()) != 0 and len(self.body.get()) != 0
 
    def add_record(self):
         if self.validation():
             query = "INSERT INTO user_memo VALUES ('{}','{}','{}',current_timestamp(),current_timestamp())".format(self.curr_user,self.title.get(), self.body.get())
             self.run_query(query)
             self.message['text'] = 'Memo added!'.format(self.title.get())
 
             '''Empty the fields'''
             self.title.delete(0, END)
             self.body.delete(0, END)
 
         else:
             self.message['text'] = 'Fields not completed! Complete all fields...'
 
         self.veiwing_records()
 
    '''Function for using buttons'''
 
    def add(self):
         ad = tkinter.messagebox.askquestion('Add Memo', 'Do you want to add a New Memo?')
         if ad == 'yes':
             self.add_record()
 
    ''' Deleting a Record '''
 
    def delete_record(self):
        # To clear output
        self.message['text'] = ''
    
        try:
            
            self.tree.item(self.tree.selection())['values'][0]
    
        except IndexError as e:
            self.message['text'] = 'Please select a record to delete!'
            return
        
        # Again clear output
        self.message['text'] = ''
        
        title = self.tree.item(self.tree.selection())['values'][0]
        query = 'DELETE FROM user_memo WHERE title = "{}" and username="{}"'.format(title,self.curr_user)
        
        self.run_query(query)
        self.message['text'] = 'Memo {} deleted!'.format(title)
        
        # Printing new database
        
        self.veiwing_records()
    
     # Function to add functionality in buttons
 
    def delet(self):
        de = tkinter.messagebox.askquestion('Delete Record', 'Are you sure you want to delete this Record?')
        if de == 'yes':
            self.delete_record()


    '''Add User'''
    
    def add_user_final(self, new_username,new_pass,new_confirm_pass):
        if new_pass == new_confirm_pass:
            query = "INSERT INTO users VALUES('{}','{}')".format(new_username, new_pass)
            self.run_query(query)
            self.add_user_root.destroy()
            self.message['text'] = '{}: New User Added !'.format(new_username)
        else:
            tkinter.messagebox.showinfo('Password Mismatch','Please make sure to re-type passwords correctly.')
        self.veiwing_records()

    def add_user_1(self):
        self.add_user_root = Toplevel()
        self.add_user_root.title('Add User')
        self.add_user_root.geometry('305x355+600+200')
 
        
        Label(self.add_user_root, text='User Name').grid(row=1, column=1, sticky=W,padx=(10, 10),pady=(5, 5))
        new_username = Entry(self.add_user_root , textvariable=StringVar(self.add_user_root))
        new_username.grid(row=1, column=2,padx=(10, 10),pady=(5, 5))
        
        Label(self.add_user_root, text='New Password').grid(row=3, column=1, sticky=W,padx=(10, 10),pady=(5, 5))
        new_pass = Entry(self.add_user_root,textvariable=StringVar(self.add_user_root))
        new_pass.grid(row=3, column=2,padx=(10, 10),pady=(5, 5))
        
        Label(self.add_user_root, text='Confirm Password').grid(row=5, column=1, sticky=W,padx=(10, 10),pady=(5, 5))
        new_confirm_pass = Entry(self.add_user_root,textvariable=StringVar(self.add_user_root))
        new_confirm_pass.grid(row=5, column=2,padx=(10, 10),pady=(5, 5))
 
        Button(self.add_user_root, text='Add User', command=lambda: self.add_user_final(new_username.get(), new_pass.get(), new_confirm_pass.get())).grid(row=12, column=2, sticky=W,padx=(10, 10),pady=(5, 5))
 
        self.add_user_root.mainloop()    
    
    def add_user(self):
        anu = tkinter.messagebox.askquestion('Add user', 'Are you sure?')
        if anu == 'yes':
            self.add_user_1()

    '''EDIT RECORD'''
 
    '''CREATING A POP UP WINDOW FOR EDIT'''
 
    def edit_box(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
 
        except IndexError as e:
            self.message['text'] = 'Please select a Memo to Edit!'
            return
 
        title = self.tree.item(self.tree.selection())['values'][0]
        body = self.tree.item(self.tree.selection())['values'][1]
 
        self.edit_root = Toplevel()
        self.edit_root.title('Edit Memo')
        self.edit_root.geometry('305x355+600+200')
 
        Label(self.edit_root, text='Old Title').grid(row=0, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=title), state='readonly').grid(row=0,
                                                                                                          column=2)
        Label(self.edit_root, text='New Title').grid(row=1, column=1, sticky=W)
        new_title = Entry(self.edit_root , textvariable=StringVar(self.edit_root, value=title))
        new_title.grid(row=1, column=2)

        Label(self.edit_root, text='Old Body').grid(row=2, column=1, sticky=W)
        Entry(self.edit_root, textvariable=StringVar(self.edit_root, value=body), state='readonly').grid(row=2,
                                                                                                          column=2)
        Label(self.edit_root, text='New Body').grid(row=3, column=1, sticky=W)
        new_body = Entry(self.edit_root,textvariable=StringVar(self.edit_root, value=body))
        new_body.grid(row=3, column=2)
 
        Button(self.edit_root, text='Save Changes', command=lambda: self.edit_record(new_title.get(), title, new_body.get(), body)).grid(row=12, column=2, sticky=W)
 
        self.edit_root.mainloop()
 
    def edit_record(self, new_title, title, new_body, body):
        query = "UPDATE user_memo SET title='{}', body='{}', update_dtm=current_timestamp() WHERE username='{}' and title='{}' and body='{}'".format(new_title, new_body,self.curr_user, title, body)
        self.run_query(query)
        self.edit_root.destroy()
        self.message['text'] = '{} Memo is updated !'.format(title, new_title)
        self.veiwing_records()

    def edit(self):
        ed = tkinter.messagebox.askquestion('Edit Record', 'Want to Edit this Record?')
        if ed == 'yes':
            self.edit_box()
 
    '''HELP'''
    def help(self):
        tkinter.messagebox.showinfo('Log','Report Sent!')
 
    '''EXIT'''
    '''EXIT'''
    def ex(self):
        exit = tkinter.messagebox.askquestion('Exit Application','Are you sure you want to close this application?')
        if exit == 'yes':
            self.root.destroy()


'''MAIN'''

if __name__ == '__main__':
    root = Tk()
    # root.geometry('585x515+500+200')
    application = Memo_window(root, 'user1')
    root.mainloop()
