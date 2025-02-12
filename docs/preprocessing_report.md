### **📄 Data Preprocessing Report**
---

## **📌 1. Introduction**
This report documents the preprocessing steps applied to the raw dataset before training a machine learning model. The dataset contains sensor readings from different engines, along with operational settings.

---

## **📌 2. Exploratory Data Analysis (EDA)**  
Before preprocessing, an exploratory analysis was conducted to understand the dataset's structure and identify potential issues.

### **🔹 Dataset Overview:**
- **Total Records (Before Preprocessing):** 101,181  
- **Total Features:** 28  
- **Sensor Features:** 21  
- **Categorical Features:** dataset_name, source  
- **Missing Values:** None  

### **🔹 Data Issues Identified:**
- Presence of outliers in multiple sensor readings.  
- Need for feature scaling due to varying magnitudes of sensor values.  

---

## **📌 3. Preprocessing Steps**  
The following preprocessing steps were applied to clean and prepare the dataset for model training.

### **🔹 Step 1: Handling Missing Values**  
✅ No missing values were found in the dataset.  
✅ Therefore, no imputation was required.  

### **🔹 Step 2: Outlier Removal**  
✅ Applied **Z-score method** to remove outliers using a **threshold of 4.0**.  
✅ **Outliers Removed:** 2,985 rows  
✅ **Final Record Count:** 98,196  

### **🔹 Step 3: Feature Scaling**  
✅ Normalization applied to all sensor values using **Min-Max Scaling**.  
✅ Ensured all sensor values were transformed between **0 and 1**.  

### **🔹 Step 4: Data Storage**  
✅ The **preprocessed dataset** was stored in a **PostgreSQL database** under the table:  


---

## **📌 4. Preprocessed Data Summary**  
After applying all preprocessing steps, the final dataset is structured as follows:

### **🔹 Dataset Information**  
| Metric | Value |
|--------|-------|
| **Total Records (After Preprocessing)** | 98,196 |
| **Total Features** | 28 |
| **Missing Values** | None |

### **🔹 Summary Statistics**  
| Feature | Min | Max | Mean | Std Dev |
|---------|-----|-----|------|---------|
| **cycle** | 1 | 362 | 96.88 | 65.02 |
| **sensor_1** | 0.0 | 1.0 | 0.02 | 0.01 |
| **sensor_2** | 0.1 | 0.7 | 0.38 | 0.14 |
| **sensor_3** | 0.2 | 0.6 | 0.37 | 0.12 |

---

## **📌 5. Conclusion & Next Steps**  
✅ Preprocessing is complete, and the dataset is now ready for training.  
✅ The next phase involves training machine learning models to predict engine failures based on sensor data.  
✅ The `preprocessed_data.csv` file should be used for model development.  

📍 **Author:** Alireza Panahi  
📍 **Project:** CMAPSS Data Preprocessing  
📍 **Date:** February 2025  
