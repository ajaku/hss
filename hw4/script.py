# Variables in the dataset:

# schlid: School ID. 
#         The dataset includes 100 schools labeled from 1 to 100.

# year: Year of observation.
#       For each school, data is collected for 10 years.

# studid: Student ID.
#         Each school has 500 students per year.

# schleff: School-specific effects.
#          Larger schools are constructed to perform better in the dataset.

# ability: Student-specific measure of ability.
#          Generated as a random variable influenced by school effects, meaning students 
#          in better schools tend to have higher ability.

# motive: Student-specific measure of motivation.
#         Also influenced by school effects.

# ap_schl: Indicator for whether a school offers AP classes.
#          Top 20 schools offer AP; the rest do not.

# ap: Indicator for whether a student takes AP classes.
#     1 if the student takes AP classes; 0 otherwise.

# wage: Future wage of the student.
#       Determined as a function of ability, motivation, random effects, and a $50 bonus
#       for taking AP classes. The causal effect of taking AP is $50 higher wages.


import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.api import OLS, add_constant
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv')

'''
# 1a
X_ap = df['ap']  # AP indicator
X_ap = add_constant(X_ap)
y_wage = df['wage']  # Wage

model_a = OLS(y_wage, X_ap).fit()
print(model_a.summary())

# 1b
X_ap_ability_motive = df[['ap', 'ability', 'motive']]  # AP, ability, and motivation
X_ap_ability_motive = add_constant(X_ap_ability_motive)
y_wage = df['wage']  # Wage

model_b = OLS(y_wage, X_ap_ability_motive).fit()
print(model_b.summary())

# Prepare an empty list to store results
coefficients = []

# Group by school and run the regression for each school
ap_off = df[df['ap_schl'] == 1]
for school, group in ap_off.groupby('schlid'):  # Assuming `school` is the column for school identifier
    if len(group) > 1:  # Ensure there are enough observations to run the regression
        X = group[['ap', 'ability', 'motive']]  # AP, ability, and motive
        X = add_constant(X)  # Add constant for intercept
        y = group['wage']
        
        model = OLS(y, X).fit()
        
        coefficients.append(model.params['ap'])

average_ap_coefficient = np.mean(coefficients)
print(f"Average AP Coefficient Across Schools: {average_ap_coefficient}")

# 1c
# Run fixed-effects regression
# model_c = smf.ols('wage ~ ap + C(schlid)', data=df).fit()
# print(model_c.summary())

'''

f_df = df[df['schlid'].isin([1, 75])]

# Run the DID regression
X_did = f_df[['ap_schl', 'ap_schl2']]
X_did = add_constant(X_did)  # Add constant for intercept

y_wage = f_df['wage']

model_did = OLS(y_wage, X_did).fit()
print(model_did.summary())

# Group by year and school, calculate the mean wage
grouped = f_df.groupby(['year', 'schlid'])['wage'].mean().reset_index()

# Plot the trends for both schools
plt.figure(figsize=(10, 6))
for school in [1, 75]:
    school_data = grouped[grouped['schlid'] == school]
    plt.plot(school_data['year'], school_data['wage'], label=f"School {school}")

plt.axvline(x=5, color='red', linestyle='--', label="Year 5: AP Start for School 75")
plt.xlabel('Year')
plt.ylabel('Average Wage')
plt.title('Wage Trend for Schools 1 and 75')
plt.legend()
plt.savefig("img.png")


# Create the Treatment dummy (1 if treated, 0 if not)
f_df['treated'] = (f_df['schlid'] == 75).astype(int)

# Create the Post dummy (1 if after year 5, 0 if before)
f_df['post'] = (f_df['year'] >= 5).astype(int)

# Create the interaction term (Treated * Post)
f_df['treated_post'] = f_df['treated'] * f_df['post']

# Define the dependent variable (wage) and independent variables (including the dummies and interaction term)
X = f_df[['treated', 'post', 'treated_post']]  # Independent variables
X = sm.add_constant(X)  # Add a constant for the intercept
y = f_df['wage']  # Dependent variable

# Run the OLS regression
model = sm.OLS(y, X).fit()

# Print the regression results
print(model.summary())

'''
Treatement      -> Add AP exam
Outcome         -> Increase in wages
Treated Group   -> School 75
Control Group   -> School 1

Dummy Var (treatement): 1 if 75 and 0 if 1
Dummy var (after): 0 if <= 5 years, 1 if > 5 years
Interaction = Dummy Var (treat) * Dummy Var (after)

Outcome = B_0 + B_1 * (after dummy) + B_2 * (treatment dummy) + B_3 * (after_dummy * treatement dummy)
'''

# Create the Treatment dummy: 1 if treated (school 75), 0 if control (school 1)
f_df['treated'] = (f_df['schlid'] == 75).astype(int)

# Create the After dummy: 1 if year > 5, 0 if year <= 5
f_df['after'] = (f_df['year'] > 5).astype(int)

# Create the Interaction term: treated * after
f_df['treated_after'] = f_df['treated'] * f_df['after']

# Define the dependent variable (wage) and independent variables
X = f_df[['treated', 'after', 'treated_after']]  # Independent variables
X = sm.add_constant(X)  # Add a constant for the intercept
y = f_df['wage']  # Dependent variable

# Run the OLS regression
model = sm.OLS(y, X).fit()

# Print the regression results
print(model.summary())
