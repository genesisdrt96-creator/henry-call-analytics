import pandas as pd
import glob
import os
import warnings

warnings.filterwarnings('ignore')

# --- 1. CẤU HÌNH ---
FOLDER_PATH = r'E:\Python\Data_ring_csv\12302025'
OUTPUT_REPORT = r'E:\Python\Data_ring_csv\12302025\Bao_Cao_Dung_Thuc_Te.xlsx'

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
    except:
        return 0

def translate_desc(desc):
    desc = str(desc).lower()
    if "not a valid number" in desc or "disconnected" in desc: return "Data Sai/Số Ảo"
    if "not answered" in desc: return "Khách Không Nghe Máy"
    if "busy" in desc: return "Máy Bận"
    if "internet connection" in desc or "offline" in desc: return "Lỗi Mạng/Thiết Bị (Sale)"
    if "accepted" in desc or "connected" in desc: return "Kết Nối Thành Công"
    if "hung up" in desc: return "Khách Dập Máy Sớm"
    return "Khác/Chưa xác định"

# --- 2. XỬ LÝ DỮ LIỆU ---
all_files = glob.glob(os.path.join(FOLDER_PATH, "*.csv"))

if not all_files:
    print("Không tìm thấy file!")
else:
    # Đọc file và xử lý bỏ dòng trống
    df = pd.concat([pd.read_csv(f, skip_blank_lines=True, low_memory=False) for f in all_files])
    
    # Bỏ trùng lặp
    df = df.drop_duplicates().copy()
    
    # Xử lý cột Extension: Tách lấy số nội bộ (ví dụ '340 - Holden Bui' -> '340')
    df['Ext_Clean'] = df['Extension'].str.extract(r'(\d+)').fillna('Unknown')
    
    # Chuyển đổi thời gian
    df['Sec'] = df['Duration'].apply(to_seconds)
    df['Status_VN'] = df['Result Description'].apply(translate_desc)
    
    # Lọc cuộc gọi đi
    df_out = df[df['Direction'] == 'Outgoing'].copy()

    # --- 3. PHÂN TÍCH ---
    def get_stats(group):
        total = len(group)
        # Bắt máy dựa trên Action Result hoặc Duration > 0
        conn = ((group['Action Result'] == 'Call connected') | (group['Sec'] > 0)).sum()
        
        return pd.Series({
            'Tổng gọi đi': total,
            'Bắt máy thực tế': conn,
            'Tỷ lệ %': round(conn/total*100, 2) if total > 0 else 0,
            'Trên 1p': (group['Sec'] >= 60).sum(),
            'Trên 5p': (group['Sec'] >= 300).sum(),
            'Trên 10p': (group['Sec'] >= 600).sum(),
            'Trên 30p': (group['Sec'] >= 1800).sum(),
            'Lỗi hay gặp': group['Status_VN'].value_counts().idxmax()
        })

    report = df_out.groupby('Ext_Clean').apply(get_stats, include_groups=False).reset_index()
    report = report.sort_values('Trên 5p', ascending=False)

    # --- 4. XUẤT FILE ---
    with pd.ExcelWriter(OUTPUT_REPORT) as writer:
        report.to_excel(writer, sheet_name='Hieu_Suat_Nhan_Vien', index=False)
        # Thêm sheet chi tiết lỗi của toàn hệ thống
        df_out['Status_VN'].value_counts().to_excel(writer, sheet_name='Tong_Hop_Loi_He_Thong')

    print("\n" + "="*80)
    print(f"ĐÃ PHÂN TÍCH XONG DỮ LIỆU THỰC TẾ!")
    print(f"File lưu tại: {OUTPUT_REPORT}")
    print("="*80)
    print(report.head(5).to_string(index=False))