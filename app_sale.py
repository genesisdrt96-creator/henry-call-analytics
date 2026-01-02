import streamlit as st
import pandas as pd
import plotly.express as px
import re
import numpy as np

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Dream Talent - Analytics", layout="wide")

st.title("🚀 Thống kê Data Ringcentral - Dream Talent")
st.markdown("---")

# --- 2. DANH SÁCH AGENT & MÃ VÙNG ---
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

    # Alabama (AL)
    '205': 'AL', '251': 'AL', '256': 'AL', '334': 'AL', '659': 'AL', '938': 'AL',
    # Alaska (AK)
    '907': 'AK',
    # Arizona (AZ)
    '480': 'AZ', '520': 'AZ', '602': 'AZ', '623': 'AZ', '928': 'AZ',
    # Arkansas (AR)
    '327': 'AR', '479': 'AR', '501': 'AR', '870': 'AR',
    # California (CA)
    '209': 'CA', '213': 'CA', '279': 'CA', '310': 'CA', '323': 'CA', '341': 'CA', 
    '408': 'CA', '415': 'CA', '424': 'CA', '442': 'CA', '510': 'CA', '530': 'CA', 
    '559': 'CA', '562': 'CA', '619': 'CA', '626': 'CA', '628': 'CA', '650': 'CA', 
    '657': 'CA', '661': 'CA', '669': 'CA', '707': 'CA', '714': 'CA', '747': 'CA', 
    '760': 'CA', '805': 'CA', '818': 'CA', '820': 'CA', '831': 'CA', '858': 'CA', 
    '909': 'CA', '916': 'CA', '925': 'CA', '949': 'CA', '951': 'CA',
    # Colorado (CO)
    '303': 'CO', '719': 'CO', '720': 'CO', '970': 'CO', '983': 'CO',
    # Connecticut (CT)
    '203': 'CT', '475': 'CT', '860': 'CT', '959': 'CT',
    # Delaware (DE)
    '302': 'DE',
    # Florida (FL)
    '239': 'FL', '305': 'FL', '321': 'FL', '352': 'FL', '386': 'FL', '407': 'FL', 
    '448': 'FL', '561': 'FL', '645': 'FL', '689': 'FL', '727': 'FL', '754': 'FL', 
    '772': 'FL', '786': 'FL', '813': 'FL', '850': 'FL', '863': 'FL', '904': 'FL', '941': 'FL', '954': 'FL',
    # Georgia (GA)
    '229': 'GA', '404': 'GA', '470': 'GA', '478': 'GA', '678': 'GA', '706': 'GA', '762': 'GA', '770': 'GA', '912': 'GA',
    # Hawaii (HI)
    '808': 'HI',
    # Idaho (ID)
    '208': 'ID', '986': 'ID',
    # Illinois (IL)
    '217': 'IL', '224': 'IL', '309': 'IL', '312': 'IL', '331': 'IL', '447': 'IL', 
    '464': 'IL', '618': 'IL', '630': 'IL', '708': 'IL', '730': 'IL', '773': 'IL', 
    '779': 'IL', '815': 'IL', '847': 'IL', '861': 'IL', '872': 'IL',
    # Indiana (IN)
    '219': 'IN', '260': 'IN', '317': 'IN', '463': 'IN', '574': 'IN', '765': 'IN', '812': 'IN', '930': 'IN',
    # Iowa (IA)
    '319': 'IA', '515': 'IA', '563': 'IA', '641': 'IA', '712': 'IA',
    # Kansas (KS)
    '316': 'KS', '620': 'KS', '785': 'KS', '913': 'KS',
    # Kentucky (KY)
    '270': 'KY', '364': 'KY', '502': 'KY', '606': 'KY', '859': 'KY',
    # Louisiana (LA)
    '225': 'LA', '318': 'LA', '337': 'LA', '504': 'LA', '985': 'LA',
    # Maine (ME)
    '207': 'ME',
    # Maryland (MD)
    '227': 'MD', '240': 'MD', '301': 'MD', '410': 'MD', '443': 'MD', '667': 'MD',
    # Massachusetts (MA)
    '339': 'MA', '351': 'MA', '413': 'MA', '508': 'MA', '617': 'MA', '774': 'MA', '781': 'MA', '857': 'MA', '978': 'MA',
    # Michigan (MI)
    '231': 'MI', '248': 'MI', '269': 'MI', '313': 'MI', '517': 'MI', '586': 'MI', 
    '616': 'MI', '679': 'MI', '734': 'MI', '810': 'MI', '906': 'MI', '947': 'MI', '989': 'MI',
    # Minnesota (MN)
    '218': 'MN', '320': 'MN', '507': 'MN', '612': 'MN', '651': 'MN', '763': 'MN', '952': 'MN',
    # Mississippi (MS)
    '228': 'MS', '601': 'MS', '662': 'MS', '769': 'MS',
    # Missouri (MO)
    '314': 'MO', '417': 'MO', '557': 'MO', '573': 'MO', '636': 'MO', '660': 'MO', '816': 'MO', '975': 'MO',
    # Montana (MT)
    '406': 'MT',
    # Nebraska (NE)
    '308': 'NE', '402': 'NE', '531': 'NE',
    # Nevada (NV)
    '702': 'NV', '725': 'NV', '775': 'NV',
    # New Hampshire (NH)
    '603': 'NH',
    # New Jersey (NJ)
    '201': 'NJ', '551': 'NJ', '609': 'NJ', '640': 'NJ', '732': 'NJ', '848': 'NJ', '856': 'NJ', '862': 'NJ', '908': 'NJ', '973': 'NJ',
    # New Mexico (NM)
    '505': 'NM', '575': 'NM',
    # New York (NY)
    '212': 'NY', '315': 'NY', '332': 'NY', '347': 'NY', '516': 'NY', '518': 'NY', 
    '585': 'NY', '607': 'NY', '631': 'NY', '646': 'NY', '680': 'NY', '716': 'NY', '718': 'NY', '838': 'NY', '845': 'NY', '914': 'NY', '917': 'NY', '929': 'NY', '934': 'NY',
    # North Carolina (NC)
    '252': 'NC', '336': 'NC', '704': 'NC', '743': 'NC', '828': 'NC', '910': 'NC', '919': 'NC', '980': 'NC', '984': 'NC',
    # North Dakota (ND)
    '701': 'ND',
    # Ohio (OH)
    '216': 'OH', '220': 'OH', '234': 'OH', '283': 'OH', '326': 'OH', '330': 'OH', 
    '380': 'OH', '419': 'OH', '440': 'OH', '513': 'OH', '567': 'OH', '614': 'OH', '740': 'OH', '937': 'OH',
    # Oklahoma (OK)
    '405': 'OK', '539': 'OK', '580': 'OK', '918': 'OK',
    # Oregon (OR)
    '458': 'OR', '503': 'OR', '541': 'OR', '971': 'OR',
    # Pennsylvania (PA)
    '215': 'PA', '223': 'PA', '267': 'PA', '272': 'PA', '412': 'PA', '445': 'PA', 
    '484': 'PA', '570': 'PA', '610': 'PA', '717': 'PA', '724': 'PA', '814': 'PA', '878': 'PA',
    # Rhode Island (RI)
    '401': 'RI',
    # South Carolina (SC)
    '803': 'SC', '839': 'SC', '843': 'SC', '854': 'SC', '864': 'SC',
    # South Dakota (SD)
    '605': 'SD',
    # Tennessee (TN)
    '423': 'TN', '615': 'TN', '629': 'TN', '731': 'TN', '865': 'TN', '901': 'TN', '931': 'TN',
    # Texas (TX)
    '210': 'TX', '214': 'TX', '254': 'TX', '281': 'TX', '325': 'TX', '346': 'TX', 
    '361': 'TX', '409': 'TX', '430': 'TX', '432': 'TX', '469': 'TX', '512': 'TX', 
    '682': 'TX', '713': 'TX', '726': 'TX', '737': 'TX', '806': 'TX', '817': 'TX', 
    '830': 'TX', '832': 'TX', '903': 'TX', '915': 'TX', '936': 'TX', '940': 'TX', '956': 'TX', '972': 'TX', '979': 'TX',
    # Utah (UT)
    '385': 'UT', '435': 'UT', '801': 'UT',
    # Vermont (VT)
    '802': 'VT',
    # Virginia (VA)
    '276': 'VA', '434': 'VA', '540': 'VA', '571': 'VA', '703': 'VA', '757': 'VA', '804': 'VA',
    # Washington (WA)
    '206': 'WA', '253': 'WA', '360': 'WA', '425': 'WA', '509': 'WA', '564': 'WA',
    # West Virginia (WV)
    '304': 'WV', '681': 'WV',
    # Wisconsin (WI)
    '262': 'WI', '274': 'WI', '414': 'WI', '534': 'WI', '608': 'WI', '715': 'WI', '920': 'WI',
    # Wyoming (WY)
    '307': 'WY',
    # Washington DC
    '202': 'DC',
    '514': 'Canada (QC)',
    '540': 'VA',  # Virginia (Số 1540... trong log của bạn)
    '762': 'GA',  # Georgia
    '668': 'International',
    '648': 'Unknown/Special',
    '120': 'Internal/Test'

}

# --- 3. HÀM HỖ TRỢ ---
def get_state(phone):
    if pd.isna(phone) or str(phone).strip() == "": 
        return "N/A (No Number)"
    
    # Chuyển về dạng chỉ có chữ số
    digits = re.sub(r'\D', '', str(phone))
    
    # Lấy Area Code (AC)
    ac = None
    if len(digits) == 10:
        ac = digits[:3]
    elif len(digits) == 11 and digits.startswith('1'):
        ac = digits[1:4]
    else:
        # Nếu định dạng lạ, thử dùng Regex tìm trong ngoặc đơn như cũ
        match = re.search(r'\((\d{3})\)', str(phone))
        if match: ac = match.group(1)

    if ac:
        if ac in ['800', '888', '877', '866', '855', '844', '833']: 
            return "Toll-Free"
        return AC_TO_STATE.get(ac, f"Khác ({ac})")
    
    return "N/A (Format Error)"

def to_seconds(s):
    if pd.isna(s) or str(s).lower() == 'in progress' or s == '-': return 0
    try:
        parts = str(s).strip().split(':')
        if len(parts) == 3: return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2: return int(parts[0]) * 60 + int(parts[1])
        return 0
    except: return 0

def classify_duration(sec):
    if 10 < sec <= 30: return "01. 10s - 30s"
    if 30 < sec <= 60: return "02. 30s - 1m"
    if 60 < sec <= 300: return "03. 1m - 5m"
    if 300 < sec <= 600: return "04. 5m - 10m"
    if 600 < sec <= 1800: return "05. 10m - 30m"
    if sec <= 1800 : return "06.Trên 30m"

def identify_agent(to_phone):
    to_phone = str(to_phone)
    for num, name in AGENT_MAP.items():
        if num in to_phone:
            return name
    return None

# --- 4. TẢI FILE ---
uploaded_file = st.file_uploader("📂 Tải file CSV Call Log", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, sep=',', on_bad_lines='skip', low_memory=False)
    except:
        df = pd.read_csv(uploaded_file, sep=';', on_bad_lines='skip', low_memory=False)
    
    df = df.drop_duplicates().copy()
    
    # Xử lý Extension
    if 'Extension' in df.columns:
        df[['Ext_Num', 'Staff_Name']] = df['Extension'].str.split(' - ', n=1, expand=True)
        df['Staff_Name'] = df['Staff_Name'].fillna('Unknown Staff')
    
    # Tạo các cột tính toán
    df['Sec'] = df['Duration'].apply(to_seconds)
    df['Duration_Group'] = df['Sec'].apply(classify_duration)
    df['Agent_Name'] = df['To'].apply(identify_agent)
    
    df_out = df[df['Direction'] == 'Outgoing'].copy()
    df_out['State'] = df_out['To'].apply(get_state)

    # --- 5. TỔNG QUAN METRICS ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📞 Tổng gọi đi", f"{len(df_out)}")
    m2.metric("✅ Khách nhấc máy", f"{(df_out['Sec'] > 0).sum()}")
    
    agent_calls = df_out[df_out['Agent_Name'].notna()].copy()
    m3.metric("🎧 Kết Nối Agent", f"{len(agent_calls)}")
    
    state_counts = df_out['State'].value_counts().reset_index()
    state_counts.columns = ['Bang', 'Count']
    m4.metric("🌎 Bang chủ lực", state_counts['Bang'].iloc[0] if not state_counts.empty else "N/A")

    st.divider()

    # --- 6. PHÂN TÍCH AGENT (MÀU ĐẬM NHẠT) ---
    st.subheader("👥 Thống kê Hiệu suất kết nối Agent ")

    if not agent_calls.empty:
        agent_stats = agent_calls.groupby(['Agent_Name', 'Duration_Group']).size().reset_index(name='Số lượng')
        
        custom_blues_ordered = {
            "01. 10s - 30s": "#deebf7",
            "02. 30s - 1m": "#9ecae1",
            "03. 1m - 5m": "#4292c6",
            "04. 5m - 10m": "#08519c",
            "05. 10m - 30m": "#08306b",
            "06.Trên 30m" : "#050E3C"
        }

        col_a1, col_a2 = st.columns([6, 4])
        with col_a1:
            fig_agent = px.bar(
                agent_stats, x='Agent_Name', y='Số lượng', color='Duration_Group', 
                title="Số lượng cuộc kết nối Agent ",
                text_auto=True, barmode='stack',
                category_orders={"Duration_Group": ["01. 10s - 30s", "02. 30s - 1m", "03. 1m - 5m", "04. 5m - 10m", "05. Trên 10m"]},
                color_discrete_map=custom_blues_ordered
            )
            st.plotly_chart(fig_agent, use_container_width=True)
        
        with col_a2:
            agent_total = agent_calls['Agent_Name'].value_counts().reset_index()
            agent_total.columns = ['Agent', 'Cuộc gọi']
            fig_pie_agent = px.pie(agent_total, values='Cuộc gọi', names='Agent', hole=0.4, 
                                   title="Tỷ lệ kết nối Agent",
                                   color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(fig_pie_agent, use_container_width=True)
    else:
        st.warning("Chưa có dữ liệu kết nối Agent.")

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
            st.success(f"Top {i}: **{r.Staff_Name}** ({r.C} cuộc phone)")

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
    st.info("👋 Chào Henry Team! Vui lòng tải file CSV Call Log để bắt đầu.")
