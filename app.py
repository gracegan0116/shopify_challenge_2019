from flask import Flask, request, jsonify, json
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(dbname='shopify_challenge', host='localhost', port=5432)
cur = conn.cursor()


@app.route('/search')
def search_products():
    output = []
    params = ['title', 'price', 'product_id', 'inventory_count']
    query_parameters = {}
    query_string = ''
    for param in params:
        result = request.args.get(param)
        if result is not None:
            query_parameters[param] = result

    for index, key in enumerate(query_parameters):
        if index == len(query_parameters) - 1:
            query_string += key + '=%s'
        else:
            query_string += key + '=%s AND '

    if not query_parameters:
        cur.execute('SELECT product_id,title,price,inventory_count FROM products WHERE inventory_count > 0;')

    else:
        query = 'SELECT product_id,title,price,inventory_count FROM products WHERE ' + query_string
        cur.execute(query, tuple(query_parameters.values()))

    rows = set(cur.fetchall())
    # putting into the right format
    for row in rows:
        output.append({'product_id': row[0], 'title': row[1], 'price': row[2], 'inventory_count': row[3]})
    return jsonify(output), 200


@app.route('/purchase', methods=['POST'])
def purchase_products():
    if len(request.data) == 0:
        return jsonify({'error': 'body is empty'}), 400
    body = json.loads(request.data)
    product_id = body['product_id']
    # check if row is empty
    query1 = 'SELECT * FROM products WHERE product_id = %s'
    cur.execute(query1, (product_id,))
    if cur.fetchone() is None:
        return jsonify({'error': 'invalid product_id'}), 400
    else:
        query1 = 'SELECT inventory_count FROM products WHERE product_id = %s'
        cur.execute(query1, (product_id,))
        if cur.fetchone()[0] == 0:
            return jsonify({'message': 'Out of inventory'}), 202

    query2 = 'UPDATE products SET inventory_count = inventory_count -1 WHERE product_id = %s;'
    cur.execute(query2, (product_id,))
    conn.commit()
    return jsonify({'message': 'success'}), 200


@app.route('/create_cart', methods=['POST'])
def create_shopping_cart():
    query_shopping_cart = 'INSERT INTO shopping_cart (purchase_status) VALUES(false) RETURNING cart_id;'
    cur.execute(query_shopping_cart)
    conn.commit()
    cart_id = cur.fetchall()[0][0]
    return jsonify({'cart_id': cart_id}), 200


@app.route('/add_to_cart', methods=['PUT'])
def add_to_cart():
    if len(request.data) == 0:
        return jsonify({'error': 'body is empty'}), 400
    body = json.loads(request.data)
    product_id = body['product_id']
    num_product = body['number']
    cart_id = body['cart_id']

    # check if any parameter is none
    if num_product is None or product_id is None or cart_id is None:
        return jsonify({'error': 'enter cart_id, product_id and number'}), 400

    # check if product_id  and cart_id exist
    cur.execute('SELECT * FROM products WHERE product_id = ' + str(product_id))
    if cur.fetchone() is None:
        return jsonify({'error': 'invalid product_id'}), 400
    cur.execute('SELECT * FROM shopping_cart WHERE cart_id = ' + str(cart_id))
    if cur.fetchone() is None:
        return jsonify({'error': 'invalid cart_id'}), 400

    try:
        query_items_in_cart = 'INSERT INTO items_in_cart (cart_id,product_id,item_count) VALUES(%s,%s,%s);'
        cur.execute(query_items_in_cart, (cart_id, product_id, num_product,))
        conn.commit()
    # product_id already exist in items_in_cart
    except Exception as e:
        conn.rollback()
        query_update = 'UPDATE items_in_cart SET item_count = item_count + %s WHERE product_id = %s and cart_id = %s'
        cur.execute(query_update, (num_product, product_id, cart_id,))
        conn.commit()

    # return total price
    query = 'SELECT product_id, item_count FROM items_in_cart WHERE cart_id = %s;'
    cur.execute(query, (cart_id,))
    items = cur.fetchall()
    price = 0
    for item in items:
        cur.execute('SELECT price FROM products WHERE product_id = ' + str(item[0]))
        price = price + cur.fetchall()[0][0] * item[1]
    return jsonify({'total_cost_of_cart': price}), 200


@app.route('/remove_from_cart', methods=['PUT'])
def remove():
    if len(request.data) == 0:
        return jsonify({'error': 'body is empty'}), 400
    body = json.loads(request.data)
    product_id = body['product_id']
    num_product = body['number']
    cart_id = body['cart_id']

    if num_product is None or product_id is None or cart_id is None:
        return jsonify({'error': 'enter all product_id, cart_id and number'}), 400

    # check if product_id  and cart_id exist
    cur.execute('SELECT * FROM products WHERE product_id = ' + str(product_id))
    if cur.fetchone() is None:
        return jsonify({'error': 'invalid product_id'}), 400
    cur.execute('SELECT * FROM shopping_cart WHERE cart_id = ' + str(cart_id))
    if cur.fetchall() is None:
        return jsonify({'error': 'invalid cart_id'}), 400

    # remove items from cart
    cur.execute('SELECT item_count FROM items_in_cart WHERE product_id = '+str(product_id) + ' and cart_id = ' + str(cart_id))
    item_num = cur.fetchall()
    if item_num[0][0] < int(num_product):
        return jsonify({'error': 'invalid number of items to remove'}), 400
    query_update = 'UPDATE items_in_cart SET item_count = item_count - %s WHERE product_id = %s and cart_id = %s'
    cur.execute(query_update, (num_product, product_id, cart_id,))
    conn.commit()

    # return total price
    query = 'SELECT product_id, item_count FROM items_in_cart WHERE cart_id = %s;'
    cur.execute(query, (cart_id,))
    items = cur.fetchall()
    price = 0
    for item in items:
        cur.execute('SELECT price FROM products WHERE product_id = ' + str(item[0]))
        price = price + cur.fetchall()[0][0] * item[1]
    return jsonify({'total_cost_of_cart': price}), 200


@app.route('/purchase_cart', methods=['POST'])
def purchase_cart():
    if len(request.data) == 0:
        return jsonify({'error': 'body is empty'}), 400
    body = json.loads(request.data)
    cart_id = body['cart_id']
    purchase_status = {}
    if cart_id is None:
        return jsonify({'error': 'enter cart_id'}), 400

    # check shopping_cart status
    query = 'SELECT purchase_status FROM shopping_cart WHERE cart_id = %s'
    cur.execute(query, (cart_id,))
    status = cur.fetchall()
    if status[0][0]:
        return jsonify({'message': 'cart ' + str(cart_id) + ' already purchased'}), 200

    # get items in cart
    query = 'SELECT product_id, item_count FROM items_in_cart WHERE cart_id = %s;'
    cur.execute(query, (cart_id,))
    items_in_cart = cur.fetchall()
    if not items_in_cart:
        return jsonify({'message': 'cart ' + str(cart_id) + ' is empty'}), 200

    for item in items_in_cart:
        query = 'SELECT inventory_count, title FROM products WHERE product_id = %s'
        cur.execute(query, (item[0],))
        info = cur.fetchall()
        if info[0][0] < item[1]:
            purchase_status[info[0][1]] = 'insufficient amount of ' + info[0][1] + ' in stock'
        else:
            query_update = 'UPDATE products SET inventory_count = inventory_count - %s WHERE product_id = %s'
            cur.execute(query_update, (item[1], item[0],))
            conn.commit()
            purchase_status[info[0][1]] = 'complete'

    # update status
    query = 'UPDATE shopping_cart SET purchase_status = TRUE WHERE cart_id = %s'
    cur.execute(query, (cart_id,))
    conn.commit()
    return jsonify(purchase_status), 200


if __name__ == '__main__':
    app.run()
