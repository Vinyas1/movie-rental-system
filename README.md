
# 🎬 Movie Streaming Access Platform 

NOTE :(Beginer level without API calls and no complex backend integration)
A **Flask + MySQL web application** where users can register, log in, and watch movies that are unlocked by an administrator.
The admin panel allows granting movie access and viewing analytics charts of user activity and payments.

---

# 🚀 Features

### 👤 User Features

* User registration and login
* Secure password hashing using **Flask-Bcrypt**
* Personalized dashboard
* Access only to **unlocked movies**
* Payment submission form

### 🛠 Admin Features

* Admin authentication
* Grant movie access to specific users
* View analytics charts:

  * Movies accessed per user
  * Users per movie
  * Top active users
  * Movies with no access
  * Payment analytics

### 📊 Data Analytics

Admin dashboards generate charts using:

* **Matplotlib**
* **Pandas**
---

# 🧰 Tech Stack

**Backend**

* Python
* Flask

**Database**

* MySQL

**Libraries**

* Flask-MySQLdb
* Flask-Bcrypt
* Matplotlib
* Pandas

**Frontend**

* HTML
* CSS
* Jinja2 Templates

---

# 📁 Project Structure

```
https://res.cloudinary.com/dokuv73yo/image/upload/v1773229259/Screenshot_2026-03-11_170952_uxey8k.png
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```
clone my REPO using 
git clone https://github.com/Vinyas1/movie-rental-system.git
cd movie-rental-system
```
---

## 2️⃣ Create Virtual Environment

```
python -m venv venv
```
venv\Scripts\activate
 
---

## 3️⃣ Install Dependencies

```
pip install flask flask-mysqldb flask-bcrypt matplotlib pandas
---

## 4️⃣ Setup Database

Login to MySQL:

```
mysql -u root -p
```

Paste  the  database.sql file in  MYsql and run it;
```

## 5️⃣ Create Admin Account
NOTE: Before creating admin account open up static folder and add videos (by referring <vid src =""> in the files)
so that video displays as soon as you run the project


Run:

```
python init_admin.py
```

Default admin login:

```
Email: admin12345@admin.com
Password: admin@12345
```

---

## 6️⃣ Run the Application

```
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

# 🔐 Admin Panel

Admin Login URL:

```
http://127.0.0.1:5000/admin_login
```

Admin can:

* Unlock movies for users
* View analytics charts
* Monitor platform activity

---

# 📊 Analytics Dashboard

Admin charts include:

* Movies accessed per user
* Users per movie
* Access distribution
* Top active users
* Payment statistics
---

# 💳 Payment Logging

Payments can be processed using razorpay and sending Recipt in the dashboard that is sent to the admin

```


