import math
import pandas as pd
from .myutils import print_deco
def buy(loan_amount,interest_rate=0.059,years=30):
    period = {
        'WEEKLY':7,
        'FORTNIGHTLY':14,
        'MONTHLY':30.4375
    }
    days=365.25*years
    payment_instance_cnt = days/period['WEEKLY']
    payment_instance_base_amount = loan_amount/payment_instance_cnt
    #print(payment_instance_cnt,payment_instance_base_amount)
    remain_instance_loan_amount = [loan_amount - payment_instance_base_amount * xth_period for xth_period in range(1,math.ceil(payment_instance_cnt)+1)]
    interest_instance_amount = [interest_rate/(365.25/period['WEEKLY']) * x for x in remain_instance_loan_amount]
    return interest_instance_amount

@print_deco
def buy_amortized(*, loan_amount,interest_rate, years=30, year_days = 365.25, repay_day_apart = 365.25/52):
    #, period='WEEKLY', period_calc_choice = 'DEFAULT'):
    n = (years*year_days/repay_day_apart)
    r = interest_rate/(year_days/repay_day_apart)
    D = ((1+r)**n-1)/(r*(1+r)**n)
    total_payment = loan_amount*(r*(1+r)**n)/((1+r)**n-1)
    
    return round(total_payment)


def stamp_duty(price):
    # from july 2023
    # $0 to $16,000	$1.25 for every $100 (minimum $20) minimum duty $10, prior to 1 February 2024
    # $16,000 to $35,000	$200 plus $1.50 for every $100 over $16,000
    # $35,000 to $93,000	$485 plus $1.75 for every $100 over $35,000
    # $93,000 to $351,000	$1,500 plus $3.50 for every $100 over $93,000
    # $351,000 to $1,168,000	$10,530 plus $4.50 for every $100 over $351,000
    # Over $1,168,000 $47,295 plus $5.50 for every $100 over $1,168,000
    if price <= 16000:
        return max(20,1.25*price/100)
    elif price <= 35000:
        return 200+1.5*(price-16000)/100
    elif price <= 93000:
        return 485+1.75*(price-35000)/100
    elif price <= 351000:
        return 1500+3.5*(price-93000)/100
    elif price <= 1168000:
        return 10530+4.5*(price-93000)/100
    else:
        return 47295+5.5*(price-1168000)/100

def project_n_years_property_spend(
    target:int = 500_000,
    rental_income_weekly:int = 300,
    rent_out_week_per_year:int = 48,
    tax_deductible_proportion:float = 1.,
    yearly_routine_cost_est = (332+171.5+1071.2)*4, # water + council + strata
    initial_deposit = 100_000, 
    projection_years = 5, 
    mortgage_interest_rate = 0.066,
    yearly_appreciation_rate = 1.04,
):
    print(f"--price:{target}----y0_rent:{rental_income_weekly}---"
          f"y0_rent_total:{rental_income_weekly*52}--"
          f"stamp_duty:{stamp_duty(target)}--"
          f"deposit:{initial_deposit}------")
    no_txn_in_1_year = period = 12

    # interest for each payment [n * period] in total
    interest = [0]*(no_txn_in_1_year*30)

    # remain principal after each payment, [0] is initial, [n * period + 1] in total, [-1] < 0
    remain_principal = [0]*(52*30+1)    
    remain_principal[0] = target - initial_deposit
    
    #TODO pass this in as a param to compare different mortgage options
    periodic_payment = buy_amortized(
        loan_amount = remain_principal[0],
        interest_rate = mortgage_interest_rate, 
        years = 30, 
        year_days = 365.25, 
        repay_day_apart = 365.25/no_txn_in_1_year
    )

    for i in range(1,no_txn_in_1_year*30+1):
        interest[i-1] = round(1/no_txn_in_1_year * mortgage_interest_rate * remain_principal[i-1], 2)
        remain_principal[i] = remain_principal[i-1] - (periodic_payment-interest[i-1])

    relevant_statistics = pd.DataFrame(columns=[
        '年还贷支出',
        '年常态支出',
        '年总支出',
        '年偿还利息',
        '年抵税（比例后）',
        '年房租',
        '年增值',
        '同等存款年息',
    ])
    for i in range(projection_years):
        年还贷支出 = periodic_payment * no_txn_in_1_year
        年常态支出 = yearly_routine_cost_est
        年总支出 = 年还贷支出 + 年常态支出
        年偿还利息 = sum(interest[i*no_txn_in_1_year:(i+1)*no_txn_in_1_year])
        年抵税 = (年常态支出 + 年偿还利息) * tax_deductible_proportion
        年房租 = rental_income_weekly * rent_out_week_per_year * (1.01**i)
        年增值 = target*(yearly_appreciation_rate**i-yearly_appreciation_rate**(i-1)) 
        同等存款年息 = initial_deposit * \
            ( 
                (mortgage_interest_rate+1)**i - (mortgage_interest_rate+1)**(i-1)
            ) * 0.8 # 税后
        relevant_statistics.loc[i] = [
            年还贷支出,
            年常态支出,
            年总支出,
            年偿还利息,
            年抵税,
            年房租,
            年增值,
            同等存款年息,
        ]
        
        #with pd.option_context('display.precision',2):#,'display.max_colwidth',10):
        #  target_price_return_stat_prediction_df.rename(columns=lambda x: x[:10], inplace=True)
        #  display(target_price_return_stat_prediction_df)
    return relevant_statistics