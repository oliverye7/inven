# inven
grocery tracking 

# Setup:
run `npm i`

### Connecting to the DB

install pSQL from https://www.postgresql.org/download/

confirm pSQL works by running `psql -u postgres` in your terminal. you should be prompted for a password, and if your command line has something that looks like `postgres=#`, you should be good to go.


**_the table/db process is not yet automated. it is coming soon but you have to manually create it for now._**

copy the code from `/server/database.sql` into the psql session:

1) run `CREATE DATABASE inven_app;`
2) move into the `inven_app` db by running `\c inven_app`. your command line should now have `inven_app=#`.
3) create the three tables by copying them in one by one. 

set the environment variable `DATABASE_URL` to the connection string for your newly created `inven_app` database.

___

### Client Setup

From the root of this repository, run `pip install -e .`.

### Server Setup

Run `nodemon index.js` in `/server`, and the server should start listening on port 4000. Feel free to update the port as needed.
