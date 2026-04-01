import streamlit as st
import pandas as pd
from dateutil import parser
from datetime import date

# 1. 網頁基本設定
st.set_page_config(page_title="Quincy Limo Prices", layout="centered")

# 自訂 CSS 讓選項看起來有框架感，並調整文字對齊
st.markdown("""
    <style>
    .option-container {
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        height: 100px;
    }
    .small-text {
        font-size: 0.8rem;
        color: gray;
        margin-bottom: 5px;
    }
    /* 隱藏原生 checkbox 標籤，改用自訂排版 */
    div[data-testid="stCheckbox"] > label > div[data-testid="stMarkdownContainer"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Logo 與 標題 ---
logo_url = "https://raw.githubusercontent.com/QuincyLimousine/Quincy-Limousine-Prices/main/quincyLimo_Q.png"
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
        <img src="{logo_url}" style="height: 40px;">
        <h1 style="margin: 0; font-size: 2rem;">Quincy Limo 預約報價系統</h1>
    </div>
    """,
    unsafe_allow_html=True
)

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
    st.error("無法載入資料庫。")
else:
    # --- 第一步：日期時間 ---
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
                st.caption("⚠️ 格式錯誤")

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
            selected_district = st.selectbox("區域:", districts)
        else:
            selected_district = st.selectbox("區域:", ["請先選擇地區"])

    st.divider()

    # --- 第三步：附加選項 (對稱框架設計) ---
    st.subheader("👶 第三步：附加選項")
    
    col_opt1, col_opt2 = st.columns(2)
    
    # 左側：兒童安全座椅
    with col_opt1:
        st.markdown('<div class="option-container">', unsafe_allow_html=True)
        c1, c2 = st.columns([0.7, 0.3])
        with c1:
            st.write("**兒童安全座椅**")
            st.write("$120/張")
        with c2:
            # 為了讓勾選格在右方，這裡使用 number_input 或 checkbox
            seat_count = st.number_input("數量", min_value=0, max_value=4, value=0, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        seat_fee = seat_count * 120

    # 右側：Meet And Greet
    meet_greet_fee = 0
    with col_opt2:
        if selected_type == "Airport Transfer(Arrival)":
            st.markdown('<div class="option-container">', unsafe_allow_html=True)
            c1, c2 = st.columns([0.7, 0.3])
            with c1:
                st.markdown('<div class="small-text">Pickup Point: Arrival Hall A</div>', unsafe_allow_html=True)
                st.write("**Meet & Greet**")
                st.write("$80")
            with c2:
                # 勾選格置於右側
                is_meet_greet = st.checkbox("MG", key="mg_check", label_visibility="collapsed")
                if is_meet_greet:
                    meet_greet_fee = 80
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # 不符合條件時顯示空白框架保持對稱
            st.markdown('<div class="option-container" style="border: 1px dashed #eee;"></div>', unsafe_allow_html=True)

    st.divider()

    # --- 最終報價 ---
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
            
            total_price = base_price + seat_fee + night_fee + meet_greet_fee
            
            st.subheader("📍 預約彙總與報價")
            summary_df = pd.DataFrame({
                "項目": ["日期", "時間", "行程", "安全座椅", "接機服務", "車資總計"],
                "內容": [selected_date.strftime("%Y-%m-%d"), pickup_input, 
                        f"{selected_type}", f"{seat_count} 張", 
                        "已選 ($80)" if meet_greet_fee > 0 else "未選", 
                        f"HKD ${total_price}"]
            })
            st.table(summary_df)
            st.metric("總預算 (Total)", f"${total_price}")
        else:
            st.warning("查無價格。")
