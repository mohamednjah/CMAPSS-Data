// backend/server.js
const express = require('express');
const cors = require('cors');

const { Pool } = require('pg'); // For PostgreSQL

const app = express();
const port = 5001;

const pool = new Pool({
  user: process.env.DB_USER || "myuser", // Use environment variables or defaults
  password: process.env.DB_PASSWORD || "mypassword",
  host: process.env.DB_HOST || "localhost",
  port: process.env.DB_PORT || 5432, // Port should be a number
  database: process.env.DB_NAME || "mydatabase",
});

// Test the database connection
pool.connect()
  .then(() => console.log('Connected to PostgreSQL'))
  .catch(err => console.error('PostgreSQL connection error:', err));


app.use(cors());  // Allow all origins

app.use(express.json());

app.get('/api/data', async (req, res) => {
  try {
    const client = await pool.connect();
    const result = await client.query('SELECT * FROM "trainning_data_results";'); 

    // shorten the data
    const data = result.rows.map(row => ({
        model: row.model,
        calculations: typeof row.calculations === 'string' ? JSON.parse(row.calculations) : row.calculations,
        predictions: typeof row.predictions === 'string' ? JSON.parse(row.predictions) : row.predictions
      }));
      
    client.release(); 
    
    res.json(data);
  } catch (err) {
    console.error("Error fetching data:", err);
    res.status(500).json({ error: 'Failed to fetch data' });
  }
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});