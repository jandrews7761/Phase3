// npm install --save mysql2

// get the client
const mysql = require('mysql2');

// create the connection to database
const connection = mysql.createConnection({
  host: 'academic-mysql.cc.gatech.edu',
  user: 'cs4400_Group_',
  password: '',
  database: 'cs4400_Group_'
});

connection.query(
    'SELECT * FROM `User`;',
    function(err, results, fields) {
      console.log(results); // results contains rows returned by server
    //   console.log(fields); // fields contains extra meta data about results, if available
    }
  );