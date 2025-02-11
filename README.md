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

## Getting Started

To run this project locally or in a cloud environment:

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