import streamlit as st

st.set_page_config(
    page_title="Simple Calculator v2",
    page_icon="🧮",
    layout="centered",
)

st.title("🧮 Simple Calculator (v2)")
st.write("เวอร์ชันแป้นกดตัวเลข 0–9, '.' และ '='")

# ---------- initial state ----------
if "num1_str" not in st.session_state:
    st.session_state.num1_str = ""
if "num2_str" not in st.session_state:
    st.session_state.num2_str = ""
if "result" not in st.session_state:
    st.session_state.result = None

# ---------- helper ----------
def press_key(key: str):
    target = st.session_state.target_input  # "Number 1" หรือ "Number 2"

    if key == "C":
        # ล้างค่าทุกอย่าง
        st.session_state.num1_str = ""
        st.session_state.num2_str = ""
        st.session_state.result = None
        return

    if key == "=":
        # คำนวณผลลัพธ์
        try:
            num1 = float(st.session_state.num1_str or "0")
            num2 = float(st.session_state.num2_str or "0")
        except ValueError:
            st.session_state.result = "Input ไม่ถูกต้อง"
            return

        op = st.session_state.operation

        if op == "+":
            st.session_state.result = num1 + num2
        elif op == "-":
            st.session_state.result = num1 - num2
        elif op == "*":
            st.session_state.result = num1 * num2
        elif op == "/":
            if num2 == 0:
                st.session_state.result = "หาร 0 ไม่ได้"
            else:
                st.session_state.result = num1 / num2
        return

    # ถ้าเป็นตัวเลขหรือจุด → ต่อ string
    if target == "Number 1":
        if key == "." and "." in st.session_state.num1_str:
            return  # ไม่ให้มีจุดสองอัน
        st.session_state.num1_str += key
    else:  # Number 2
        if key == "." and "." in st.session_state.num2_str:
            return
        st.session_state.num2_str += key


# ---------- เลือกว่าจะกรอกช่องไหน ----------
st.subheader("Inputs")

col_disp1, col_disp2 = st.columns(2)

with col_disp1:
    st.write("**Number 1**")
    st.code(st.session_state.num1_str or " ", language="text")

with col_disp2:
    st.write("**Number 2**")
    st.code(st.session_state.num2_str or " ", language="text")

st.radio(
    "กำลังกรอกช่อง:",
    ["Number 1", "Number 2"],
    key="target_input",
    horizontal=True,
)

# ---------- เลือก operation ----------
operation = st.selectbox(
    "Operation",
    ["+", "-", "*", "/"],
    key="operation",
)

st.markdown("---")

# ---------- keypad ----------
st.subheader("Keypad")

rows = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["0", ".", "="],
]

for row in rows:
    c1, c2, c3 = st.columns(3)
    for key, col in zip(row, (c1, c2, c3)):
        with col:
            if st.button(key, use_container_width=True):
                press_key(key)

# ปุ่ม Clear แยกไว้ด้านล่าง
if st.button("Clear (C)", type="secondary"):
    press_key("C")

st.markdown("---")

# ---------- แสดงผลลัพธ์ ----------
if st.session_state.result is not None:
    st.success(
        f"Result: {st.session_state.num1_str or '0'} "
        f"{st.session_state.operation} "
        f"{st.session_state.num2_str or '0'} "
        f"= {st.session_state.result}"
    )
