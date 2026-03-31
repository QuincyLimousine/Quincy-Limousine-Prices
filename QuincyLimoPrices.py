import streamlit as st
import pandas as pd
from dateutil import parser

# 1. 網頁基本設定
st.set_page_config(page_title="Quincy Limo Prices", layout="centered")
st.title("🚗 Quincy Limo 預約報價系統")

# 2. 資料來源 (Google Sheets CSV)
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTUroRgmX-R1wQx5ndR5B8plTm7uajQg4OdpdxV8UK21exlpKhmix-wjLKGgG2HrLqWLhHQpQn-Gmfv/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    data = pd.read_csv(sheet_url)
    data.columns = data.columns.str.strip()
    return data

try:
    df = load_data()
    
    # --- 第一部分：行程篩選 ---
    col1, col2 = st.columns(2)
    with col1:
        models = sorted(df['Model'].dropna().unique())
        selected_model = st.selectbox("選擇車型 (Model):", models)
    with col2:
        available_regions = sorted(df[df['Model'] == selected_model]['Region'].dropna().unique())
        selected_region = st.selectbox("選擇地區 (Region):", available_regions)

    # --- 第二部分：附加選項 ---
    col3, col4 = st.columns(2)
    with col3:
        seat_count = st.number_input("兒童安全座椅 ($120/張):", min_value=0, max_value=4, value=0)
        seat_fee = seat_count * 120

    with col4:
        pickup_input = st.text_input("預約上車時間 (Pick-up Time):", placeholder="例如: 23:30 或 11:00 PM")
        
        # 夜間收費判斷邏輯
        night_fee = 0
        if pickup_input:
            try:
                parsed_time = parser.parse(pickup_input).time()
                # 判斷是否在 22:00 至 07:00 之間
                if parsed_time >= pd.to_datetime("22:00").time() or parsed_time <= pd.to_datetime("07:00").time():
                    night_fee = 100
            except:
                st.caption("⚠️ 無法識別時間格式，請輸入正確時間 (如 22:30)")

    st.divider()

    # --- 第三部分：結果與金額總計 ---
    final_result = df[(df['Model'] == selected_model) & (df['Region'] == selected_region)]

    if not final_result.empty:
        # 假設 Result 欄位內是數字字串 (例如 "500")，我們嘗試將其轉為整數進行計算
        base_price_raw = final_result.iloc[0]['Result']
        
        # 嘗試從報價中提取數字（若 Excel 內包含 "HKD" 等字眼需先處理）
        try:
            base_price = int(''.join(filter(str.isdigit, str(base_price_raw))))
        except:
            base_price = 0
            st.error("Excel 報價格式錯誤，請確保 Result 欄位為純數字。")

        # 總計金額
        total_price = base_price + seat_fee + night_fee
        
        st.subheader("📍 預約明細與報價:")
        
        # 建立費用明細表
        fees_detail = {
            "項目 (Item)": ["基本行程費用", "安全座椅費用", "夜間服務費 (22:00-07:00)"],
            "金額 (Amount)": [f"${base_price}", f"${seat_fee}", f"${night_fee}"]
        }
        st.table(pd.DataFrame(fees_detail))
        
        # 醒目顯示總金額
        st.metric(label="預計總費用 (Total Estimated Price)", value=f"HKD ${total_price}")
        
        if night_fee > 0:
            st.warning("🌙 已自動計入夜間服務費 $100 元。")
            
    else:
        st.warning("查無此組合資料，請重新選擇。")

except Exception as e:
    st.error("資料讀取發生錯誤。")
