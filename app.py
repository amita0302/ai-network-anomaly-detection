import streamlit as st
import psutil
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
from sklearn.ensemble import IsolationForest
from streamlit_autorefresh import st_autorefresh

# ================= AUTO REFRESH =================
st_autorefresh(interval=2000, key="refresh")

# ================= PAGE CONFIG ==========



# =======
st.set_page_config(page_title="SOC AI Network Dashboard", layout="wide")

# ================= LOGIN SYSTEM =================
USER = "admin"
PASS = "admin123"

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: none;}
        .block-container {padding-top: 1rem;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
            <div style="
                background: #111827;
                padding: 35px;
                border-radius: 16px;
                box-shadow: 0px 0px 25px rgba(0,0,0,0.6);
                text-align: center;
            ">
                <h2 style="color:white;">🛡 Secure Login</h2>
            </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        st.markdown(
            "<div style='text-align:right; font-size:12px; color:#60a5fa;'>Forgot Password?</div>",
            unsafe_allow_html=True
        )

        if st.button("Sign In"):
            if username == USER and password == PASS:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    st.stop()

# ================= DATABASE =================
def get_connection():
    return sqlite3.connect("soc_logs.db", check_same_thread=False)

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    upload REAL,
    download REAL,
    total REAL,
    status TEXT
)
""")
conn.commit()

# ================= SESSION STATE =================
if "model" not in st.session_state:
    st.session_state.model = IsolationForest(contamination=0.05)
    st.session_state.data = []
    st.session_state.upload = []
    st.session_state.download = []
    st.session_state.prev_sent = 0
    st.session_state.prev_recv = 0
    st.session_state.trained = False
    st.session_state.simulate = False

# ================= HEADER =================
st.title("🛡 SOC AI Network Security Dashboard")
st.markdown("Real-time monitoring • AI anomaly detection • App intelligence")

# ================= SIDEBAR =================
st.sidebar.header("💻 System Info")
st.sidebar.write(f"CPU: {psutil.cpu_percent()}%")
st.sidebar.write(f"RAM: {psutil.virtual_memory().percent}%")

if st.sidebar.button("🚨 Simulate Attack"):
    st.session_state.simulate = not st.session_state.simulate

# ================= NETWORK =================
net = psutil.net_io_counters()

if st.session_state.prev_sent == 0:
    st.session_state.prev_sent = net.bytes_sent
    st.session_state.prev_recv = net.bytes_recv

upload = (net.bytes_sent - st.session_state.prev_sent) / 1024
download = (net.bytes_recv - st.session_state.prev_recv) / 1024

st.session_state.prev_sent = net.bytes_sent
st.session_state.prev_recv = net.bytes_recv

if st.session_state.simulate:
    upload *= 5
    download *= 5

total = upload + download

# ================= STORE DATA =================
st.session_state.data.append([upload, download, total])
st.session_state.upload.append(upload)
st.session_state.download.append(download)

for arr in [st.session_state.data, st.session_state.upload, st.session_state.download]:
    if len(arr) > 80:
        arr.pop(0)

# ================= AI MODEL =================
if len(st.session_state.data) > 25:
    if not st.session_state.trained:
        st.session_state.model.fit(st.session_state.data)
        st.session_state.trained = True

    pred = st.session_state.model.predict(st.session_state.data)
    anomaly = pred[-1] == -1
else:
    anomaly = False

# ================= ATTACK CLASSIFICATION =================
if st.session_state.simulate:
    threat = "🚨 CRITICAL - Simulated Attack"

elif total > 5000:
    threat = "🚨 Possible DDoS Attack"

elif anomaly:
    threat = "🤖 Suspicious Behavior Detected"

elif total > 100:
    threat = "⚠ Traffic Spike"

else:
    threat = "🟢 Normal"

# ================= LOG TO DATABASE =================
cursor.execute("""
INSERT INTO logs (time, upload, download, total, status)
VALUES (?, ?, ?, ?, ?)
""", (
    datetime.now().strftime("%H:%M:%S"),
    upload,
    download,
    total,
    threat
))
conn.commit()

# ================= METRICS =================
col1, col2, col3, col4 = st.columns(4)

col1.metric("⬆ Upload KB/s", f"{upload:.2f}")
col2.metric("⬇ Download KB/s", f"{download:.2f}")
col3.metric("⚡ Total KB/s", f"{total:.2f}")
col4.metric("🚨 Threat Level", threat)

# ================= ALERT SYSTEM =================
st.subheader("🚨 Alerts")

if "CRITICAL" in threat or "DDoS" in threat:
    st.error(f"ALERT: {threat}")

elif "Suspicious" in threat:
    st.warning(f"Warning: {threat}")

else:
    st.success("No active threats detected.")

# ================= AI INSIGHT =================
st.subheader("🧠 AI Insight")

if anomaly:
    st.error(f"⚠️ Anomaly detected! Traffic spike at {total:.2f} KB/s")
else:
    st.success("Traffic is within normal behavioral range.")

# ================= GRAPH =================
st.subheader("📈 Network Trend")

df_graph = pd.DataFrame({
    "Upload": st.session_state.upload,
    "Download": st.session_state.download,
    "Total": [x[2] for x in st.session_state.data]
})

st.line_chart(df_graph)

# ================= PIE CHART =================
st.subheader("📊 Traffic Distribution")

df_pie = pd.DataFrame({
    "Type": ["Upload", "Download"],
    "Value": [sum(st.session_state.upload), sum(st.session_state.download)]
})

fig = px.pie(df_pie, names="Type", values="Value")
st.plotly_chart(fig, use_container_width=True)

# ================= STATISTICS =================
st.subheader("📊 Statistics")

avg_traffic = sum([x[2] for x in st.session_state.data]) / len(st.session_state.data)
max_traffic = max([x[2] for x in st.session_state.data])

col1, col2 = st.columns(2)
col1.metric("Average Traffic", f"{avg_traffic:.2f} KB/s")
col2.metric("Peak Traffic", f"{max_traffic:.2f} KB/s")

# ================= SECURITY LOGS =================
st.subheader("📜 Security Logs")

cursor.execute("""
SELECT time, upload, download, total, status 
FROM logs ORDER BY id DESC LIMIT 20
""")

logs = cursor.fetchall()

log_df = pd.DataFrame(logs, columns=["Time", "Upload", "Download", "Total", "Status"])
st.dataframe(log_df, use_container_width=True)

# ================= DOWNLOAD LOGS =================
st.subheader("📥 Export Logs")

st.download_button(
    label="Download Logs as CSV",
    data=log_df.to_csv(index=False),
    file_name="network_logs.csv",
    mime="text/csv"
)