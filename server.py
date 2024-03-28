from flask import Flask, jsonify
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

@app.route('/predicted_return')
def index():
    data = get_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
