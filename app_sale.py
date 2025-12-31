import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Cấu hình trang web
st.set_page_config(page_title="Hệ thống Quản trị Henry Team", layout="wide")

st.title("🚀 Hệ thống Quản trị Sale & Chất lượng Data")
st.markdown("---")

# --- 1. DANH SÁCH MÃ VÙNG ĐẦY ĐỦ (Full 50 States USA) ---
AC_TO_STATE = {
    '201': 'NJ', '202': 'DC', '203': 'CT', '205': 'AL', '206': 'WA', '207': 'ME', '208': 'ID', '209': 'CA', '210': 'TX', '212': 'NY', '213': 'CA', '214': 'TX', '215': 'PA', '216': 'OH', '217': 'IL', '218': 'MN', '219': 'IN', '220': 'OH', '223': 'PA', '224': 'IL', '225': 'LA', '226': 'ON', '228': 'MS', '229': 'GA', '231': 'MI', '234': 'OH', '239': 'FL', '240': 'MD', '248': 'MI', '251': 'AL', '252': 'NC', '253': 'WA', '254': 'TX', '256': 'AL', '260': 'IN', '262': 'WI', '267': 'PA', '269': 'MI', '270': 'KY', '272': 'PA', '276': 'VA', '281': 'TX', '301': 'MD', '302': 'DE', '303': 'CO', '304': 'WV', '305': 'FL', '307': 'WY', '308': 'NE', '309': 'IL', '310': 'CA', '312': 'IL', '313': 'MI', '314': 'MO', '315': 'NY', '316': 'KS', '317': 'IN', '318': 'LA', '319': 'IA', '320': 'MN', '321': 'FL', '323': 'CA', '325': 'TX', '326': 'OH', '330': 'OH', '331': 'IL', '332': 'NY', '334': 'AL', '336': 'NC', '337': 'LA', '339': 'MA', '341': 'CA', '346': 'TX', '347': 'NY', '351': 'MA', '352': 'FL', '360': 'WA', '361': 'TX', '364': 'KY', '380': 'OH', '385': 'UT', '386': 'FL', '401': 'RI', '402': 'NE', '404': 'GA', '405': 'OK', '406': 'MT', '407': 'FL', '408': 'CA', '409': 'TX', '410': 'MD', '412': 'PA', '413': 'MA', '414': 'WI', '415': 'CA', '417': 'MO', '419': 'OH', '423': 'TN', '424': 'CA', '425': 'WA', '428': 'OH', '430': 'TX', '432': 'TX', '434': 'VA', '435': 'UT', '440': 'OH', '442': 'CA', '443': 'MD', '445': 'PA', '447': 'IL', '458': 'OR', '463': 'IN', '469': 'TX', '470': 'GA', '475': 'CT', '478': 'GA', '479': 'AR', '480': 'AZ', '484': 'PA', '501': 'AR', '502': 'KY', '503': 'OR', '504': 'LA', '505': 'NM', '507': 'MN', '508': 'MA', '509': 'WA', '510': 'CA', '512': 'TX', '513': 'OH', '515': 'IA', '516': 'NY', '517': 'MI', '518': 'NY', '520': 'AZ', '530': 'CA', '531': 'NE', '534': 'WI', '539': 'OK', '540': 'VA', '541': 'OR', '551': 'NJ', '559': 'CA', '561': 'FL', '562': 'CA', '563': 'IA', '564': 'WA', '567': 'OH', '570': 'PA', '571': 'VA', '573': 'MO', '574': 'IN', '575': 'NM', '580': 'OK', '585': 'NY', '586': 'MI', '601': 'MS', '602': 'AZ', '603': 'NH', '605': 'SD', '606': 'KY', '607': 'NY', '608': 'WI', '609': 'NJ', '610': 'PA', '612': 'MN', '614': 'OH', '615': 'TN', '616': 'MI', '617': 'MA', '618': 'IL', '619': 'CA', '620': 'KS', '623': 'AZ', '626': 'CA', '628': 'CA', '629': 'TN', '630': 'IL', '631': 'NY', '633': 'MO', '636': 'MO', '640': 'NJ', '641': 'IA', '646': 'NY', '650': 'CA', '651': 'MN', '656': 'FL', '657': 'CA', '660': 'MO', '661': 'CA', '662': 'MS', '667': 'MD', '669': 'CA', '678': 'GA', '679': 'MI', '680': 'NY', '681': 'WV', '682': 'TX', '686': 'VA', '689': 'FL', '701': 'ND', '702': 'NV', '703': 'VA', '704': 'NC', '706': 'GA', '707': 'CA', '708': 'IL', '712': 'IA', '713': 'TX', '714': 'CA', '715': 'WI', '716': 'NY', '717': 'PA', '718': 'NY', '719': 'CO', '720': 'CO', '724': 'PA', '725': 'NV', '726': 'TX', '727': 'FL', '731': 'TN', '732': 'NJ', '734': 'MI', '737': 'TX', '740': 'OH', '743': 'NC', '747': 'CA', '754': 'FL', '757': 'VA', '760': 'CA', '762': 'GA', '763': 'MN', '765': 'IN', '769': 'MS', '770': 'GA', '772': 'FL', '773': 'IL', '774': 'MA', '775': 'NV', '779': 'IL', '781': 'MA', '785': 'KS', '786': 'FL', '787': 'PR', '801': 'UT', '802': 'VT', '803': 'SC', '804': 'VA', '805': 'CA', '806': 'TX', '808': 'HI', '810': 'MI', '812': 'IN', '813': 'FL', '814': 'PA', '815': 'IL', '816': 'MO', '817': 'TX', '818': 'CA', '820': 'CA', '828': 'NC', '830': 'TX', '831': 'CA', '832': 'TX', '838': 'NY', '840': 'CA', '843': 'SC', '845': 'NY', '847': 'IL', '848': 'NJ', '850': 'FL', '854': 'SC', '856': 'NJ', '857': 'MA', '858': 'CA', '859': 'KY', '860': 'CT', '862': 'NJ', '863': 'FL', '864': 'SC', '865': 'TN', '870': 'AR', '872': 'IL', '878': 'PA', '901': 'TN', '903': 'TX', '904': 'FL', '906': 'MI', '907': 'AK', '908': 'NJ', '909': 'CA', '910': 'NC', '912': 'GA', '913': 'KS', '914': 'NY', '915': 'TX', '916': 'CA', '917': 'NY', '918': 'OK', '919': 'NC', '920': 'WI', '925': 'CA', '928': 'AZ', '929': 'NY', '930': 'IN', '931': 'TN', '934': 'NY', '936': 'TX', '937': 'OH', '938': 'AL', '940': 'TX', '941': 'FL', '945': 'TX', '947': 'MI', '948': 'VA', '949': 'CA', '951': 'CA', '952': 'MN', '954': 'FL', '956': 'TX', '959': 'CT', '970': 'CO', '971': 'OR', '972': 'TX', '973': 'NJ', '978': 'MA', '979': 'TX', '980': 'NC', '984': 'NC', '985': 'LA', '986': 'ID', '989': 'MI'
}

# --- 2. HÀM HỖ TRỢ ---
def get_state(phone):
    if pd.isna(phone): return "N/A"
    match = re.search(r'\((\d{3})\)', str(phone))
    if match:
        ac = match.group(1)
        if ac in ['800', '888', '877', '866', '855', '844', '833']: return "Toll-Free"
        return AC_TO_STATE.get(ac, f"Khác ({ac})")
    return "N/A"

def to_seconds(s):
    if pd.isna(s) or str(s).lower() == 'in progress' or s == '-': return 0
    try:
        parts = str(s).strip().split(':')
        if len(parts) == 3: return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2: return int(parts[0]) * 60 + int(parts[1])
        return 0
    except: return 0

# --- 3. TẢI VÀ XỬ LÝ FILE ---
uploaded_file = st.file_uploader("📂 Tải file CSV Call Log", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, sep=',', on_bad_lines='skip', low_memory=False)
    except:
        df = pd.read_csv(uploaded_file, sep=';', on_bad_lines='skip', low_memory=False)
    
    df = df.drop_duplicates().copy()
    
    if 'Extension' in df.columns:
        df[['Ext_Num', 'Staff_Name']] = df['Extension'].str.split(' - ', n=1, expand=True)
        df['Staff_Name'] = df['Staff_Name'].fillna('Unknown Staff')
    
    df['Sec'] = df['Duration'].apply(to_seconds)
    df['Hour'] = pd.to_datetime(df['Time'], errors='coerce').dt.hour
    
    df_out = df[df['Direction'] == 'Outgoing'].copy()
    df_out['State'] = df_out['To'].apply(get_state)

    # --- 4. HIỂN THỊ METRICS TỔNG QUAN ---
    state_counts = df_out['State'].value_counts().reset_index()
    state_counts.columns = ['Bang', 'Cuộc gọi']
    
    m1, m2, m3 = st.columns(3)
    m1.metric("📞 Tổng cuộc gọi đi", f"{len(df_out)}")
    m2.metric("✅ Kết nối (có nhấc máy)", f"{(df_out['Sec'] > 0).sum()}")
    m3.metric("🇺🇸 Bang được gọi nhiều nhất", state_counts['Bang'].iloc[0] if not state_counts.empty else "N/A")

    st.divider()

    # --- 5. BIỂU ĐỒ TIỂU BANG & TOP 3 NHÂN VIÊN ---
    col1, col2 = st.columns([6, 4])
    with col1:
        st.subheader("📍 Thống kê 50 Tiểu bang USA")
        fig_state = px.bar(state_counts.head(50), x='Bang', y='Cuộc gọi', color='Cuộc gọi', text_auto=True)
        st.plotly_chart(fig_state, use_container_width=True)

    with col2:
        st.subheader("🏆 Top 3 Cày Cuộc Gọi")
        top_staff = df_out.groupby('Staff_Name').size().nlargest(3).reset_index(name='Count')
        for i, row in enumerate(top_staff.itertuples(), 1):
            st.success(f"Hạng {i}: **{row.Staff_Name}** ({row.Count} cuộc)")

    st.divider()

    # --- 6. PHÂN TÍCH KHUNG GIỜ VÀNG (ĐÃ CẬP NHẬT LOGIC MỚI) ---
    st.subheader("⏰ Phân tích Khung Giờ Vàng (Dựa trên số khách đã nhấc máy)")
    
    # Chỉ tính trên những cuộc gọi có kết nối (Sec > 0)
    df_connected = df_out[df_out['Sec'] > 0].copy()
    
    hourly_connected = df_connected.groupby('Hour').size() # Tổng khách nhấc máy mỗi giờ
    hourly_long = df_connected[df_connected['Sec'] >= 900].groupby('Hour').size() # Số khách nói trên 15p mỗi giờ
    
    hourly_stats = pd.DataFrame({
        'Đã nhấc máy': hourly_connected, 
        'Trên 15p': hourly_long
    }).fillna(0)
    
    # Tính tỷ lệ % chất lượng cuộc gọi
    hourly_stats['Tỷ lệ %'] = 0.0
    mask = hourly_stats['Đã nhấc máy'] > 0
    hourly_stats.loc[mask, 'Tỷ lệ %'] = round((hourly_stats.loc[mask, 'Trên 15p'] / hourly_stats.loc[mask, 'Đã nhấc máy']) * 100, 1)
    hourly_stats = hourly_stats.reset_index()

    # Hiển thị Info Box cho khung giờ tốt nhất (điều kiện có ít nhất 5 cuộc nhấc máy để số liệu chuẩn)
    reliable_data = hourly_stats[hourly_stats['Đã nhấc máy'] >= 5]
    if not reliable_data.empty:
        best_row = reliable_data.loc[reliable_data['Tỷ lệ %'].idxmax()]
        st.info(f"💡 **Khám phá:** Khung giờ **{int(best_row['Hour'])}h** là thời điểm khách hàng dễ tính nhất. Trong số khách nghe máy, có **{best_row['Tỷ lệ %']}%** người sẵn sàng nói chuyện trên 15 phút.")

    fig_time = px.line(hourly_stats, x='Hour', y='Tỷ lệ %', markers=True, 
                       title="Tỷ lệ khách hàng chịu nói chuyện lâu sau khi nhấc máy (%)",
                       labels={'Hour': 'Giờ trong ngày', 'Tỷ lệ %': 'Tỷ lệ nói chuyện >15p (%)'})
    fig_time.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig_time, use_container_width=True)

    st.divider()

    # --- 7. BẢNG HIỆU SUẤT CHI TIẾT ---
    st.subheader("📊 Hiệu suất chi tiết toàn bộ nhân viên")
    report_final = df_out.groupby('Staff_Name').agg(
        Tong_goi=('Direction', 'count'),
        Tren_15p=('Sec', lambda x: (x >= 900).sum())
    ).reset_index().sort_values('Tren_15p', ascending=False)
    
    report_final.columns = ['Nhân Viên', 'Tổng gọi', 'Trên 15 phút']
    st.dataframe(report_final, use_container_width=True)

    csv = report_final.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Tải Báo Cáo Tổng Hợp", data=csv, file_name='Bao_Cao_Henry_Team.csv')
