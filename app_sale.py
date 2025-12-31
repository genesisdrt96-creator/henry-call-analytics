import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Cấu hình trang web
st.set_page_config(page_title="Hệ thống Quản trị Henry Team", layout="wide")

st.title("🚀 Hệ thống Quản trị Sale & Chất lượng Data")
st.markdown("---")

# --- 1. DỮ LIỆU TỔNG LỰC: MÃ VÙNG 50 TIỂU BANG HOA KỲ ---
# Danh sách này đã bao gồm đầy đủ các mã vùng chính thức của US
AC_TO_STATE = {
    '205': 'AL', '251': 'AL', '256': 'AL', '334': 'AL', '938': 'AL', '907': 'AK', '480': 'AZ', '520': 'AZ', '602': 'AZ', '623': 'AZ', '928': 'AZ', '479': 'AR', '501': 'AR', '870': 'AR', '209': 'CA', '213': 'CA', '310': 'CA', '323': 'CA', '408': 'CA', '415': 'CA', '424': 'CA', '442': 'CA', '510': 'CA', '530': 'CA', '559': 'CA', '562': 'CA', '619': 'CA', '626': 'CA', '628': 'CA', '650': 'CA', '657': 'CA', '661': 'CA', '669': 'CA', '707': 'CA', '714': 'CA', '747': 'CA', '760': 'CA', '805': 'CA', '818': 'CA', '820': 'CA', '831': 'CA', '840': 'CA', '858': 'CA', '909': 'CA', '916': 'CA', '925': 'CA', '949': 'CA', '951': 'CA', '303': 'CO', '719': 'CO', '720': 'CO', '970': 'CO', '203': 'CT', '475': 'CT', '860': 'CT', '959': 'CT', '302': 'DE', '202': 'DC', '239': 'FL', '305': 'FL', '321': 'FL', '352': 'FL', '386': 'FL', '407': 'FL', '561': 'FL', '689': 'FL', '727': 'FL', '754': 'FL', '772': 'FL', '786': 'FL', '813': 'FL', '850': 'FL', '863': 'FL', '904': 'FL', '941': 'FL', '954': 'FL', '229': 'GA', '404': 'GA', '470': 'GA', '478': 'GA', '678': 'GA', '706': 'GA', '762': 'GA', '770': 'GA', '912': 'GA', '808': 'HI', '208': 'ID', '986': 'ID', '217': 'IL', '224': 'IL', '309': 'IL', '312': 'IL', '331': 'IL', '618': 'IL', '630': 'IL', '708': 'IL', '773': 'IL', '779': 'IL', '815': 'IL', '847': 'IL', '872': 'IL', '219': 'IN', '260': 'IN', '317': 'IN', '463': 'IN', '574': 'IN', '765': 'IN', '812': 'IN', '930': 'IN', '319': 'IA', '515': 'IA', '563': 'IA', '641': 'IA', '712': 'IA', '316': 'KS', '620': 'KS', '785': 'KS', '913': 'KS', '270': 'KY', '364': 'KY', '502': 'KY', '606': 'KY', '859': 'KY', '225': 'LA', '318': 'LA', '337': 'LA', '504': 'LA', '985': 'LA', '207': 'ME', '240': 'MD', '301': 'MD', '410': 'MD', '443': 'MD', '667': 'MD', '339': 'MA', '351': 'MA', '413': 'MA', '508': 'MA', '617': 'MA', '774': 'MA', '781': 'MA', '857': 'MA', '978': 'MA', '231': 'MI', '248': 'MI', '269': 'MI', '313': 'MI', '517': 'MI', '586': 'MI', '616': 'MI', '734': 'MI', '810': 'MI', '906': 'MI', '947': 'MI', '989': 'MI', '218': 'MN', '320': 'MN', '507': 'MN', '612': 'MN', '651': 'MN', '763': 'MN', '952': 'MN', '228': 'MS', '601': 'MS', '662': 'MS', '769': 'MS', '314': 'MO', '417': 'MO', '573': 'MO', '636': 'MO', '660': 'MO', '816': 'MO', '406': 'MT', '308': 'NE', '402': 'NE', '531': 'NE', '702': 'NV', '725': 'NV', '775': 'NV', '603': 'NH', '201': 'NJ', '551': 'NJ', '609': 'NJ', '640': 'NJ', '732': 'NJ', '848': 'NJ', '856': 'NJ', '862': 'NJ', '908': 'NJ', '973': 'NJ', '505': 'NM', '575': 'NM', '212': 'NY', '315': 'NY', '332': 'NY', '347': 'NY', '516': 'NY', '518': 'NY', '585': 'NY', '607': 'NY', '631': 'NY', '646': 'NY', '680': 'NY', '716': 'NY', '718': 'NY', '838': 'NY', '845': 'NY', '914': 'NY', '917': 'NY', '929': 'NY', '934': 'NY', '252': 'NC', '336': 'NC', '704': 'NC', '743': 'NC', '828': 'NC', '910': 'NC', '919': 'NC', '980': 'NC', '984': 'NC', '701': 'ND', '216': 'OH', '234': 'OH', '326': 'OH', '330': 'OH', '380': 'OH', '419': 'OH', '440': 'OH', '513': 'OH', '567': 'OH', '614': 'OH', '740': 'OH', '937': 'OH', '405': 'OK', '539': 'OK', '580': 'OK', '918': 'OK', '458': 'OR', '503': 'OR', '541': 'OR', '971': 'OR', '215': 'PA', '223': 'PA', '267': 'PA', '272': 'PA', '412': 'PA', '484': 'PA', '570': 'PA', '610': 'PA', '717': 'PA', '724': 'PA', '814': 'PA', '878': 'PA', '401': 'RI', '803': 'SC', '843': 'SC', '854': 'SC', '864': 'SC', '605': 'SD', '423': 'TN', '615': 'TN', '629': 'TN', '731': 'TN', '865': 'TN', '901': 'TN', '931': 'TN', '210': 'TX', '214': 'TX', '254': 'TX', '281': 'TX', '325': 'TX', '346': 'TX', '361': 'TX', '409': 'TX', '430': 'TX', '432': 'TX', '469': 'TX', '512': 'TX', '682': 'TX', '713': 'TX', '726': 'TX', '737': 'TX', '806': 'TX', '817': 'TX', '830': 'TX', '832': 'TX', '903': 'TX', '915': 'TX', '936': 'TX', '940': 'TX', '945': 'TX', '956': 'TX', '972': 'TX', '979': 'TX', '385': 'UT', '435': 'UT', '801': 'UT', '802': 'VT', '276': 'VA', '434': 'VA', '540': 'VA', '571': 'VA', '703': 'VA', '757': 'VA', '804': 'VA', '948': 'VA', '206': 'WA', '253': 'WA', '360': 'WA', '425': 'WA', '509': 'WA', '564': 'WA', '304': 'WV', '681': 'WV', '262': 'WI', '414': 'WI', '534': 'WI', '608': 'WI', '715': 'WI', '920': 'WI', '307': 'WY'
}

def get_state(phone):
    if pd.isna(phone): return "Không xác định"
    match = re.search(r'\((\d{3})\)', str(phone))
    if match:
        ac = match.group(1)
        # Nếu không tìm thấy trong danh sách 50 bang, trả về Toll-free hoặc Other
        if ac in ['800', '888', '877', '866', '855', '844', '833']: return "Toll-Free"
        return AC_TO_STATE.get(ac, f"Khác ({ac})")
    return "Không xác định"

# (Phần hàm to_seconds và translate_desc giữ nguyên như cũ...)
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
    df['Hour'] = pd.to_datetime(df['Time'], errors='coerce').dt.hour
    
    df_out = df[df['Direction'] == 'Outgoing'].copy()
    df_out['State'] = df_out['To'].apply(get_state)

    # --- 3. METRICS TỔNG QUAN ---
    state_counts = df_out['State'].value_counts().reset_index()
    state_counts.columns = ['Tiểu bang', 'Số cuộc gọi']
    
    m1, m2, m3 = st.columns(3)
    m1.metric("📞 Tổng cuộc gọi đi", f"{len(df_out)}")
    m2.metric("✅ Kết nối thành công", f"{(df_out['Sec'] > 0).sum()}")
    m3.metric("🇺🇸 Bang gọi nhiều nhất", state_counts['Tiểu bang'].iloc[0] if not state_counts.empty else "N/A")

    st.divider()

    # --- 4. BIỂU ĐỒ TIỂU BANG (HIỂN THỊ ĐỦ 50 BANG NẾU CÓ DỮ LIỆU) ---
    st.subheader("📍 Thống kê chi tiết theo Tiểu bang (USA)")
    # Chỉ lấy top các bang có cuộc gọi để biểu đồ không bị quá dày
    fig_state = px.bar(state_counts.head(50), x='Tiểu bang', y='Số cuộc gọi', 
                       color='Số cuộc gọi', text_auto=True,
                       title="Xếp hạng lưu lượng cuộc gọi theo địa phương",
                       color_continuous_scale='Portland')
    st.plotly_chart(fig_state, use_container_width=True)

    st.divider()

    # --- 5. PHÂN TÍCH GIỜ VÀNG & TỶ LỆ CHỐT (>15 PHÚT) ---
    st.subheader("⏰ Phân tích Khung Giờ Chất Lượng (>15 Phút)")
    
    hourly_all = df_out.groupby('Hour').size()
    hourly_long = df_out[df_out['Sec'] >= 900].groupby('Hour').size()
    
    hourly_stats = pd.DataFrame({'Tổng': hourly_all, 'Trên 15p': hourly_long}).fillna(0)
    hourly_stats['Tỷ lệ %'] = round((hourly_stats['Trên 15p'] / hourly_stats['Tổng']) * 100, 1)
    hourly_stats = hourly_stats.reset_index()

    if not hourly_stats.empty:
        best_hour = hourly_stats.loc[hourly_stats['Tỷ lệ %'].idxmax()]
        st.info(f"💡 **Phát hiện:** Khung giờ **{int(best_hour['Hour'])}h** đạt tỷ lệ cuộc gọi dài cao nhất (**{best_hour['Tỷ lệ %']}%**).")

    fig_time = px.line(hourly_stats, x='Hour', y='Tỷ lệ %', markers=True, 
                       title="Biểu đồ tỷ lệ cuộc gọi chất lượng theo giờ")
    st.plotly_chart(fig_time, use_container_width=True)

    st.divider()

    # --- 6. TOP CHAMPIONS ---
    st.subheader("🏆 Vinh danh Top 3 Nhân viên xuất sắc")
    report_staff = df_out.groupby('Staff_Name').agg(
        Tổng_gọi=('Direction', 'count'),
        Trên_15p=('Sec', lambda x: (x >= 900).sum())
    ).reset_index()
    
    c1, c2, c3 = st.columns(3)
    top3 = report_staff.nlargest(3, 'Tổng_gọi')
    # Hiển thị vinh danh
    for i, (col, row) in enumerate(zip([c1, c2, c3], top3.itertuples()), 1):
        col.metric(f"Top {i} Champion", row.Staff_Name, f"{row.Tổng_gọi} cuộc")

    st.divider()
    st.subheader("📊 Bảng dữ liệu chi tiết")
    st.dataframe(report_staff.sort_values('Trên_15p', ascending=False), use_container_width=True)
