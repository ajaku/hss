import pandas as pd
import glob
import os

# Will stitch the python files
# Worked hand in hand w/ mr. chat

csv_files = sorted(glob.glob('*.csv'))
try:
    if (os.path.exists('fmli221.csv')):
        csv_files.remove('fmli221.csv')
    if (os.path.exists('fmli.csv')):
        csv_files.remove('fmli.csv')
    if (os.path.exists('filtered_fmli.csv')):
        csv_files.remove('filtered_fmli.csv')
except:
    print("Strange error.")

combined_csv = pd.concat([pd.read_csv(f, low_memory=False) for f in csv_files])
data = combined_csv

keep = [
    'NEWID',
    'FAM_SIZE',
    'NUM_AUTO',
    'FINCBTXM',
    'TOTEXPPQ',
    'TOTEXPCQ',
    'ALCBEVCQ',
    'ALCBEVPQ',
    'FOODCQ',
    'FOODPQ',
    'FDHOMECQ',
    'FDHOMEPQ',
    'FDMAPCQ',
    'FDMAPPQ',
    'FDAWAYCQ',
    'FDAWAYPQ',
    'MAJAPPCQ',
    'MAJAPPPQ',
    'TENTRMNC',
    'TENTRMNP',
    'EDUCACQ',
    'EDUCAPQ',
    'ELCTRCCQ',
    'ELCTRCPQ'
]

filtered_data = data[keep]

columns_to_sum = {
    'TOTEXP' : ['TOTEXPPQ', 'TOTEXPCQ'],
    'ALCBEV': ['ALCBEVCQ', 'ALCBEVPQ'],
    'FOOD': ['FOODCQ', 'FOODPQ'],
    'FDHOME': ['FDHOMECQ', 'FDHOMEPQ'],
    'FDMAP': ['FDMAPCQ', 'FDMAPPQ'],
    'FDAWAY': ['FDAWAYCQ', 'FDAWAYPQ'],
    'MAJAPP': ['MAJAPPCQ', 'MAJAPPPQ'],
    'TENTRM': ['TENTRMNC', 'TENTRMNP'],
    'EDUCA': ['EDUCACQ', 'EDUCAPQ'],
    'ELCTRC': ['ELCTRCCQ', 'ELCTRCPQ']
}

# Create a dictionary to hold the new summed columns
new_columns = {}

# Sum the specified columns and store in the new_columns dictionary
for new_col, cols in columns_to_sum.items():
    new_columns[new_col] = 4*data[cols].sum(axis=1)

# Create a new DataFrame with the new summed columns
new_data = pd.DataFrame(new_columns)
print(new_data)

# Combine the new DataFrame with the original DataFrame, keeping only the desired columns
filtered_data = pd.concat([data[[
    'NEWID',
    'FAM_SIZE',
    'NUM_AUTO',
    'FINCBTXM',
]], new_data], axis=1)

print(filtered_data)

# Save the modified DataFrame to a new CSV file
filtered_data.to_csv('filtered_fmli.csv', index=False)