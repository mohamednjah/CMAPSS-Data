'use client';

import React, { useState, useEffect } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const Home = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null);
  const [bestModelRUL, setBestModelRUL] = useState(null);
  const [fetchingRUL, setFetchingRUL] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5001/api/data'); // Your backend endpoint
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const jsonData = await response.json();
    
        // Reduce the number of points to display
        const downsampleFactor = 5; // Display every 5th data point
    
        const formattedData = jsonData.map(model => ({
          model: model.model,
          predictions: model.predictions
            .filter((_, index) => index % downsampleFactor === 0)
            .map((value, index) => ({
              index: index + 1,
              value: value
            })),
          calculations: model.calculations
        }));
    
        setData(formattedData);
      } catch (err) {
        setError(err);
        console.error("Error fetching data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleFileUpload = async (event) => {
    const uploadedFile = event.target.files[0];
    if (!uploadedFile) return;
    setFile(uploadedFile);
    setFetchingRUL(true);

    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
      const response = await fetch('http://localhost:5001/api/rul', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setBestModelRUL(data.rul);
    } catch (err) {
      console.error("Error fetching RUL:", err);
      setBestModelRUL(null);
    } finally {
      setFetchingRUL(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="bg-gray-300 animate-pulse h-32 w-64 rounded-md"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 text-center font-semibold p-4">
        Error: {error.message}
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-center">Model Predictions</h1>

      <div className="flex flex-col items-center space-y-4">
        <input
          type="file"
          className="border p-2 rounded-md w-80"
          onChange={handleFileUpload}
        />
      </div>

      {bestModelRUL !== null && (
        <div className="bg-green-100 p-4 rounded-md text-center">
          <h2 className="text-lg font-bold text-black">Best Model RUL</h2>
          <p className="text-xl font-semibold">{bestModelRUL}</p>
        </div>
      )}

      {data.map((modelData, idx) => (
        <div key={idx} className="bg-white shadow-md rounded-lg p-4">
          <div className="border-b pb-2 font-semibold text-lg text-black">{modelData.model}</div>
          <div className="p-2">
            <div className="flex flex-wrap gap-4">
              {/* Display Calculations */}
              <div className="w-full md:w-1/3 p-4 border rounded-lg bg-gray-50 shadow-sm">
                <h3 className="text-sm font-semibold text-black">Performance Metrics</h3>
                <ul className="text-gray-700 text-sm space-y-1 mt-2">
                  {Object.entries(modelData.calculations).map(([key, value]) => (
                    <li key={key}>
                      <span className="font-medium">{key}:</span> 
                      {key === "Accuracy" ? `${(parseFloat(value) * 100).toFixed(2)}%` : parseFloat(value).toFixed(4)}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Display Chart */}
              <div className="w-full md:w-2/3">
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={modelData.predictions}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="index" label={{ value: "Index", position: "insideBottom", offset: -5 }} />
                    <YAxis label={{ value: "Predicted Value", angle: -90, position: "insideLeft" }} />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="value" stroke="#8884d8" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Home;
