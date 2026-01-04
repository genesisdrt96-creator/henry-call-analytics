import streamlit as st
import pandas as pd
import plotly.express as px
import re
import numpy as np

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Dream Talent - Master Analytics", layout="wide")

st.title("📊 Thống kê Data Ringcentral - Dream Talent")
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
    '714': 'CA', '406': 'MT', '843': 'SC', '757': 'VA', '508': 'MA', '281': 'TX', 
    '330':'OH','513':'OH','973':'NJ','706':'GA','703':'VA','469':'TX','540':'VA',
    '205': 'AL', '251': 'AL', '256': 'AL', '334': 'AL', '659': 'AL', '938': 'AL',
    '907': 'AK', '480': 'AZ', '520': 'AZ', '602': 'AZ', '623': 'AZ', '928': 'AZ',
    '327': 'AR', '479': 'AR', '501': 'AR', '870': 'AR', '209': 'CA', '213': 'CA', 
    '310': 'CA', '323': 'CA', '341': 'CA', '408': 'CA', '415': 'CA', '949': 'CA',
    '303': 'CO', '719': 'CO', '720': 'CO', '970': 'CO', '203': 'CT', '860': 'CT',
    '302': 'DE', '305': 'FL', '321': 'FL', '352': 'FL', '386': 'FL', '407': 'FL', 
    '448': 'FL', '561': 'FL', '645': 'FL', '689': 'FL', '727': 'FL', '754': 'FL', 
    '772': 'FL', '786': 'FL', '813': 'FL', '850': 'FL', '863': 'FL', '904': 'FL', 
    '941': 'FL', '954': 'FL', '229': 'GA', '404': 'GA', '470': 'GA', '478': 'GA', 
    '678': 'GA', '706': 'GA', '762': 'GA', '770': 'GA', '912': 'GA', '808': 'HI',
    '208': 'ID', '986': 'ID', '217': 'IL', '224': 'IL', '309': 'IL', '312': 'IL', 
    '331': 'IL', '447': 'IL', '464': 'IL', '618': 'IL', '630': 'IL', '708': 'IL', 
    '730': 'IL', '773': 'IL', '779': 'IL', '815': 'IL', '847': 'IL', '861': 'IL', '872': 'IL',
    '219': 'IN', '260': 'IN', '317': 'IN', '463': 'IN', '574': 'IN', '765': 'IN', '812': 'IN', '930': 'IN',
    '319': 'IA', '515': 'IA', '563': 'IA', '641': 'IA', '712': 'IA',
    '316': 'KS', '620': 'KS', '785': 'KS', '913': 'KS',
    '270': 'KY', '364': 'KY', '502': 'KY', '606': 'KY', '859': 'KY',
    '225': 'LA', '318': 'LA', '337': 'LA', '504': 'LA', '985': 'LA',
    '207': 'ME', '227': 'MD', '240': 'MD', '301': 'MD', '410': 'MD', '443': 'MD', '667': 'MD',
    '339': 'MA', '351': 'MA', '413': 'MA', '508': 'MA', '617': 'MA', '774': 'MA', '781': 'MA', '857': 'MA', '978': 'MA',
    '231': 'MI', '248': 'MI', '269': 'MI', '313': 'MI', '517': 'MI', '586': 'MI', 
    '616': 'MI', '679': 'MI', '734': 'MI', '810': 'MI', '906': 'MI', '947': 'MI', '989': 'MI',
    '218': 'MN', '320': 'MN', '507': 'MN', '612': 'MN', '651': 'MN', '763': 'MN', '952': 'MN',
    '228': 'MS', '601': 'MS', '662': 'MS', '769': 'MS',
    '314': 'MO', '417': 'MO', '557': 'MO', '573': 'MO', '636': 'MO', '660': 'MO', '816': 'MO', '975': 'MO',
    '406': 'MT', '308': 'NE', '402': 'NE', '531': 'NE',
    '702': 'NV', '725': 'NV', '775': 'NV', '603': 'NH',
    '201': 'NJ', '551': 'NJ', '609': 'NJ', '640': 'NJ', '732': 'NJ', '848': 'NJ', '856': 'NJ', '862': 'NJ', '908': 'NJ', '973': 'NJ',
    '505': 'NM', '575': 'NM', '212': 'NY', '315': 'NY', '332': 'NY', '347': 'NY', '516': 'NY', '518': 'NY', 
    '585': 'NY', '607': 'NY', '631': 'NY', '646': 'NY', '680': 'NY', '716': 'NY', '718': 'NY', '838': 'NY', '845': 'NY', '914': 'NY', '917': 'NY', '929': 'NY', '934': 'NY',
    '252': 'NC', '336': 'NC', '704': 'NC', '743': 'NC', '828': 'NC', '910': 'NC', '919': 'NC', '980': 'NC', '984': 'NC',
    '701': 'ND', '216': 'OH', '220': 'OH', '234': 'OH', '283': 'OH', '326': 'OH', '330': 'OH', 
    '380': 'OH', '419': 'OH', '440': 'OH', '513': 'OH', '567': 'OH', '614': 'OH', '740': 'OH', '937': 'OH',
    '405': 'OK', '539': 'OK', '580': 'OK', '918': 'OK', '458': 'OR', '503': 'OR', '541': 'OR', '971': 'OR',
    '215': 'PA', '223': 'PA', '267': 'PA', '272': 'PA', '412': 'PA', '445': 'PA', 
    '484': 'PA', '570': 'PA', '610': 'PA', '717': 'PA', '724': 'PA', '814': 'PA', '878': 'PA',
    '401': 'RI', '803': 'SC', '839': 'SC', '843': 'SC', '854': 'SC', '864': 'SC', '605': 'SD',
    '423': 'TN', '615': 'TN', '629': 'TN', '731': 'TN', '865': 'TN', '901': 'TN', '931': 'TN',
    '210': 'TX', '214': 'TX', '254': 'TX', '281': 'TX', '325': 'TX', '346': 'TX', 
    '361': 'TX', '409': 'TX', '430': 'TX', '432': 'TX', '469': 'TX', '512': 'TX', 
    '682': 'TX', '713': 'TX', '726': 'TX', '737': 'TX', '806': 'TX', '817': 'TX', 
    '830': 'TX', '832': 'TX', '903': 'TX', '915': 'TX', '936': 'TX', '940': 'TX', '956': 'TX', '972': 'TX', '979': 'TX',
    '385': 'UT', '435': 'UT', '801': 'UT', '802': 'VT',
    '276': 'VA', '434': 'VA', '540': 'VA', '571': 'VA', '703': 'VA', '757': 'VA', '804': 'VA',
    '206': 'WA', '253': 'WA', '360': 'WA', '425': 'WA', '509': 'WA', '564': 'WA',
    '304': 'WV', '681': 'WV', '262': 'WI', '274': 'WI', '414': 'WI', '534': 'WI', '608': 'WI', '715': 'WI', '920': 'WI',
    '307': 'WY', '202': 'DC'
}

# --- 3. HÀM HỖ TRỢ ---
def get_state(phone):
    if pd.isna(phone): return "N/A"
    digits = re.sub(r'\D', '', str(phone))
    ac = None
    if len(digits) == 10: ac = digits[:3]
    elif len(digits) == 11 and digits.startswith('1'): ac = digits[1:4]
    if ac:
        state = AC_TO_STATE.get(ac)
        return state if state else None
    return None

def to_seconds(s):
    if pd.isna(s) or str(s).lower() == 'in progress' or s == '-': return 0
    try:
        parts = str(s).strip().split(':')
        if len(parts) == 3: return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2: return int(parts[0]) * 60 + int(parts[1])
        return 0
    except: return 0

def classify_duration(sec):
    if sec == 0: return "00. Không nhấc máy"
    if 0 < sec <= 10: return "01. 0s - 10s"
    if 10 < sec <= 30: return "02. 10s - 30s"
    if 30 < sec <= 60: return "03. 30s - 1m"
    if 60 < sec <= 300: return "04. 1m - 5m"
    if 300 < sec <= 600: return "05. 5m - 10m"
    if 600 < sec <= 1800: return "06. 10m - 30m"
    return "07. Trên 30m"

def categorize_health(res):
    res = str(res).lower()
    if "connected" in res or "accepted" in res: return "✅ Kết nối thành công"
    if "wrong number" in res: return "❌ Data sai (Wrong Num)"
    if "offline" in res: return "⚠️ Lỗi Kỹ thuật (Offline)"
    if "busy" in res or "no answer" in res: return "⏳ Khách bận/Ko nghe"
    return "📉 Khác"

def identify_agent(to_phone):
    to_phone = str(to_phone)
    for num, name in AGENT_MAP.items():
        if num in to_phone: return name
    return None

# Bảng màu chung
CUSTOM_BLUES = {
    "00. Không nhấc máy": "#f7fbff", "01. 0s - 10s": "#deebf7", "02. 10s - 30s": "#c6dbef",
    "03. 30s - 1m": "#9ecae1", "04. 1m - 5m": "#6baed6", "05. 5m - 10m": "#4292c6",
    "06. 10m - 30m": "#2171b5", "07. Trên 30m": "#08306b"
}

# --- 4. TẢI FILE ---
uploaded_file = st.file_uploader("📂 Tải file CSV Call Log", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, low_memory=False)
    
    if 'Extension' in df.columns:
        df[['Ext_Num', 'Staff_Name']] = df['Extension'].str.split(' - ', n=1, expand=True)
        df['Staff_Name'] = df['Staff_Name'].fillna('Unknown Staff')
    
    df['Sec'] = df['Duration'].apply(to_seconds)
    df['Duration_Group'] = df['Sec'].apply(classify_duration)
    df['Agent_Name'] = df['To'].apply(identify_agent)
    df['Data_Health'] = df['Action Result'].apply(categorize_health)
    
    df_out = df[df['Direction'] == 'Outgoing'].copy()
    df_out['State'] = df_out['To'].apply(get_state)
    
    # --- 5. TỔNG QUAN ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📞 Tổng gọi đi", f"{len(df_out)}")
    m2.metric("✅ Khách nhấc máy", f"{(df_out['Sec'] > 0).sum()}")
    agent_calls = df_out[df_out['Agent_Name'].notna()].copy()
    m3.metric("🎧 Kết Nối Agent", f"{len(agent_calls)}")
    m4.metric("🛡️ Độ sạch Data", f"{(len(df_out[df_out['Data_Health'] != '❌ Data sai (Wrong Num)']) / len(df_out) * 100):.1f}%")

    st.divider()

    # --- 6. SỨC KHỎE DATA ---
    st.subheader("🔍 Phân tích Sức khỏe Data & Kết nối")
    health_stats = df_out['Data_Health'].value_counts().reset_index()
    health_stats.columns = ['Trạng thái', 'Số lượng']
    fig_h = px.bar(
        health_stats, x='Trạng thái', y='Số lượng', color='Trạng thái', text_auto=True,
        color_discrete_sequence=px.colors.sequential.Blues_r, title="Chi tiết tình trạng kết nối hệ thống"
    )
    fig_h.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', xaxis_title="", yaxis_title="Số lượng cuộc gọi")
    st.plotly_chart(fig_h, use_container_width=True)

    st.divider()

    # --- 7. HIỆU SUẤT AGENT ---
    st.subheader("👥 Thống kê Hiệu suất & Độ sâu kết nối Agent")
    if not agent_calls.empty:
        agent_depth = agent_calls.groupby(['Agent_Name', 'Duration_Group']).size().reset_index(name='Số lượng')
        col_a1, col_a2 = st.columns([6, 4])
        with col_a1:
            fig_a = px.bar(
                agent_depth, x='Agent_Name', y='Số lượng', color='Duration_Group', 
                text_auto=True, barmode='stack', color_discrete_map=CUSTOM_BLUES,
                category_orders={"Duration_Group": sorted(list(CUSTOM_BLUES.keys()))}
            )
            st.plotly_chart(fig_a, use_container_width=True)
        with col_a2:
            fig_pie = px.pie(agent_calls['Agent_Name'].value_counts().reset_index(), values='count', names='Agent_Name', hole=0.4, color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

   # --- 8. ĐỊA LÝ & CHAMPIONS (Hiển thị Toàn bộ 50 Tiểu Bang) ---
    c_geo, c_champ = st.columns([7, 3])
    
    def format_k(n):
        if n >= 1000:
            return f"{n/1000:.1f}k" if n % 1000 != 0 else f"{int(n/1000)}k"
        return str(n)

    with c_geo:
        st.markdown("### 🗺️ Bản đồ Mật độ Cuộc gọi trên Toàn bộ 50 Bang")
        
        # Lấy dữ liệu toàn bộ các bang có trong file
        state_data_all = df_out['State'].dropna().value_counts().reset_index()
        state_data_all.columns = ['State_Code', 'Count']
        
        # Danh sách các bang rất nhỏ (Không hiện chữ để tránh chồng chéo)
        SMALL_STATES = ['RI', 'DE', 'CT', 'NJ', 'MD', 'MA', 'NH', 'VT', 'HI', 'DC', 'ME', 'WV']

        # Logic tạo nhãn: Chỉ hiện chữ cho các bang lớn
        state_data_all['Label'] = state_data_all.apply(
            lambda r: f"{r['State_Code']}<br>{format_k(r['Count'])}" if r['State_Code'] not in SMALL_STATES else "", 
            axis=1
        )

        # Dải màu Gradient Xanh từ Trắng -> Đậm
        blue_gradient = [
            [0.0, "#ffffff"], # Không có call
            [0.1, "#f7fbff"], # Rất ít
            [0.4, "#9ecae1"], # Trung bình
            [0.7, "#2171b5"], # Cao
            [1.0, "#08306b"]  # Cao nhất (Champion State)
        ]

        fig_map = px.choropleth(
            state_data_all,
            locations='State_Code',
            locationmode="USA-states",
            color='Count',
            scope="usa",
            color_continuous_scale=blue_gradient,
            labels={'Count': 'Số lượng'}
        )

        # Hiển thị chữ lên các bang lớn
        fig_map.add_scattergeo(
            locations=state_data_all['State_Code'],
            locationmode="USA-states",
            text=state_data_all['Label'],
            mode='text',
            textfont=dict(
                size=10, 
                color="#1a1a1a", 
                family="Verdana"
            ),
        )

        fig_map.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            geo=dict(
                bgcolor='rgba(0,0,0,0)',
                projection_type='albers usa',
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'
            ),
            dragmode=False # Khóa kéo bản đồ
        )
        
        fig_map.update_coloraxes(showscale=True) 
        
        # Hiển thị bản đồ và khóa Zoom
        st.plotly_chart(
            fig_map, 
            use_container_width=True, 
            config={'scrollZoom': False, 'displayModeBar': False}
        )

    with c_champ:
        st.markdown("### 🏆 TOP 3 CHAMPION")
        top_s = df_out.groupby('Staff_Name').size().nlargest(3).reset_index(name='C')
        
        for i, r in enumerate(top_s.itertuples(), 1):
            val = format_k(r.C)
            bg_color = "linear-gradient(90deg, #08306b, #2171b5)" if i==1 else ("linear-gradient(90deg, #4292c6, #9ecae1)" if i==2 else "linear-gradient(90deg, #c6dbef, #deebf7)")
            text_color = "white" if i==1 else "#08306b"
            st.markdown(f"""
            <div style='background: {bg_color}; padding: 15px; border-radius: 10px; margin-bottom: 12px; color: {text_color}; border-left: 8px solid rgba(0,0,0,0.2);'>
                <span style='font-family: Verdana; font-size: 18px;'><b>TOP {i}: {r.Staff_Name}</b></span><br>
                <span style='font-family: Arial; font-size: 15px;'>Số lượng: {val}</span>
            </div>
            """, unsafe_allow_html=True)

        # --- 9. BẢNG HIỆU SUẤT CHI TIẾT ---
    st.subheader("📋 Bảng hiệu suất cuộc phone chi tiết từng nhân viên")
    
    # Tính toán báo cáo
    # Cột 1: Kết nối Agent (Độc lập)
    # Các cột tiếp theo: Thời lượng cuộc gọi chung (Độc lập)
    report_raw = df_out.groupby('Staff_Name').agg(
        Tong_goi=('Direction', 'count'),
        Agent_Conn=('Agent_Name', lambda x: x.notna().sum()), # Cột 1: Có bao nhiêu cuộc nối Agent
        # Nhóm các cột thời lượng cho TOÀN BỘ cuộc gọi (không liên quan đến Agent)
        Time_1_30s=('Sec', lambda x: ((x >= 1) & (x <= 30)).sum()),
        Time_30s_1p=('Sec', lambda x: ((x > 30) & (x <= 60)).sum()),
        Time_1_5p=('Sec', lambda x: ((x > 60) & (x <= 300)).sum()),
        Time_5_10p=('Sec', lambda x: ((x > 300) & (x <= 600)).sum()),
        Time_10_30p=('Sec', lambda x: ((x > 600) & (x <= 1800)).sum()),
        Time_Over30p=('Sec', lambda x: (x > 1800).sum())
    ).reset_index()

    # 9b. BIỂU ĐỒ TỔNG GỌI (Giữ nguyên giao diện xanh chuyên nghiệp)
    fig_total_calls = px.bar(
        report_raw.sort_values('Tong_goi', ascending=False), 
        x='Staff_Name', y='Tong_goi',
        title="Biểu đồ Tổng cuộc gọi theo nhân viên",
        text_auto=True,
        color='Tong_goi',
        color_continuous_scale='Blues'
    )
    fig_total_calls.update_layout(showlegend=False, xaxis_title="Nhân viên", yaxis_title="Tổng cuộc gọi")
    st.plotly_chart(fig_total_calls, use_container_width=True)

    # 9c. BẢNG SỐ LIỆU HIỂN THỊ (Thiết kế lại theo đúng yêu cầu)
    report_final = pd.DataFrame()
    report_final['Nhân Viên'] = report_raw['Staff_Name']
    report_final['Tổng call'] = report_raw['Tong_goi']
    report_final['Kết nối Agent'] = report_raw['Agent_Conn'] # Cột 1 theo ý bạn
    
    # Các cột thời lượng riêng biệt
    report_final['1 - 30s'] = report_raw['Time_1_30s']
    report_final['30s - 1p'] = report_raw['Time_30s_1p']
    report_final['1p - 5p'] = report_raw['Time_1_5p']
    report_final['5p - 10p'] = report_raw['Time_5_10p']
    report_final['10p - 30p'] = report_raw['Time_10_30p']
    report_final['Trên 30p'] = report_raw['Time_Over30p']
    
    # Sắp xếp theo tổng gọi để dễ theo dõi
    report_final = report_final.sort_values('Tổng call', ascending=False)
    
    # Hiển thị bảng dữ liệu
    st.dataframe(report_final, use_container_width=True)
    
    # Nút tải báo cáo
    csv = report_final.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Tải Báo Cáo Tổng Hợp", data=csv, file_name='Bao_cao_Hieu_Suat_DreamTalent.csv')

    # --- 10. PHÂN TÍCH GIỜ VÀNG ---
    st.subheader("⏳ Phân tích Giờ Vàng (Cuộc gọi trên 30 phút)")
    try:
        df_out['Hour'] = pd.to_datetime(df_out['Time']).dt.hour
        df_long_calls = df_out[df_out['Sec'] > 1800].copy()
        if not df_long_calls.empty:
            golden_hours = df_long_calls.groupby('Hour').size().reset_index(name='Số lượng')
            golden_hours['Khung Giờ'] = golden_hours['Hour'].apply(lambda x: f"{x}:00")
            col_g1, col_g2 = st.columns([7, 3])
            with col_g1:
                fig_golden = px.area(golden_hours, x='Khung Giờ', y='Số lượng', markers=True, color_discrete_sequence=['#08306b'])
                fig_golden.update_traces(fillcolor='rgba(8, 48, 107, 0.2)')
                st.plotly_chart(fig_golden, use_container_width=True)
            with col_g2:
                best_hour = golden_hours.loc[golden_hours['Số lượng'].idxmax()]
                st.metric("⏰ Giờ Cao Điểm", f"{best_hour['Khung Giờ']}")
    except:
        st.error("Lỗi phân tích giờ.")
        
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #EEEEEE;'>✨ THANK YOU! ✨</h2>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; font-style: italic; font-size: 20px;'>“Thành công không phải là cuối cùng, thất bại không phải là dấu chấm hết: lòng can đảm để tiếp tục mới là điều quan trọng nhất.”</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-weight: bold;'>— Winston Churchill</p>", unsafe_allow_html=True)
    
    st.balloons() 

else:
    st.info("👋 Chào các Dreamer! Vui lòng tải file CSV.")
