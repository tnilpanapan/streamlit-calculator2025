import streamlit as st

st.title("Calculator v2 – input ว่างได้")

if "confirmed_value" not in st.session_state:
    st.session_state.confirmed_value = None

number_str = st.text_input(
    "กรอกตัวเลข",
    value="",              # 🔥 ว่างจริง
    placeholder="พิมพ์ตัวเลข…",
    key="current_value"
)

col1, col2 = st.columns(2)

with col1:
    if st.button("="):
        try:
            st.session_state.confirmed_value = float(number_str)
        except:
            st.session_state.confirmed_value = None

with col2:
    if st.button("C"):
        st.session_state.current_value = ""
        st.session_state.confirmed_value = None

st.write("---")

x = st.session_state.confirmed_value
if x is not None:
    st.success(f"ผลลัพธ์ = {x * 2}")
else:
    st.info("ยังไม่ได้กด = หรือค่าผิดรูปแบบ")
