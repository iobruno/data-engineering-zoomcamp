#!/usr/bin/env python3

from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Replace the following with your PostgreSQL database connection details
db_connection_params = {
    'host': 'localhost',
    'database': 'dev',
    'user': 'root',
    'port': 4566,
}

def run_query(query):
    connection = psycopg2.connect(**db_connection_params)
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result

@app.route('/get_busiest_zones', methods=['GET'])
def get_busiest_zones():
    # Replace the following with your SQL query for busiest zones
    query = 'SELECT * FROM busiest_zones_1_min'
    result = run_query(query)
    return jsonify(result)

@app.route('/get_longest_trips', methods=['GET'])
def get_longest_trips():
    # Replace the following with your SQL query for longest trips
    query = 'SELECT * FROM longest_trip_1_min'
    result = run_query(query)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)