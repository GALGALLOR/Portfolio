from flask_mysqldb import MySQL
from flask import  get_flashed_messages, session,Flask,render_template,redirect,request,flash,url_for
app=Flask(__name__)
import datetime
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
app.secret_key=os.getenv('secret_key')
#bring env loader
#bring flask stuff
#bring email sender----
import ssl
from email.message import EmailMessage
import smtplib

mydb=MySQL(app)

app.config['MYSQL_HOST']=os.getenv('host')
app.config['MYSQL_USER']=os.getenv('user')
app.config['MYSQL_PASSWORD']=os.getenv('password')
app.config['MYSQL_DB']=os.getenv('database')

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        sender= str(request.form['name'])
        contact=str(request.form['email'])
        message=str(request.form['message'])
        try:
            email_sender = 'web.galgalloroba@gmail.com'
            email_password= os.getenv('code')
            email_receiver='web.galgalloroba@gmail.com'

            subject='✅URGENT MESSAGE FROM PORTFOLIO'
            body=f""" You have received an important message from {sender}:
            
            Email : {contact}

            Message : {message}
            """
            em=EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(email_sender,email_password)
                smtp.sendmail(email_sender,email_receiver,em.as_string())
        except:
            print('failure')
        

        datetime_=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        cursor=mydb.connection.cursor()
        cursor.execute('INSERT INTO EMAILS(NAMES,EMAIL,MESSAGE,DATETIME)VALUES(%s,%s,%s,%s)',(sender,contact,message,datetime_))
        mydb.connection.commit()

    return render_template('index.html')
@app.route('/admin')
def admin():
    cursor=mydb.connection.cursor()
    cursor.execute('SELECT * FROM EMAILS')
    msgs=cursor.fetchall()
    return render_template('admin.html',msgs=msgs)

if __name__ == '__main__':
    app.run(debug=True)