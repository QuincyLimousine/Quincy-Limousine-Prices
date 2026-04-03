# --- 在「第一步：客戶聯絡資料」區塊中替換 ---

# 1. 定義完整的國家清單 (包含國旗、名稱、區號)
# 格式為: (顯示標籤, 純區號數字)
raw_codes = [
    ("🇦🇫 Afghanistan +93", "+93"), ("🇦🇱 Albania +355", "+355"), ("🇩🇿 Algeria +213", "+213"),
    ("🇦🇩 Andorra +376", "+376"), ("🇦🇴 Angola +244", "+244"), ("🇦🇷 Argentina +54", "+54"),
    ("🇦🇲 Armenia +374", "+374"), ("🇦🇺 Australia +61", "+61"), ("🇦🇹 Austria +43", "+43"),
    ("🇦🇿 Azerbaijan +994", "+994"), ("🇧Ｈ Bahrain +973", "+973"), ("🇧🇩 Bangladesh +880", "+880"),
    ("🇧🇪 Belgium +32", "+32"), ("🇧🇿 Belize +501", "+501"), ("🇧🇯 Benin +229", "+229"),
    ("🇧Ｔ Bhutan +975", "+975"), ("🇧🇴 Bolivia +591", "+591"), ("🇧🇦 Bosnia +387", "+387"),
    ("🇧🇼 Botswana +267", "+267"), ("🇧🇷 Brazil +55", "+55"), ("🇧🇳 Brunei +673", "+673"),
    ("🇧🇬 Bulgaria +359", "+359"), ("🇰Ｈ Cambodia +855", "+855"), ("🇨🇲 Cameroon +237", "+237"),
    ("🇨🇦 Canada +1", "+1"), ("🇨Ｌ Chile +56", "+56"), ("🇨🇳 China +86", "+86"),
    ("🇨🇴 Colombia +57", "+57"), ("🇨🇷 Costa Rica +506", "+506"), ("🇭🇷 Croatia +385", "+385"),
    ("🇨🇺 Cuba +53", "+53"), ("🇨🇾 Cyprus +357", "+357"), ("🇨🇿 Czech +420", "+420"),
    ("🇩🇰 Denmark +45", "+45"), ("🇪🇨 Ecuador +593", "+593"), ("🇪🇬 Egypt +20", "+20"),
    ("🇫🇮 Finland +358", "+358"), ("🇫🇷 France +33", "+33"), ("🇩🇪 Germany +49", "+49"),
    ("🇬Ｈ Ghana +233", "+233"), ("🇬Ｒ Greece +30", "+30"), ("🇭Ｋ Hong Kong +852", "+852"),
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
    ("🇵Ｈ Philippines +63", "+63"), ("🇵Ｌ Poland +48", "+48"), ("🇵Ｔ Portugal +351", "+351"),
    ("🇶Ａ Qatar +974", "+974"), ("🇷Ｏ Romania +40", "+40"), ("🇷Ｕ Russia +7", "+7"),
    ("🇸Ａ Saudi Arabia +966", "+966"), ("🇸🇬 Singapore +65", "+65"), ("🇸Ｋ Slovakia +421", "+421"),
    ("🇿Ａ South Africa +27", "+27"), ("🇪🇸 Spain +34", "+34"), ("🇱Ｋ Sri Lanka +94", "+94"),
    ("🇸Ｅ Sweden +46", "+46"), ("🇨Ｈ Switzerland +41", "+41"), ("🇹🇼 Taiwan +886", "+886"),
    ("🇹Ｈ Thailand +66", "+66"), ("🇹Ｒ Turkey +90", "+90"), ("🇺Ａ Ukraine +380", "+380"),
    ("🇦Ｅ UAE +971", "+971"), ("🇬Ｂ United Kingdom +44", "+44"), ("🇺Ｓ United States +1", "+1"),
    ("🇺Ｙ Uruguay +598", "+598"), ("🇺Ｚ Uzbekistan +998", "+998"), ("🇻🇪 Venezuela +58", "+58"),
    ("🇻🇳 Vietnam +84", "+84")
]

# 2. 按國家名稱 A-Z 排序 (國旗 Emoji 後面的字母會參與排序)
country_codes = sorted(raw_codes, key=lambda x: x[0][3:])

# 3. 建立兩欄佈局
col_country, col_phone_num = st.columns([0.45, 0.55])

with col_country:
    # 預設選中香港
    hk_index = next((i for i, c in enumerate(country_codes) if "+852" in c[1]), 0)
    selected_code_display = st.selectbox(
        "Code", 
        options=[c[0] for c in country_codes], 
        index=hk_index,
        help="Select your country/region code"
    )
    # 獲取實際區號
    selected_code = next(c[1] for c in country_codes if c[0] == selected_code_display)

with col_phone_num:
    phone_val = st.text_input(L['phone_label'], placeholder="9123 4567")

# 4. 最終組合
user_phone = f"{selected_code} {phone_val}" if phone_val else ""
