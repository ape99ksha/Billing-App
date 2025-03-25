# Import necessary libraries
from flask import Flask, request, jsonify # Flask for creating the API, request to handle requests, and jsonify to return JSON responses
from flask_cors import CORS  # Enables CORS to allow frontend to communicate with the backend
import psycopg2  # PostgreSQL database adapter for Python
#from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)  

# Enable CORS for the entire app (allows frontend requests from different origins)
CORS(app)  

# PostgreSQL Database Configuration (Make sure these match your actual database settings)
DB_CONFIG = {
    "dbname": "Bill",       # **Database name** - Ensure this matches your PostgreSQL database
    "user": "postgres",     # **Database user** - Check if this is correct
    "password": "minal@1999",  # **Database password** - Secure this in a real application!
    "host": "localhost",    # **Database host** - "localhost" for local development
    "port": "5432"         # **Database port** - Default PostgreSQL port is 5432
}

# Function to establish a new database connection
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Open a database connection and create a cursor to execute queries
conn = get_db_connection()
cur = conn.cursor()


# API Endpoint: Add a Bill
@app.route('/api/add_bills', methods=['POST']) # This is a Flask route decorator.
def add_bill(): #POST is used to send data to the server (e.g., to create a new bill).
    data = request.json  # Get JSON data from the frontend request
    
    # Extract relevant data from the JSON request
    
    customer_name = data['customer']         # **Customer name**
    products = data['products']              # **List of products purchased**
    total_amount = data['finalTotal']        # **Final total amount for the bill**
    payment_method = data['paymentMethod']   # **Payment method (cash, card, etc.)**

    try: 
        conn = get_db_connection()  # Establish a new database connection
        cur = conn.cursor() #Creates a cursor object using the database connection.

        cur.execute(
            "INSERT INTO customers (customer_name) VALUES (%s) RETURNING customer_id;", (customer_name,))
        customer_id = cur.fetchone()[0]  # Fetch the newly generated customer ID

        # Insert bill details into the "bills" table
        cur.execute(
            "INSERT INTO bills (customer_id, total_amount, payment_method) VALUES (%s, %s, %s) RETURNING customer_id;",
            (customer_id, total_amount, payment_method)  #datetime.now()
        )
        bill_id = cur.fetchone()[0]
        # customer_id = cur.fetchone()[0]

        # Insert products into the "bill_items" table
        for product in products:
            cur.execute(
                "INSERT INTO bill_items (product_id, quantity, discount, total_price) "
                "VALUES ((SELECT product_id FROM products WHERE product_name = %s LIMIT 1), %s, %s, %s) RETURNING bill_item_id ;",
                (product['product_name'], product['quantity'], product['discount'], product['total'])  
            )
        # bill_item_id = cur.fetchone()[0]

        conn.commit()  # Save changes to the database
        cur.close()
        conn.close()
        
        return jsonify({"message": "Bill added successfully!"}), 201  # Return success message

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message if something goes wrong

# API Endpoint: Get All Bills
@app.route('/api/get_bills', methods=['GET'])
def get_bills():
    try:
        conn = get_db_connection()  # Establish a new database connection
        cur = conn.cursor()

        # Fetch all bills along with customer names
        cur.execute("""
            SELECT b.bill_id, c.customer_name, b.total_amount, b.payment_method
            FROM bills b
            JOIN customers c ON b.customer_id = c.customer_id
        """)
        bills = cur.fetchall()  # Get all results

        cur.close()
        conn.close()

        # Returning the bills in JSON format
        bill_list = []
        for bill in bills:
            bill_list.append({
                "id": bill[0],
                "customer": bill[1],
                "payment_method": bill[2],
                "total_amount": bill[3]
            })

        return jsonify(bill_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message if something goes wrong
    
@app.route('/api/get_bill/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch bill details
        cur.execute("""
            SELECT b.bill_id, c.customer_name, b.payment_method, b.total_amount, b.bill_date
            FROM bills b
            JOIN customers c ON b.customer_id = c.customer_id
            WHERE b.bill_id = %s;
        """, (bill_id,))
        bill = cur.fetchone()

        if not bill:
            return jsonify({"error": "Bill not found"}), 404

        # Fetch products for the bill
        cur.execute("""
            SELECT p.product_name, bi.quantity, bi.discount, bi.total_price
            FROM bill_items bi
            JOIN products p ON bi.product_id = p.product_id
            WHERE bi.bill_id = %s;
        """, (bill_id,))
        products = cur.fetchall()

        # Format the response
        bill_details = {
            "id": bill[0],
            "customer": bill[1],
            "payment_method": bill[2],
            "total_amount": bill[3],
            "bill_date": bill[4],
            "products": [
                {
                    "product_name": product[0],
                    "quantity": product[1],
                    "discount": product[2],
                    "total_price": product[3]
                }
                for product in products
            ]
        }

        return jsonify(bill_details), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Start the server in debug mode
