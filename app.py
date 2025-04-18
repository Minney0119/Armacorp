import streamlit as st
import pandas as pd

st.set_page_config(page_title="견적서 뷰어", layout="wide")
st.title("📋 벤더 견적서 관리 프로그램")

uploaded_file = st.file_uploader("📤 견적서 Excel 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    try:
        excel_file = pd.ExcelFile(uploaded_file)
        sheet = excel_file.sheet_names[0]
        df = excel_file.parse(sheet, skiprows=7)
        
        df = df[df["No."].notna()]
        df = df.dropna(axis=1, how='all')

        st.success("✅ 견적서가 성공적으로 불러와졌습니다!")
        st.dataframe(df, use_container_width=True)

        with st.expander("🔍 필터링 기능"):
            part_number = st.text_input("P/N (품번)으로 검색")
            if part_number:
                filtered_df = df[df["P/N"].astype(str).str.contains(part_number, case=False, na=False)]
                st.dataframe(filtered_df, use_container_width=True)
    except Exception as e:
        st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")
else:
    st.info("엑셀 파일을 업로드하면 견적서 내용이 여기에 표시됩니다.")