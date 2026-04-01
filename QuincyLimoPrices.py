import streamlit as st
import pandas as pd
from dateutil import parser
from datetime import date

# 1. 初始化背景模式 (Session State)
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'light'  # 預設為淺色

# 定義切換函數
def toggle_theme():
    if st.session_state.theme_mode == 'light':
        st.session_state.theme_mode = 'dark'
    else:
        st.session_state.theme_mode = 'light'

# 2. 網頁基本設定
st.set_page_config(page_title="Quincy Limo Prices", layout="centered")

# --- 根據狀態注入 CSS 改變背景 ---
if st.session_state.theme_mode == 'dark':
    bg_color = "#0E1117"
    text_color = "#FFFFFF"
    btn_label = "☀️ 切換淺色模式 (Light Mode)"
else:
    bg_color = "#FFFFFF"
    text_color = "#000000"
    btn_label = "🌙 切換深色模式 (Dark Mode)"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 頂部 Logo 與 標題 (含切換按鈕) ---
col_header, col_btn = st.columns([0.8, 0.2])

with col_header:
    # 請替換為您的 GitHub Logo Raw 連結
    logo_url = "https://raw.githubusercontent.com/QuincyLimousine/Quincy-Limousine-Prices/main/quincyLimo_Q.png"
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 15px;">
            <img src="{logo_url}" style="height: 40px;">
            <h1 style="margin: 0; font-size: 1.8rem; color: {text_color};">Quincy Limo 預約報價系統</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_btn:
    st.button(btn_label, on_click=toggle_theme)

# 3. 資料來源
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
    # --- 第一步：預約時間與日期 ---
    st.subheader("📅 第一步：預約時間與日期")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        selected_date = st.date_input("預約上車日期:", value=date.today(), min_value=date.today())
    with col_t2:
        pickup_input = st.text_input("預約上車時間:", placeholder="例如: 22:30")
        night_fee = 0
        if pickup_input:
            try:
                parsed_time = parser.parse(pickup_input).time()
                if parsed_time >= pd.to_datetime("22:00").time() or parsed_time <= pd.to_datetime("07:00").time():
                    night_fee = 100
            except:
                st.caption("⚠️ 格式參考: 22:30")

    st.divider()

    # --- 第二步：接送詳情 ---
    st.subheader("🚘 第二步：接送詳情")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        transfer_types = ["請選擇"] + sorted(df['Transfer Type'].dropna().unique().tolist())
        selected_type = st.selectbox("接送類型:", transfer_types)
        regions = ["請選擇"] + sorted(df['Region'].dropna().unique().tolist())
        selected_region = st.selectbox("地區:", regions)
    with col_s2:
        models = ["請選擇"] + sorted(df['Model'].dropna().unique().tolist())
        selected_model = st.selectbox("車型:", models)
        if selected_region != "請選擇":
            districts = ["請選擇"] + sorted(df[df['Region'] == selected_region]['District'].dropna().unique().tolist())
        else:
            districts = ["請先選擇地區"]
        selected_district = st.selectbox("區域 (District):", districts)

    st.divider()

    # --- 第三步：附加選項 ---
    st.subheader("👶 第三步：附加選項")
    seat_count = st.number_input("兒童安全座椅 ($120/張):", min_value=0, max_value=4, value=0)
    seat_fee = seat_count * 120

    st.divider()

    # --- 最終報價顯示 ---
    required_fields = [selected_type, selected_model, selected_region, selected_district]
    if "請選擇" not in required_fields and "請先選擇地區" not in required_fields:
        final_result = df[(df['Transfer Type'] == selected_type) & (df['Model'] == selected_model) & 
                          (df['Region'] == selected_region) & (df['District'] == selected_district)]

        if not final_result.empty:
            base_price_raw = final_result.iloc[0]['Result']
            try:
                base_price = int(''.join(filter(str.isdigit, str(base_price_raw))))
            except:
                base_price = 0
            
            total_price = base_price + seat_fee + night_fee
            
            st.subheader("📍 預約彙總與報價")
            summary_data = {
                "項目": ["日期", "時間", "行程", "安全座椅", "基本車資", "其他費用"],
                "內容": [selected_date.strftime("%Y-%m-%d"), pickup_input if pickup_input else "未輸入",
                        f"{selected_type} ({selected_region}-{selected_district})", f"{seat_count} 張",
                        f"${base_price}", f"${seat_fee + night_fee}"]
            }
            st.table(pd.DataFrame(summary_data))
            st.metric(label="預計總費用", value=f"HKD ${total_price}")
        else:
            st.warning("查無此組合價格。")
    else:
        st.info("💡 請依序完成所有選單以獲取報價。")
