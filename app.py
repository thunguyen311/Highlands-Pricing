import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Cấu hình trang ---
st.set_page_config(page_title="Highlands Pricing Strategy", layout="wide")
st.title("☕ Highlands Coffee - Chiến lược Tối ưu hóa Giá")

# --- 2. Load Data ---
@st.cache_data
def load_data():
    try:
        # Đọc dữ liệu từ file csv nằm cùng thư mục
        df = pd.read_csv('transaction_data.csv')
        cus = pd.read_csv('customer_profile.csv')
        return df, cus
    except FileNotFoundError:
        return None, None
    except Exception as e:
        return None, None

df, cus = load_data()

# --- 3. Giao diện chính ---
if df is None:
    st.error("⚠️ Lỗi: Không tìm thấy file dữ liệu! Vui lòng kiểm tra lại tên file 'transaction_data.csv' và 'customer_profile.csv' trên GitHub.")
else:
    # Tạo 3 Tabs
    tab1, tab2, tab3 = st.tabs(["Tổng quan", "Phân khúc", "Tối ưu hóa"])

    # --- TAB 1: TỔNG QUAN ---
    with tab1:
        st.header("Bức tranh kinh doanh")
        col1, col2 = st.columns(2)
        
        # Tính toán chỉ số cơ bản
        total_txns = len(df)
        total_revenue = df['Total_Paid'].sum()
        
        col1.metric("Tổng số giao dịch", f"{total_txns:,}")
        col2.metric("Doanh thu ước tính", f"{total_revenue:,.0f} VNĐ")
        
        st.subheader("Dữ liệu giao dịch chi tiết")
        st.dataframe(df.head(10))

    # --- TAB 2: PHÂN KHÚC ---
    with tab2:
        st.header("Phân khúc khách hàng (Demo)")
        st.write("Biểu đồ phân phối thu nhập khách hàng:")
        
        # Vẽ biểu đồ
        fig, ax = plt.subplots(figsize=(10, 6))
        if 'Income level' in cus.columns:
            sns.countplot(data=cus, y='Income level', ax=ax, palette="viridis", order=cus['Income level'].value_counts().index)
            plt.title("Phân bổ khách hàng theo mức thu nhập")
            st.pyplot(fig)
        else:
            st.warning("Không tìm thấy cột 'Income level' trong file dữ liệu.")

    # --- TAB 3: TỐI ƯU HÓA ---
    with tab3:
        st.header("Giả lập Tối ưu giá")
        st.info("Điều chỉnh thanh trượt bên dưới để xem tác động đến doanh thu dự kiến.")
        
        col_input, col_result = st.columns([1, 2])
        
        with col_input:
            price = st.slider("Giá bán đề xuất (VNĐ)", min_value=30000, max_value=60000, value=45000, step=1000)
            current_price = 45000
            
        with col_result:
            # Giả lập đơn giản: Giá tăng 10% -> Lượng giảm 15% (Elasticity = -1.5)
            percent_change_price = (price - current_price) / current_price
            elasticity = -1.5 
            percent_change_qty = percent_change_price * elasticity
            
            # Tính toán giả định
            current_daily_revenue = total_revenue / 365 # Giả sử data là 1 năm
            new_daily_revenue = current_daily_revenue * (1 + percent_change_price) * (1 + percent_change_qty)
            
            delta = new_daily_revenue - current_daily_revenue
            
            st.metric(
                label="Doanh thu ngày dự kiến",
                value=f"{new_daily_revenue:,.0f} VNĐ",
                delta=f"{delta:,.0f} VNĐ",
                delta_color="normal"
            )
            
            if delta > 0:
                st.success(f"🚀 Chiến lược này có thể tăng doanh thu thêm {delta:,.0f} VNĐ/ngày")
            elif delta < 0:
                st.error(f"📉 Cảnh báo: Giá này có thể làm giảm doanh thu {abs(delta):,.0f} VNĐ/ngày")
            else:
                st.write("Giá không đổi, doanh thu giữ nguyên.")
```

### Tại sao code cũ bị lỗi?
Đoạn cuối code cũ của bạn chứa:
```python
# 1. Lấy địa chỉ IP...
!streamlit run app.py & ...
