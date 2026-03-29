content = open('frontend/app.py', encoding='utf-8').read()

# ── FIX 1: Chat chips — make them copyable via st.code instead of broken onclick HTML ──
old1 = '''    chips_html = "".join(f'<span class="chat-chip" onclick="void(0)" title="{c}">🌿 {c[:40]}{"..." if len(c)>40 else ""}</span>' for c in chips)
    st.markdown(f'<div style="margin-bottom:12px">{chips_html}</div>', unsafe_allow_html=True)
    st.caption("💡 Click a chip or type below. Copy a chip text to the chat input to use it.")'''

new1 = '''    chip_cols = st.columns(3)
    for i, c in enumerate(chips):
        with chip_cols[i % 3]:
            if st.button(f"🌿 {c[:45]}{'…' if len(c)>45 else ''}", key=f"chip_{i}", use_container_width=True):
                st.session_state["prefill_chat"] = c'''

print('FIX1 found:', old1 in content)
content = content.replace(old1, new1)

# ── FIX 2: Weather loading — show spinner and clear error when backend down ──
old2 = '''    if st.session_state.weather_data is None and st.session_state.farmer_location:
        try:
            wr = requests.get(f"{API}/weather", params={"location": st.session_state.farmer_location}, timeout=10)
            if wr.status_code == 200:
                st.session_state.weather_data = wr.json()
                audit("Weather Fetch", f"Location: {st.session_state.farmer_location}", source="online")
        except Exception:
            pass

    w = st.session_state.weather_data'''

new2 = '''    if st.session_state.weather_data is None and st.session_state.farmer_location:
        with st.spinner("Loading weather..."):
            try:
                wr = requests.get(f"{API}/weather", params={"location": st.session_state.farmer_location}, timeout=10)
                if wr.status_code == 200:
                    st.session_state.weather_data = wr.json()
                    audit("Weather Fetch", f"Location: {st.session_state.farmer_location}", source="online")
                else:
                    st.session_state.weather_data = {"_error": True}
            except Exception:
                st.session_state.weather_data = {"_error": True}

    w = st.session_state.weather_data'''

print('FIX2 found:', old2 in content)
content = content.replace(old2, new2)

# ── FIX 2b: Show error state in weather widget ──
old2b = '''    else:
        st.info(f"⏳ Weather loading for {st.session_state.farmer_location}... (Backend must be running)")'''

new2b = '''    elif w and w.get("_error"):
        st.warning(f"⚠️ Could not load weather for **{st.session_state.farmer_location}**. Check backend is running.")
        if st.button("🔄 Retry Weather", key="retry_weather_header"):
            st.session_state.weather_data = None
            st.rerun()
    else:
        st.info(f"⏳ Weather loading for {st.session_state.farmer_location}...")'''

print('FIX2b found:', old2b in content)
content = content.replace(old2b, new2b)

# ── FIX 3: Clear pest result when new image uploaded ──
old3 = '''    upload_col, info_col = st.columns([1, 1])
    with upload_col:
        img = st.file_uploader(
            "Upload crop photo (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        if img:
            st.image(img, use_column_width=True, caption="Uploaded crop image")'''

new3 = '''    upload_col, info_col = st.columns([1, 1])
    with upload_col:
        img = st.file_uploader(
            "Upload crop photo (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        if img:
            # Clear stale result when a new image is uploaded
            img_key = f"{img.name}_{img.size}"
            if st.session_state.get("_last_pest_img") != img_key:
                st.session_state.pop("pest_result", None)
                st.session_state["_last_pest_img"] = img_key
            st.image(img, use_column_width=True, caption="Uploaded crop image")'''

print('FIX3 found:', old3 in content)
content = content.replace(old3, new3)

# ── FIX 4: Language hint — only append for non-advisory messages ──
old4 = '''    if user_input:
        # Append language hint if non-English
        message_with_lang = user_input
        if lang_code != "en":
            message_with_lang = f"{user_input}\\n[Please respond in {st.session_state.language}]"'''

new4 = '''    if user_input:
        # Append language hint only for short user messages, not long advisory prompts
        message_with_lang = user_input
        if lang_code != "en" and len(user_input) < 500:
            message_with_lang = f"{user_input}\\n[Please respond in {st.session_state.language}]"'''

print('FIX4 found:', old4 in content)
content = content.replace(old4, new4)

# ── FIX 5: agri-card divs — replace with st.container approach (remove broken HTML wrappers in crop plan) ──
old5 = '''                # Details in 3 columns
                d1, d2, d3 = st.columns(3)
                with d1:
                    st.markdown('<div class="agri-card">', unsafe_allow_html=True)
                    st.markdown("**🌤️ Weather Summary**")
                    st.write(data.get("weather_summary", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)
                with d2:
                    st.markdown('<div class="agri-card">', unsafe_allow_html=True)
                    st.markdown("**🧪 Soil Advice**")
                    st.write(data.get("soil_advice", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)
                with d3:
                    st.markdown('<div class="agri-card">', unsafe_allow_html=True)
                    st.markdown("**🌱 Planting Tips**")
                    st.write(data.get("planting_tips", "—"))
                    st.markdown('</div>', unsafe_allow_html=True)'''

new5 = '''                # Details in 3 columns
                d1, d2, d3 = st.columns(3)
                with d1:
                    with st.container(border=True):
                        st.markdown("**🌤️ Weather Summary**")
                        st.write(data.get("weather_summary", "—"))
                with d2:
                    with st.container(border=True):
                        st.markdown("**🧪 Soil Advice**")
                        st.write(data.get("soil_advice", "—"))
                with d3:
                    with st.container(border=True):
                        st.markdown("**🌱 Planting Tips**")
                        st.markdown(data.get("planting_tips", "—"))'''

print('FIX5 found:', old5 in content)
content = content.replace(old5, new5)

# ── FIX 6: Schemes summary — use st.info instead of broken agri-card HTML ──
old6 = '''        if data.get("summary"):
            st.markdown(f'<div class="agri-card">{data["summary"]}</div>', unsafe_allow_html=True)'''

new6 = '''        if data.get("summary"):
            st.info(data["summary"])'''

print('FIX6 found:', old6 in content)
content = content.replace(old6, new6)

# ── FIX 7: Voice prefill — use st.session_state flag + rerun to ensure it fires ──
old7 = '''    prefill = st.session_state.pop("prefill_chat", "")
    lang_code = lang_hint.get(st.session_state.language, "en")
    
    user_input = st.chat_input("Type in English, Hindi, Marathi, or any language...") or (prefill if prefill else None)'''

new7 = '''    prefill = st.session_state.pop("prefill_chat", "")
    lang_code = lang_hint.get(st.session_state.language, "en")

    typed_input = st.chat_input("Type in English, Hindi, Marathi, or any language...")
    user_input = typed_input or (prefill if prefill else None)'''

print('FIX7 found:', old7 in content)
content = content.replace(old7, new7)

# ── FIX 8: Currency — fix Rs. to ₹ in market tab ──
old8a = "                c1.metric(\"Current\", f\"Rs.{data.get('current_price_per_kg', 0)}/kg\")"
new8a = "                c1.metric(\"Current\", f\"₹{data.get('current_price_per_kg', 0)}/kg\")"
old8b = "                c2.metric(\"7-Day\", f\"Rs.{data.get('predicted_price_7d', 0)}/kg\")"
new8b = "                c2.metric(\"7-Day\", f\"₹{data.get('predicted_price_7d', 0)}/kg\")"
old8c = "                c3.metric(\"30-Day\", f\"Rs.{data.get('predicted_price_30d', 0)}/kg\")"
new8c = "                c3.metric(\"30-Day\", f\"₹{data.get('predicted_price_30d', 0)}/kg\")"
# These are in the simple market tab (not the styled one) - check if they exist
print('FIX8a found:', old8a in content)
print('FIX8b found:', old8b in content)
content = content.replace(old8a, new8a).replace(old8b, new8b).replace(old8c, new8c)

# ── FIX 9: Weather tab — show spinner when loading from tab ──
old9 = '''    w = st.session_state.get("weather_data")
    if not w:
        wloc = st.text_input("Enter location", value=st.session_state.farmer_location, key="weather_loc_input")
        if st.button("🔍 Load Weather", type="primary"):
            with st.spinner("Fetching weather..."):
                try:
                    wr = requests.get(f"{API}/weather", params={"location": wloc}, timeout=10)
                    if wr.status_code == 200:
                        st.session_state.weather_data = wr.json()
                        st.session_state.farmer_location = wloc
                        audit("Weather Fetch", f"Location: {wloc}", source="online")
                        st.rerun()
                except Exception as e:
                    st.error(f"Weather fetch failed: {e}")'''

new9 = '''    w = st.session_state.get("weather_data")
    if not w or w.get("_error"):
        wloc = st.text_input("Enter location", value=st.session_state.farmer_location, key="weather_loc_input")
        if st.button("🔍 Load Weather", type="primary"):
            with st.spinner("Fetching live weather data..."):
                try:
                    wr = requests.get(f"{API}/weather", params={"location": wloc}, timeout=15)
                    if wr.status_code == 200:
                        st.session_state.weather_data = wr.json()
                        st.session_state.farmer_location = wloc
                        audit("Weather Fetch", f"Location: {wloc}", source="online" if not wr.json().get("offline") else "offline")
                        st.rerun()
                    else:
                        st.error(f"Could not fetch weather for '{wloc}'. Try a different city name.")
                except Exception as e:
                    st.error(f"Weather fetch failed: {e}. Make sure backend is running.")'''

print('FIX9 found:', old9 in content)
content = content.replace(old9, new9)

# ── FIX 10: Audit export — move download button outside the if-button block so it renders ──
old10 = '''        if st.button("📥 Export JSON", key="export_audit"):
            audit_json = json.dumps(log, indent=2)
            st.download_button(
                "⬇️ Download audit.json",
                data=audit_json,
                file_name=f"agrigenaai_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )'''

new10 = '''        audit_json = json.dumps(log, indent=2, ensure_ascii=False)
        st.download_button(
            "📥 Export audit.json",
            data=audit_json,
            file_name=f"agrigenaai_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            key="export_audit"
        )'''

print('FIX10 found:', old10 in content)
content = content.replace(old10, new10)

open('frontend/app.py', 'w', encoding='utf-8').write(content)
print('All fixes applied. Size:', len(content))
