import streamlit as st

st.set_page_config(page_title="Calculator v2", layout="centered")

st.title("Calculator v2 – iPhone style keypad")

# ---------- Session state ----------
if "display" not in st.session_state:
    st.session_state.display = ""
if "confirmed_value" not in st.session_state:
    st.session_state.confirmed_value = None


# ---------- Helper ----------
def press(key: str):
    # กดตัวเลข / จุดทศนิยม
    if key in "0123456789":
        st.session_state.display += key

    elif key == ".":
        # ไม่ให้มีจุดซ้ำในตัวเลขเดียว
        if "." not in st.session_state.display:
            if st.session_state.display == "":
                # เริ่มด้วย 0.
                st.session_state.display = "0."
            else:
                st.session_state.display += "."

    elif key == "C":
        st.session_state.display = ""
        st.session_state.confirmed_value = None

    elif key == "⌫":
        st.session_state.display = st.session_state.display[:-1]

    elif key == "=":
        # กดเท่ากับ = แปลงเป็นตัวเลข 1 ค่า
        text = st.session_state.display
        if text == "" or text == ".":
            st.session_state.confirmed_value = None
        else:
            try:
                st.session_state.confirmed_value = float(text)
            except ValueError:
                st.session_state.confirmed_value = None


# ---------- Custom CSS ให้ปุ่มดูคล้าย iPhone ----------
st.markdown(
    """
    <style>
    .keypad-btn > button {
        width: 100%;
        height: 64px;
        font-size: 24px;
        border-radius: 32px;
    }
    .keypad-equal > button {
        font-weight: 700;
    }
    .keypad-func > button {
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Display ----------
st.text_input(
    "ค่าที่กำลังกรอก",
    value=st.session_state.display if st.session_state.display != "" else "0",
    disabled=True,
)

if st.session_state.confirmed_value is not None:
    st.success(f"ค่าที่กด = {st.session_state.confirmed_value:g}")

st.write("---")

# ---------- Keypad layout ----------
# แถว 1: 1 2 3
row1 = st.columns(3)
with row1[0]:
    if st.button("1", key="k1", use_container_width=True):
        press("1")
with row1[1]:
    if st.button("2", key="k2", use_container_width=True):
        press("2")
with row1[2]:
    if st.button("3", key="k3", use_container_width=True):
        press("3")

# แถว 2: 4 5 6
row2 = st.columns(3)
with row2[0]:
    if st.button("4", key="k4", use_container_width=True):
        press("4")
with row2[1]:
    if st.button("5", key="k5", use_container_width=True):
        press("5")
with row2[2]:
    if st.button("6", key="k6", use_container_width=True):
        press("6")

# แถว 3: 7 8 9
row3 = st.columns(3)
with row3[0]:
    if st.button("7", key="k7", use_container_width=True):
        press("7")
with row3[1]:
    if st.button("8", key="k8", use_container_width=True):
        press("8")
with row3[2]:
    if st.button("9", key="k9", use_container_width=True):
        press("9")

# แถว 4: . 0 =
row4 = st.columns(3)
with row4[0]:
    if st.button(".", key="kdot", use_container_width=True):
        press(".")
with row4[1]:
    if st.button("0", key="k0", use_container_width=True):
        press("0")
with row4[2]:
    if st.button("=", key="keq", use_container_width=True):
        press("=")

# แถว 5: C  ⌫  (ช่องว่าง)
row5 = st.columns(3)
with row5[0]:
    if st.button("C", key="kC", use_container_width=True):
        press("C")
with row5[1]:
    if st.button("⌫", key="kback", use_container_width=True):
        press("⌫")
# ช่องขวาสุดปล่อยว่างไว้เฉย ๆ
