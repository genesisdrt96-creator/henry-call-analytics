import pandas as pd
import glob
import os
import warnings

# Tắt cảnh báo định dạng ngày tháng
warnings.filterwarnings('ignore')

# --- 1. CẤU HÌNH ĐƯỜNG DẪN ---
FOLDER_PATH = r'E:\Python\Data_ring_csv\12302025'
OUTPUT_FILE = r'E:\Python\Data_ring_csv\12302025\Bao_Cao_Nhan_Vien_Deep_Clean.xlsx'

# --- 2. HÀM CHUYỂN ĐỔI THỜI GIAN ---
def to_seconds(s):
    try:
        if pd.isna(s) or s == '-' or str(s).strip() == "": return 0
        parts = str(s).replace('"', '').strip().split(':')
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        return 0
    except:
        return 0

# --- 3. ĐỌC VÀ LÀM SẠCH DỮ LIỆU ---
all_files = glob.glob(os.path.join(FOLDER_PATH, "*.csv"))

if not all_files:
    print(f"LỖI: Không tìm thấy file CSV nào tại {FOLDER_PATH}")
else:
    print(f"Đang xử lý dữ liệu từ {len(all_files)} file CSV...")
    
    # Gộp dữ liệu từ tất cả các file
    df = pd.concat([pd.read_csv(f, low_memory=False) for f in all_files], ignore_index=True)

    # --- DÒNG CODE BỎ SỰ TRÙNG LẶP ---
    # Lọc bỏ các dòng giống hệt nhau (Duplicate rows)
    before_clean = len(df)
    df = df.drop_duplicates().copy()
    after_clean = len(df)
    print(f"-> Đã loại bỏ {before_clean - after_clean} dòng trùng lặp.")
    # ---------------------------------
    
    # Tiền xử lý
    df['Duration_Sec'] = df['Duration'].apply(to_seconds)
    
    # Lọc cuộc gọi đi (Outgoing)
    df_out = df[df['Direction'] == 'Outgoing'].copy()

    # --- 4. PHÂN TÍCH THEO NHÂN VIÊN ---
    def employee_stats(group):
        total_calls = len(group)
        connected = (group['Action Result'] == 'Call connected').sum()
        total_talk_time = group['Duration_Sec'].sum()
        
        # Đếm các cuộc gọi hiệu quả theo mốc
        c_1m = (group['Duration_Sec'] >= 60).sum()
        c_5m = (group['Duration_Sec'] >= 300).sum()
        c_10m = (group['Duration_Sec'] >= 600).sum()
        c_30m = (group['Duration_Sec'] >= 1800).sum()
        
        return pd.Series({
            'Tổng gọi đi': total_calls,
            'Bắt máy': connected,
            'Tỷ lệ bắt máy (%)': round((connected / total_calls * 100), 2) if total_calls > 0 else 0,
            'Số cuộc > 1phút': c_1m,
            'Số cuộc > 5phút': c_5m,
            'Số cuộc > 10phút': c_10m,
            'Số cuộc > 30phút': c_30m,
            'Tổng giây nói chuyện': total_talk_time
        })

    # Group by Extension (Nhân viên)
    report = df_out.groupby('Extension').apply(employee_stats, include_groups=False).reset_index()
    
    # Sắp xếp theo hiệu quả (Người có cuộc gọi > 5p nhiều nhất đứng đầu)
    report = report.sort_values(by='Số cuộc > 5phút', ascending=False)

    # --- 5. HIỂN THỊ KẾT QUẢ ---
    print("\n" + "="*110)
    print(f"{'BẢNG HIỆU SUẤT NHÂN VIÊN (DỮ LIỆU ĐÃ LỌC TRÙNG)':^110}")
    print("="*110)
    print(report.to_string(index=False))
    print("="*110)

    # --- 6. XUẤT BÁO CÁO ---
    report.to_excel(OUTPUT_FILE, index=False)
    print(f"\n✅ THÀNH CÔNG: Báo cáo sạch đã lưu tại: {OUTPUT_FILE}")