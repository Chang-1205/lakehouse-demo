import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Cấu hình trang Web
st.set_page_config(page_title="Hệ thống Quản trị Data Lakehouse - Nhóm 1", layout="wide")

# --- PHẦN 1: GIẢ LẬP DỮ LIỆU (BACKEND) ---
@st.cache_data
def generate_data():
    np.random.seed(42)
    data = []
    start_time = datetime.now() - timedelta(hours=24)
    channels = ['Mobile App', 'Internet Banking', 'ATM', 'POS']
    segments = ['VIP', 'Mass', 'Corporate']
    
    for i in range(100):
        amount = np.random.choice([
            np.random.randint(1, 10)*1e6, 
            np.random.randint(10, 50)*1e6, 
            np.random.randint(100, 500)*1e6
        ], p=[0.7, 0.2, 0.1])
        
        data.append({
            "txn_id": f"TXN{984500 + i}",
            "source_acc": f"10293{np.random.randint(1000,9999)}",
            "target_acc": f"19034{np.random.randint(1000,9999)}",
            "amount": amount,
            "timestamp": start_time + timedelta(minutes=i*15),
            "channel": np.random.choice(channels),
            "segment": np.random.choice(segments)
        })
    return pd.DataFrame(data)

df_raw = generate_data()

# --- PHẦN 2: GIAO DIỆN SIDEBAR (ĐIỀU KHIỂN) ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/b/bf/Logo_PTIT.png", width=100)
st.sidebar.header("🏦 QUẢN TRỊ LAKEHOUSE")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Chọn tầng dữ liệu quan sát:", 
                         ["Tổng quan", "1. Bronze Layer (Raw)", "2. Silver Layer (Cleaned)", "3. Gold Layer (Analytics)"])

st.sidebar.markdown("---")
st.sidebar.subheader("Kiểm thử hệ thống")
run_acid = st.sidebar.button("Simulate ACID Failure")

# --- PHẦN 3: HIỂN THỊ NỘI DUNG ---
st.title("🛡️ Data Lakehouse Financial Management Dashboard")
st.info(f"Mã giao dịch mẫu đang truy vết: **TXN984573** | Trạng thái: {menu}")

if menu == "Tổng quan":
    st.markdown("""
    ### Chào mừng đến với giải pháp Data Lakehouse của Nhóm 01
    Hệ thống này mô phỏng kiến trúc **Medallion** giúp ngân hàng hợp nhất:
    * **Quản trị CSDL:** Đảm bảo tính toàn vẹn ACID.
    * **Bảo mật:** Tự động Masking dữ liệu nhạy cảm.
    * **Phân tích:** Dashboard rủi ro và thanh khoản thời gian thực.
    """)
    st.image("https://www.databricks.com/wp-content/uploads/2022/03/medallion-architecture-1.png")

elif menu == "1. Bronze Layer (Raw)":
    st.subheader("📁 Lớp Bronze: Lưu trữ chứng từ gốc điện tử")
    st.write("Dữ liệu thô, bất biến (Immutable), phục vụ mục đích kiểm toán sau này.")
    st.dataframe(df_raw, use_container_width=True)

elif menu == "2. Silver Layer (Cleaned)":
    st.subheader("✨ Lớp Silver: Dữ liệu đã làm sạch & Bảo mật")
    st.success("Đã thực hiện: Khử trùng lặp, Chuẩn hóa và Data Masking (Nghị định 13).")
    
    df_silver = df_raw.copy()
    df_silver['source_acc'] = df_silver['source_acc'].apply(lambda x: str(x)[:3] + "****")
    df_silver['target_acc'] = df_silver['target_acc'].apply(lambda x: str(x)[:3] + "****")
    
    st.dataframe(df_silver, use_container_width=True)

elif menu == "3. Gold Layer (Analytics)":
    st.subheader("📊 Lớp Gold: Thông tin chiến lược & Báo cáo tuân thủ")
    
    # Logic Gold Layer
    df_gold = df_raw.copy()
    df_gold['risk_status'] = df_gold['amount'].apply(lambda x: "HIGH RISK" if x > 1e8 else "NORMAL")
    
    # Chỉ số nhanh
    c1, c2, c3 = st.columns(3)
    c1.metric("Tổng thanh khoản", f"{df_gold['amount'].sum()/1e9:.2f} tỷ VNĐ")
    c2.metric("Giao dịch nghi vấn (AML)", len(df_gold[df_gold['risk_status']=="HIGH RISK"]))
    c3.metric("Năng lực đáp ứng (BCBS 239)", "100%")

    # Biểu đồ động
    tab1, tab2, tab3 = st.tabs(["Biến động Thanh khoản", "Cơ cấu Khách hàng", "Radar Rủi ro"])
    
    with tab1:
        fig1 = px.area(df_gold, x='timestamp', y='amount', title="Biến động dòng tiền nội ngày")
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        fig2 = px.treemap(df_gold, path=['segment', 'channel'], values='amount', title="Phân đoạn khách hàng (Customer 360)")
        st.plotly_chart(fig2, use_container_width=True)
        
    with tab3:
        df_risk = df_gold[df_gold['risk_status'] == "HIGH RISK"]
        fig3 = px.sunburst(df_risk, path=['channel', 'txn_id'], values='amount', title="Truy vết giao dịch rủi ro (AML Alert)")
        st.plotly_chart(fig3, use_container_width=True)

# Giả lập ACID
if run_acid:
    with st.sidebar:
        st.error("🚨 LỖI KẾT NỐI MẠNG!")
        st.write("Đang thực hiện giao dịch... Gặp sự cố tại bước ghi dữ liệu.")
        st.info("Lakehouse Transaction Manager: Đang ROLLBACK...")
        st.success("✅ Đã hoàn trả trạng thái ban đầu. Dữ liệu an toàn!")