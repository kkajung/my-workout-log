import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import json

# [수정된 영역] 파일 대신 Secrets에서 열쇠를 가져옵니다.
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

if "gcp_service_account" in st.secrets:
    # Secrets에 저장한 데이터를 읽어옵니다.
    creds_dict = json.loads(st.secrets["gcp_service_account"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
else:
    st.error("Streamlit Cloud의 Secrets 설정에 'gcp_service_account'가 없습니다!")
    st.stop()

# 구글 시트 열기
sheet = client.open("Workout_Data").sheet1 

# --- 아래는 기존과 동일한 UI 및 로직입니다 ---

st.title("💪 나의 운동 일기장")

with st.form("input_form"):
    ex_name = st.selectbox("어떤 운동을 했나요?", ["레그프레스", "체스트프레스", "렛풀다운", "런닝머신"])
    weight = st.number_input("무게 (kg)", min_value=0, step=5)
    reps = st.number_input("몇 번 했나요? (회)", min_value=0, step=1)
    sets = st.number_input("몇 세트 했나요?", min_value=0, step=1)
    
    submit = st.form_submit_button("기록 저장하기!")

if submit:
    now = datetime.now().strftime("%Y-%m-%d")
    sheet.append_row([now, ex_name, weight, reps, sets])
    st.success("참 잘했어요! 시트에 저장되었습니다.")

st.subheader("📊 나의 최근 운동 기록")
try:
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    st.dataframe(df.tail(10)) 
except:
    st.info("아직 저장된 기록이 없습니다.")