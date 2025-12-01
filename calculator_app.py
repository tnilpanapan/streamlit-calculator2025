import streamlit as st

st.set_page_config(page_title="Calculator 3 Inputs", layout="centered")
st.title("Calculator – x, y, z + เงื่อนไข z")

# ---------- ฟังก์ชันคำนวณ ----------
def compute_results(x_str: str, y_str: str, z_str: str):
    """
    รับ string x_str, y_str, z_str
    แปลง x_str, y_str เป็น float
    ถ้า z เป็น d หรือ D: x = x * 2
    ถ้าไม่ใช่: y = y * 10
    คืนค่า (x_หลังปรับ, y_หลังปรับ, result_1, result_2)
    """

    # แปลง x, y เป็น float (ถ้าไม่ได้จะ raise ValueError)
    x = float(x_str)
    y = float(y_str)

    # ปรับตามค่า z
    if z_str.lower() == "d":
        x = x * 2
    else:
        y = y * 10

    # คำนวณผลลัพธ์
    result_1 = x + y
    result_2 = x - y

    return x, y, result_1, result_2


# ---------- ส่วนรับค่า input ----------
x_str = st.text_input("ตัวเลขที่ 1 (x)", value="", placeholder="พิมพ์ตัวเลข…")
y_str = st.text_input("ตัวเลขที่ 2 (y)", value="", placeholder="พิมพ์ตัวเลข…")
z_str = st.text_input("ตัวแปรเงื่อนไข (z)", value="", placeholder='เช่น d หรือ D')

# ปุ่มเท่ากับ
calculate = st.button(" = ", type="primary")

st.write("---")

# ---------- เมื่อกดปุ่ม = ----------
if calculate:
    # เช็คว่ากรอก x, y ถูกเป็นตัวเลขหรือไม่
    try:
        x_adj, y_adj, result_1, result_2 = compute_results(x_str, y_str, z_str)
        valid = True
    except ValueError:
        valid = False

    if not valid:
        st.error("กรุณากรอก x และ y เป็นตัวเลขให้ถูกต้อง")
    else:
        # แสดงค่า x, y หลังถูกปรับตาม z
        st.write(f"ค่า x หลังปรับ = {x_adj}")
        st.write(f"ค่า y หลังปรับ = {y_adj}")

        # แสดง output 2 ช่อง
        st.success(f"Result_1 = x + y = {result_1}")
        st.info(f"Result_2 = x - y = {result_2}")
