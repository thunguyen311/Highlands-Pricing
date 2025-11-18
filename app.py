import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Cấu hình trang ---
st.set_page_config(page_title="Highlands Pricing Strategy", layout="wide")
st.title("Highlands Coffee - Chiến lược Tối ưu hóa Giá")

# --- 2. Load Data ---
@st.cache_data
def load_data():
    # Lưu ý: Trên Colab file nằm ngay thư mục gốc
    try:
        df = pd.read_csv('transaction_data.csv')
        cus = pd.read_csv('customer_profile.csv')
        return df, cus
    except:
        return None, None

df, cus = load_data()

if df is None:
    st.error("Chưa tìm thấy file dữ liệu! Hãy upload file csv vào thư mục bên trái.")
else:
    # --- 3. Giao diện chính ---
    tab1, tab2, tab3 = st.tabs(["Tổng quan", "Phân khúc", "Tối ưu hóa"])

    with tab1:
        st.header("Bức tranh kinh doanh")
        col1, col2 = st.columns(2)
        col1.metric("Tổng số giao dịch", f"{len(df):,}")
        col2.metric("Doanh thu ước tính", f"{df['Total_Paid'].sum():,.0f} VNĐ")
        
        st.subheader("Dữ liệu chi tiết")
        st.dataframe(df.head())

    with tab2:
        st.header("Phân khúc khách hàng (Demo)")
        st.write("Biểu đồ phân phối thu nhập khách hàng:")
        fig, ax = plt.subplots()
        # Giả lập biểu đồ đơn giản từ data có sẵn
        if 'Income level' in cus.columns:
            sns.countplot(data=cus, y='Income level', ax=ax, palette="viridis")
            st.pyplot(fig)
        else:
            st.warning("Không tìm thấy cột Income level")

    with tab3:
        st.header("Giả lập Tối ưu giá")
        price = st.slider("Điều chỉnh giá bán (VNĐ)", 30000, 60000, 45000, step=1000)
        st.write(f"Nếu giá bán là **{price:,} VNĐ**, dự báo doanh thu sẽ thay đổi...")
        # (Chỗ này sau này bạn sẽ dán code thuật toán tối ưu vào)
# 1. Lấy địa chỉ IP của máy Colab (Dùng làm mật khẩu đăng nhập)
print("MẬT KHẨU CỦA BẠN LÀ:")
!wget -q -O - ipv4.icanhazip.com

# 2. Chạy Streamlit qua LocalTunnel

!streamlit run app.py & npx localtunnel --port 8501
