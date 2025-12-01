import streamlit as st

st.set_page_config(page_title="Calculator v2 (Keyboard)", layout="centered")

st.title("Calculator v2 – พิมพ์ด้วยคีย์บอร์ด")

# ---------- Session state ----------
if "confirmed_value" not in st.session_state:
    st.session_state.confirmed_value = None

# ---------- Input หลัก: ใช้คีย์บอร์ด / keyboard บน iPhone ----------
number = st.number_input(
    "กรอกตัวเลขที่ต้องการ",   # label
    value=0.0,                  # ค่าเริ่มต้น
    step=1.0,                   # เวลากดลูกศรขึ้นลง
    format="%.4f",              # แสดงทศนิยม 4 ตำแหน่ง (ปรับได้)
    key="current_value",
)

# ---------- ปุ่มกดเหมือนเครื่องคิดเลข ----------
col1, col2 = st.columns(2)

with col1:
    if st.button("=", use_container_width=True):
        st.session_state.confirmed_value = float(number)

with col2:
    if st.button("C", use_container_width=True):
        st.session_state.current_value = 0.0
        st.session_state.confirmed_value = None

st.write("---")

# แสดงผลลัพธ์ที่ยืนยันแล้ว
if st.session_state.confirmed_value is not None:
    st.success(f"ค่าที่กด = {st.session_state.confirmed_value:g}")
else:
    st.info("ยังไม่ได้กด = ยืนยันค่า")
# --- ใช้ค่าไปคำนวณต่อ (ใส่ตรงนี้) ---
x = st.session_state.confirmed_value  # ค่าที่ user ยืนยันด้วยการกด =
if x is not None:
    result = x * 2  # ตัวอย่าง
    st.write("ผลลัพธ์ =", result)
else:
    st.info("ยังไม่ได้กด = เพื่อยืนยันค่า")
