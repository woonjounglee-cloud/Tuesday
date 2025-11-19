"""
Tuesday - Excel Portfolio Management Web App
Streamlit 기반 웹 애플리케이션
"""
import streamlit as st
import pandas as pd
import os
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="Tuesday - Portfolio Manager",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 스타일링
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 데이터 디렉토리 확인
DB_DIR = Path("db")
DB_DIR.mkdir(exist_ok=True)

def main():
    """메인 함수"""

    # 헤더
    st.markdown('<h1 class="main-header">📊 Tuesday</h1>', unsafe_allow_html=True)
    st.markdown("### Excel Portfolio Management System")

    # 사이드바 - 탭 선택
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/1f77b4/ffffff?text=Tuesday", use_column_width=True)
        st.markdown("---")

        main_tab = st.radio(
            "Main Category",
            ["Home", "WJ", "MG"],
            key="main_tab"
        )

        # 서브 탭 선택
        if main_tab == "Home":
            sub_tab = st.radio("Sub Category", ["IRP"])
        elif main_tab == "WJ":
            sub_tab = st.radio("Sub Category", ["ISA", "주식"])
        else:  # MG
            sub_tab = st.radio("Sub Category", ["IRP", "개인연금"])

        st.markdown("---")
        st.info("💡 Tip: 브라우저에서 실행되는 웹 앱입니다!")

    # 메인 컨텐츠
    if main_tab == "Home" and sub_tab == "IRP":
        show_home_irp()
    else:
        st.info(f"🚧 {main_tab} - {sub_tab} 탭은 준비 중입니다.")


def show_home_irp():
    """Home - IRP 탭 표시"""
    from pages import irp_page
    irp_page.show()


if __name__ == "__main__":
    main()
