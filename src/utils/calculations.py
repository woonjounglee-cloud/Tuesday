"""계산 로직 유틸리티"""


class Calculator:
    """재무 계산 함수들"""

    @staticmethod
    def calculate_evaluation(quantity, current_price):
        """평가금 계산: 수량 * 종가"""
        try:
            qty = float(quantity) if quantity else 0
            price = float(current_price) if current_price else 0
            return qty * price
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def calculate_roi(evaluation, initial_investment):
        """수익률 계산: (평가금 - 초기투자금) / 초기투자금 * 100"""
        try:
            eval_amt = float(evaluation) if evaluation else 0
            initial = float(initial_investment) if initial_investment else 0

            if initial == 0:
                return 0

            return ((eval_amt - initial) / initial) * 100
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def calculate_balance_roi(balance, principal):
        """잔고 수익률 계산: (잔고 - 투자원금) / 투자원금 * 100"""
        try:
            bal = float(balance) if balance else 0
            prin = float(principal) if principal else 0

            if prin == 0:
                return 0

            return ((bal - prin) / prin) * 100
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def calculate_investment_allocation(total_principal, setting_ratio):
        """투자금 배분 계산: 총 투자원금 * 세팅비중"""
        try:
            total = float(total_principal) if total_principal else 0
            ratio = float(setting_ratio) if setting_ratio else 0

            return total * (ratio / 100)
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def calculate_current_ratio(evaluation, total_evaluation):
        """현재비중 계산: 개별 평가금 / 전체 평가금 총합"""
        try:
            eval_amt = float(evaluation) if evaluation else 0
            total = float(total_evaluation) if total_evaluation else 0

            if total == 0:
                return 0

            return (eval_amt / total) * 100
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def calculate_rebalancing(setting_ratio, current_ratio, total_evaluation):
        """빨강매수 계산: (세팅비중 - 현재비중) * 전체 평가금 총합"""
        try:
            setting = float(setting_ratio) if setting_ratio else 0
            current = float(current_ratio) if current_ratio else 0
            total = float(total_evaluation) if total_evaluation else 0

            return ((setting - current) / 100) * total
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def format_number(value, decimals=0):
        """숫자 포맷팅"""
        try:
            num = float(value) if value else 0
            if decimals == 0:
                return f"{int(num):,}"
            else:
                return f"{num:,.{decimals}f}"
        except (ValueError, TypeError):
            return "0"

    @staticmethod
    def format_percentage(value, decimals=2):
        """퍼센트 포맷팅"""
        try:
            num = float(value) if value else 0
            return f"{num:.{decimals}f}%"
        except (ValueError, TypeError):
            return "0.00%"

    @staticmethod
    def format_rebalancing(value):
        """빨강매수 포맷팅 (양수: 빨강, 음수: 괄호)"""
        try:
            num = float(value) if value else 0
            if num < 0:
                return f"({abs(num):,.0f})"
            else:
                return f"{num:,.0f}"
        except (ValueError, TypeError):
            return "0"
