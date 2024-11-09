import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import pearsonr
import statsmodels.api as sm
import statsmodels.formula.api as smf

df = pd.read_csv('cleaned_data.csv')

print((df.describe()).T)

print("2a) Compute the mean difference in birthweight by smoking status")
# Ensure 'dbrwt' and 'tobacco' columns exist in the dataset
if 'dbrwt' in df.columns and 'tobacco' in df.columns:
    # Compute mean birth weight for each smoking status (1: smoker, 0: non-smoker)
    birthweight_by_smoking = df.groupby('tobacco')['dbrwt'].mean()
    
    # Calculate the mean difference
    mean_diff = birthweight_by_smoking[1] - birthweight_by_smoking[0]
    
    print("Mean birth weight for smokers:", birthweight_by_smoking[1])
    print("Mean birth weight for non-smokers:", birthweight_by_smoking[0])
    print("Mean difference in birth weight by smoking status:", mean_diff)
else:
    print("The required columns 'dbrwt' or 'tobacco' are missing from the dataset.")

bins = [0, 10, 20, 30, 40, 97, 98]  # 98 represents 98 or more cigarettes in the dataset
labels = ['0', '1-10', '11-20', '21-30', '31-40', '41+']

# Create a new column with bins
df['cigarette_bin'] = pd.cut(df['cigar'], bins=bins, labels=labels, right=False)

# Calculate the mean birth weight within each bin
mean_birthweight_by_bin = df.groupby('cigarette_bin', observed=True)['dbrwt'].mean()

# Get the mean birth weight for the 0-cigarette bin
mean_birthweight_0 = mean_birthweight_by_bin['0']

# Calculate the difference in mean birth weight between each bin and the 0-cigarette bin
mean_diff_from_0 = mean_birthweight_by_bin - mean_birthweight_0

print("Mean birth weight by cigarette bin:")
print(mean_birthweight_by_bin)

print("\nMean difference in birth weight compared to 0-cigarette bin:")
print(mean_diff_from_0)

print("\n2b) Under what circumstances can one idenitfy the average treatment effect of maternal smoking by comparing" + 
      " the unadjusted difference in mean birth weight of infants of smoking and non-smoking mothers?")

print("- For one to identify the difference there would need to be no omitted variables that may have an impact - i.e. all" +
      "all else would need to be help constant (ceritus paribus). ")

# Define treatment and control groups
treatment_group = df[df['tobacco'] == 0]  # Smoking mothers
control_group = df[df['tobacco'] == 1]    # Non-smoking mothers

# Select covariates to test
covariates = ['dmage', 'alcohol', 'cigar', 'wgain', 'pldel3', 'dmeduc', 'adequacy', 'nlbnl', 'monpre', 'nprevist',
              'isllb10']

# Initialize results dictionary
results = {
    'Covariate': [],
    'Overall Mean': [],
    'Smoking Mean': [],
    'Non-Smoking Mean': [],
    'p-value': [],
    't-stat': [],
    'Covariate-Outcome Corr': [],
    'Covariate-Treatment Corr': [],
    'Bias Sign': []
}

# Calculate means and p-values for each covariate
for covariate in covariates:
    overall_mean = df[covariate].mean()
    smoking_mean = treatment_group[covariate].mean()
    non_smoking_mean = control_group[covariate].mean()
    
    # Perform t-test between smoking and non-smoking groups
    t_stat, p_val = ttest_ind(treatment_group[covariate], control_group[covariate])
    
    # Append results
    results['Covariate'].append(covariate)
    results['Overall Mean'].append(overall_mean)
    results['Smoking Mean'].append(smoking_mean)
    results['Non-Smoking Mean'].append(non_smoking_mean)
    results['p-value'].append(p_val)
    results['t-stat'].append(t_stat)

    cov_outcome_corr, _= pearsonr(df[covariate], df['dbrwt'])
    cov_treatment_corr, _ = pearsonr(df[covariate], df['tobacco'])
    bias_sign = cov_outcome_corr * cov_treatment_corr

    results['Covariate-Outcome Corr'].append(cov_outcome_corr)
    results['Covariate-Treatment Corr'].append(cov_treatment_corr)
    results['Bias Sign'].append(bias_sign)

# Create DataFrame for the results table
table_df = pd.DataFrame(results)

# Display the table
print(table_df)

'''
2e
'''

# Define the formula for the regression: dbrwt ~ tobacco (binary variable for smoking status)
formula = 'dbrwt ~ tobacco'

# Fit the model with robust standard errors
model = smf.ols(formula, data=df).fit(cov_type='HC3')  # HC3 is a robust estimator for standard errors

# Print the regression summary
print(model.summary())

# Define the formula for the regression: dbrwt ~ tobacco (binary variable for smoking status)
formula = 'dbrwt ~ cigar'

# Fit the model with robust standard errors
model = smf.ols(formula, data=df).fit(cov_type='HC3')  # HC3 is a robust estimator for standard errors

# Print the regression summary
print(model.summary())

'''
2f
'''

# Choose covariates to include in the model
covariates = ['tobacco', 'dmage', 'wgain', 'dmeduc', 'alcohol', 'adequacy']

# Define the formula with multiple covariates
formula_with_covariates = 'dbrwt ~ tobacco + dmage + wgain + dmeduc + alcohol + adequacy'

# Fit the model with robust standard errors
model_with_covariates = smf.ols(formula_with_covariates, data=df).fit(cov_type='HC3')

# Print the regression summary
print(model_with_covariates.summary())

'''
2g
'''

# Define the formula with the added "useless" controls
formula_with_useless_controls = 'dbrwt ~ tobacco + dmage + wgain + dmeduc + alcohol + adequacy + csex'

# Fit the model with robust standard errors
model_with_useless_controls = smf.ols(formula_with_useless_controls, data=df).fit(cov_type='HC3')

# Print the regression summary
print(model_with_useless_controls.summary())

'''
2h
'''
# Let's assume 'health_complications' is the column for maternal health issues
# Define the formula with the "bad" control added
formula_with_bad_control = 'dbrwt ~ tobacco + dmage + wgain + dmeduc + alcohol + adequacy + lung'

# Fit the model with robust standard errors
model_with_bad_control = smf.ols(formula_with_bad_control, data=df).fit(cov_type='HC3')

# Print the regression summary
print(model_with_bad_control.summary())