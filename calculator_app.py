import streamlit as st

st.set_page_config(
    page_title="Simple Calculator",
    page_icon="🧮",
    layout="centered",
)

st.title("🧮 Simple Calculator")
st.write("ทดลองใช้งานเครื่องคิดเลขบน Streamlit (รองรับ + − × ÷)")

num1 = st.number_input("Number 1", value=0.0, format="%.6f")
num2 = st.number_input("Number 2", value=0.0, format="%.6f")

operation = st.selectbox("Operation", ["+", "-", "*", "/"])

if st.button("Calculate"):
    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "/":
        if num2 == 0:
            st.error("หารด้วยศูนย์ไม่ได้ครับ")
            result = None
        else:
            result = num1 / num2

    if result is not None:
        st.success(f"Result: {num1} {operation} {num2} = {result}")
