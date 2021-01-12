from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

app= Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='database'
mysql = MySQL(app)

@app.route('/',methods=['GET','POST'])

def home():
    if request.method =='POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO data (Name, password, Email ) VALUES(%s,%s,%s)",(name,password,email,))
        mysql.connection.commit()
        cur.close()
        return redirect('/login')
    return render_template("registration.html")


@app.route('/login',methods=['GET','POST'])

def login():
    msg=""
    if request.method =='POST' :
        
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        cur=mysql.connection.cursor()
        cur.execute('Select * from data where Name = %s AND password = %s AND Email= %s',(username,password,email,))
        account = cur.fetchone()
        
	
        if account:
            str="/users/" + email
            return redirect(str)
        else:
            msg = "INCORRECT USERNAME PASSWORD"
        
    return render_template("login.html",msg=msg)


@app.route('/users/<email>',methods=['GET','POST'])
def user(email):
    if request.method =='POST':
        
        name = request.form['text']
        email=email
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO posttable ( text,emaill ) VALUES(%s,%s)",(name,email,))
        mysql.connection.commit()
        cur.close()
        
    cur=mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM posttable")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('homePage.html',userDetails=userDetails)
    
@app.route('/users/<int:id>',methods=['GET','POST'])
def post(id):
    if request.method =='POST':
        
        name = request.form['text']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO commenttable ( Text,post_id ) VALUES(%s,%s)",(name,id,))
        mysql.connection.commit()
        cur.close()
    cur=mysql.connection.cursor()
    
    resultValue = cur.execute("SELECT * FROM posttable where id=%s",(id,))
    if resultValue > 0:
        userDetails = cur.fetchall()

        result = cur.execute("SELECT * FROM commenttable where post_id=%s",(id,))
        if result>0:
            userDetail = cur.fetchall()

            return render_template('post.html',userDetails=userDetails,userDetail=userDetail)
        else:
            return render_template('post.html',userDetails=userDetails)
    return ('post.html')
@app.route('/users/post/<int:id>',methods=['GET','POST'])
def postupdate(id):
    if request.method=='POST':
        
        name = request.form['text']
        cur=mysql.connection.cursor()
        cur.execute("UPDATE posttable SET  text= %s WHERE id = %s",(name,id,))
        mysql.connection.commit()
        cur.close()
        s=str(id)
        str1="/users/"+s
        return redirect(str1)
    
    return render_template('postupdate.html')
@app.route('/users/comment/<int:id>/<int:id1>',methods=['GET','POST'])
def comment(id,id1):
    if request.method=='POST':
        
        name = request.form['text']
        cur=mysql.connection.cursor()
        cur.execute("UPDATE commenttable SET  text= %s WHERE id = %s",(name,id1,))
        mysql.connection.commit()
        cur.close()
        s1=str(id)
        s1="/users/"+s1
        return redirect(s1)
    return render_template('comments.html')
@app.route('/users/remove/<int:id>/<int:id1>',methods=['GET','POST'])
def remove(id,id1):
    if request.method=='POST':
        
        cur=mysql.connection.cursor()
        cur.execute("DELETE FROM commenttable WHERE id = %s",(id1,))
        mysql.connection.commit()
        cur.close()
        s1=str(id)
        s1="/users/"+s1
        return redirect(s1)
    return render_template('remove.html')
    
    
if __name__=='__main__':
     app.run(debug=True)
    
