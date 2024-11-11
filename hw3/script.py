import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import pearsonr
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col
from stargazer.stargazer import Stargazer
import imgkit
from PIL import Image
from bs4 import BeautifulSoup

def perf_multi_lin_reg(df, formula, x_p_labels, y_p, name):
    # Fit the model with robust standard errors
    model = smf.ols(formula, data=df).fit(cov_type='HC3')
    
    # Render the model using Stargazer
    stargazer = Stargazer([model])
    html = stargazer.render_html()
    
    # Replace predictor names with more readable labels
    for var, label in x_p_labels.items():
        html = html.replace(var, label)
    html = html.replace(model.model.endog_names, y_p)  # Replace the dependent variable name

    const = f"Intercept (β₀)"
    html = html.replace("Intercept", const)
    
    # Parse the HTML
    soup = BeautifulSoup(html, "html.parser")

    # Locate the Intercept (β₀) and Tobacco (β₁) rows
    intercept_row = None
    tobacco_row = None
    for row in soup.find_all("tr"):
        if "Intercept (β₀)" in row.text:
            intercept_row = row
        elif "Tobacco (β₁)" in row.text:
            tobacco_row = row

    # Ensure Tobacco rows follow Intercept rows
    if intercept_row and tobacco_row:
        # Find the rows following Intercept and insert Tobacco there
        intercept_next_row = intercept_row.find_next_sibling("tr")
        
        # Remove Tobacco rows and their parentheses row to reinsert them
        tobacco_row_next = tobacco_row.find_next_sibling("tr")
        tobacco_row.extract()
        tobacco_row_next.extract()

        # Insert Tobacco rows directly after Intercept rows
        intercept_next_row.insert_after(tobacco_row_next)
        intercept_next_row.insert_after(tobacco_row)

    # Get the modified HTML
    sorted_html = str(soup)
    html = sorted_html

    # Save the HTML to an image file
    img_name = f"{name}.png"
    imgkit.from_string(html, img_name)
    img = Image.open(img_name)

    # Crop the image if necessary
    cropped_img = img.crop((0, 0, img.width - 475, img.height))
    cropped_img.save(img_name)

df = pd.read_csv('cleaned_data.csv')

'''
1g
'''

'''
2a
'''
print((df.describe()).T)

# Define treatment and control groups
treatment_group = df[df['tobacco'] == 0]  # Smoking mothers
control_group = df[df['tobacco'] == 1]    # Non-smoking mothers


smoking_mean = (treatment_group['dbrwt']).mean()
non_smoking_mean = (control_group['dbrwt']).mean()
print(smoking_mean)
print(non_smoking_mean)
print(smoking_mean - non_smoking_mean)
print("Mean birth weight for smokers:", smoking_mean)
print("Mean birth weight for non-smokers:", non_smoking_mean)
print("Mean difference in birth weight by smoking status (smokers vs. non-smokers):", (smoking_mean - non_smoking_mean))

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

'''
2b
'''
print("\n2b) Under what circumstances can one idenitfy the average treatment effect of maternal smoking by comparing" + 
      " the unadjusted difference in mean birth weight of infants of smoking and non-smoking mothers?")

print("- For one to identify the difference there would need to be no omitted variables that may have an impact - i.e. all" +
      "all else would need to be help constant (ceritus paribus). ")

'''
2c
'''

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
2d
'''

# We can use the data based signs of the correlations to make this analysis - idk how to really state the direction in one way or another in most of these cases


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

# Define variable labels for each model
x_p_labels= {
    'tobacco': 'Tobacco (β₁)'
}

x_p_labels_useless = {
    'tobacco': 'Tobacco (β₁)',
    'dmage': 'Mother’s Age',
    'wgain': 'Weight Gain',
    'dmeduc': 'Education',
    'alcohol': 'Alcohol',
    'adequacy': 'Prenatal Care Adequacy',
    'csex': 'Child Sex'
}

x_p_labels_bad = {
    'tobacco': 'Tobacco (β₁)',
    'dmage': 'Mother’s Age',
    'wgain': 'Weight Gain',
    'dmeduc': 'Education',
    'alcohol': 'Alcohol',
    'adequacy': 'Prenatal Care Adequacy',
    'lung': 'Lung Health'
}

# Generate outputs for each model
perf_multi_lin_reg(df, 
                   formula, 
                   x_p_labels, 
                   "Infant Birth Weight", 
                   "model_simple")
perf_multi_lin_reg(df, 
                   formula_with_useless_controls, 
                   x_p_labels_useless, 
                   "Infant Birth Weight", 
                   "model_useless")

perf_multi_lin_reg(df, 
                   formula_with_bad_control, 
                   x_p_labels_bad, 
                   "Infant Birth Weight", 
                   "model_bad")