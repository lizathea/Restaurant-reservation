from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'db/reservation.db'

# Connect Database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reservations')
def reservations():
    conn = get_db_connection()
    reservations = conn.execute('''
        SELECT r.reservation_id, c.name, t.table_id, r.reservation_date, r.reservation_time, r.num_guests, r.status
        FROM Reservations r
        JOIN Customers c ON r.customer_id = c.customer_id
        JOIN RestaurantTables t ON r.table_id = t.table_id
    ''').fetchall()
    conn.close()
    return render_template('reservations.html', reservations=reservations)

@app.route('/add', methods=['GET', 'POST'])
def add_reservation():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        table_id = request.form['table_id']
        date = request.form['date']
        time = request.form['time']
        guests = request.form['guests']
        conn.execute('INSERT INTO Customers (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
        customer_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.execute('''
            INSERT INTO Reservations (customer_id, table_id, reservation_date, reservation_time, num_guests) VALUES (?, ?, ?, ?, ?)
        ''', (customer_id, table_id, date, time, guests))
        conn.commit()
        conn.close()
        return '', 200  # Respond OK for AJAX
    tables = conn.execute('SELECT * FROM RestaurantTables').fetchall()
    reservations = conn.execute('''
        SELECT r.reservation_id, c.name, r.table_id, r.reservation_date, r.reservation_time, r.num_guests, r.status
        FROM Reservations r
        JOIN Customers c ON r.customer_id = c.customer_id
    ''').fetchall()
    conn.close()
    return render_template('add_reservation.html', tables=tables, reservations=reservations)

@app.route('/get_reservations')
def get_reservations():
    conn = get_db_connection()
    reservations = conn.execute('''
        SELECT r.reservation_id, c.name, r.table_id, r.reservation_date, r.reservation_time, r.num_guests, r.status
        FROM Reservations r
        JOIN Customers c ON r.customer_id = c.customer_id
    ''').fetchall()
    conn.close()
    # Convert to list of dicts
    return jsonify([dict(r) for r in reservations])

if __name__ == '__main__':
    app.run(debug=True, port=4000)