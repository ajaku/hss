'''
Datasets:
- We care about interview year 2021 -> 211, 212, 213, 214
- We skip out on 221 because that is the information on year 2022

Variable names
- NEWID: HH identification number
- FAM_SIZE: family size
- NUM_AUTO: number of vehicles owned
- FINCBTXM: final income before taxes (imputed in case of missing information) in the past 12 months
- TOTEXPPQ: total expenditure in the previous quarter
- TOTEXPCQ: total expenditure in the current quarter
- ALCBEVCQ/ ALCBEVPQ: spending on alcoholic beverages in current and previous quarter
- FOODCQ/ FOODPQ: spending on food in current quarter and in previous quarter
- FDHOMECQ/ FDHOMEPQ: food at home this quarter and previous quarter
- FDMAPCQ/ FDMAPPQ: meals as pay this quarter and previous quarter
- FDAWAYCQ/ FDAWAYPQ: food away from home excluding meals as pay this quarter and previous quarter
- MAJAPPCQ/ MAJAPPPQ: spending on major appliances in current quarter and previous quarter
- TENTRMNC/ TENTRMNP: spending on entertainment (sporting events, movies, and recreational vehicles) in current and previous quarters
- EDUCACQ/ EDUCAPQ: spending on education in this quarter and previous quarter
- ELCTRCCQ/ ELCTRCPQ: spending on electricity this quarter and in previous quarter 

Goal:
- We want to use this data on expenditure and income to compute the MPC.

Tasks:
a) Stitch files: 211, 212, 213, 214
b) Clean data
c) Determine regression
d) Estimate regression
e) Compare MPCs
f) Estimate MPC for essential and non-essential categories
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
import imgkit
from scipy.stats import ttest_ind
from sklearn.linear_model import LinearRegression
from stargazer.stargazer import Stargazer
from PIL import Image

def perf_lin_reg(df, x_name, y_name, x_p, y_p, name):
    x = df[x_name]
    y = df[y_name]

    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()

    stargazer = Stargazer([model])
    html = stargazer.render_html()
    x_p = f"{x_p} (β₁)"
    const = f"Const (β₀)"
    html = html.replace(x_name, x_p)
    html = html.replace("const", const)
    html = html.replace(y_name, y_p)

    name = f"{name}.png"
    imgkit.from_string(html, name)
    img = Image.open(name)

    cropped_img = img.crop((0, 0, img.width - 500, img.height))
    cropped_img.save(name)


data = pd.read_csv('filtered_fmli.csv')
unique_newids_count = data['NEWID'].nunique()
newids_count = data['NEWID'].count()

data = data[data['FINCBTXM'] > 0]

desc = (data.describe()).T
desc.to_excel('desc.xlsx')

perf_lin_reg(data, 'FINCBTXM', 'TOTEXP', 'INCOME', 'TOTAL EXP.', 'inc_v_texp')

median= data['FINCBTXM'].median()
print(f"Median = {median}\n")
data['Inc_Cat'] = data['FINCBTXM'].apply(
    lambda x: 'High Income' if x > (data['FINCBTXM'].median()) else 'Low Income')
high_income_data = data[data['Inc_Cat'] == 'High Income']
low_income_data = data[data['Inc_Cat'] == 'Low Income']

perf_lin_reg(high_income_data, 'FINCBTXM', 'TOTEXP', 'INCOME', 'TOTAL EXP.', 'highinc_v_texp')
perf_lin_reg(low_income_data, 'FINCBTXM', 'TOTEXP', 'INCOME', 'TOTAL EXP.', 'lowinc_v_texp')
perf_lin_reg(data, 'FINCBTXM', 'FDHOME', 'INCOME', 'FOOD HOME EXP.', 'inc_v_foodhomeexp')
perf_lin_reg(data, 'FINCBTXM', 'FDAWAY', 'INCOME', 'FOOD AWAY EXP..', 'inc_v_foodawayexp')
