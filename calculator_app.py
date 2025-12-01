import streamlit as st

st.set_page_config(page_title="Calculator 3 Inputs", layout="centered")
st.title("Calculator – x, y, z + เงื่อนไข z")

# ---------- ฟังก์ชันคำนวณ ----------
def compute_results(V_str: str, PC_str: str, D_str: str):
    """
    รับ string x_str, y_str, z_str
    แปลง x_str, y_str เป็น float
    ถ้า z เป็น d หรือ D: x = x * 2
    ถ้าไม่ใช่: y = y * 10
    คืนค่า (x_หลังปรับ, y_หลังปรับ, result_1, result_2)
    """

    # แปลง x, y เป็น float (ถ้าไม่ได้จะ raise ValueError)
    V = float(V_str)
    PC = float(PC_str)

    # ปรับตามค่า z
    if D_str.lower() == "d":
        PC = PC/1.732
    else:
        V = V/1.732

    # คำนวณผลลัพธ์
    # result_1 = x + y
    # result_2 = x - y

    return V, PC


# ---------- ส่วนรับค่า input ----------
V_str = st.text_input("PRI VOL V", value="", placeholder="พิมพ์ตัวเลข…")
PC_str = st.text_input("PRI CUR I", value="", placeholder="พิมพ์ตัวเลข…")
D_str = st.text_input("INPUT VOL Y OR D", value="", placeholder='เช่น d หรือ D หรือ y หรือ Y')

# ปุ่มเท่ากับ
calculate = st.button(" = ", type="primary")

st.write("---")

# ---------- เมื่อกดปุ่ม = ----------
if calculate:
    # เช็คว่ากรอก x, y ถูกเป็นตัวเลขหรือไม่
    try:
        V_adj, PC_adj = compute_results(V_str, PC_str, D_str)
        valid = True
    except ValueError:
        valid = False

    if not valid:
        st.error("กรุณากรอก V และ PC เป็นตัวเลขให้ถูกต้อง")
    else:
        # แสดงค่า x, y หลังถูกปรับตาม z
        st.write(f"ค่า V หลังเงื่อนไข Y OR D บรรทัด 10 = {V_adj}")
        st.write(f"ค่า PC หลังเงื่อนไข Y OR D บรรทัด 10 = {PC_adj}")

        # แสดง output 2 ช่อง
        st.success(f"V = x + y = {V_adj}")
        st.info(f"PC = x - y = {PC_adj}")
