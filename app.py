from curses import flash
from flask import Flask, redirect, render_template, request, session 
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors
import json
import aicontent

local_server = True
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask (__name__)
app.secret_key = 'super-secret-key'

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
# Intialize MySQL
mysql = MySQL(app)

db = SQLAlchemy(app)
#now = datetime.datetime.now()
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(20), nullable=False)

class usertable(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    user_password = db.Column(db.String(12), nullable=False)
    user_email = db.Column(db.String(20), nullable=False)


@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/index")
def helloagain():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/generator", methods=["GET", "POST"])
def generator():
    return render_template('generator.html', **locals())



##ai    

@app.route("/generator/productdescription", methods=["GET", "POST"])
def productgenerator():
    if request.method == 'POST':
        query = request.form['productDescription']
        
        openAIAnswer = aicontent.productgenerator(query)
        prompt = 'Generate a detailed product description for: {}'.format(query)
        print("open ai anwer and prompt")
    print("return")
    return render_template('productdescription.html', **locals())


@app.route("/generator/email", methods=["GET", "POST"])
def emailgenerator():
    if request.method == 'POST':
        submission = request.form['emailgenerator']
        query = 'Write a formal email for: {}'.format(submission)
        openAIAnswerUnformatted= aicontent.emailgenerator(query)
        openAIAnswer =  openAIAnswerUnformatted.replace('\n','<br>')
        prompt = 'Ai suggestion for {} is:'.format(submission)
        print("open ai anwer and prompt")
    print("return")
    return render_template('email.html', **locals())
    

@app.route("/generator/blogidea", methods=["GET", "POST"])
def blogideagenerator():
    if request.method == 'POST':
        submission = request.form['blogidea']
        query = 'Generate a Blog headline and outline for: {}'.format(submission)
        openAIAnswer = aicontent.blogideagenerator(query)
        prompt = 'Ai suggestion for {} is:'.format(submission)
        print("open ai anwer and prompt")
    print("return")
    return render_template('blogidea.html', **locals())


@app.route("/generator/twitterpost", methods=["GET", "POST"])
def twitterpostgenerator():
    if request.method == 'POST':
        submission = request.form['twitterpost']
        query = 'Generate a twitter post about: {}'.format(submission)
        openAIAnswer = aicontent.twitterpostgenerator(query)
        prompt = 'Ai suggestion for {} is :'.format(submission)
        print("open ai anwer and prompt")
    print("return")
    return render_template('twitterpost.html', **locals())
    

@app.route("/generator/summarization", methods=["GET", "POST"])
def summarizationgenerator():
    if request.method == 'POST':
        submission = request.form['summarization']
        query = 'summarize the following paragraph: {}'.format(submission)
        openAIAnswer = aicontent.summarizationgenerator(query)
        prompt = 'Ai suggestion is:'.format(submission)
        print("open ai anwer and prompt")
    print("return")
    return render_template('summarization.html', **locals())






@app.route("/adminlogin", methods = ['GET', 'POST'])
def adminlogin():
    if "user" in session and session['user']==params['admin_user']:

        return render_template("dashboard.html", params=params)

    if request.method=="POST":
        username = request.form.get("uname")
        userpass = request.form.get("upass")
        if username==params['admin_user'] and userpass==params['admin_password']:
            # set the session variable
            session['user']=username
            return render_template("dashboard.html", params=params)
    else:
        return render_template("login.html", params=params)


@app.route("/login", methods = ['GET', 'POST'])
def login():
    if "user" in session and session['user']==params['admin_user']:

        return render_template("index.html", params=params)

    if request.method=="POST":
        username = request.form.get("username")
        userpass = request.form.get("user_password")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, userpass))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return render_template('index.html')
        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username/password!")
    return render_template('login.html')


    
@app.route("/register", methods = ['GET', 'POST'])
def register():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('phone')
        entry = usertable(username = name ,user_email = email, user_password = password)
        db.session.add(entry)
        db.session.commit()
    flash("You have successfully registered!", "success")
    return render_template('register.html')



@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message,email = email )
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/index')

@app.route('/dashboard')
def dashboard():
    
    return render_template('dashboard.html')


app.run(debug=True)