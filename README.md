# shopify_challenge_2019

https://github.com/gracegan0116/shopify_challenge_2019

## Installation
Postgres installation
1. Install postgres [downloads](https://www.postgresql.org/download/)
2. Start Postgres `pg_ctl -D /usr/local/var/postgres start`
3. Create database `createdb demo`
4. Run SQL script to create tables and initial products `psql  -d demo -1 -f dump.sql`

Python & pip environments
1. `pip install virtualenv` to create your environment
2. `virtualenv demo`
2. `source demo/bin/activate` to enter the virtual environment
3. `pip install -r requirements.txt` to install the requirements in the current environment

## Usage
`python app.py`

## API Documentation

- [GET] `/search`  
  Description: Search for products, if there's no input parameters then it will return all products with inventory number greater than 1  
  Input Param(URL query):
  - `product_id` [OPTIONAL]
  - `title` [OPTIONAL]  
  - `price` [OPTIONAL]
  - `inventory_count` [OPTIONAL]
  
  Example Output:
  ```
   [
    {
        "inventory_count": 5,
        "price": 4,
        "product_id": 13,
        "title": "Peach"
    },
    {
        "inventory_count": 7,
        "price": 4,
        "product_id": 3,
        "title": "Pear"
    }
  ]
  ```
  

- [POST] `/purchase`  
  Description: purchase 1 item with the associated product_id  
  Input Param(Body):
  - `product_id`   
  
  Example Output:
  ```
  {
    "message": "success"
  }
  ```

- [POST] `/create_cart`  
  Description: create a shopping cart and get back its associated cart_id  
  No Input Param  
  
  Example Output:
   ```
  {
    "cart_id": 17
  }
  ```
  
- [PUT] `/add_to_cart`  
  Description: add product(s) to the specified cart and return the total cost of all the items in the cart  
  Input Param(Body):
  - `cart_id`
  - `product_id`
  - `number`  
  
  Example Output:
  ```
  {
    "total_cost_of_cart": 8
  }
  ```
- [PUT] `/remove_from_cart`  
  Description: remove product(s) from the specified cart and return the total cost of all items in the cart  
  Input Param(Body):
  - `cart_id`
  - `product_id`
  - `number`  
  
  Example Output:
  ```
  {
    "total_cost_of_cart": 4
  }
  ```
  
 - [POST] `/purchase_cart`  
  Description: purchase all items in the specified cart and return the purchase status of each item in the cart  
  Input Param(Body):
   - `cart_id`  
  
   Example Output:
   ```
   {
     "Orange": "insufficient amount of Orange in stock",
     "Peach": "complete"
   }
   ```
