import streamlit as st
import pandas as pd
from dateutil import parser

# 1. 網頁基本設定
st.set_page_config(page_title="Quincy Limo Prices", layout="centered")
st.title("🚗 Quincy Limousine 預約報價系統")

# 2. 資料來源
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTUroRgmX-R1wQx5ndR5B8plTm7uajQg4OdpdxV8UK21exlpKhmix-wjLKGgG2HrLqWLhHQpQn-Gmfv/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        data = pd.read_csv(sheet_url)
        data.columns = data.columns.str.strip()
        return data
    except:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("無法載入資料庫，請檢查 Google Sheet 設定。")
else:
    st.subheader("第一步：行程詳細資料")
    
    col1, col2 = st.columns(2)
    with col1:
        # 1. 接送類型
        transfer_types = ["請選擇"] + sorted(df['Transfer Type'].dropna().unique().tolist())
        selected_type = st.selectbox("接送類型 (Transfer Type):", transfer_types)
    
    with col2:
        # 2. 車型
        models = ["請選擇"] + sorted(df['Model'].dropna().unique().tolist())
        selected_model = st.selectbox("選擇車型 (Model):", models)

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        # 3. 先選擇 Region (例如：九龍、新界)
        regions = ["請選擇"] + sorted(df['Region'].dropna().unique().tolist())
        selected_region = st.selectbox("地區 (Region):", regions)

    with col_d2:
        # 4. 根據選定的 Region 篩選 District (例如：尖沙咀、旺角)
        if selected_region != "請選擇":
            # 關鍵邏輯：只抓取符合該 Region 的 District
            filtered_districts = df[df['Region'] == selected_region]['District'].dropna().unique().tolist()
            districts = ["請選擇"] + sorted(filtered_districts)
        else:
            districts = ["請先選擇地區"]
        
        selected_district = st.selectbox("區域 (District):", districts)

    st.divider()

    # --- 第二部分：附加選項 ---
    st.subheader("第二步：附加選項與時間")
    col3, col4 = st.columns(2)
    with col3:
        seat_count = st.number_input("兒童安全座椅 ($120/張):", min_value=0, max_value=4, value=0)
        seat_fee = seat_count * 120

    with col4:
        pickup_input = st.text_input("預約上車時間 (Pick-up Time):", placeholder="例如: 22:30")
        
        night_fee = 0
        if pickup_input:
            try:
                parsed_time = parser.parse(pickup_input).time()
                if parsed_time >= pd.to_datetime("22:00").time() or parsed_time <= pd.to_datetime("07:00").time():
                    night_fee = 100
            except:
                st.caption("⚠️ 格式參考: 22:30 或 10:30 PM")

    st.divider()

    # --- 第三部分：結果顯示 ---
    # 檢查是否所有必要選項都已選擇
    required_selections = [selected_type, selected_model, selected_region, selected_district]
    
    if "請選擇" not in required_selections and "請先選擇地區" not in required_selections:
        
        final_result = df[
            (df['Transfer Type'] == selected_type) & 
            (df['Model'] == selected_model) & 
            (df['Region'] == selected_region) & 
            (df['District'] == selected_district)
        ]

        if not final_result.empty:
            base_price_raw = final_result.iloc[0]['Result']
            try:
                # 提取數字進行計算
                base_price = int(''.join(filter(str.isdigit, str(base_price_raw))))
            except:
                base_price = 0
            
            total_price = base_price + seat_fee + night_fee
            
            st.subheader("📍 報價明細:")
            
            # 費用明細表
            detail_data = {
                "項目 (Item)": ["基本行程費用", "安全座椅費用", "夜間服務費"],
                "金額 (Amount)": [f"${base_price}", f"${seat_fee}", f"${night_fee}"]
            }
            st.table(pd.DataFrame(detail_data))
            
            st.metric(label="預計總費用 (Total Price)", value=f"HKD ${total_price}")
            
            if night_fee > 0:
                st.warning("🌙 已包含夜間服務費 $100 (22:00-07:00)")
        else:
            st.warning("目前資料庫中無此組合的價格。")
    else:
        st.info("💡 請完成所有選項（由上至下）以獲取預估報價。")
