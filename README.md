# shopify_challenge_2019

## Installation
Postgres installation
1. Install postgres [downloads](https://www.postgresql.org/download/)
2. Start Postgres `pg_ctl -D /usr/local/var/postgres start`
3. Create database `createdb demo`
4. Run SQL script to create tables and initial products `psql  -d demo -1 -f dump.sql`

Python & pip environments
1. `pip install venv` to create your environment
2. `source venv/bin/activate` to enter the virtual environment
3. `pip install -r requirements.txt` to install the requirements in the current environment
