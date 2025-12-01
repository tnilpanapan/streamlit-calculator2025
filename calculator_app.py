import streamlit as st

st.set_page_config(page_title="Calculator 2 Inputs", layout="centered")
st.title("Calculator – กรอก 2 ค่า แล้วกด =")

# ----- ช่องกรอกตัวเลข (ใช้ text_input) -----
x_str = st.text_input("ตัวเลขที่ 1 (x)", value="", placeholder="พิมพ์ตัวเลข…")
y_str = st.text_input("ตัวเลขที่ 2 (y)", value="", placeholder="พิมพ์ตัวเลข…" )

# ----- เลือก operator -----
operator = st.selectbox("เลือกเครื่องหมาย", ["+", "-", "*", "/"])

# ----- ปุ่มคำนวณ (=) -----
calculate = st.button(" = ", type="primary")

# ----- เมื่อกด = เท่านั้น -----
if calculate:
    # ตรวจว่าป้อนเลขถูกต้องไหม
    try:
        x = float(x_str)
        y = float(y_str)
        valid = True
    except:
        valid = False

    if not valid:
        st.error("กรุณากรอกตัวเลขให้ถูกต้อง (เป็นค่าว่างหรือข้อความอื่นไม่ได้นะ)")
    else:
        # คำนวณตาม operator
        if operator == "+":
            result = x + y
        elif operator == "-":
            result = x - y
        elif operator == "*":
            result = x * y
        elif operator == "/":
            if y == 0:
                result = "หารด้วย 0 ไม่ได้"
            else:
                result = x / y

        st.success(f"ผลลัพธ์ = {result}")
