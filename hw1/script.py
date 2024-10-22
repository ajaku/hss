import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
# MR CHAT INCLUDES
import statsmodels.api as sm
import seaborn as sns

data = pd.read_csv('data.csv')
#data.describe().to_excel("total_data_output.xlsx", sheet_name="Summary")

num_cigs = 0
for cig_count in data['cigs']:
    if cig_count > 0:
        num_cigs = num_cigs + 1


print(f"Percentage of smokers: {(num_cigs/data['cigs'].count()) * 100}")

# Redo summary statistics for smokers
smokers = data[data['cigs'] > 0]
non_smokers = data[data['cigs'] == 0]

combined_describe = pd.concat([smokers.describe(
), non_smokers.describe()], axis=1, keys=['Smokers', 'Non-Smokers'])
combined_describe.to_excel("combined_describe_smokers_nonsmokers.xlsx")

# d)
(t_educ, p_educ) = ttest_ind(
    smokers['educ'], non_smokers['educ'], equal_var=False)
print(f"t_educ: {t_educ}\np_educ: {p_educ}")
# thus my hypothesis is false

# e)
print(smokers['income'], non_smokers['income'])

print(smokers['income'].mean(), non_smokers['income'].mean())

(t_income, p_income) = ttest_ind(
    smokers['income'], non_smokers['income'], equal_var=False)
print(f"t_income: {t_income}\np_income: {p_income}")
# thus my hypothesis is true

white = data[data['white'] == 1]
non_white = data[data['white'] == 0]

white_smokers = white[white['cigs'] > 0]
white_non_smokers = white[white['cigs'] == 0]

non_white_smokers = non_white[non_white['cigs'] > 0]
non_white_non_smokers = non_white[non_white['cigs'] == 0]

print(f"Number of white smokers: {white_smokers['personid'].count()}")
print(f"Number of white individuals: {white['personid'].count()}")

print(f"Number of non-white smokers: {non_white_smokers['personid'].count()}")
print(f"Number of non-white individuals: {non_white['personid'].count()}")

# f)
print(
    f"ratio of smokers to total sample (non-white): {non_white_smokers['personid'].count()/ non_white['personid'].count()}")
print(
    f"ratio of smokers to total sample (white): {white_smokers['personid'].count()/ white['personid'].count()}")

# g)
plt.hist(data['cigs'], bins=50, color='red', edgecolor='black')

# Adding labels and title
plt.xlabel('Number of Cigarettes Smoked')
plt.ylabel('Frequency')
plt.title('Cigarette Frequency Histogram')

# Display the plot
plt.savefig('cigs_histogram.png')

# h) avg. cigs smoked per income
cigs = np.array(data['cigs'].values[:]).reshape(-1, 1)
income = np.array(data['income'].values[:])
model = LinearRegression()
model.fit(cigs, income)

r_sq = model.score(cigs, income)
print(f"coefficient of determination: {r_sq}")

# Calculate the correlation coefficient
correlation = data['income'].corr(data['cigs'])
print(
    f"Correlation coefficient between income and cigarettes smoked: {correlation}")

# PLOT INCOME AND CIGS
sns.set(style='whitegrid')

# Scatter plot
plt.figure(figsize=(5, 5))
sns.scatterplot(x='income', y='cigs', data=data)
plt.title('Income vs. Cigarettes Smoked Per Day')
plt.xlabel('Income')
plt.ylabel('Cigarettes Smoked Per Day')
plt.savefig("income_v_cigs_p_day.png")


# i) avg. cigs smoked per price
cigs = np.array(data['cigs'].values[:]).reshape(-1, 1)
price = np.array(data['cigpric'].values[:])
model = LinearRegression()
model.fit(cigs, price)

r_sq = model.score(cigs, price)
print(f"coefficient of determination: {r_sq}")

# Calculate the correlation coefficient
correlation = data['cigpric'].corr(data['cigs'])
print(
    f"Correlation coefficient between price and cigarettes smoked: {correlation}")

# PLOT INCOME AND CIGS
sns.set(style='whitegrid')

# Scatter plot
plt.figure(figsize=(5, 5))
sns.scatterplot(x='cigpric', y='cigs', data=data)
plt.title('Price vs. Cigarettes Smoked Per Day')
plt.xlabel('Price')
plt.ylabel('Cigarettes Smoked Per Day')
plt.savefig("price_v_cig_p_day.png")
