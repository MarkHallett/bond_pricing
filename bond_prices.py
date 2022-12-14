# bond_prices

import datetime

class CashFlow:
    #CashFlow, input details, plus calculated days.
    def __init__(self, start_date, end_date, coupon) -> None:
        format_str: str = '%d/%m/%Y'
        self.start_date = datetime.datetime.strptime(start_date, format_str).date()
        self.end_date = datetime.datetime.strptime(end_date, format_str).date()
        self.coupon: float = coupon
        self.days: int = (self.end_date - self.start_date).days

def get_cashflows() -> list[CashFlow]:
    #Details of cash flows, start_date, end_date, coupon.
    cashflows: list[CashFlow] = []
    cashflows.append(CashFlow('15/02/2016', '15/08/2016', 30.00))    # 1
    cashflows.append(CashFlow('15/08/2016', '15/02/2017', 30.00))    # 2
    cashflows.append(CashFlow('15/02/2017', '15/08/2017', 30.00))    # 3
    cashflows.append(CashFlow('15/08/2017', '15/02/2018', 30.00))    # 4
    cashflows.append(CashFlow('15/02/2018', '15/08/2018', 30.00))    # 5
    cashflows.append(CashFlow('15/08/2018', '15/02/2019', 30.00))    # 6
    cashflows.append(CashFlow('15/02/2019', '15/08/2019', 30.00))    # 7
    cashflows.append(CashFlow('15/08/2019', '15/02/2020', 30.00))    # 8
    cashflows.append(CashFlow('15/02/2020', '15/08/2020', 30.00))    # 9
    cashflows.append(CashFlow('15/08/2020', '15/02/2021', 30.00))    # 10
    cashflows.append(CashFlow('15/02/2021', '15/08/2021', 30.00))    # 11
    cashflows.append(CashFlow('15/08/2021', '15/02/2022', 30.00))    # 12
    cashflows.append(CashFlow('15/02/2022', '15/08/2022', 30.00))    # 13
    cashflows.append(CashFlow('15/08/2022', '15/02/2023', 30.00))    # 14
    cashflows.append(CashFlow('15/02/2023', '15/08/2023', 30.00))    # 15
    cashflows.append(CashFlow('15/08/2023', '15/02/2024', 30.00))    # 16
    cashflows.append(CashFlow('15/02/2024', '15/08/2024', 30.00))    # 17
    cashflows.append(CashFlow('15/08/2024', '15/02/2025', 30.00))    # 18
    cashflows.append(CashFlow('15/02/2025', '15/08/2025', 30.00))    # 19
    cashflows.append(CashFlow('15/08/2025', '15/02/2026', 1030.00))  # 20
    return cashflows


class Bond:
    #Bond for input cashflows and frequency, calculates basic values.
    #Default values for demonination and par.
    def __init__(self, cashflows, frequency) -> None:
        format_str: str = '%d-%b-%y'
        settlement = '10-Jun-16'
        self.settlement	= datetime.datetime.strptime(settlement, format_str).date()
        self.denomination = 1000
        self.par = 100.0000  # percent
        self.frequency = frequency
        self.cashflows = cashflows
        end_date = self.cashflows[-1].end_date
        self.maturity_date = end_date
        self.maturity = (end_date - self.settlement).days/365
        self.coupon = self.cashflows[0].coupon
        self.nominal = self.cashflows[-1].coupon - self.coupon

    def calc_pv(self, irr_percent: float, a: float) -> float:
        #For a given irr, calculate the present value.
        pv = 0
        irr = irr_percent / 100
        for i, cash_flow in enumerate(self.cashflows, 1):
            discount_factor_i = 1/(1+irr/self.frequency)**(i-1+a)
            pvn = cash_flow.coupon * discount_factor_i
            pv += pvn
        return pv


def calc_initial_guess(bond: Bond, current_details: dict) -> float:
    #Calculate a first enstimate of the irr.
    coupon = bond.frequency * bond.coupon/bond.nominal
    mkt_clean_price_percent = current_details['mkt_clean_price']/100
    return (coupon + ((1 - mkt_clean_price_percent)/bond.maturity)) / ((1 + mkt_clean_price_percent)/bond.frequency)


def calc_gradient(bond: Bond, r: float, delta: float) -> float:
    #Calculate the gradient of the curve at a given irr (and delta).
    pv1 = bond.calc_pv(r, remaining_coupon_fraction)
    pv2 = bond.calc_pv(r+delta, remaining_coupon_fraction)
    gradient = (pv2-pv1)/delta
    return gradient


def newton_raphson(bond: Bond, current_guess: float, delta: float) -> float:
    #The Newton Raphson menthod for honing in on the irr.
    def next_guess(bond: Bond, best_guess_percent: float) -> float:
        irr = best_guess_percent
        gradient = calc_gradient(bond, best_guess_percent, delta)
        y_intersect = bond.calc_pv(irr, remaining_coupon_fraction) - dirty_price_percent*10
        better_guess = best_guess_percent - (y_intersect/gradient)
        return better_guess

    better_guess = next_guess(bond, current_guess)
    while abs(current_guess - better_guess) > 0.00001:
        current_guess = better_guess
        better_guess = next_guess(bond, current_guess)
    return better_guess


if __name__ == '__main__':
    print('Calc irr from clean market price for eg bond.')

    date_today_i: str = '10-Jun-16'
    # quoted_clean_price = '139-01+'
    mkt_clean_price_i = 139+3/64
    delta = -0.01
    denomination = 1000

    bond = Bond(get_cashflows(), frequency=2)

    format_str: str = '%d-%b-%y'
    date_today = datetime.datetime.strptime(date_today_i, format_str).date()
    end_date = bond.cashflows[-1].end_date
    maturity = (end_date - date_today).days/365

    current_details = {'mkt_clean_price': mkt_clean_price_i,
                       'date_today': date_today,
                       'maturity': maturity,
                       }

    coupon = bond.coupon
    nominal = bond.cashflows[-1].coupon - bond.cashflows[0].coupon

    first_coupon_start_date = bond.cashflows[0].start_date
    accrued_days = (date_today - first_coupon_start_date).days
    total_days = bond.cashflows[0].days
    remaining_days = total_days - accrued_days
    accrued_fraction = accrued_days / total_days
    remaining_coupon_fraction = remaining_days / total_days
    coupon_percent = 100*(coupon/nominal)
    accrued_percent = (nominal * coupon_percent * accrued_fraction) / nominal

    dirty_price_percent = mkt_clean_price_i + accrued_percent

    initial_guess = calc_initial_guess(bond, current_details) * 100
    irr = newton_raphson(bond, initial_guess, delta)

    print(f'  {round(irr,6)=}')

    dirty_value_from_irr = bond.calc_pv(irr, remaining_coupon_fraction)
    dirty_value_from_shifted_irr = bond.calc_pv(irr+delta, remaining_coupon_fraction)
    print(f'  {round(dirty_value_from_irr,6)=}')

    error = bond.calc_pv(irr, remaining_coupon_fraction) - (dirty_price_percent*bond.nominal)/100
    print(f'  {error=}')

    face = denomination * bond.nominal
    clean_price_percent = current_details['mkt_clean_price'] / 100
    total_coupons = sum(cf.coupon for cf in bond.cashflows)
    numerical_dv01 = dirty_value_from_shifted_irr - dirty_value_from_irr
    dv01 = numerical_dv01 * (face/denomination)

    print('-----')
    print('Bond Details')
    print('  Settlement     ', current_details['date_today'].strftime("%d-%b-%y"))
    print('  Denomination   ', denomination)
    print('  Par (%)        ', 100)
    print('  Clean Price (%)', round(current_details['mkt_clean_price'], 4))
    print('  Coupon (%)     ', 100*bond.coupon*bond.frequency/bond.nominal)
    print('  Frequency      ', bond.frequency)
    print('  Maturity Date  ', bond.maturity_date.strftime("%d-%b-%y"))
    print('  Maturity       ', round(bond.maturity, 2))
    print('  ')
    print('Current Coupon')
    print('  Accrued Days   ', accrued_days)
    print('  Remaining      ', remaining_days)
    print('  Total          ', total_days)
    print('  Accrued Fraction', round(accrued_fraction, 5))
    print('  Coupon Fraction ', round(remaining_coupon_fraction, 5))
    print('  ')
    print('Yield to Maturity(YTM)')
    print('  Initial guess (%)', round(initial_guess, 6))
    print('  YTM Used (%)     ', round(irr, 6))
    print('  Shift_size (%)   ', delta)
    print('  ')
    print('Invoice  ')
    print('  Face         ', face)
    print('  Coupons Due  ', denomination * total_coupons)
    print('  Principal    ', face * clean_price_percent)
    print('  Accrued      ', round(face * accrued_percent / 100, 2))
    print('  Total PV     ', round(face * dirty_price_percent / 100, 2))
    print('  DV01         ', round(dv01, 2))
    print('  ')
    print('Bond Price  ')
    print('  Clean Price (%) ', round(clean_price_percent, 6))
    print('  Accrued (%)     ', round(accrued_percent, 4))
    print('  Dirty Price (%) ', round(dirty_price_percent, 4))
    print('  ',)
    print('Total Coupons    ', total_coupons)
    print('Total PV         ', round(dirty_value_from_irr, 2))
    print('Shifted Total PV ', round(dirty_value_from_shifted_irr, 2))
    print('Numerical DV01   ', round(numerical_dv01, 5))
