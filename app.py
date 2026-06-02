from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import random, time
import os
import pandas as pd
import joblib
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "stress_ai_secret"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'xyz@gmail.com'//demo gmail use your mail and password 
app.config['MAIL_PASSWORD'] = 'asdfvvddeffgg'//demo password 

mail = Mail(app)

# LOAD MODEL
model = joblib.load("model.pkl")


def get_suggestion(data): 
    suggestions = []

    if data[3] < 5:
        suggestions.append("Improve sleep schedule")

    if data[7] > 7:
        suggestions.append("Reduce screen time")

    if data[10] > 7:
        suggestions.append("Practice meditation")

    if data[0] > 100:
        suggestions.append("Do breathing exercises")

    if data[8] > 7:
        suggestions.append("Manage work pressure")

    if data[9] > 7:
        suggestions.append("Take study breaks")

    if not suggestions:
        return "You are doing well, maintain your routine"

    return ", ".join(suggestions)

# OTP FUNCTION
def send_otp(email):
    otp = random.randint(100000, 999999)
    session['otp'] = otp
    session['otp_expiry'] = time.time() + 300

    msg = Message(
        "StressAI OTP Verification",
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )
    msg.body = f"Your OTP is {otp}. Valid for 5 minutes."
    mail.send(msg)


if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists("data/users.csv"):
    with open("data/users.csv", "w") as f:
        f.write("id,name,email,password\n")

if not os.path.exists("data/predictions.csv"):
    with open("data/predictions.csv", "w") as f:
        f.write("user_id,heart_rate,bp_sys,bp_dia,sleep_hours,fatigue_level,headache_frequency,physical_activity,screen_time,work_pressure,study_pressure,anxiety_level,mood_swings,concentration_level,stress_level\n")

users_file = "data/users.csv"
pred_file = "data/predictions.csv"

# HOME
@app.route("/")
def home():
    return render_template("index.html")

# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        df = pd.read_csv(users_file)

        if email in df["email"].values:
            return "Email already registered"

        session["temp_user"] = {
            "name": name,
            "email": email,
            "password": password
        }

        send_otp(email)
        return redirect("/verify_register")

    return render_template("register.html")

# VERIFY REGISTER OTP
@app.route("/verify_register", methods=["GET", "POST"])
def verify_register():
    if request.method == "POST":
        user_otp = int(request.form["otp"])

        if time.time() > session.get("otp_expiry", 0):
            return "OTP expired"

        if user_otp == session.get("otp"):
            df = pd.read_csv(users_file)
            new_id = len(df) + 1
            temp = session["temp_user"]

            new_user = {
                "id": new_id,
                "name": temp["name"],
                "email": temp["email"],
                "password": temp["password"]
            }

            df = df._append(new_user, ignore_index=True)
            df.to_csv(users_file, index=False)

            session.pop("temp_user", None)
            return redirect("/login")
        else:
            return "Invalid OTP"

    return render_template("verify_register.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        df = pd.read_csv(users_file)
        df["email"] = df["email"].astype(str).str.strip()

        user = df[df["email"] == email]

        if not user.empty and check_password_hash(user.iloc[0]["password"], password):
            session["user_id"] = int(user.iloc[0]["id"])
            session["name"] = user.iloc[0]["name"]
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid Email or Password ❌")

    return render_template("login.html")

# FORGOT PASSWORD
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        df = pd.read_csv(users_file)

        if email not in df["email"].values:
            return "Email not found"

        session["reset_email"] = email
        send_otp(email)
        return redirect("/verify_reset")

    return render_template("forgot_password.html")

# VERIFY RESET
@app.route("/verify_reset", methods=["GET", "POST"])
def verify_reset():
    if "reset_email" not in session:
        return redirect("/forgot_password")

    if request.method == "POST":
        user_otp = int(request.form["otp"])
        new_password = request.form["new_password"]

        if time.time() > session.get("otp_expiry", 0):
            return render_template("verify_reset.html", error="OTP expired ❌")

        if user_otp == session.get("otp"):
            df = pd.read_csv(users_file)
            email = session["reset_email"]

            user_index = df.index[df["email"] == email][0]
            df.loc[user_index, "password"] = generate_password_hash(new_password)
            df.to_csv(users_file, index=False)

            session.pop("reset_email", None)
            return redirect("/login")
        else:
            return render_template("verify_reset.html", error="Invalid OTP")

    return render_template("verify_reset.html")

# PROFILE
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    df = pd.read_csv(users_file)
    user = df[df["id"] == session["user_id"]].iloc[0]

    return render_template("profile.html", name=user["name"], email=user["email"])

# CHANGE PASSWORD
@app.route("/change_password", methods=["POST"])
def change_password():
    if "user_id" not in session:
        return redirect("/login")

    current = request.form["current_password"]
    new_pass = generate_password_hash(request.form["new_password"])

    df = pd.read_csv(users_file)
    user_index = df.index[df["id"] == session["user_id"]][0]

    if check_password_hash(df.loc[user_index, "password"], current):
        df.loc[user_index, "password"] = new_pass
        df.to_csv(users_file, index=False)

        return render_template("profile.html",
                               name=session["name"],
                               error="Password updated successfully ")
    else:
        return render_template("profile.html",
                               name=session["name"],
                               error="Current password incorrect ")

# PREDICT
@app.route("/predict", methods=["POST"])
def predict():

    if "user_id" not in session:
        return redirect("/login")

    inputs = [
        float(request.form["heart_rate"]),
        float(request.form["bp_sys"]),
        float(request.form["bp_dia"]),
        float(request.form["sleep_hours"]),
        float(request.form["fatigue_level"]),
        float(request.form["headache_frequency"]),
        float(request.form["physical_activity"]),
        float(request.form["screen_time"]),
        float(request.form["work_pressure"]),
        float(request.form["study_pressure"]),
        float(request.form["anxiety_level"]),
        float(request.form["mood_swings"]),
        float(request.form["concentration_level"])
    ]

    prediction = model.predict([inputs])[0]

    if prediction == 0:
        result = "Low Stress"
    elif prediction == 1:
        result = "Medium Stress"
    else:
        result = "High Stress"

    tip = get_suggestion(inputs)

    df = pd.read_csv(pred_file)

    new_row = {
        "user_id": session["user_id"],
        "heart_rate": inputs[0],
        "bp_sys": inputs[1],
        "bp_dia": inputs[2],
        "sleep_hours": inputs[3],
        "fatigue_level": inputs[4],
        "headache_frequency": inputs[5],
        "physical_activity": inputs[6],
        "screen_time": inputs[7],
        "work_pressure": inputs[8],
        "study_pressure": inputs[9],
        "anxiety_level": inputs[10],
        "mood_swings": inputs[11],
        "concentration_level": inputs[12],
        "stress_level": result
    }

    df = df._append(new_row, ignore_index=True)
    df.to_csv(pred_file, index=False)

    return render_template("result.html", result=result, tip=tip)

# HISTORY
@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect("/login")

    df = pd.read_csv(pred_file)
    user_data = df[df["user_id"] == session["user_id"]]

    labels = list(range(1, len(user_data) + 1))
    stress_map = {"Low Stress":1,"Medium Stress":2,"High Stress":3}
    values = [stress_map[x] for x in user_data["stress_level"]]

    return render_template("history.html",
                           data=user_data.to_dict(orient="records"),
                           chart_labels=labels,
                           chart_values=values)

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# RUN
if __name__ == "__main__":
    app.run(debug=True)
