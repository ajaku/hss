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

# 1c
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

f_df = df[df['schlid'].isin([1, 75])]

# Create the Treatment dummy: 1 if treated (school 75), 0 if control (school 1)
f_df['treated'] = (f_df['schlid'] == 75).astype(int)

# Create the After dummy: 1 if year > 5, 0 if year <= 5
f_df['after'] = (f_df['year'] > 5).astype(int)

# Create the Interaction term: treated * after
f_df['treated_after'] = f_df['treated'] * f_df['after']

# Define the dependent variable (wage) and independent variables
X = f_df[['treated', 'after', 'treated_after']]  # Independent variables
X = sm.add_constant(X)  # Add a constant for the intercept
y = f_df['wage2']  # Dependent variable

# Run the OLS regression
model = sm.OLS(y, X).fit()

# Print the regression results
print(model.summary())

f_df = df[df['schlid'].isin([1, 75])]

# Group by school and year, then calculate the average wage for each group
avg_wages_yearly = f_df.groupby(['schlid', 'year'])['wage2'].mean().reset_index()

# Print the average wages for each school at each year
print(avg_wages_yearly)

years_0_4 = f_df[f_df['year'] <= 4]
years_5_10 = f_df[(f_df['year'] > 5) & (f_df['year'] <= 10)]
# Calculate the average wage for each year in both periods
avg_wages_0_4 = years_0_4.groupby(['schlid', 'year'])['wage2'].mean().reset_index()
avg_wages_5_10 = years_5_10.groupby(['schlid', 'year'])['wage2'].mean().reset_index()

# Concatenate the two periods together
avg_wages_combined = pd.concat([avg_wages_0_4, avg_wages_5_10])

# Define a function to fit and plot the slopes
def plot_slope(data, school_id, color, label):
    # Filter data for the specific school
    school_data = data[data['schlid'] == school_id]
    
    # For School 75, we want two slopes:
    if school_id == 75:
        # Fit linear regression for the period 0-4
        X_0_4 = sm.add_constant(school_data[school_data['year'] <= 5]['year'])
        y_0_4 = school_data[school_data['year'] <= 5]['wage2']
        model_0_4 = sm.OLS(y_0_4, X_0_4).fit()

        # Fit linear regression for the period 5-10
        X_5_10 = sm.add_constant(school_data[school_data['year'] > 4]['year'])
        y_5_10 = school_data[school_data['year'] > 4]['wage2']
        model_5_10 = sm.OLS(y_5_10, X_5_10).fit()
        
        # Create the years for predictions
        years_0_4 = np.linspace(0, 5, 100)
        years_5_10 = np.linspace(5, 10, 100)
        
        # Predict the wages using the regression models
        wage_preds_0_4 = model_0_4.predict(sm.add_constant(years_0_4))
        wage_preds_5_10 = model_5_10.predict(sm.add_constant(years_5_10))
        
        # Plot the regression lines
        plt.plot(years_0_4, wage_preds_0_4, color=color, label=f"{label} 0-10 years", linestyle='-')
        plt.plot(years_5_10, wage_preds_5_10, color=color, linestyle='-')
        plt.scatter(school_data[school_data['year'] <= 10]['year'], 
                    school_data[school_data['year'] <= 10]['wage2'], 
                    color=color, s=50, zorder=5)

        plt.scatter(school_data[school_data['year'] == 5]['year'], 
                    school_data[school_data['year'] == 5]['wage2'], 
                    color=color, s=50, zorder=5)

    # For School 1, fit a single continuous slope across all years:
    else:
        X_0_10 = sm.add_constant(school_data[school_data['year'] <= 10]['year'])
        y_0_10 = school_data[school_data['year'] <= 10]['wage2']
        model_0_10 = sm.OLS(y_0_10, X_0_10).fit()
    
        # Create the years for predictions
        years_0_10 = np.linspace(0, 10, 200)
    
        # Predict the wages using the regression models
        wage_preds_0_10 = model_0_10.predict(sm.add_constant(years_0_10))
    
        # Plot the regression lines
        plt.plot(years_0_10, wage_preds_0_10, color=color, label=f"{label} 0-10 years", linestyle='-')
        plt.scatter(school_data['year'], school_data['wage2'], 
                color=color, s=50, zorder=5)

# Plot the slopes for School 1 (Control) and School 75 (Treatment)
plot_slope(avg_wages_combined, school_id=1, color='blue', label="School 1 (Control)")
plot_slope(avg_wages_combined, school_id=75, color='red', label="School 75 (Treatment)")

# Labels and title
plt.xlabel('Year')
plt.ylabel('Average Wage')
plt.title('Difference in Differences of wages per year')

# Add a vertical line to separate years 0-4 and 5-10
plt.axvline(x=5, color='grey', linestyle='--')

# Show legend
plt.legend()

# Display the plot
plt.savefig("FINAL.png")