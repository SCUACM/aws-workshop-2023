from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# MySQL connection configuration
mysql_config = {
    'host': '<endpoint>',
    'user': 'admin',
    'password': '<password>',
    'database': 'sample',
}

# Function to create a MySQL connection
def create_connection():
    return mysql.connector.connect(**mysql_config)

# Read endpoint to get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute('SELECT * FROM EMPLOYEES')
        employees = cursor.fetchall()

        return jsonify(employees)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        connection.close()

# Write endpoint to add a new employee
@app.route('/employees', methods=['POST'])
def add_employee():
    try:
        connection = create_connection()
        cursor = connection.cursor()

        data = request.get_json()
        name = data['name']
        address = data['address']

        cursor.execute('INSERT INTO EMPLOYEES (NAME, ADDRESS) VALUES (%s, %s)', (name, address))
        connection.commit()

        return jsonify({'message': 'Employee added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)