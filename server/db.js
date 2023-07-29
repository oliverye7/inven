const Pool = require("pg").Pool;

const pool = new Pool({
    user: "rahul",
    password: "rahul",
    host: "localhost",
    database: "inven_app",
    port: 5432
});

module.exports = pool;
