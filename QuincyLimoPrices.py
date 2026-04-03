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

# --- 2. 翻譯字典 ---
texts = {
    'CH': {
        'title': 'Quincy Limousine 報價系統',
        'step1': '步驟 1: 客戶聯絡資料',
        'step2': '步驟 2: 接送行程與時間',
        'step3': '步驟 3: 附加選項',
        'step4': '步驟 4: 最終預約報價',
        'next': '下一步',
        'prev': '返回上一步',
        'fill_all': '⚠️ 請填寫所有必填項以繼續。',
        'name_label': '姓名 (Full Name):',
        'phone_label': '電話號碼 (Phone Number):',
        'email_label': 'Gmail 地址:',
        'email_error': '⚠️ 請輸入有效的電地址 (需包含 @gmail.com)',
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
        'step2': 'Step 2: Journey & Time',
        'step3': 'Step 3: Extra Options',
        'step4': 'Step 4: Final Quote',
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

# --- 3. 網頁設定 ---
st.set_page_config(page_title="Quincy Limo Prices", layout="centered")

col_title, col_lang = st.columns([0.8, 0.2])
with col_title:
    logo_url = "https://raw.githubusercontent.com/QuincyLimousine/Quincy-Limousine-Prices/main/quincyLimo_Q.png"
    st.markdown(f'<div style="display: flex; align-items: center; gap: 15px;"><img src="{logo_url}" style="height: 40px;"><h1 style="margin: 0; font-size: 1.8rem;">{L["title"]}</h1></div>', unsafe_allow_html=True)
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

# --- 5. 分步流程 ---

# 步驟 1: 聯絡資料
if st.session_state.step == 1:
    st.subheader(L['step1'])
    u_name = st.text_input(L['name_label'], value=st.session_state.get('u_name', '')).strip()
    
    # 全球區號清單 (格式：國旗 + 國名 + 區號)
    raw_codes = [
        ("🇦🇫 Afghanistan +93", "+93"), ("🇦🇱 Albania +355", "+355"), ("🇩🇿 Algeria +213", "+213"),
        ("🇦🇩 Andorra +376", "+376"), ("🇦🇴 Angola +244", "+244"), ("🇦🇷 Argentina +54", "+54"),
        ("🇦🇲 Armenia +374", "+374"), ("🇦🇺 Australia +61", "+61"), ("🇦🇹 Austria +43", "+43"),
        ("🇦🇿 Azerbaijan +994", "+994"), ("🇧Ｈ Bahrain +973", "+973"), ("🇧🇩 Bangladesh +880", "+880"),
        ("🇧🇪 Belgium +32", "+32"), ("🇧🇿 Belize +501", "+501"), ("🇧🇯 Benin +229", "+229"),
        ("🇧Ｔ Bhutan +975", "+975"), ("🇧 Bolivia +591", "+591"), ("🇧🇦 Bosnia +387", "+387"),
        ("🇧🇼 Botswana +267", "+267"), ("🇧🇷 Brazil +55", "+55"), ("🇧🇳 Brunei +673", "+673"),
        ("🇧🇬 Bulgaria +359", "+359"), ("🇰Ｈ Cambodia +855", "+855"), ("🇨🇲 Cameroon +237", "+237"),
        ("🇨🇦 Canada +1", "+1"), ("🇨Ｌ Chile +56", "+56"), ("🇨🇳 China +86", "+86"),
        ("🇨🇴 Colombia +57", "+57"), ("🇨🇷 Costa Rica +506", "+506"), ("🇭🇷 Croatia +385", "+385"),
        ("🇨🇺 Cuba +53", "+53"), ("🇨🇾 Cyprus +357", "+357"), ("🇨🇿 Czech +420", "+420"),
        ("🇩🇰 Denmark +45", "+45"), ("🇪🇨 Ecuador +593", "+593"), ("🇪🇬 Egypt +20", "+20"),
        ("🇫🇮 Finland +358", "+358"), ("🇫🇷 France +33", "+33"), ("🇩🇪 Germany +49", "+49"),
        ("🇬Ｈ Ghana +233", "+233"), ("🇬Ｒ Greece +30", "+30"), ("🇭🇰 Hong Kong +852", "+852"),
        ("🇭Ｕ Hungary +36", "+36"), ("🇮🇸 Iceland +354", "+354"), ("🇮🇳 India +91", "+91"),
        ("🇮🇩 Indonesia +62", "+62"), ("🇮🇷 Iran +98", "+98"), ("🇮🇶 Iraq +964", "+964"),
        ("🇮🇪 Ireland +353", "+353"), ("🇮🇱 Israel +972", "+972"), ("🇮🇹 Italy +39", "+39"),
        ("🇯🇲 Jamaica +1876", "+1876"), ("🇯🇵 Japan +81", "+81"), ("🇯🇴 Jordan +962", "+962"),
        ("🇰🇿 Kazakhstan +7", "+7"), ("🇰Ｅ Kenya +254", "+254"), ("🇰Ｗ Kuwait +965", "+965"),
        ("🇱🇦 Laos +856", "+856"), ("🇱🇧 Lebanon +961", "+961"), ("🇲🇴 Macau +853", "+853"),
        ("🇲🇾 Malaysia +60", "+60"), ("🇲Ｖ Maldives +960", "+960"), ("🇲Ｔ Malta +356", "+356"),
        ("🇲Ｘ Mexico +52", "+52"), ("🇲🇨 Monaco +377", "+377"), ("🇲🇳 Mongolia +976", "+976"),
        ("🇲Ａ Morocco +212", "+212"), ("🇲Ｍ Myanmar +95", "+95"), ("🇳🇵 Nepal +977", "+977"),
        ("🇳Ｌ Netherlands +31", "+31"), ("🇳Ｚ New Zealand +64", "+64"), ("🇳🇬 Nigeria +234", "+234"),
        ("🇳Ｏ Norway +47", "+47"), ("🇵Ｋ Pakistan +92", "+92"), ("🇵🇦 Panama +507", "+507"),
        ("🇵Ｇ Papua New Guinea +675", "+675"), ("🇵Ｙ Paraguay +595", "+595"), ("🇵Ｅ Peru +51", "+51"),
        ("🇵Ｈ Philippines +63", "+63"), ("🇵Ｌ Poland +48", "+48"), ("🇵 Portugal +351", "+351"),
        ("🇶Ａ Qatar +974", "+974"), ("🇷Ｏ Romania +40", "+40"), ("🇷Ｕ Russia +7", "+7"),
        ("🇸Ａ Saudi Arabia +966", "+966"), ("🇸🇬 Singapore +65", "+65"), ("🇸Ｋ Slovakia +421", "+421"),
        ("🇿Ａ South Africa +27", "+27"), ("🇪🇸 Spain +34", "+34"), ("🇱Ｋ Sri Lanka +94", "+94"),
        ("🇸Ｅ Sweden +46", "+46"), ("🇨Ｈ Switzerland +41", "+41"), ("🇹🇼 Taiwan +886", "+886"),
        ("🇹Ｈ Thailand +66", "+66"), ("🇹Ｒ Turkey +90", "+90"), ("🇺Ａ Ukraine +380", "+380"),
        ("🇦Ｅ UAE +971", "+971"), ("🇬Ｂ United Kingdom +44", "+44"), ("🇺Ｓ United States +1", "+1"),
        ("🇻🇳 Vietnam +84", "+84")
    ]
    # 按國家名稱 (Emoji 之後的字串) A-Z 排序
    country_codes = sorted(raw_codes, key=lambda x: x[0][3:])
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
            st.session_state.u_name, st.session_state.u_phone_raw, st.session_state.u_phone_full, st.session_state.u_email = u_name, u_phone_raw, f"{sel_code} {u_phone_raw}", u_email
            st.session_state.step = 2
            st.rerun()
        else:
            if u_email and not email_valid: st.error(L['email_error'])
            else: st.warning(L['fill_all'])

# 步驟 2: 合併頁面 (日期、時間、行程)
elif st.session_state.step == 2:
    st.subheader(L['step2'])
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        s_date = st.date_input(L['date_label'], value=st.session_state.get('s_date', date.today()), min_value=date.today())
    with col_t2:
        p_time = st.text_input(L['time_label'], value=st.session_state.get('p_time', ''), placeholder=L['time_placeholder']).strip()
    
    st.divider()
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        t_types = [L['select_op']] + sorted(df['Transfer Type'].dropna().unique().tolist())
        s_type = st.selectbox(L['type_label'], t_types, index=t_types.index(st.session_state.get('s_type')) if st.session_state.get('s_type') in t_types else 0)
        regs = [L['select_op']] + sorted(df['Region'].dropna().unique().tolist())
        s_region = st.selectbox(L['region_label'], regs, index=regs.index(st.session_state.get('s_region')) if st.session_state.get('s_region') in regs else 0)
    with col_s2:
        mods = [L['select_op']] + sorted(df['Model'].dropna().unique().tolist())
        s_model = st.selectbox(L['model_label'], mods, index=mods.index(st.session_state.get('s_model')) if st.session_state.get('s_model') in mods else 0)
        if s_region != L['select_op']:
            dists = [L['select_op']] + sorted(df[df['Region'] == s_region]['District'].dropna().unique().tolist())
            s_district = st.selectbox(L['district_label'], dists, index=dists.index(st.session_state.get('s_district')) if st.session_state.get('s_district') in dists else 0)
        else:
            s_district = st.selectbox(L['district_label'], [L['select_reg_first']])

    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button(L['prev']): st.session_state.step = 1; st.rerun()
    with col_nav2:
        if st.button(L['next']):
            try:
                parser.parse(p_time)
                if all(x != L['select_op'] and x != L['select_reg_first'] for x in [s_type, s_model, s_region, s_district]):
                    st.session_state.update({"s_date": s_date, "p_time": p_time, "s_type": s_type, "s_model": s_model, "s_region": s_region, "s_district": s_district})
                    st.session_state.step = 3
                    st.rerun()
                else: st.warning(L['fill_all'])
            except: st.error(L['time_error'])

# 步驟 3: 附加選項
elif st.session_state.step == 3:
    st.subheader(L['step3'])
    seat_count = st.number_input(L['seat_label'], min_value=0, max_value=4, value=st.session_state.get('seat_count', 0))
    mg_selected = st.session_state.get('mg_selected', False)
    if "Arrival" in st.session_state.s_type:
        st.markdown(f"**{L['mg_label']}**")
        mg_selected = st.checkbox(L['mg_pickup'], value=mg_selected)

    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button(L['prev']): st.session_state.step = 2; st.rerun()
    with col_nav2:
        if st.button(L['next']):
            st.session_state.seat_count = seat_count
            st.session_state.mg_selected = mg_selected
            st.session_state.step = 4
            st.rerun()

# 步驟 4: 報價彙總
elif st.session_state.step == 4:
    st.subheader(L['step4'])
    res = df[(df['Transfer Type'].astype(str).str.strip() == st.session_state.s_type) & (df['Model'].astype(str).str.strip() == st.session_state.s_model) & (df['Region'].astype(str).str.strip() == st.session_state.s_region) & (df['District'].astype(str).str.strip() == st.session_state.s_district)]

    if not res.empty:
        base_price = int(''.join(filter(str.isdigit, str(res.iloc[0]['Result']))))
        night_fee = 100 if (parser.parse(st.session_state.p_time).time() >= pd.to_datetime("22:00").time() or parser.parse(st.session_state.p_time).time() <= pd.to_datetime("07:00").time()) else 0
        mg_fee = 80 if st.session_state.mg_selected else 0
        seat_fee = st.session_state.seat_count * 120
        total = base_price + night_fee + mg_fee + seat_fee
        
        route = f"HKIA → {st.session_state.s_district}" if "Arrival" in st.session_state.s_type else (f"{st.session_state.s_district} → HKIA" if "Departure" in st.session_state.s_type else f"{st.session_state.s_type} ({st.session_state.s_district})")
        
        summary_df = pd.DataFrame({L['item']: L['items_list'], L['details']: [st.session_state.u_name, st.session_state.u_phone_full, st.session_state.u_email, st.session_state.s_date.strftime("%Y-%m-%d"), st.session_state.p_time, route, f"{st.session_state.seat_count} {L['seat_unit']}", f"${mg_fee}" if mg_fee > 0 else "N/A", f"${base_price}", f"HKD ${total}"]})
        st.table(summary_df)
        st.metric(label=L['total_metric'], value=f"HKD ${total}")
        if night_fee > 0: st.warning(L['night_warning'])
    else: st.error(L['no_price'])
    
    if st.button(L['prev']): st.session_state.step = 3; st.rerun()
