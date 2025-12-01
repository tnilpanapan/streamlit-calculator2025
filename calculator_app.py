import streamlit as st

st.set_page_config(
    page_title="Simple Calculator v2.1",
    page_icon="🧮",
    layout="centered",
)

st.title("🧮 Simple Calculator (Keypad ver.)")
st.write("แป้นกด 0–9, '.' และ '=' เลือกช่องด้วยปุ่มสลับด้านล่าง")

# ---------- initial state ----------
if "num1_str" not in st.session_state:
    st.session_state.num1_str = ""
if "num2_str" not in st.session_state:
    st.session_state.num2_str = ""
if "result" not in st.session_state:
    st.session_state.result = None
if "target" not in st.session_state:
    st.session_state.target = "num1"   # num1 หรือ num2

def toggle_target():
    st.session_state.target = "num2" if st.session_state.target == "num1" else "num1"

# ---------- helper ----------
def press_key(key: str):
    # ล้าง
    if key == "C":
        st.session_state.num1_str = ""
        st.session_state.num2_str = ""
        st.session_state.result = None
        return

    # คำนวณ
    if key == "=":
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

    # ต่อ string ตามช่องที่กำลังแก้
    if st.session_state.target == "num1":
        if key == "." and "." in st.session_state.num1_str:
            return
        st.session_state.num1_str += key
    else:
        if key == "." and "." in st.session_state.num2_str:
            return
        st.session_state.num2_str += key


# ---------- แสดงค่า Number 1 / 2 ----------
st.subheader("Values")

col1, col2 = st.columns(2)
with col1:
    st.write("**Number 1**")
    st.code(st.session_state.num1_str or " ", language="text")
with col2:
    st.write("**Number 2**")
    st.code(st.session_state.num2_str or " ", language="text")

# ปุ่มสลับช่องที่กำลังแก้
target_label = "Number 1" if st.session_state.target == "num1" else "Number 2"
if st.button(f"กำลังกรอก: {target_label} (กดเพื่อสลับ)"):
    toggle_target()

# ---------- เลือก operation ----------
operation = st.selectbox(
    "Operation",
    ["+", "-", "*", "/"],
    key="operation",
)

st.markdown("---")

# ---------- keypad ----------
st.subheader("Keypad")

# หมายเหตุ: บนมือถือ columns ของ Streamlit จะ stack แนวตั้งเอง
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

# ปุ่ม Clear
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
