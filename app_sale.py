import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Cấu hình trang web
st.set_page_config(page_title="Hệ thống Quản trị Henry Team", layout="wide")

st.title("🚀 Hệ thống Quản trị Sale & Chất lượng Data")
st.markdown("---")

# --- 1. DỮ LIỆU HỖ TRỢ (Mã vùng -> Tiểu bang) ---
AC_TO_STATE = {
    "714": "California", "408": "California", "209": "California", "213": "California", "310": "California",
    "678": "Georgia", "770": "Georgia", "404": "Georgia", "706": "Georgia",
    "832": "Texas", "281": "Texas", "713": "Texas", "214": "Texas", "210": "Texas",
    "407": "Florida", "305": "Florida", "321": "Florida", "813": "Florida",
    "614": "Ohio", "330": "Ohio", "513": "Ohio",
    "757": "Virginia", "804": "Virginia",
    "412": "Pennsylvania", "215": "Pennsylvania",
    "508": "Massachusetts", "617": "Massachusetts",
    "205": "Alabama", "334": "Alabama",
}

def get_state(phone):
    if pd.isna(phone): return "Unknown"
    match = re.search(r'\((\d{3})\)', str(phone))
    if match:
        ac = match.group(1)
        return AC_TO_STATE.get(ac, f"Other ({ac})")
    return "Unknown"

def to_seconds(s):
    if pd.isna(s) or str(s).lower() == 'in progress' or s == '-': return 0
    try:
        parts = str(s).strip().split(':')
        if len(parts) == 3: return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2: return int(parts[0]) * 60 + int(parts[1])
        return 0
    except: return 0

def translate_desc(desc):
    desc = str(desc).lower()
    if "not a valid number" in desc or "disconnected" in desc: return "Data Sai/Số Ảo"
    if "not answered" in desc: return "Khách Không Nghe Máy"
    if "busy" in desc: return "Máy Bận"
    if "accepted" in desc or "connected" in desc: return "Kết Nối Thành Công"
    return "Khác/Chưa xác định"

# --- 2. TẢI FILE ---
uploaded_file = st.file_uploader("📂 Kéo thả file CSV Call Log vào đây", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, sep=',', on_bad_lines='skip', low_memory=False)
    except:
        df = pd.read_csv(uploaded_file, sep=';', on_bad_lines='skip', low_memory=False)
    
    df = df.drop_duplicates().copy()
    
    # Xử lý dữ liệu
    if 'Extension' in df.columns:
        df[['Ext_Num', 'Staff_Name']] = df['Extension'].str.split(' - ', n=1, expand=True)
    
    df['Sec'] = df['Duration'].apply(to_seconds)
    df['Status_VN'] = df['Result Description'].apply(translate_desc)
    df['Hour'] = pd.to_datetime(df['Time'], errors='coerce').dt.hour
    
    df_out = df[df['Direction'] == 'Outgoing'].copy()
    
    # Phân tích tiểu bang
    df_out['State'] = df_out['To'].apply(get_state)
    state_counts = df_out['State'].value_counts().reset_index()
    state_counts.columns = ['Tiểu bang', 'Số cuộc gọi']

    # --- 3. METRICS TỔNG QUAN ---
    total_calls = len(df_out)
    success_calls = (df_out['Sec'] > 0).sum()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("📞 Tổng cuộc gọi đi", f"{total_calls}")
    m2.metric("✅ Kết nối thành công", f"{success_calls}", f"{round(success_calls/total_calls*100,1)}%")
    m3.metric("🇺🇸 Tiểu bang gọi nhiều nhất", state_counts['Tiểu bang'].iloc[0] if not state_counts.empty else "N/A")

    st.divider()

    # --- 4. BIỂU ĐỒ TIỂU BANG & TOP NHÂN VIÊN ---
    col_left, col_right = st.columns([6, 4])
    with col_left:
        st.subheader("📍 Thống kê theo Tiểu bang")
        fig_state = px.bar(state_counts.head(10), x='Tiểu bang', y='Số cuộc gọi', color='Số cuộc gọi', text_auto=True)
        st.plotly_chart(fig_state, use_container_width=True)

    with col_right:
        st.subheader("🥇 Top 3 'Cày' Cuộc Gọi")
        def get_stats(group):
            return pd.Series({
                'Staff': group['Staff_Name'].iloc[0] if 'Staff_Name' in group.columns else "N/A",
                'Total': len(group)
            })
        report_staff = df_out.groupby('Ext_Num').apply(get_stats).reset_index()
        top3 = report_staff.nlargest(3, 'Total')
        for i, row in enumerate(top3.itertuples(), 1):
            st.success(f"Top {i}: **{row.Staff}** ({row.Total} cuộc)")

    st.divider()

    # --- 5. PHÂN TÍCH GIỜ VÀNG & TỶ LỆ CHỐT (>15 PHÚT) ---
    st.subheader("⏰ Phân tích Khung Giờ Chất Lượng (>15 Phút)")
    
    # Tính toán tỷ lệ theo giờ
    hourly_all = df_out.groupby('Hour').size()
    hourly_long = df_out[df_out['Sec'] >= 900].groupby('Hour').size()
    
    # Kết hợp lại thành DataFrame
    hourly_stats = pd.DataFrame({'Tổng gọi': hourly_all, 'Trên 15p': hourly_long}).fillna(0)
    hourly_stats['Tỷ lệ %'] = round((hourly_stats['Trên 15p'] / hourly_stats['Tổng gọi']) * 100, 1)
    hourly_stats = hourly_stats.reset_index()

    # Tìm giờ có tỷ lệ cao nhất
    if not hourly_stats.empty:
        best_hour = hourly_stats.loc[hourly_stats['Tỷ lệ %'].idxmax()]
        st.info(f"💡 **Khám phá:** Khung giờ **{int(best_hour['Hour'])}h** có tỷ lệ cuộc gọi chất lượng cao nhất (**{best_hour['Tỷ lệ %']}%** cuộc gọi kéo dài trên 15 phút).")

    # Biểu đồ đường kết hợp
    fig_time = px.line(hourly_stats, x='Hour', y='Tỷ lệ %', markers=True, 
                       title="Tỷ lệ % cuộc gọi kéo dài >15 phút theo khung giờ",
                       labels={'Hour': 'Khung giờ (24h)', 'Tỷ lệ %': 'Tỷ lệ cuộc gọi >15p (%)'})
    fig_time.update_traces(line_color='#FF4B4B', line_width=3)
    st.plotly_chart(fig_time, use_container_width=True)

    st.divider()

    # --- 6. SO SÁNH NHÂN VIÊN & XUẤT BÁO CÁO ---
    st.subheader("📊 Hiệu suất chi tiết toàn bộ Team")
    report_all = df_out.groupby('Staff_Name').agg(
        Tổng_gọi=('Direction', 'count'),
        Trên_15p=('Sec', lambda x: (x >= 900).sum())
    ).reset_index()
    
    st.dataframe(report_all.sort_values('Trên 15p', ascending=False), use_container_width=True)
    
    csv = report_all.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Tải Báo Cáo Tổng Hợp", data=csv, file_name='Bao_Cao_Henry_Team.csv')
