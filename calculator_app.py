import streamlit as st

st.set_page_config(page_title="Calculator 3 Inputs", layout="centered")
st.title("3-Phases--Calculator")

# ---------- ฟังก์ชันคำนวณ ----------
def compute_new_V(V_str: str, PC_str: str, D_str: str):
  V = float(V_str)
  PC = float(PC_str)
  if D_str.lower() == "d":
      PC = PC/1.732
  else:
      V = V/1.732

  return V, PC

def compute_PM_T_TX(B_str: str, DI_str: str, L_str: str, P_str: str, PA_str: str):
  B = float(B_str)
  DI = float(DI_str)
  L = float(L_str)
  P = float(P_str)
  PA = float(PA_str)
  PM = B*3.14159*DI*L/P/(10**6)
  T = V/(4.44*50*PM)
  TX = T/P*PA

  return PM, T, TX

def compute_Area(CI_str: str, DA_str: str, J_str: str):
  CI = float(CI_str)
  DA = float(DA_str)
  J = int(J_str)
  A = 0
  for i in range(J):
    AI = CI*3.14159*(DA**2)/4.0
    A = A + AI
  return A

def compute_other(A_adj, V_adj,PC_adj,P: str,S: str, DI: str,L: str,B: str,PA :str, 
                  TX_adj,T_adj):
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
  return CON_AREA_A, CS, CJ, SP, SM, SN, T, TX, TC, TURN_SLOT


# ---------- ส่วนรับค่า input ----------
V = st.text_input("PRI VOL V", value="", placeholder="พิมพ์ตัวเลข…")
PC = st.text_input("PRI CUR I", value="", placeholder="พิมพ์ตัวเลข…")
YorD = st.text_input("INPUT VOL Y OR D", value="", placeholder='(Y/D)? หรือ (y/d)?')
DI = st.text_input("DIAMETER D MM.", value="", placeholder="พิมพ์ตัวเลข…")
L = st.text_input("CORE LENGTH L MM.", value="", placeholder="พิมพ์ตัวเลข…")
P = st.text_input("NO OF POLE P", value="", placeholder="พิมพ์ตัวเลขจำนวนเต็ม")
S = st.text_input("NO OF SLOT S", value="", placeholder="พิมพ์ตัวเลขจำนวนเต็ม")

PA = st.text_input("NO OF PARALLEL PA", value="", placeholder="พิมพ์ตัวเลขจำนวนเต็ม")
B = st.text_input("FLUX DEN B", value="", placeholder="พิมพ์ตัวเลข…")

J = st.text_input("DIFF CON SIZE IN //", value="", placeholder="พิมพ์ตัวเลขจำนวนเต็ม")
#For J
CI = st.text_input("NO OF CONDUCTOR", value="", placeholder="พิมพ์ตัวเลขจำนวนเต็ม")
DA = st.text_input("SIZE NO OF DIAMETER", value="", placeholder="พิมพ์ตัวเลข…")


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
        PM_adj, T_adj, TX_adj = compute_PM_T_TX(B, DI, L, P, PA)
        valid = True
    except ValueError:
        valid = False

    if not valid:
        st.error("F2 กรุณากรอก B, DI, L, P, PA เป็นตัวเลข ให้ถูกต้อง")
    # ฟังก์ชั่นสาม loop J 
    try:
        A_adj = compute_Area(CI, DA, J)
        valid = True
    except ValueError:
        valid = False

    if not valid:
        st.error("F3 กรุณากรอก CI, DA, J เป็นตัวเลข ให้ถูกต้อง")\
      
    # ฟังก์ชั่นสี่ ค่าที่เหลือ CON_AREA_A, CS, CJ, SP, SM, SN, T, TX, TC, TURN_SLOT    
    try: 
        CON_AREA_A, CS_adj, CJ_adj, SP_adj, SM_adj, SN_adj,T_adj,TX_adj,TC_adj,TURN_SLOT = 
        compute_other(A_adj, V_adj,PC_adj,P,S, DI,L,B,PA,TX_adj,T_adj) 
                                                  
        valid = True
    except ValueError:
        valid = False

    if not valid:
        st.error("F4 กรุณากรอก ค่าต่างๆ เป็นตัวเลข ให้ถูกต้อง")
    




    if valid:
        # แสดง output
        st.success(f"V = x + y = {V_adj}")
        st.info(f"PC = x - y = {PC_adj}")

        # ตรวจสอบทีละขั้นตอนที่คำนวณค่า
        st.write(f"ค่า V หลัง Y OR D บรรทัด 10 = {V_adj}")
        st.write(f"ค่า PC หลัง Y OR D บรรทัด 10 = {PC_adj}")

