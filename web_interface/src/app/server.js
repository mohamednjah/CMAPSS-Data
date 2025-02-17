const express = require('express');
const cors = require('cors');
const multer = require('multer');
const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');
const tf = require('@tensorflow/tfjs-node'); // Load TensorFlow.js


const app = express();
const port = 5001;

const pool = new Pool({
  user: process.env.DB_USER || "myuser",
  password: process.env.DB_PASSWORD || "mypassword",
  host: process.env.DB_HOST || "localhost",
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || "mydatabase",
});

// Test the database connection
pool.connect()
  .then(() => console.log('Connected to PostgreSQL'))
  .catch(err => console.error('PostgreSQL connection error:', err));

app.use(cors());
app.use(express.json());

const upload = multer({ dest: 'uploads/' });

app.get('/api/data', async (req, res) => {
  try {
    const client = await pool.connect();
    const result = await client.query('SELECT * FROM "trainning_data_results";');
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

// Load the trained TensorFlow model
const modelPath = path.join(__dirname, '..', '..', 'notebooks', 'models', 'model.json');

let model;
(async () => {
  try {
    model = await tf.loadLayersModel(`file://${modelPath}`);
    console.log("Model loaded successfully");
  } catch (err) {
    console.error("Error loading model:", err);
  }
})();


// Endpoint for file upload and prediction
app.post('/api/rul', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }

    console.log(`File received: ${req.file.originalname}`);
    const filePath = path.join(__dirname, req.file.path);

    // Read and process input data
    const rawData = fs.readFileSync(filePath, 'utf-8');
    const inputData = JSON.parse(rawData); // Assume JSON file for simplicity
    
    // Convert input data to tensor
    const inputTensor = tf.tensor2d(inputData.data, [inputData.data.length, inputData.features]);
    
    // Make prediction
    const prediction = model.predict(inputTensor);
    const predictionArray = await prediction.array();
    
    res.json({ prediction: predictionArray });
    
    // Delete the uploaded file after processing
    fs.unlink(filePath, (err) => {
      if (err) console.error(`Error deleting file: ${err}`);
    });
  } catch (err) {
    console.error("Prediction error:", err);
    res.status(500).json({ error: "Error processing the file" });
  }
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
