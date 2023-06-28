const Pool = require("pg").Pool;

const pool = new Pool({
    user: "postgres",
    password: "oliverye77",
    host: "localhost",
    port: 5432,
    database: "inven_app"
});

module.exports = pool;
