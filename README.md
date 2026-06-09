🚨 Sentiinel-AI

An intelligent SOC (Security Operations Center) dashboard that monitors system and network activity in real-time and detects anomalies using data analysis and visualization techniques.

---

📌 Overview

This project is designed to simulate a lightweight AI-powered network monitoring system that helps identify unusual patterns in system performance and network traffic.

It combines:

- 📊 Real-time monitoring
- 🧠 Data analysis
- 📈 Interactive dashboards

to provide insights into potential anomalies that may indicate security threats or abnormal system behavior.

---

🚀 Features

- 🔍 Real-Time Monitoring
  
  - Tracks CPU usage, memory usage, and system stats using "psutil"

- 📊 Interactive Dashboard
  
  - Built with "Streamlit" for live visualization

- 📈 Data Visualization
  
  - Graphs and charts using "Plotly"

- 🧠 Anomaly Detection Logic
  
  - Identifies unusual spikes or deviations in system behavior

- 💾 Data Storage
  
  - Stores logs using "SQLite3"

---

🛠️ Tech Stack

- Frontend / Dashboard: Streamlit
- Backend / Logic: Python
- Libraries:
  - "psutil" – system monitoring
  - "pandas" – data processing
  - "plotly" – visualization
- Database: SQLite

---

📂 Project Structure

ai-network-anomaly-detection/
│── app.py            # Main dashboard (Streamlit app)
│── monitor.py        # System monitoring logic
│── init_db.py        # Database initialization
│── model.py          # Anomaly detection logic
│── soc_logs.db       # SQLite database
│── .gitignore

---

⚙️ Installation & Setup

1️⃣ Clone the repository

git clone https://github.com/amita0302/ai-network-anomaly-detection.git
cd ai-network-anomaly-detection

2️⃣ Create virtual environment

python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install dependencies

pip install -r requirements.txt

(If requirements.txt is missing, install manually: streamlit, psutil, pandas, plotly)

---

▶️ Run the Application

streamlit run app.py

Then open in browser:

http://localhost:8501

---

🎯 Use Cases

- 🔐 Cybersecurity monitoring (SOC simulation)
- 🖥️ System performance analysis
- 📊 Learning data visualization & anomaly detection
- 🎓 Academic / internship project

---

🔮 Future Enhancements

- 🤖 Integrate Machine Learning models (Isolation Forest, etc.)
- 🌐 Monitor real network packets
- 🔔 Alert system (Email / SMS)
- ☁️ Deploy on cloud (AWS / Azure)

---

🙌 Contribution

Contributions are welcome!
Feel free to fork the repo and submit a pull request.

---

📜 License

This project is for educational purposes.

---

👩‍💻 Author

Amita Singh
B.Tech CS | AI & Cybersecurity Enthusiast

---

⭐ If you like this project, give it a star!
