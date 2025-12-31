import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình trang web
st.set_page_config(page_title="Hệ thống Quản trị Henry Team", layout="wide")

st.title("🚀 Hệ thống Quản trị Sale & Chất lượng Data")
st.markdown("---")

# --- 1. HÀM HỖ TRỢ ---
def to_seconds(s):
    if pd.isna(s) or str(s).lower() == 'in progress' or s == '-':
        return 0
    try:
        parts = str(s).strip().split(':')
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        return 0
    except: return 0

def translate_desc(desc):
    desc = str(desc).lower()
    if "not a valid number" in desc or "disconnected" in desc: return "Data Sai/Số Ảo"
    if "not answered" in desc: return "Khách Không Nghe Máy"
    if "busy" in desc: return "Máy Bận"
    if "internet connection" in desc or "offline" in desc: return "Lỗi Mạng/Thiết Bị"
    if "accepted" in desc or "connected" in desc: return "Kết Nối Thành Công"
    if "hung up" in desc: return "Khách Dập Máy Sớm"
    return "Khác/Chưa xác định"

# --- 2. TẢI FILE ---
uploaded_file = st.file_uploader("📂 Kéo thả file CSV Call Log vào đây", type=["csv"])

if uploaded_file is not None:
    # Đọc dữ liệu
    df = pd.read_csv(uploaded_file, low_memory=False)
    df = df.drop_duplicates().copy()
    
    # Xử lý cột Extension & Thời gian
    df[['Ext_Num', 'Staff_Name']] = df['Extension'].str.split(' - ', n=1, expand=True)
    df['Ext_Num'] = df['Ext_Num'].fillna('Unknown')
    df['Staff_Name'] = df['Staff_Name'].fillna('Unknown Staff')
    df['Sec'] = df['Duration'].apply(to_seconds)
    df['Status_VN'] = df['Result Description'].apply(translate_desc)
    
    # Lấy giờ gọi (0-23) để làm biểu đồ giờ vàng
    df['Hour'] = pd.to_datetime(df['Time'], format='%I:%M %p', errors='coerce').dt.hour
    
    # Lọc cuộc gọi đi
    df_out = df[df['Direction'] == 'Outgoing'].copy()

    # --- 3. TÍNH CHỈ SỐ TỔNG QUAN (METRICS) ---
    total_calls = len(df_out)
    success_calls = (df_out['Sec'] > 0).sum()
    hot_calls = (df_out['Sec'] >= 1800).sum()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("📞 Tổng cuộc gọi đi", f"{total_calls} cuộc")
    m2.metric("✅ Cuộc gọi có kết nối", f"{success_calls} cuộc", f"{round(success_calls/total_calls*100,1)}%")
    m3.metric("🔥 Cuộc gọi VIP (>30p)", f"{hot_calls} cuộc")

    # --- 4. PHÂN TÍCH THEO NHÂN VIÊN ---
    def get_stats(group):
        total = len(group)
        conn = ((group['Action Result'] == 'Call connected') | (group['Sec'] > 0)).sum()
        
        # Sắp xếp giờ để lấy cuộc đầu và cuối
        sorted_group = group.sort_values(by=['Date', 'Time'], ascending=True)
        first_c = sorted_group['Time'].iloc[0]
        last_c = sorted_group['Time'].iloc[-1]
        
        return pd.Series({
            'Tên Nhân Viên': group['Staff_Name'].iloc[0],
            'Bắt đầu': first_c,
            'Kết thúc': last_c,
            'Tổng gọi': total,
            'Bắt máy': conn,
            'Tỷ lệ %': round(conn/total*100, 1) if total > 0 else 0,
            'Trên 5p': (group['Sec'] >= 300).sum(),
            'Trên 10p': (group['Sec'] >= 600).sum(),
            'Trên 30p': (group['Sec'] >= 1800).sum(),
            'Lỗi hay gặp nhất': group['Status_VN'].value_counts().idxmax()
        })

    report = df_out.groupby('Ext_Num').apply(get_stats, include_groups=False).reset_index()
    report = report.sort_values('Trên 5p', ascending=False)

    # --- 5. HIỂN THỊ CHI TIẾT ---
    st.subheader("🏆 Bảng Xếp Hạng Hiệu Suất & Kỷ Luật")
    st.dataframe(report, use_container_width=True)

    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("⏰ Phân tích Giờ Vàng (Toàn Team)")
        hourly_data = df_out.groupby('Hour').size().reset_index(name='Số lượng cuộc gọi')
        fig_hour = px.line(hourly_data, x='Hour', y='Số lượng cuộc gọi', markers=True, title="Lưu lượng cuộc gọi theo giờ")
        st.plotly_chart(fig_hour, use_container_width=True)
        

    with c2:
        st.subheader("🚨 Cảnh báo Chất lượng Data")
        bad_data_count = (df_out['Status_VN'] == 'Data Sai/Số Ảo').sum()
        st.warning(f"Phát hiện {bad_data_count} cuộc gọi vào số ảo/số chết. Chiếm {round(bad_data_count/total_calls*100,1)}% tổng Data.")
        
        error_df = df_out['Status_VN'].value_counts().reset_index()
        fig_error = px.pie(error_df, values='count', names='Status_VN', title="Tỷ lệ các loại lỗi")
        st.plotly_chart(fig_error, use_container_width=True)
        

    # --- 6. XUẤT BÁO CÁO ---
    st.divider()
    csv_data = report.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Tải Báo Cáo Sạch Về Máy",
        data=csv_data,
        file_name='Bao_Cao_Henry_Team_Final.csv',
        mime='text/csv'
    )