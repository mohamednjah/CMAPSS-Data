# Big Data Technologies Project

This repository is part of the **Big Data Technologies** project, focusing on creating an end-to-end solution using **CMAPSS (Commercial Modular Aero-Propulsion System Simulation)** Jet Engine Simulated Data. The project demonstrates how to design and implement a big data architecture that processes large-scale sensor data, trains a machine learning model for predictive analytics, and uploads the model parameters to a web interface for real-time predictions.

---

## Table of Contents
1. [Project Overview](#project-overview)  
2. [CMAPSS Jet Engine Data](#cmapss-jet-engine-data)    
3. [Getting Started](#getting-started)  

---

## Project Overview

This project showcases how to:
- **Ingest large-scale sensor data** from jet engines.  
- **Process and store** the data with a big data architecture. 
- **Train a machine learning model** for predicting jet engine performance or remaining useful life.  
- **Deploy** the model parameters onto a web interface, making them accessible for real-time predictions and insights.

The ultimate goal is to demonstrate **predictive maintenance** capabilities using advanced analytics, which is a critical use case in modern IoT and big data scenarios.

---

## CMAPSS Jet Engine Data

**CMAPSS** stands for **Commercial Modular Aero-Propulsion System Simulation** and is a dataset provided by NASA to simulate the behavior of jet engines under various operating conditions. It includes:
- Multiple **operational settings** (throttle resolver angle, altitude, Mach number, etc.).  
- **Sensor measurements** (fan speed, core speed, temperatures, pressures, etc.) recorded over time.  
- **Run-to-failure** cycles for engines, allowing you to train and validate models that predict remaining useful life (RUL) or other performance metrics.


### **  Data Preprocessing**  

Before training the machine learning model, the CMAPSS dataset underwent a structured **data preprocessing pipeline** to enhance data quality, ensure consistency, and optimize it for model training. The following preprocessing steps were applied:  

---  

### **  1. Handling Missing Values**  
  The dataset was analyzed for missing values across all features.  
  No missing values were found, so no imputation or data filling was necessary.  

---  

### **  2. Outlier Detection & Removal**  
  **Outliers** were detected using the **Z-score method** with a threshold of **4.0** to remove extreme values that could distort model performance.  
  **2,985** rows were identified as outliers and removed, ensuring the dataset reflects **realistic engine performance patterns**.  

---  

### **  3. Feature Scaling & Normalization**  
  **Min-Max Scaling** was applied to normalize sensor values and operational settings, ensuring all numerical values fall within a range of **0 to 1**.  
  This step prevents large-valued features from dominating smaller ones and improves **training stability**.  

---  

### **  4. Data Storage & Accessibility**  
  The **cleaned dataset** was stored securely in a **PostgreSQL database** under the table:  
```plaintext
preprocessed_data
```
  A **backup CSV file** was generated and saved for accessibility in:  
📂 `notebooks/data/preprocessed_data.csv`  

  This ensures that the data remains easily accessible for further analysis and model training.  

---  

### **  5. Next Steps**  
  The preprocessed dataset is **ready for machine learning training** and further analysis.  
  The ML team should use the cleaned dataset stored in `preprocessed_data.csv` for **model development and training**.  
  Future steps may involve **feature engineering, model selection, and hyperparameter tuning** based on the preprocessed data.  

---  

📚 **For detailed information on each preprocessing step, refer to:**  
📍 `docs/preprocessing_report.md`



## Getting Started

To run this project locally or in cloud  environment:

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/mohamednjah/CMAPSS-Data.git
   cd CMAPSS-Data
2. **Install requirements**  
   ```bash
   pip install -r requirements.txt
3. **Run containers**  
   ```bash
   .\scripts\run_postgres.ps1
   
4. **Ingest messages to PostgreSQL**
   ```bash
   #for direct ingestion without using a message queuer:
   py ingestion/direct_ingestion.py
   
5.
   **otherwise (still has bugs)**
   ```bash
   #to use a message queuer
   py ingestion/producer.py
   py ingestion/consumer.py
