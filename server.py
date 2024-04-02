
from flask import Flask, jsonify, request
from flask_cors import CORS
import pyodbc



app = Flask(__name__)
CORS(app)

def get_data():
    connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=stocksserver.database.windows.net;DATABASE=stockdb;UID=evelyn@stocksserver;PWD=Apple2327'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()


    cursor.execute('SELECT * FROM stockdb.dbo.Predicted_Return')
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))
    conn.close()
    return data

def get_symbols():
    connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=stocksserver.database.windows.net;DATABASE=stockdb;UID=evelyn@stocksserver;PWD=Apple2327'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Fetch data from the Symbols table
    cursor.execute('SELECT * FROM stockdb.dbo.Symbols')
    columns_symbols = [column[0] for column in cursor.description]
    data_symbols = []
    for row in cursor.fetchall():
        data_symbols.append(dict(zip(columns_symbols, row)))

    conn.close()

    return data_symbols

@app.route('/user', methods=['GET'])
def get_user():
    
    connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=stocksserver.database.windows.net;DATABASE=stockdb;UID=evelyn@stocksserver;PWD=Apple2327'
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    email = request.args.get('email')
    if email is None:
        return jsonify({'error': 'Email parameter is required'}), 400

    cursor.execute("SELECT * FROM Users WHERE Email = ?", email)
    row = cursor.fetchone()
    if row:
        user = {
            'UserId': row.UserId,
            'Name': row.Name,
            'Lastname': row.Lastname,
            'Password' : row.Password,
        }
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/user', methods=['POST'])
def create_user():
    try:
        # Connect to the database
        connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=stocksserver.database.windows.net;DATABASE=stockdb;UID=evelyn@stocksserver;PWD=Apple2327'
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Get user data from request JSON
        data = request.get_json()
        if 'Name' not in data or 'Lastname' not in data or 'Password' not in data or 'email' not in data:
            return jsonify({'error': 'Incomplete user data'}), 400

        # Extract user data
        name = data['Name']
        lastname = data['Lastname']
        password = data['Password']
        email = data['email']

        # Check if the user already exists
        cursor.execute("SELECT * FROM Users WHERE email = ?", email)
        
        if cursor.fetchone():
            return jsonify({'error': 'User already exists'}), 409

        # Insert new user into the database
        cursor.execute("INSERT INTO Users (Name, Lastname, Password, email) VALUES (?, ?, ?, ?)",
                       (name, lastname, password, email))
        conn.commit()

        return jsonify({'message': 'User created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()


@app.route('/predicted_return')
def index():
    data = get_data()
    return jsonify(data)


@app.route('/symbols')
def get_symbols_api():
    data = get_symbols()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
