from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_mysqldb import MySQL
from flask import redirect
from flask_bcrypt import Bcrypt
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
import csv
import io
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'movie_rental'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

# ===================== Routes =======================

@app.route('/')
def index():
    return redirect(url_for('login'))

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (uname, email, password))
        mysql.connection.commit()
        flash('Registered successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", [email])
        user = cur.fetchone()
        if user and bcrypt.check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        flash("Invalid credentials", 'danger')
    return render_template('login.html')

# User Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT m.name 
        FROM access a
        JOIN movies m ON a.movie_id = m.id
        WHERE a.user_id = %s
    """, [session['user_id']])
    
    unlocked_movies = [row[0] for row in cur.fetchall()]
    return render_template('dashboard.html', username=session['username'], unlocked_movies=unlocked_movies)



@app.route("/play1")
def play_video1():
    return render_template("1.html")
@app.route("/play2")
def play_video2():
    return render_template("2.html")
@app.route("/play3")
def play_video3():
    return render_template("3.html")

@app.route("/play4")
def play_video4():
    return render_template("4.html")

@app.route("/play5")
def play_video5():
    return render_template("5.html")

@app.route("/play6")
def play_video6():
    return render_template("6.html")





@app.route('/website')
def websiteopen():
    return redirect("")   #your payment website


@app.route('/forms')
def formopen():
    return render_template("bookf.html")




@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admins WHERE email=%s", [email])
        admin = cur.fetchone()
        if admin and bcrypt.check_password_hash(admin[2], password):
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Unauthorized access", 'danger')
    return render_template('admin.html')


# Admin Dashboard
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username FROM users")
    users = cur.fetchall()

    cur.execute("SELECT id, name FROM movies")
    movies = cur.fetchall()

    if request.method == 'POST':
        user_id = request.form['user_id']
        movie_id = request.form['movie_id']
        cur.execute("INSERT INTO access (user_id, movie_id) VALUES (%s, %s)", (user_id, movie_id))
        mysql.connection.commit()
        flash('Movie access granted!', 'success')

    return render_template('admin_dashboard.html', users=users, movies=movies)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin_charts')
def admin_charts():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cur = mysql.connection.cursor()

    # 1. Movies accessed per user
    cur.execute("""
        SELECT u.username, COUNT(a.movie_id)
        FROM users u
        LEFT JOIN access a ON u.id = a.user_id
        GROUP BY u.id
    """)
    user_data = cur.fetchall()
    usernames = [row[0] for row in user_data]
    movie_counts = [row[1] for row in user_data]

    fig1 = plt.figure(figsize=(6, 4))
    plt.bar(usernames, movie_counts, color='blue')
    plt.title('Movies Accessed per User')
    plt.xlabel('User')
    plt.ylabel('Movies')
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf1 = BytesIO()
    fig1.savefig(buf1, format='png')
    buf1.seek(0)
    user_chart = base64.b64encode(buf1.getvalue()).decode('utf-8')
    plt.close(fig1)

    # 2. Users per movie
    cur.execute("""
        SELECT m.name, COUNT(a.user_id)
        FROM movies m
        LEFT JOIN access a ON m.id = a.movie_id
        GROUP BY m.id
    """)
    movie_data = cur.fetchall()
    movie_names = [row[0] for row in movie_data]
    user_counts = [row[1] for row in movie_data]

    fig2 = plt.figure(figsize=(6, 4))
    plt.bar(movie_names, user_counts, color='orange')
    plt.title('Users with Access per Movie')
    plt.xlabel('Movie')
    plt.ylabel('Users')
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf2 = BytesIO()
    fig2.savefig(buf2, format='png')
    buf2.seek(0)
    movie_chart = base64.b64encode(buf2.getvalue()).decode('utf-8')
    plt.close(fig2)

    # 3. Pie chart: Access distribution by movie
    fig3 = plt.figure(figsize=(6, 6))
    plt.pie(user_counts, labels=movie_names, autopct='%1.1f%%', startangle=140)
    plt.title('Access Distribution by Movie')
    buf3 = BytesIO()
    plt.tight_layout()
    fig3.savefig(buf3, format='png')
    buf3.seek(0)
    pie_chart = base64.b64encode(buf3.getvalue()).decode('utf-8')
    plt.close(fig3)

    # 4. Top 5 active users
    cur.execute("""
        SELECT u.username, COUNT(a.movie_id) as total 
        FROM users u 
        LEFT JOIN access a ON u.id = a.user_id 
        GROUP BY u.id 
        ORDER BY total DESC 
        LIMIT 5
    """)
    top_users_data = cur.fetchall()
    top_usernames = [row[0] for row in top_users_data]
    top_counts = [row[1] for row in top_users_data]

    fig4 = plt.figure(figsize=(6, 4))
    plt.bar(top_usernames, top_counts, color='green')
    plt.title('Top 5 Most Active Users')
    plt.xlabel('User')
    plt.ylabel('Movies Accessed')
    plt.tight_layout()
    buf4 = BytesIO()
    fig4.savefig(buf4, format='png')
    buf4.seek(0)
    top_users_chart = base64.b64encode(buf4.getvalue()).decode('utf-8')
    plt.close(fig4)

    # 5. Movies with no access
    cur.execute("""
        SELECT m.name 
        FROM movies m 
        LEFT JOIN access a ON m.id = a.movie_id 
        WHERE a.user_id IS NULL
    """)
    no_access_movies = cur.fetchall()
    no_access_names = [row[0] for row in no_access_movies]

    fig5 = plt.figure(figsize=(6, 4))
    plt.bar(no_access_names, [1]*len(no_access_names), color='red')
    plt.title('Movies with No Access')
    plt.xlabel('Movie')
    plt.ylabel('No Access')
    plt.tight_layout()
    buf5 = BytesIO()
    fig5.savefig(buf5, format='png')
    buf5.seek(0)
    no_access_chart = base64.b64encode(buf5.getvalue()).decode('utf-8')
    plt.close(fig5)

    return render_template(
        'admin_charts.html',
        user_chart=user_chart,
        movie_chart=movie_chart,
        pie_chart=pie_chart,
        top_users_chart=top_users_chart,
        no_access_chart=no_access_chart
    )

@app.route('/submit_payment', methods=['POST'])
def submit_payment():
    data = {
        'Username': request.form['carid'],
        'Movie': request.form['carname'],
        'PaidAmount': request.form['name'],
        'PayID_UTR': request.form['age'],
        'PaidDate': request.form['booking_date'],
        'PaymentTime': request.form['return_date'],
        'Email': request.form['email']
    }

    file_exists = os.path.isfile('payments.csv')

    with open('payments.csv', 'a', newline='') as csvfile:
        fieldnames = ['Username', 'Movie', 'PaidAmount', 'PayID_UTR', 'PaidDate', 'PaymentTime', 'Email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

    return render_template('hi.html')
    



@app.route('/payment_charts')
def payment_charts():
    csv_file = 'payments.csv'
    if not os.path.exists(csv_file):
        return "No payment data available yet."

    df = pd.read_csv(csv_file)
    df.fillna(0, inplace=True)

    # Graph 1: Movies bought per user
    fig1 = plt.figure(figsize=(6, 4))
    user_movie_counts = df.groupby(['Username', 'Movie']).size().unstack(fill_value=0)
    user_movie_counts.plot(kind='bar', stacked=True, ax=plt.gca())
    plt.title('Movies Bought by Each User')
    plt.xlabel('Username')
    plt.ylabel('Number of Purchases')
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf1 = BytesIO()
    fig1.savefig(buf1, format='png')
    buf1.seek(0)
    chart1 = base64.b64encode(buf1.getvalue()).decode('utf-8')
    plt.close(fig1)

    # Graph 2: Highest Paying Customers
    df['PaidAmount'] = pd.to_numeric(df['PaidAmount'], errors='coerce')
    paid_totals = df.groupby('Username')['PaidAmount'].sum().sort_values(ascending=False)
    fig2 = plt.figure(figsize=(6, 4))
    paid_totals.plot(kind='bar', ax=plt.gca(), color='green')
    plt.title('Total Amount Paid by Users')
    plt.xlabel('Username')
    plt.ylabel('Total Paid')
    plt.tight_layout()
    buf2 = BytesIO()
    fig2.savefig(buf2, format='png')
    buf2.seek(0)
    chart2 = base64.b64encode(buf2.getvalue()).decode('utf-8')
    plt.close(fig2)

    # Graph 3: Most Popular Movies
    fig3 = plt.figure(figsize=(6, 4))
    movie_counts = df['Movie'].value_counts()
    movie_counts.plot(kind='bar', ax=plt.gca(), color='purple')
    plt.title('Most Bought Movies')
    plt.xlabel('Movie')
    plt.ylabel('Times Bought')
    plt.tight_layout()
    buf3 = BytesIO()
    fig3.savefig(buf3, format='png')
    buf3.seek(0)
    chart3 = base64.b64encode(buf3.getvalue()).decode('utf-8')
    plt.close(fig3)

    return render_template("payment_charts.html", chart1=chart1, chart2=chart2, chart3=chart3)

if __name__ == "__main__":
    app.run(debug=True)
