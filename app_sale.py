import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Cấu hình trang web
st.set_page_config(page_title="Dream Talent - Analytics", layout="wide")

st.title("🚀 Thống kê Data Ringcentral - Dream Talent")
st.markdown("---")

# --- 1. DANH SÁCH AGENT & MÃ VÙNG ---
AGENT_MAP = {
    "(713) 277-8125": "Anh Leon",
    "(832) 980-4749": "Anh Hưng",
    "(678) 200-5647": "Chị Hà",
    "(210) 251-8822": "Chị Celine",
    "(832) 887-1033": "Anh Tỷ",
    "(678) 921-4288": "Chị Vicky",
    "(949) 554-7999": "Chị Gina"
}

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

def categorize_depth(sec):
    if sec == 0: return "0. Không kết nối"
    if sec <= 10: return "1. 0-10 giây"
    if sec <= 30: return "2. 10-30 giây"
    if sec <= 60: return "3. 30 giây-1 phút"
    if sec <= 300: return "4. 1 phút-5p"
    if sec <= 600: return "5. 5p-10p"
    if sec <= 1800: return "6. 10p-30p"
    return "7. Trên 30p"

def identify_agent(to_phone):
    to_phone = str(to_phone)
    for num, name in AGENT_MAP.items():
        if num in to_phone:
            return name
    return None

# --- 3. TẢI FILE ---
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
    df['Depth'] = df['Sec'].apply(categorize_depth)
    df['Agent_Name'] = df['To'].apply(identify_agent)
    
    df_out = df[df['Direction'] == 'Outgoing'].copy()
    df_out['State'] = df_out['To'].apply(get_state)

    # --- 4. TỔNG QUAN METRICS ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📞 Tổng gọi đi", f"{len(df_out)}")
    m2.metric("✅ Khách nhấc máy", f"{(df_out['Sec'] > 0).sum()}")
    
    agent_calls = df_out[df_out['Agent_Name'].notna()]
    m3.metric("🎧 Kết Nối Agent", f"{len(agent_calls)}")
    
    state_counts = df_out['State'].value_counts().reset_index()
    state_counts.columns = ['Bang', 'Count']
    m4.metric("🌎 Bang chủ lực", state_counts['Bang'].iloc[0] if not state_counts.empty else "N/A")

    st.divider()

    # --- 5. PHÂN TÍCH HIỆU SUẤT AGENT (MÀU XANH ĐẬM ĐẾN NHẠT) ---
    st.subheader("👥 Thống kê Hiệu suất kết nối Agent (3-way/Transfer)")
    if not agent_calls.empty:
        agent_stats = agent_calls.groupby(['Agent_Name', 'Depth']).size().reset_index(name='Số lượng')
        
        # Bảng màu Blues: Từ đậm đến nhạt
        # Plotly sử dụng các bảng màu như 'Blues' hoặc 'GnBu'
        custom_blues = ['#08306b', '#08519c', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef', '#deebf7']
        
        col_a1, col_a2 = st.columns([6, 4])
        with col_a1:
            fig_agent = px.bar(agent_stats, x='Agent_Name', y='Số lượng', color='Depth', 
                               title="Sản lượng cuộc gọi Agent nhận được (Phân loại theo thời lượng)",
                               text_auto=True, barmode='stack',
                               color_discrete_sequence=custom_blues) # Áp dụng màu xanh
            st.plotly_chart(fig_agent, use_container_width=True)
        
        with col_a2:
            agent_total = agent_calls['Agent_Name'].value_counts().reset_index()
            agent_total.columns = ['Agent', 'Cuộc gọi']
            fig_pie_agent = px.pie(agent_total, values='Cuộc gọi', names='Agent', hole=0.4, 
                                   title="Tỷ lệ kết nối Agent",
                                   color_discrete_sequence=px.colors.sequential.Blues_r) # Blues_r là đậm -> nhạt
            st.plotly_chart(fig_pie_agent, use_container_width=True)
    else:
        st.warning("Chưa có dữ liệu kết nối Agent trong file này.")

    st.divider()

    # --- 6. ĐỊA LÝ & CHAMPIONS ---
    c_geo, c_champ = st.columns([6, 4])
    with c_geo:
        st.subheader("📍 Thống kê cuộc phone trên 50 Tiểu bang USA")
        fig_s = px.bar(state_counts.head(20), x='Bang', y='Count', color='Count', text_auto=True, color_continuous_scale='Portland')
        st.plotly_chart(fig_s, use_container_width=True)
    with c_champ:
        st.subheader("🏆 Top 3 Coldcall The Most")
        top_s = df_out.groupby('Staff_Name').size().nlargest(3).reset_index(name='C')
        for i, r in enumerate(top_s.itertuples(), 1):
            st.success(f"Hạng {i}: **{r.Staff_Name}** ({r.C} cuộc)")

    st.divider()

    # --- 7. ĐỘ SÂU HỘI THOẠI (TEAM) ---
    st.subheader("📊 Độ sâu Cuộc hội thoại (Toàn Team)")
    df_conn = df_out[df_out['Sec'] > 0].copy()
    depth_sum = df_conn['Depth'].value_counts().sort_index().reset_index()
    depth_sum.columns = ['Phân lớp', 'Số lượng']
    st.plotly_chart(px.bar(depth_sum, x='Phân lớp', y='Số lượng', color='Phân lớp', text_auto=True), use_container_width=True)

    st.divider()

    # --- 8. BẢNG HIỆU SUẤT CHI TIẾT ---
    st.subheader("📋 Bảng hiệu suất chi tiết nhân viên")
    report = df_out.groupby('Staff_Name').agg(
        Tong_goi=('Direction', 'count'),
        Lượt_Agent=('Agent_Name', 'count'),
        Lop1=('Sec', lambda x: ((x > 0) & (x <= 10)).sum()),
        Lop2=('Sec', lambda x: ((x > 10) & (x <= 30)).sum()),
        Lop3=('Sec', lambda x: ((x > 30) & (x <= 60)).sum()),
        Lop4=('Sec', lambda x: ((x > 60) & (x <= 300)).sum()),
        Lop5=('Sec', lambda x: ((x > 300) & (x <= 600)).sum()),
        Lop6=('Sec', lambda x: ((x > 600) & (x <= 1800)).sum()),
        Lop7=('Sec', lambda x: (x > 1800).sum())
    ).reset_index()
    
    report = report.sort_values('Lượt_Agent', ascending=False)
    report.columns = ['Nhân Viên', 'Tổng gọi', 'Kết Nối Agent', '0-10s', '10-30s', '30s-1m', '1m-5p', '5-10p', '10-30p', '>30p']
    st.dataframe(report, use_container_width=True)

    csv = report.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Tải Báo Cáo Dream Talent", data=csv, file_name='Thong_Ke_Dream_Talent.csv')

else:
    st.info("👋 Chào Henry Team! Vui lòng tải file CSV Call Log.")
