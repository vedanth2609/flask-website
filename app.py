from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

EXCEL_FILE = "users.xlsx"

# Ensure the Excel file exists with proper columns
def get_user_data():
    """Ensure users.xlsx exists and read data from it."""
    if not os.path.exists(EXCEL_FILE):  # Check if file exists
        df = pd.DataFrame(columns=["Name", "Department", "Year", "Section", "Password"])
        df.to_excel(EXCEL_FILE, index=False)  # Create file with correct columns
    return pd.read_excel(EXCEL_FILE)

# Home Route
@app.route("/")
def index():
    return redirect(url_for("register"))

# Registration Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        department = request.form["department"]
        year = request.form["year"]
        section = request.form["section"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Validate password match
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("register"))

        df = get_user_data()

        # Check if username already exists
        if name in df["Name"].values:
            flash("Username already exists!", "error")
            return redirect(url_for("register"))

        # Append new user data
        new_user = pd.DataFrame([[name, department, year, section, password]], 
                                columns=["Name", "Department", "Year", "Section", "Password"])
        df = pd.concat([df, new_user], ignore_index=True)

        # Save back to Excel
        df.to_excel(EXCEL_FILE, index=False)

        flash("Registration successful!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        df = get_user_data()

        # Check credentials
        user = df[(df["Name"] == username) & (df["Password"] == password)]
        if not user.empty:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            flash("Incorrect username or password", "error")

    return render_template("login.html")

# Home Page Route (Requires Login)
@app.route("/home")
def home():
    if "user" in session:
        return render_template("home.html", username=session["user"])
    return redirect(url_for("login"))

# Logout Route
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("exit_page"))

# Exit Page Route
@app.route("/exit")
def exit_page():
    return render_template("exit.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
