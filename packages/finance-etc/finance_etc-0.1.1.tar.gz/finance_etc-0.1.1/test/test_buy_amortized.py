from src.mortgage import buy_amortized, buy
# https://www.westpac.com.au/personal-banking/home-loans/calculator/mortgage-repayment/?cid=wc:hl:UF-Gen_2003:sem:goog:_best%20loan%20calculator_b&gad_source=1&gclid=CjwKCAjwvKi4BhABEiwAH2gcwxUU6-4GCtt2C40a1OUQOKMRT8rRvIzoyjzgYUp5_RclJcmmuYSwuBoCUM0QAvD_BwE&gclsrc=aw.ds
buy_amortized(300_000, 0.06, years = 30, period = 'MONTHLY', period_calc_choice = 'WESTPAC') # correct 1799
buy_amortized(300_000, 0.06, years = 30, period = 'FORTNIGHTLY', period_calc_choice = 'WESTPAC') # wrong 900
buy_amortized(300_000, 0.06, years = 30, period = 'WEEKLY', period_calc_choice = 'WESTPAC') # wrong 450


#https://www.commbank.com.au/digital/home-buying/calculator/home-loan-repayments?ei=calculator-inter-calc-tab-home-loan-repayments
buy_amortized(300_000, 0.06, years = 30, period = 'MONTHLY', period_calc_choice = 'CBA') # correct 1799
buy_amortized(300_000, 0.06, years = 30, period = 'FORTNIGHTLY', period_calc_choice = 'CBA') # wrong 831
buy_amortized(300_000, 0.06, years = 30, period = 'WEEKLY', period_calc_choice = 'CBA') # wrong 416


import matplotlib.pyplot as plt
plt.plot(buy(300_000))
#plt.show()
