from flask import Flask, render_template, request
# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session,sessionmaker

# engine = create_engine('postgresql+psycopg2://postgres:Duclong123@localhost:5432/long')
# db=scoped_session(sessionmaker(bind=engine))

import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
engine=create_engine('postgresql+psycopg2://postgres:Duclong123@localhost:5432/notes')
db= scoped_session(sessionmaker(bind=engine))
app=Flask(__name__)
pw1=''
pw2=''

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/userinfo',methods=["POST",'GET'])
def userinfo():
    fname=request.form.get('firstname')
    lname=request.form.get('lastname')
    username=request.form.get('username')
    age=request.form.get('age')
    pw1=request.form.get('pw1')
    pw2=request.form.get('pw2')
    is_register=False
    if pw1!=pw2:
        return render_template('form.html',pw1=pw1,pw2=pw2,is_register=is_register)
    else:
        usernames = db.execute("select username from customer;").fetchall()
        for user in usernames:
            if user.username == username:
                is_register=True
        
        if is_register==False:
            name = fname+' '+lname
            db.execute("insert into customer(name,age,username,password) values(:name,:age,:username,:password);",{'name':name,"age":age,'username':username,'password':pw1})
            db.commit()
            cust1=db.execute('select * from customer where username= :username;',{'username':username}).fetchall()[0]
            notes=db.execute('select note from notes where cus_id=:cust1',{'cust1':cust1.id}).fetchall()
            return render_template('userinfo.html',cust1=cust1, is_register=is_register,notes=notes)
        else:   
            return render_template('form.html',pw1=pw1,pw2=pw2,is_register=is_register)

@app.route('/userinfo/<id>',methods=['POST','GET'])
def note(id):
    cust1=db.execute('select * from customer where id= :id;',{'id':id}).fetchall()[0]
    note=request.form.get('note')
    db.execute("insert into notes(cus_id,note) values (:cus_id,:note);",{'cus_id':cust1.id,'note':note})
    db.commit()
    note_full=[]
    notes=db.execute('select note from notes where cus_id=:cus_id;',{'cus_id':cust1.id}).fetchall()
    for note in notes:
        note_full.append(note.note)
    return render_template('userinfo.html',cust1=cust1, is_register=True,notes=note_full)
     


@app.route('/signin')    
def signin():
    return render_template('signin.html',boo=True)

@app.route('/info', methods=['POST'])
def signin_user():
    username=request.form.get('username')
    pw1=request.form.get('password')
    cust1=db.execute('select * from customer where username=:username and password=:pw1;',{'username':username,'pw1':pw1}).fetchone()
    if cust1 == None:
        return render_template('signin.html',boo=False)
    else:
        notes=db.execute('select note from notes where cus_id=:id;',{'id':cust1.id}).fetchall()
        note_full=[]
        for note in notes:
            note_full.append(note.note)
        return render_template('userinfo.html',cust1=cust1, is_register=True,notes=note_full)
