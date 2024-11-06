from datetime import datetime
from flask import Flask, jsonify,render_template, request
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

show_screen = ""

# app system db connection
connection  = sqlite3.connect("system_db/pinedb.db")
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS pinedb (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    database TEXT NOT NULL,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);
''')

connection.commit()
cursor.close()

# insert the names of the created database
import sqlite3
from datetime import datetime

def insert_database(database_name):
    # Connect to the database
    connection = sqlite3.connect('system_db/pinedb.db')
    cursor = connection.cursor()
    
    # Get the current datetime
    current_datetime = datetime.now()
    
    # Check if the record already exists
    cursor.execute('''
        SELECT COUNT(*) FROM pinedb WHERE database = ?;
    ''', (database_name,))
    
    exists = cursor.fetchone()[0] > 0
    
    if not exists:
        # Insert the new record if it does not exist
        cursor.execute('''
            INSERT INTO pinedb (database, datetime) VALUES (?, ?);
        ''', (database_name, current_datetime))
        connection.commit()
        print(f"Inserted new database entry: {database_name} at {current_datetime}")
    else:
        print(f"Database entry '{database_name}' already exists. No insertion made.")
    
    # Clean up
    cursor.close()
    connection.close()


    
    
def get_all_databases():
    connection = sqlite3.connect('system_db/pinedb.db')
    cursor = connection.cursor()
    cursor.execute('SELECT database, datetime FROM pinedb')
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    
    # Convert rows into a list of dictionaries
    databases = []
    for row in rows:
        databases.append({
            'database': row[0],
            'datetime': row[1]
        })
    
    return databases

# Route to fetch all databases
@app.route('/api/databases', methods=['GET'])
def fetch_databases():
    databases = get_all_databases()
    return jsonify(databases)


app.template_folder = "template"
app.static_folder = "static"

@app.route("/")
def app_home():
    return render_template('dashboard.html', dblist="grid",createdb="flex")

@app.route("/managedb/<string:database>")
def db_home(database):
    print(database+"xxxxxxxxxxx")
    return render_template('dashboard.html', dblist="none",createdb="none")


@app.route('/createdb', methods=['POST'])
def create_database():
    data = request.get_json()
    db_name = data.get('name')
    insert_database(database_name=db_name)
    sqlite3.connect('databases/'+db_name+'.db')
    # Logic to create the database goes here
    return jsonify({"message": f"Database '{db_name}' created successfully!"}), 200


