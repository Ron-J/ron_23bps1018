from flask import Flask, request, render_template, redirect, url_for, session
from serverMongoDbInterface import *

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# --- reCAPTCHA Configuration (ADD YOUR KEYS) ---
app.config['RECAPTCHA_SITE_KEY'] = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'  # << FROM Google reCAPTCHA
app.config['RECAPTCHA_SECRET_KEY'] = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'  # << FROM Google reCAPTCHA


# --- Routes ---
@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        captcha_response = request.form.get('g-recaptcha-response')
        
        # Verify CAPTCHA first
        if not verify_recaptcha(captcha_response):
            return render_template(
                "login.html",
                error="CAPTCHA verification failed",
                captcha_error="Please complete the CAPTCHA",
                site_key=app.config['RECAPTCHA_SITE_KEY']
            )
        
        if verifyUser(username, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template(
                "login.html",
                error="Invalid credentials",
                site_key=app.config['RECAPTCHA_SITE_KEY']  # Preserve CAPTCHA
            )
    
    return render_template("login.html", site_key=app.config['RECAPTCHA_SITE_KEY'])


# --- Helper Functions ---
def verify_recaptcha(response):
    if not response:
        return False
    # Verify with Google (disabled for demo)
    # payload = {
    #    'secret': app.config['RECAPTCHA_SECRET_KEY'],
    #    'response': response
    # }
    # r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
    # return r.json().get('success', False)
    return True  # Skip in development
# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

#Home Page
@app.route('/home', methods=["GET", "POST"])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("home.html", username=session.get('username'))

#registration page
@app.route('/register', methods=['GET','POST'])
def register():
    return render_template("register.html")

#Update database temporary link
@app.route('/create-registration', methods=['POST'])
def create_registration():
    username = request.form.get("username")
    password = request.form.get("password")
    addUser(username, password)
    return redirect(url_for('home'))

#Search Page
@app.route('/search', methods =["GET", "POST"])
def search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    centers= []
    if request.method == "POST":
        x=int(request.form.get("searchby"))
        print(x+1)
        if(x==1 or x==2):
            centers=readdata(x, "")
            print(centers)
        elif(x==3):
            centers=readdata(x,request.form.get("centerName"))
        elif(x==4):
            centers=readdata(x,request.form.get("location"))
    return render_template("search.html", centers=centers)

#Review Page
@app.route('/review', methods=["GET", "POST"])
def review():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == "POST":
        name=request.form.get("name")
        typep=int(request.form.get("TypeP"))
        typec=int(request.form.get("TypeC"))
        time=int(request.form.get("time"))
        sideeffects=int(request.form.get("sideeffects"))
        location=request.form.get("location")
        inputdata(name, typep, typec, time, sideeffects, location)
        return render_template("thankyou.html")
    return render_template("review.html")

#delete page
@app.route('/delete', methods=['GET','POST'])
def delete():
    if(request.method=='POST'):
        name=request.form.get("name")
        deleteRecord(name)
        return redirect(url_for('home'))
    return render_template("delete.html")
if __name__=='__main__':
    app.run(debug=True)

