const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const app = express();
const port = 3000;

// Connect to your SQLite database
const db = new sqlite3.Database('data/2012corn.db');

// Define an API endpoint to retrieve data
app.get('/api/data', (req, res) => {
    // Write your SQLite query to fetch data
    db.all('SELECT * FROM Plant_Ht_by_Plot', (err, rows) => {
        if (err) {
            console.error(err);
            res.status(500).json({ error: 'Internal Server Error' });
        } else {
            res.json(rows); // Send the data as JSON
        }
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
