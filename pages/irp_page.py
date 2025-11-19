"""
Home - IRP 탭 페이지
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import os

from src.utils.excel_handler import ExcelHandler
from src.utils.calculations import Calculator


# 전역 변수
DB_PATH = Path("db/Home_IRP.xlsx")
calculator = Calculator()


def show():
    """IRP 탭 메인 함수"""

    # 파일 업로드 버튼
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("### 📁 데이터 관리")
    with col2:
        etf_file = st.file_uploader("ETF 파일 업로드", type=['xlsx', 'csv'], key="etf_upload")
    with col3:
        stock_file = st.file_uploader("주식 파일 업로드", type=['xlsx', 'csv'], key="stock_upload")

    # 파일 업로드 처리
    if etf_file:
        process_uploaded_file(etf_file)

    st.markdown("---")

    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["📈 ROI", "💰 Balance", "🎯 Portfolio"])

    with tab1:
        show_roi_section()

    with tab2:
        show_balance_section()

    with tab3:
        show_portfolio_section()


def show_roi_section():
    """ROI 섹션"""
    st.markdown("### 📈 ROI (Return on Investment)")

    # 데이터 로드
    if DB_PATH.exists():
        excel_handler = ExcelHandler(str(DB_PATH))
        excel_handler.load()
        roi_data = excel_handler.read_sheet_data('ROI')

        if roi_data and len(roi_data) > 1:
            # DataFrame 생성
            df = pd.DataFrame(roi_data[1:], columns=roi_data[0])

            # 숫자 컬럼 변환
            numeric_cols = ['초기투자금', '수량', '종가', '평가금', '수익률']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.replace('%', ''), errors='coerce')

            # 계산 수행
            if '수량' in df.columns and '종가' in df.columns:
                df['평가금'] = df.apply(lambda row: calculator.calculate_evaluation(
                    row.get('수량', 0), row.get('종가', 0)
                ), axis=1)

            if '평가금' in df.columns and '초기투자금' in df.columns:
                df['수익률'] = df.apply(lambda row: calculator.calculate_roi(
                    row.get('평가금', 0), row.get('초기투자금', 0)
                ), axis=1)

            # 편집 가능한 테이블
            st.markdown("#### 종목 현황")
            edited_df = st.data_editor(
                df,
                num_rows="dynamic",
                use_container_width=True,
                column_config={
                    "초기투자금": st.column_config.NumberColumn("초기투자금", format="₩%d"),
                    "종가": st.column_config.NumberColumn("종가", format="₩%d"),
                    "평가금": st.column_config.NumberColumn("평가금", format="₩%d"),
                    "수익률": st.column_config.NumberColumn("수익률", format="%.2f%%"),
                }
            )

            # 저장 버튼
            if st.button("💾 ROI 데이터 저장", key="save_roi"):
                save_roi_data(edited_df)
                st.success("✅ 저장되었습니다!")
                st.rerun()

            # 요약 통계
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_initial = df['초기투자금'].sum()
                st.metric("총 투자원금", f"₩{total_initial:,.0f}")
            with col2:
                total_eval = df['평가금'].sum()
                st.metric("총 평가금", f"₩{total_eval:,.0f}")
            with col3:
                total_profit = total_eval - total_initial
                st.metric("총 수익금", f"₩{total_profit:,.0f}")
            with col4:
                total_roi = calculator.calculate_roi(total_eval, total_initial)
                st.metric("총 수익률", f"{total_roi:.2f}%")

        else:
            st.info("📝 데이터가 없습니다. 샘플 데이터를 생성하거나 파일을 업로드하세요.")
            if st.button("🎲 샘플 데이터 생성"):
                create_sample_data()
                st.rerun()
    else:
        st.warning("⚠️ 데이터베이스 파일이 없습니다.")
        if st.button("🎲 샘플 데이터 생성"):
            create_sample_data()
            st.rerun()


def show_balance_section():
    """Balance 섹션"""
    st.markdown("### 💰 Balance (잔고 현황)")

    # 데이터 로드
    if DB_PATH.exists():
        excel_handler = ExcelHandler(str(DB_PATH))
        excel_handler.load()
        balance_data = excel_handler.read_sheet_data('Balance')

        if balance_data and len(balance_data) > 1:
            # DataFrame 생성
            df = pd.DataFrame(balance_data[1:], columns=balance_data[0])

            # 숫자 컬럼 변환
            numeric_cols = ['투자원금', '추가납입', '잔고', '수익률']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.replace('%', ''), errors='coerce')

            # ROI 데이터에서 자동 계산
            roi_data = excel_handler.read_sheet_data('ROI')
            if roi_data and len(roi_data) > 1:
                roi_df = pd.DataFrame(roi_data[1:], columns=roi_data[0])
                roi_df['초기투자금'] = pd.to_numeric(roi_df.get('초기투자금', 0).astype(str).str.replace(',', ''), errors='coerce')
                roi_df['평가금'] = pd.to_numeric(roi_df.get('평가금', 0).astype(str).str.replace(',', ''), errors='coerce')

                total_initial = roi_df['초기투자금'].sum()
                total_eval = roi_df['평가금'].sum()

                df['투자원금'] = total_initial
                df['잔고'] = total_eval
                df['수익률'] = df.apply(lambda row: calculator.calculate_balance_roi(
                    row.get('잔고', 0), row.get('투자원금', 0)
                ), axis=1)

            # 편집 가능한 테이블
            st.markdown("#### 월별 잔고")
            edited_df = st.data_editor(
                df,
                num_rows="dynamic",
                use_container_width=True,
                column_config={
                    "투자원금": st.column_config.NumberColumn("투자원금", format="₩%d"),
                    "추가납입": st.column_config.NumberColumn("추가납입", format="₩%d"),
                    "잔고": st.column_config.NumberColumn("잔고", format="₩%d"),
                    "수익률": st.column_config.NumberColumn("수익률", format="%.2f%%"),
                }
            )

            # 저장 버튼
            if st.button("💾 Balance 데이터 저장", key="save_balance"):
                save_balance_data(edited_df)
                st.success("✅ 저장되었습니다!")
                st.rerun()

            # 차트
            st.markdown("#### 📊 잔고 추이")
            if not df.empty and '잔고' in df.columns:
                df['기간'] = df['연도'].astype(str) + ' ' + df['월'].astype(str)

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df['기간'],
                    y=df['잔고'],
                    mode='lines+markers',
                    name='잔고',
                    line=dict(color='#1f77b4', width=3),
                    marker=dict(size=8)
                ))

                fig.update_layout(
                    xaxis_title="기간",
                    yaxis_title="잔고 (원)",
                    hovermode='x unified',
                    height=400
                )

                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📝 데이터가 없습니다.")
    else:
        st.warning("⚠️ 데이터베이스 파일이 없습니다.")


def show_portfolio_section():
    """Portfolio 섹션"""
    st.markdown("### 🎯 Portfolio (포트폴리오 리밸런싱)")

    # Rebalancing 버튼
    if st.button("🔄 Rebalancing 실행", key="rebalance"):
        perform_rebalancing()
        st.success("✅ 리밸런싱 완료!")
        st.rerun()

    st.markdown("---")

    # 데이터 로드
    if DB_PATH.exists():
        excel_handler = ExcelHandler(str(DB_PATH))
        excel_handler.load()
        portfolio_data = excel_handler.read_sheet_data('Portfolio')

        if portfolio_data and len(portfolio_data) > 1:
            # DataFrame 생성
            df = pd.DataFrame(portfolio_data[1:], columns=portfolio_data[0])

            # 숫자 컬럼 변환
            numeric_cols = ['세팅비중', '현재비중', '빨강매수']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.replace('%', ''), errors='coerce')

            # 편집 가능한 테이블
            st.markdown("#### 자산 배분")
            edited_df = st.data_editor(
                df,
                num_rows="dynamic",
                use_container_width=True,
                column_config={
                    "세팅비중": st.column_config.NumberColumn("세팅비중 (%)", format="%.1f%%", min_value=0, max_value=100),
                    "현재비중": st.column_config.NumberColumn("현재비중 (%)", format="%.1f%%"),
                    "빨강매수": st.column_config.NumberColumn("빨강매수", format="₩%d"),
                }
            )

            # 저장 버튼
            if st.button("💾 Portfolio 데이터 저장", key="save_portfolio"):
                save_portfolio_data(edited_df)
                st.success("✅ 저장되었습니다!")
                st.rerun()

            # 세팅비중 합계 확인
            setting_sum = edited_df['세팅비중'].sum()
            if abs(setting_sum - 100) > 0.1:
                st.warning(f"⚠️ 세팅비중 합계: {setting_sum:.1f}% (100%가 되어야 합니다)")
            else:
                st.success(f"✅ 세팅비중 합계: {setting_sum:.1f}%")
        else:
            st.info("📝 데이터가 없습니다.")
    else:
        st.warning("⚠️ 데이터베이스 파일이 없습니다.")


def process_uploaded_file(uploaded_file):
    """업로드된 파일 처리"""
    try:
        # 임시 파일로 저장
        temp_path = Path("temp_upload.xlsx")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 파일 읽기
        uploaded_data = ExcelHandler.read_uploaded_file(str(temp_path))

        # ROI 데이터 업데이트
        if DB_PATH.exists():
            excel_handler = ExcelHandler(str(DB_PATH))
            excel_handler.load()
            roi_data = excel_handler.read_sheet_data('ROI')

            if roi_data and len(roi_data) > 1:
                df = pd.DataFrame(roi_data[1:], columns=roi_data[0])

                # 종목코드 매칭하여 업데이트
                for idx, row in df.iterrows():
                    code = str(row.get('종목코드', '')).strip()
                    if code in uploaded_data:
                        df.at[idx, '종목명'] = uploaded_data[code]['종목명']
                        df.at[idx, '종가'] = uploaded_data[code]['종가']

                # 저장
                save_roi_data(df)

                # 날짜 추출
                year, month = ExcelHandler.extract_date_from_filename(uploaded_file.name)
                if year and month:
                    # Balance에 새 행 추가
                    balance_data = excel_handler.read_sheet_data('Balance')
                    if balance_data:
                        balance_df = pd.DataFrame(balance_data[1:], columns=balance_data[0]) if len(balance_data) > 1 else pd.DataFrame(columns=balance_data[0])
                        new_row = pd.DataFrame([[year, month, 0, 0, 0, 0, '']], columns=balance_data[0])
                        balance_df = pd.concat([balance_df, new_row], ignore_index=True)
                        save_balance_data(balance_df)

        # 임시 파일 삭제
        temp_path.unlink()

        st.success(f"✅ 파일 '{uploaded_file.name}'이 업로드되었습니다!")
        st.rerun()

    except Exception as e:
        st.error(f"❌ 파일 처리 오류: {str(e)}")


def save_roi_data(df):
    """ROI 데이터 저장"""
    excel_handler = ExcelHandler(str(DB_PATH))
    excel_handler.load()
    headers = ['종목코드', '종목명', '초기투자금', '수량', '종가', '평가금', '수익률']
    excel_handler.write_sheet_data('ROI', df.values.tolist(), headers)
    excel_handler.save()


def save_balance_data(df):
    """Balance 데이터 저장"""
    excel_handler = ExcelHandler(str(DB_PATH))
    excel_handler.load()
    headers = ['연도', '월', '투자원금', '추가납입', '잔고', '수익률', '기타']
    excel_handler.write_sheet_data('Balance', df.values.tolist(), headers)
    excel_handler.save()


def save_portfolio_data(df):
    """Portfolio 데이터 저장"""
    excel_handler = ExcelHandler(str(DB_PATH))
    excel_handler.load()
    headers = ['종목코드', '종목명', '자산군', '구분', '세팅비중', '현재비중', '빨강매수']
    excel_handler.write_sheet_data('Portfolio', df.values.tolist(), headers)
    excel_handler.save()


def perform_rebalancing():
    """리밸런싱 수행"""
    excel_handler = ExcelHandler(str(DB_PATH))
    excel_handler.load()

    # ROI 데이터 로드
    roi_data = excel_handler.read_sheet_data('ROI')
    roi_df = pd.DataFrame(roi_data[1:], columns=roi_data[0])
    roi_df['평가금'] = pd.to_numeric(roi_df['평가금'].astype(str).str.replace(',', ''), errors='coerce')

    total_eval = roi_df['평가금'].sum()

    # Portfolio 데이터 로드
    portfolio_data = excel_handler.read_sheet_data('Portfolio')
    portfolio_df = pd.DataFrame(portfolio_data[1:], columns=portfolio_data[0])

    # 종목코드 동기화
    portfolio_df['종목코드'] = roi_df['종목코드']
    portfolio_df['종목명'] = roi_df['종목명']

    # 계산
    portfolio_df['세팅비중'] = pd.to_numeric(portfolio_df.get('세팅비중', 0).astype(str).str.replace('%', ''), errors='coerce')

    for idx, row in portfolio_df.iterrows():
        # 현재비중 계산
        code = row.get('종목코드', '')
        eval_amt = roi_df[roi_df['종목코드'] == code]['평가금'].sum()
        current_ratio = calculator.calculate_current_ratio(eval_amt, total_eval)
        portfolio_df.at[idx, '현재비중'] = current_ratio

        # 빨강매수 계산
        setting_ratio = row.get('세팅비중', 0)
        rebalancing = calculator.calculate_rebalancing(setting_ratio, current_ratio, total_eval)
        portfolio_df.at[idx, '빨강매수'] = rebalancing

    # 저장
    save_portfolio_data(portfolio_df)


def create_sample_data():
    """샘플 데이터 생성"""
    import subprocess
    subprocess.run(["python", "create_sample_db.py"], check=True)
