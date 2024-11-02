import math
def basic_tax_liability_24_25(assessable:float)->float:
    map = (
        (18200,lambda x: 0),
        (45000,lambda x: 0.16*(x-18200)),
        (135000,lambda x: 0.3*(x-45000)+4288),
        (190000,lambda x: 0.37*(x-135000)+31288),
        (math.inf,lambda x: 0.45*(x-190000)+51638),
    )
    for x,f in map:
        if assessable <= x:
            return f(assessable)

# taxable = assessable - deduction
# basic tax liab = taxable x tax rate
# net tax liab = basic tax liab - offset
# total tax payable = net tax liab + levy - credit
def basic_tax_liability_22_24(assessable:float)->float:
    map = (
        (18200,lambda x: 0),
        (45000,lambda x: 0.19*(x-18200)),
        (120000,lambda x: 0.325*(x-45000)+5092),
        (180000,lambda x: 0.37*(x-120000)+29467),
        (math.inf,lambda x: 0.45*(x-180000)+51667),
    )
    for x,f in map:
        if assessable <= x:
            return f(assessable)

def hecs_rate_23_24(repayment_income:float)->float:
    rates = [
        (0, 51_549, 0),
        (51_550, 59_518, 1.0),
        (59_519, 63_089, 2.0),
        (63_090, 66_875, 2.5),
        (66_876, 70_888, 3.0),
        (70_889, 75_140, 3.5),
        (75_141, 79_649, 4.0),
        (79_650, 84_429, 4.5),
        (84_430, 89_494, 5.0),
        (89_495, 94_865, 5.5),
        (94_866, 100_557, 6.0),
        (100_558, 106_590, 6.5),
        (106_591, 112_985, 7.0),
        (112_986, 119_764, 7.5),
        (119_765, 126_950, 8.0),
        (126_951, 134_568, 8.5),
        (134_569, 142_642, 9.0),
        (142_643, 151_200, 9.5),
        (151_201, math.inf, 10)
    ]
    return list(filter(lambda x: x[0] <= int(repayment_income) <= x[1], rates))[0][2]/100*repayment_income

def hecs_rate_24_25(repayment_income:float)->float:
    rates = [
        (0, 54_434, 0),
        (54_435, 62_850, 1.00),
        (62_851, 66_620, 2.00),
        (66_621, 70_618, 2.50),
        (70_619, 74_855, 3.00),
        (74_856, 79_346, 3.50),
        (79_347, 84_107, 4.00),
        (84_108, 89_154, 4.50),
        (89_155, 94_503, 5.00),
        (94_504, 100_174, 5.50),
        (100_175, 106_185, 6.00),
        (106_186, 112_556, 6.50),
        (112_557, 119_309, 7.00),
        (119_310, 126_467, 7.50),
        (126_468, 134_056, 8.00),
        (134_057, 142_100, 8.50),
        (142_101, 150_626, 9.00),
        (150_627, 159_663, 9.50),
        (159_664, math.inf, 10.00),
    ]
    return list(filter(lambda x: x[0] <= int(repayment_income) <= x[1], rates))[0][2]/100*repayment_income

def income_year(date):
    year = date.year
    if date <= date.replace(month = 6, day = 30):
        return str(year-1)+'-'+str(year)
    return str(year)+'-'+str(year+1)

import duckdb
from duckdb.typing import *
def register_functions(conn):
    for fn_name in ["btl_22_24", "btl_24_25", "hr_23_24", "hr_24_25", 'income_year']:
        try:
            conn.remove_function(fn_name)
        except:
            pass
    conn.create_function("btl_22_24", basic_tax_liability_22_24, [DOUBLE], DOUBLE)
    conn.create_function("btl_24_25", basic_tax_liability_24_25, [DOUBLE], DOUBLE)
    conn.create_function("hr_23_24", hecs_rate_23_24, [DOUBLE], DOUBLE)
    conn.create_function("hr_24_25", hecs_rate_24_25, [DOUBLE], DOUBLE)
    conn.create_function("income_year", income_year, [DATE], VARCHAR)
    return conn

import pandas as pd

#TODO add multi year support (pre23, 23, 24)
def income_tax_estimator(conn = duckdb, pre_tax = [10_000 * i for i in range(5, 20, 1)], year = 2024):
    """
        depends on the availability of custom funcs in conn
    """
    salarys = pd.DataFrame({'pre_tax':pre_tax})
    x = conn.sql("""
        select
            pre_tax
            , btl_22_24(pre_tax) as total_tax
            , hr_23_24(pre_tax) as hecs
            , 0.02*pre_tax as medi_levy
            , total_tax/12 as avg_tax_per_month
            , pre_tax - total_tax as post_tax
            , pre_tax - total_tax - medi_levy - hecs as post_ato
            , lag(post_ato) over (order by pre_tax) as previous_post_ato_salary
            , (post_ato-previous_post_ato_salary)/previous_post_ato_salary as increase_percent
            , post_tax/12 as post_tax_per_month
            , post_ato/12 as post_ato_per_month
            , post_ato*0.5 as need_50
            , post_ato*0.3 as want_30
            , post_ato*0.2 as save_20
            , need_50/12   as need_monthly
            , want_30/12   as want_monthly
            , save_20/12   as save_monthly
        from salarys
    """).to_df()
    return x

def need_want_row(need_tiers: dict):
    """
        assumes: {
            need_tier_name1: {'need0':amount0, 'need1':amount1},
            need_tier_name2: {'need0':amount0, 'need1':amount1},
        }
    """
    kv = []
    for tier_name, tier_amounts in need_tiers.items():
        kv.append({
           'combo': tier_name,
           'yearly_total': sum(tier_amounts.values()),
           'monthly_total': sum(tier_amounts.values())/12,
        })
    return pd.DataFrame(kv)