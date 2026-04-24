import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

# 1. 열쇠로 구글 시트 열기
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Workout_Data").sheet1 # 아까 만든 시트 이름

st.title("💪 나의 운동 일기장")

# 2. 입력 칸 만들기 (유치원생도 할 수 있게!)
with st.form("input_form"):
    ex_name = st.selectbox("어떤 운동을 했나요?", ["레그프레스", "체스트프레스", "렛풀다운", "런닝머신"])
    weight = st.number_input("무게 (kg)", min_value=0, step=5)
    reps = st.number_input("몇 번 했나요? (회)", min_value=0, step=1)
    sets = st.number_input("몇 세트 했나요?", min_value=0, step=1)
    
    submit = st.form_submit_button("기록 저장하기!")

# 3. 저장 버튼을 누르면 일어나는 마법
if submit:
    now = datetime.now().strftime("%Y-%m-%d")
    sheet.append_row([now, ex_name, weight, reps, sets])
    st.success("참 잘했어요! 시트에 저장되었습니다.")

# 4. 저장된 데이터 보여주기
st.subheader("📊 나의 최근 운동 기록")
data = sheet.get_all_records()
df = pd.DataFrame(data)
st.dataframe(df.tail(10)) # 마지막 10개만 보여주기