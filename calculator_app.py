import streamlit as st
from datetime import datetime


st.markdown("""
<style>
/* ครอบ alert ทุกชนิด (info/success/warning/error) */
div[data-testid="stAlert"] p,
div[data-testid="stAlert"] li,
div[data-testid="stAlert"] span {
    font-size: 28px !important;
    font-weight: 600 !important;
    line-height: 1.3 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* =====================================================
   TEXT INPUT — FIX label เล็กกว่า placeholder
   ===================================================== */

/* label ชั้นนอก */
div.stTextInput label {
    line-height: 1.3 !important;
}

/* ตัวข้อความจริงใน label */
div.stTextInput label > div {
    font-size: 20px !important;
    font-weight: 600 !important;
}

/* input value */
div.stTextInput input {
    font-size: 20px !important;
    padding: 8px 12px !important;
}

/* placeholder */
div.stTextInput input::placeholder {
    font-size: 20px !important;
    opacity: 0.6;
}

</style>
""", unsafe_allow_html=True)




st.set_page_config(page_title="Calculator 3 Inputs", layout="centered")
st.title("3-Phase M-Calculator")

# ---------- ฟังก์ชันคำนวณ ----------
def compute_new_V(V_str: str, PC_str: str, YorD: str):
  V = float(V_str)
  PC = float(PC_str)
  if YorD.lower() == "d":
      PC = PC/1.732
  else:
      V = V/1.732

  return V, PC

def compute_PM_T_TX(V_str: str, B_str: str, DI_str: str, L_str: str, P_str: str, PA_str: str):
  V = float(V_str)
  B = float(B_str)
  DI = float(DI_str)
  L = float(L_str)
  P = float(P_str)
  PA = float(PA_str)
  PM = B*3.14159*DI*L/P/(10**6)
  T = V/(4.44*50*PM)
  TX = T/P*PA

  return PM, T, TX

def compute_Area(CI: list, DA: list, J_str: str):
  J = int(J_str)
  A = 0
  for i in range(J):
    AI = CI[i]*3.14159*(DA[i]**2)/4.0
    A = A + AI
  return A

def compute_other(A_adj, V_adj,PC_adj,P,S, DI,L,B,PA,TX_adj,T_adj):
  A = A_adj
  V = V_adj
  PC = PC_adj
  TX = TX_adj
  T = T_adj
  P = float(P)
  S = float(S)
  DI = float(DI)
  L = float(L)
  B = float(B)
  PA = float(PA)
  CS = 0.4*(10**6)*V*P/(S*DI*L*B*50)
  CJ = PC/(A*PA)
  SP = S/P
  SM = S/P/3
  SN = 1+SP
  TC = TX/SM
  CON_AREA_A = A*PA
  TURN_SLOT = CS*PA
  return CON_AREA_A, CS, CJ, SP, SM, SN, TC, TURN_SLOT

def parse_list(text, expected_n=None, dtype=float): #ถ้ามีสายอักขระมาเป็นชุด คั่นด้วย คอมม่า หรือ ช่องว่าง จะ return เป็น list ได้อย่างไร
    if text is None:
        return []

    # ให้รองรับการใส่ comma หรือ space คั่น
    text = text.replace(",", " ")
    tokens = [t.strip() for t in text.split() if t.strip() != ""]

    if len(tokens) == 0:
        return []

    try:
        values = [dtype(t) for t in tokens]
    except:
        raise ValueError("กรุณาใส่ตัวเลขเท่านั้น (คั่นด้วย เว้นวรรค หรือ comma)")

    if expected_n is not None and len(values) != expected_n:
        raise ValueError(
            f"จำนวนค่าที่ใส่ ({len(values)}) ไม่ตรงกับ J = {expected_n}"
        )

    return values



# ---------- ส่วนรับค่า input ----------
V = st.text_input("1.PRI VOL (V)", value="", placeholder="ค่า V")
PC = st.text_input("2.PRI CUR I (PC)", value="", placeholder="ค่า PC")
YorD = st.text_input("3.INPUT VOL Y OR D", value="", placeholder="เลือก Y/D (ตามโปรแกรมเดิม)")
DI = st.text_input("4.DIAMETER D MM. (DI)", value="", placeholder="ค่า DI")
L = st.text_input("5.CORE LENGTH L MM. (L)", value="", placeholder="ค่า L")
P = st.text_input("6.NO OF POLE (P)", value="", placeholder="ค่า P")
S = st.text_input("7.NO OF SLOT (S)", value="", placeholder="ค่า S")

PA = st.text_input("8.NO OF PARALLEL (PA)", value="", placeholder="ค่า PA")
B = st.text_input("9.FLUX DEN (B)", value="", placeholder="ค่า B")

J = st.text_input("10.DIFF CON SIZE IN (J)",  value="", placeholder="ค่า J เช่น 1, 2, 3 ...")
#For J
CI = st.text_input("11.NO OF CONDUCTOR (CI) \n กรอกตัวเลข 1 ค่า หรือหลายค่า คั่นด้วยเว้นวรรค (*จำนวน = J) ", value="", placeholder="เช่น (0.8x1) (0.85x1) กรอก 1  1 ")
DA = st.text_input("12.SIZE NO OF DIAMETER (DA) \n กรอกตัวเลข 1 ค่า หรือหลายค่า คั่นด้วยเว้นวรรค (*จำนวน = J) ", value="", placeholder="เช่น (0.8x1) (0.85x1) กรอก .8  0.85 ")


# ปุ่มเท่ากับ
calculate = st.button(" = ", type="primary")

st.write("---")

# ---------- เมื่อกดปุ่ม = ----------
if calculate:
    # ฟังก์ชั่นแรก V,PC,(Y or D)
    try:
        V_adj, PC_adj = compute_new_V(V, PC, YorD)
        valid = True
    except ValueError:
        valid = False

    if not valid:
        st.error("F1 กรุณากรอก V และ PC เป็นตัวเลข และ กรอก (Y/D)? ให้ถูกต้อง")
    # ฟังก์ชั่นสอง PM,T,TX
    try:
        PM_adj, T_adj, TX_adj = compute_PM_T_TX(V_adj, B, DI, L, P, PA)
        valid = True
    except ValueError:
        valid = False

    if not valid:
        st.error("F2 กรุณากรอก B, DI, L, P, PA เป็นตัวเลข ให้ถูกต้อง")
    # ฟังก์ชั่นสาม loop J
    if J.strip() == "":
      st.error("กรุณากรอกค่า J ก่อน")
      st.stop()
    try:
        J_int = int(J)
    except:
        st.error("J error: กรุณากรอก J เป็นจำนวนเต็ม เช่น 1, 2, 3 ...")
        st.stop()
    CI_list = parse_list(CI, expected_n=J_int)
    DA_list = parse_list(DA, expected_n=J_int)
    if CI_list is None:
        st.error("รูปแบบข้อมูล CI ไม่ถูกต้อง หรือค่าจำนวนไม่ตรง J")
        st.stop()
    if DA_list is None:
        st.error("รูปแบบข้อมูล DA ไม่ถูกต้อง หรือค่าจำนวนไม่ตรง J")
        st.stop()

    try:
        A_adj = compute_Area(CI_list, DA_list, J)
        valid = True
    except ValueError:
        valid = False

    if not valid:
        st.error("F3 กรุณากรอก J เป็นตัวเลข ให้ถูกต้อง")
        st.stop()

    # ฟังก์ชั่นสี่ ค่าที่เหลือ CON_AREA_A, CS, CJ, SP, SM, SN, TC, TURN_SLOT
    try:
        CON_AREA_A, CS_out, CJ_out, SP_out, SM_out, SN_out,TC_out,TURN_SLOT = compute_other(A_adj, V_adj,PC_adj,P,S, DI,L,B,PA,TX_adj,T_adj)

        valid = True
    except ValueError:
        valid = False

    if not valid:
        st.error("F4 กรุณากรอก ค่าต่างๆ เป็นตัวเลข ให้ถูกต้อง")
        st.stop()


    if valid:
        # แสดง output
        st.write("กรุณาแจ้งตัวเลข บรรทัดที่คำนวณผิดพลาด")
        st.success(f"Current Density =   {CJ_out}  \n Amp/Sq.mm.")
        # st.success(f"""
        # Current Density =   {CJ_out}
        #            Amp/Sq.mm.
        #            """)
        st.info(f"TURN/SLOT  =  {TURN_SLOT}")

        # ตรวจสอบทีละขั้นตอนที่คำนวณค่า
        st.write("ตรวจคำตอบทีละขั้นตอน (ลบออก/ซ่อน เมื่อ Logic ถูกต้องแล้ว)")
        st.write("(ลบออก/ซ่อน เมื่อ Logic ถูกต้องแล้ว)")
        st.write(f"1. ค่า V หลังเงื่อนไข Y OR D =  {V_adj}")
        st.write(f"2. ค่า PC หลังเงื่อน Y OR D =  {PC_adj}")
        st.write(f"3. ค่า PM =  {PM_adj}")
        st.write(f"4. ค่า T =  {T_adj}")
        st.write(f"5. ค่า TX =  {TX_adj}")
        st.write(f"6. ค่า A หลัง loop J =  {A_adj}")
        st.write(f"7. ค่า  CS =  {CS_out}")
        st.write(f"8. ค่า CON AREA A =  {CON_AREA_A}")
        st.write(f"9. ค่า  CJ =  {CJ_out}")
        st.write(f"10. CUR DEN =   {CJ_out}   A/SQ.MM.")
        st.write(f"11. SLOT/POLE  SP =  {SP_out}")
        st.write(f"12. SLOT/POLE/PHASE  SM =  {SM_out}")
        st.write(f"13. SN =  {SN_out}")
        st.write(f"14. COIL SPAN =  1 -  {SN_out}")
        st.write(f"15. TURN/PHASE  T =  {T_adj}")
        st.write(f"16. TURN/POLE  TX =  {TX_adj}")
        st.write(f"17. TURN/COIL  TC =  {TC_out}")
        st.write(f"18. TURN/SLOT  CS*PA =  {TURN_SLOT}")





