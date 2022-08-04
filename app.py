from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyBwMLMG6TlrTRWvrImpn7kgKxVEF3ExJRI",
  "authDomain": "cs-amir-gp-f.firebaseapp.com",
  "projectId": "cs-amir-gp-f",
  "storageBucket": "cs-amir-gp-f.appspot.com",
  "messagingSenderId": "531475169244",
  "appId": "1:531475169244:web:06192ca20d569bc89a5919",
  "measurementId": "G-SL0HLVBCQG",
  "databaseURL":"https://cs-amir-gp-f-default-rtdb.europe-west1.firebasedatabase.app/"
};


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'trytoguessbish'




@app.route('/', methods=['GET', 'POST'])
def signin():
    error=""
    if request.method == "POST":
        login_session['email'] = request.form['email']
        login_session['password'] = request.form['password']
        try:
            login_session['user'] = user = auth.sign_in_with_email_and_password(login_session["email"], login_session["password"])
            return(redirect('design'))
        except:
            error="problem"
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == "POST":
        login_session['email']= request.form['email']
        login_session['full_name']= request.form['full_name']
        login_session['username']= request.form['username']
        # try:
        login_session['user'] = auth.create_user_with_email_and_password(login_session["email"], request.form['password'])
        user= {"email": request.form['email'],"full_name": request.form['full_name'],"username": request.form['username'],}
        user = db.child("Users").child(login_session['user']['localId']).set(user)
        return redirect(url_for('design'))
        # except:
            # return render_template("signup.html", error="problem")
    else:
        return render_template("signup.html")


@app.route('/design')
def design():
    username = db.child("Users").child(login_session['user']['localId']).get().val()['username']
    return render_template('design.html', username = username)


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/home')
def home():
    return render_template('design.html') 

@app.route('/features')
def features():
    return render_template("features.html")

@app.route('/shop')
def shop():
    return render_template("shop.html")


@app.route('/abouts')
def abouts():
    return render_template("abouts.html")





if __name__ == '__main__':
    app.run(debug=True)