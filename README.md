# 📊 Data Analyzer

An interactive **Flask web application** that lets users upload datasets (CSV/Excel), visualize them with multiple chart types, and manage a history of generated charts.  

---

## 🚀 Features
- **Upload Datasets**  
  - Supports `.csv` and `.xlsx` files  
  - Displays a **data preview table** before analysis  

- **Interactive Charts**  
  - Choose **X-axis, Y-axis, and Chart Type**  
  - Available chart types:  
    - 📊 Bar Chart  
    - 📈 Line Chart  
    - 🥧 Pie Chart  
    - 📦 Box Plot  
    - 🔹 Scatter Plot  
    - 📉 Histogram  
    - 🌊 Area Chart  
    - 🔥 Heatmap (Correlation)  

- **Chart History**  
  - Automatically saves generated charts with **timestamp, type, and preview**  
  - Download charts as **PNG** or **HTML (interactive)**  

- **Simple UI**  
  - Built with **Bootstrap 5** for responsive design  
  - Clean navigation between **Home** and **Graph History**  

---

## 🛠️ Tech Stack
- **Backend:** Python, Flask  
- **Frontend:** HTML, Jinja2, Bootstrap 5  
- **Data Handling:** Pandas  
- **Visualization:** Plotly (Kaleido for PNG export)  

---
