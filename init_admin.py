from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'movie_rental'

mysql = MySQL(app)
bcrypt = Bcrypt(app)


admin_email = 'admin12345@admin.com'
admin_password = 'admin@12345'


hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')

# Insert predefined admin data into the database
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO admins (email, password) VALUES (%s, %s)", (admin_email, hashed_password))
    mysql.connection.commit()
    print('Admin  inserted successfully!')
