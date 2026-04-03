import streamlit as st
import pandas as pd
from dateutil import parser
from datetime import date, datetime

# --- 1. 初始化語言與步驟設定 ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'CH'
if 'step' not in st.session_state:
    st.session_state.step = 1

def toggle_language():
    st.session_state.lang = 'EN' if st.session_state.lang == 'CH' else 'CH'

# --- 2. 翻譯字典 (整合分頁所需文字) ---
texts = {
    'CH': {
        'title': 'Quincy Limousine 報價系統',
        'step1': '步驟 1: 客戶聯絡資料',
        'step2': '步驟 2: 接送日期與時間',
        'step3': '步驟 3: 行程與車型',
        'step4': '步驟 4: 附加選項與報價',
        'next': '下一步',
        'prev': '返回上一步',
        'fill_all': '⚠️ 請填寫所有必填項以繼續。',
        'name_label': '姓名 (Full Name):',
        'phone_label': '電話號碼 (Phone Number):',
        'email_label': 'Gmail 地址:',
        'email_error': '⚠️ 請輸入有效的 Gmail 地址 (需包含 @gmail.com)',
        'date_label': '使用日期:',
        'time_label': '使用時間:',
        'time_placeholder': '例如: 22:30',
        'time_error': '❌ 時間格式錯誤 (例如 22:30)',
        'night_warning': '🌙 已計入夜間服務費 $100 (22:00-07:00)',
        'type_label': '接送類型:',
        'region_label': '地區:',
        'model_label': '車型:',
        'district_label': '區域:',
        'select_op': '請選擇',
        'select_reg_first': '請先選擇地區',
        'seat_label': '兒童安全座椅 ($120/張):',
        'mg_label': '機場接機服務 ($80)',
        'mg_pickup': '需要接機服務 (接機大堂 A)',
        'summary_title': '📍 預約彙總與報價',
        'item': '項目',
        'details': '內容',
        'items_list': ["客戶姓名", "聯絡電話", "Gmail", "日期", "時間", "行程", "安全座椅", "接機服務", "基本車資", "總費用"],
        'total_metric': '預計總費用',
        'no_price': '查無此組合價格，請聯繫客服。',
        'seat_unit': '張'
    },
    'EN': {
        'title': 'Quincy Limousine Quote System',
        'step1': 'Step 1: Contact Information',
        'step2': 'Step 2: Date & Time',
        'step3': 'Step 3: Route & Vehicle',
        'step4': 'Step 4: Extras & Quote',
        'next': 'Next',
        'prev': 'Back',
        'fill_all': '⚠️ Please fill in all required fields.',
        'name_label': 'Full Name:',
        'phone_label': 'Phone Number:',
        'email_label': 'Gmail Address:',
        'email_error': '⚠️ Invalid Gmail (must contain @gmail.com)',
        'date_label': 'Date:',
        'time_label': 'Pick-up Time:',
        'time_placeholder': 'e.g. 22:30',
        'time_error': '❌ Time format error (e.g. 22:30)',
        'night_warning': '🌙 Night surcharge $100 included',
        'type_label': 'Transfer Type:',
        'region_label': 'Region:',
        'model_label': 'Vehicle Type:',
        'district_label': 'District:',
        'select_op': 'Please Select',
        'select_reg_first': 'Select region first',
        'seat_label': 'Child Seat ($120/each):',
        'mg_label': 'Meet & Greet Service ($80)',
        'mg_pickup': 'Meet & Greet (Arrival Hall A)',
        'summary_title': '📍 Summary & Quote',
        'item': 'Item',
        'details': 'Details',
        'items_list': ["Name", "Phone", "Gmail", "Date", "Time", "Route", "Child Seat", "Meet & Greet", "Base Fare", "Total"],
        'total_metric': 'Total Estimated Price',
        'no_price': 'Price not found for this combination.',
        'seat_unit': 'Seat(s)'
    }
}

L = texts[st.session_state.lang]

# --- 3. 網頁基本設定 ---
st.set_page_config(page_title="Quincy Limo Prices", layout="centered")

col_title, col_lang = st.columns([0.8, 0.2])
with col_title:
    logo_url = "https://raw.githubusercontent.com/QuincyLimousine/Quincy-Limousine-Prices/main/quincyLimo_Q.png"
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 15px;">
            <img src="{logo_url}" style="height: 40px;">
            <h1 style="margin: 0; font-size: 1.8rem;">{L['title']}</h1>
        </div>
        """, unsafe_allow_html=True
    )
with col_lang:
    st.button("🌐 EN/中文", on_click=toggle_language)

st.progress(st.session_state.step / 4)

# --- 4. 資料載入 ---
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTUroRgmX-R1wQx5ndR5B8plTm7uajQg4OdpdxV8UK21exlpKhmix-wjLKGgG2HrLqWLhHQpQn-Gmfv/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        data = pd.read_csv(sheet_url)
        data.columns = data.columns.str.strip()
        return data
    except: return pd.DataFrame()

df = load_data()

# --- 5. 分步流程邏輯 ---

# 步驟 1: 聯絡資料
if st.session_state.step == 1:
    st.subheader(L['step1'])
    u_name = st.text_input(L['name_label'], value=st.session_state.get('u_name', '')).strip()

    raw_codes = [
        ("🇦🇺 Australia +61", "+61"), ("🇨🇳 China +86", "+86"), ("🇭🇰 Hong Kong +852", "+852"),
        ("🇲🇴 Macau +853", "+853"), ("🇲🇾 Malaysia +60", "+60"), ("🇸🇬 Singapore +65", "+65"),
        ("🇹🇼 Taiwan +886", "+886"), ("🇬🇧 UK +44", "+44"), ("🇺🇸 USA +1", "+1")
    ]
    country_codes = sorted(raw_codes, key=lambda x: x[0][3:])
    
    col_c, col_p = st.columns([0.45, 0.55])
    with col_c:
        hk_idx = next((i for i, c in enumerate(country_codes) if "+852" in c[1]), 0)
        code_disp = st.selectbox("Code", options=[c[0] for c in country_codes], index=hk_idx)
        sel_code = next(c[1] for c in country_codes if c[0] == code_disp)
    with col_p:
        u_phone_raw = st.text_input(L['phone_label'], value=st.session_state.get('u_phone_raw', ''), placeholder="9123 4567").strip()
    
    u_email = st.text_input(L['email_label'], value=st.session_state.get('u_email', ''), placeholder="example@gmail.com").strip()
    email_valid = "@gmail.com" in u_email.lower() if u_email else False

    if st.button(L['next']):
        if u_name and u_phone_raw and email_valid:
            st.session_state.u_name = u_name
            st.session_state.u_phone_raw = u_phone_raw
            st.session_state.u_phone_full = f"{sel_code} {u_phone_raw}"
            st.session_state.u_email = u_email
            st.session_state.step = 2
            st.rerun()
        else:
            if u_email and not email_valid: st.error(L['email_error'])
            else: st.warning(L['fill_all'])

# 步驟 2: 日期與時間
elif st.session_state.step == 2:
    st.subheader(L['step2'])
    s_date = st.date_input(L['date_label'], value=st.session_state.get('s_date', date.today()), min_value=date.today())
    p_time = st.text_input(L['time_label'], value=st.session_state.get('p_time', ''), placeholder=L['time_placeholder']).strip()

    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button(L['prev']):
            st.session_state.step = 1
            st.rerun()
    with col_nav2:
        if st.button(L['next']):
            if p_time:
                try:
                    parser.parse(p_time)
                    st.session_state.s_date = s_date
                    st.session_state.p_time = p_time
                    st.session_state.step = 3
                    st.rerun()
                except: st.error(L['time_error'])
            else: st.warning(L['fill_all'])

# 步驟 3: 接送細節
elif st.session_state.step == 3:
    st.subheader(L['step3'])
    
    t_types = [L['select_op']] + sorted(df['Transfer Type'].dropna().unique().tolist())
    s_type = st.selectbox(L['type_label'], t_types)
    
    mods = [L['select_op']] + sorted(df['Model'].dropna().unique().tolist())
    s_model = st.selectbox(L['model_label'], mods)
    
    regs = [L['select_op']] + sorted(df['Region'].dropna().unique().tolist())
    s_region = st.selectbox(L['region_label'], regs)
    
    if s_region != L['select_op']:
        dists = [L['select_op']] + sorted(df[df['Region'] == s_region]['District'].dropna().unique().tolist())
        s_district = st.selectbox(L['district_label'], dists)
    else:
        s_district = st.selectbox(L['district_label'], [L['select_reg_first']])

    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button(L['prev']):
            st.session_state.step = 2
            st.rerun()
    with col_nav2:
        if st.button(L['next']):
            if all(x != L['select_op'] and x != L['select_reg_first'] for x in [s_type, s_model, s_region, s_district]):
                st.session_state.s_type = s_type
                st.session_state.s_model = s_model
                st.session_state.s_region = s_region
                st.session_state.s_district = s_district
                st.session_state.step = 4
                st.rerun()
            else: st.warning(L['fill_all'])

# 步驟 4: 選項與最終報價
elif st.session_state.step == 4:
    st.subheader(L['step4'])
    seat_count = st.number_input(L['seat_label'], min_value=0, max_value=4, value=0)
    seat_fee = seat_count * 120
    
    mg_fee = 0
    if "Arrival" in st.session_state.s_type:
        if st.checkbox(L['mg_pickup']): mg_fee = 80

    # 報價運算
    res = df[
        (df['Transfer Type'].astype(str).str.strip() == st.session_state.s_type) &
        (df['Model'].astype(str).str.strip() == st.session_state.s_model) &
        (df['Region'].astype(str).str.strip() == st.session_state.s_region) &
        (df['District'].astype(str).str.strip() == st.session_state.s_district)
    ]

    if not res.empty:
        base_raw = res.iloc[0]['Result']
        base_price = int(''.join(filter(str.isdigit, str(base_raw))))
        
        # 夜間費
        night_fee = 0
        parsed_t = parser.parse(st.session_state.p_time).time()
        if parsed_t >= pd.to_datetime("22:00").time() or parsed_t <= pd.to_datetime("07:00").time():
            night_fee = 100
        
        total_price = base_price + seat_fee + night_fee + mg_fee
        
        # 行程文字
        if "Arrival" in st.session_state.s_type: route = f"HKIA → {st.session_state.s_district}"
        elif "Departure" in st.session_state.s_type: route = f"{st.session_state.s_district} → HKIA"
        else: route = f"{st.session_state.s_type} ({st.session_state.s_district})"

        st.subheader(L['summary_title'])
        summary_data = [
            st.session_state.u_name, st.session_state.u_phone_full, st.session_state.u_email,
            st.session_state.s_date.strftime("%Y-%m-%d"), st.session_state.p_time,
            route, f"{seat_count} {L['seat_unit']}",
            f"${mg_fee}" if mg_fee > 0 else "N/A",
            f"${base_price}", f"HKD ${total_price}"
        ]
        
        summary_df = pd.DataFrame({L['item']: L['items_list'], L['details']: summary_data})
        st.table(summary_df)
        st.metric(label=L['total_metric'], value=f"HKD ${total_price}")
        
        if night_fee > 0: st.warning(L['night_warning'])
    else:
        st.error(L['no_price'])
    
    if st.button(L['prev']):
        st.session_state.step = 3
        st.rerun()
