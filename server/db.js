const Pool = require("pg").Pool;
const { types } = require("pg");
types.setTypeParser(1700, (x) => parseFloat(x));

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

module.exports = pool;
