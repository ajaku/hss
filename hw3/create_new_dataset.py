import pandas as pd

'''
rectype (record type)
1 - res
2 - nonres

restatus (resident status)
1 - res
2 - intra nonres ()
3 - inter nonres 
4 - foreign

pldel (place of facility of birth)
1 - hosp.
2 - birthing center
3 - clinic/doc off.
4 - residence
5 - other
9 - unknown

pldel 3 (facility of birth recode)
1 - hosp.
2 - not hosp.
3 - unknown

birattnd (attendant at birth)
1 - M.D (medicine)
2 - D.O (osteopathy)
3 - nurse midwife
4 - other midwife
5 - other
9 - unknown

stsubocc (state subcode of occurance)
appears to always be 3? so vermont? idk

stoccfip (state of occurance)
appears to always be 42? so pennsylvania

cntocpop (size of county of occurance)
0 - 1mil +
1 - 500k - 1mil
2 - 250k - 500k
3 - 100k - 250k
9 - <100k

stresfip (state of residence)
how is this diff from stsubocc, stoccfip?

dmage (age of mother)
btwn 10-49

ormoth (hispanic origin of mother)
0 - non hisp.
1 - mexican
2 - puerto rican
3 - cuban
4 - central/south american
5 - other and unknown
9 - unknown

orracem (hispanic origin and race of mother)
1 - mexican
2 - puerto rican
3 - cuban
4 - central or south am.
5 - other unknown
6 - non-hispanic white
7 - non-hispanic black
8 - non-hispanic other
9 - unknown

mrace3 (race of mother)
1 - white
2 - other
3 - black

dmeduc (education of mother)
00 - none
01-08 - elementary years
09 - 1 yr hs
...
17 - 5 yr college (adds by 1 per year w/ this as max)
99 - unknown

dmar (marital status of mother)
1 - married
2 - unmarried

mplbirr (mother birth place)
maps to a state
99 - non-classifiable

adequacy (adequacy of care records (kessner idx))
1 - adequate
2 - intermediate
3 - inadequate
4 - unknown

nlbnl (number of live births, now living)
00-30 - num births
99 - unknown

dlivord (sum of live births now living and now dead + 1)
00-31 - num of children born alive

dtotord (sum of live birth order and other terminations)
01-40 - total num. of live births and other terms.
99 - unknown

totord9 (total birth order recode)
1-8 - num of children
9 - unknown

monpre (month pregnancy prenatal care began)
00 - none
01-09 - months 1 to 9
99 - unknown

nprevist (num of prenatal visits)
00 - none
01-48 - num visits
49 - 49 or more visits
99 - unknown

disllb (interval since last birth up to this one)
777 - no prev.
000 - zero months (plural birth)
001-468 - num months
999 - unknown

isllb10 (interval since last live birth)
00 - no prev.
01 - zero months (plural birth)
03-09 - month ranges
10 - unknown

dfage (age of father)
10-98 - age
99 - unknown

orfath (hisp. origin of father)
0 - non-hisp.
1 - mexican
2 - puerto rican
3 - cuban
4 - central or south am.
5 - other 
9 - unknown

frace4 (race of father)
1 - white
2 - other
3 - black
4 - unknown

dfeduc (education of father)
00 - none
01-08 - elementary years
09 - 1 yr hs
...
17 - 5 yr college (adds by 1 per year w/ this as max)
99 - unknown

birmon (month of birth)
01-12 - map to month

weekday (day of the week)
1-7 - sun - sat

dgestat (gestation detail in weeks)
17-41 - 17th through 47th week of gestation
99 - unknown

csex (sex of child)
1 - male
2 - female

dbrwt (birth weight in grams) - typo in excel sheet
0227-8165 - num. grams
9999 - unknown

dplural (multiple kids at once)
1-5 - single, twin, ... quintuplet or higher

omaps (one minute apgar score)
00-10 - score of apgar
99 - unknown

fmaps (five minute apgar score)
00-10 : score of apgar
99 - unknown

clingest (clinical estimation of gestation)
17-47 - estimated gestation in weeks
99 - unknown

delmeth5 (method of delivery)
1 - vaginal
2 - vaginal after previous c-section
3 - primary c-section
4 - repeat c-section
5 - unknown

anemia (hct < 30/hgb <10)
1 -  anemia
2 -  no anemia

cardiac (cardiac dissease)
1 -  cardiac
2 -  no cardiac

lung (lung dissease)
1 -  lung
2 -  no lung

diabetes (diabetes dissease)
1 -  diabetes
2 -  no diabetes

herpes (herpes dissease)
1 -  herpes
2 -  no herpes

chyper (chyper dissease)
1 -  chyper
2 -  no chyper

phyper (phyper dissease)
1 -  phyper
2 -  no phyper

pre4000 (previous infant 4000+ grams)
1 -  pre4000
2 -  no pre4000

preterm (previous preterm or small-for-gestation-age infant)
1 - preterm
2 - no preterm

tobacco (tobacco use)
1 - yes
2 - no
9 - unknown

cigar (avg. num. cigs per day)
00-97 - num cigs.
98 - 98 or more cigs.
99 - unknown

cigar6 (avg. num cigs. per day recode)
useless just delete

alcohol (use of alc.)
1 - yes
2 - no
9 - unknown

drink (avg. num drinks per week)
00-97 - num drinks per week
98 - 98 or more per week
99 - unknown

drink5 (drinks recode)
just delete

wgain (weight gain)
00-97 - num. lbs
98 - 98 or more lbs
99 - unknown

'''

# Load your data into a DataFrame (replace 'data.csv' with your actual filename)
df = pd.read_csv('pennbirthwgt0.csv')

# Define "unknown" values across different columns
unknown_values = {
    'pldel': [9],
    'pldel3': [3],
    'birattnd': [9],
    'cntocpop': [9],
    'ormoth': [5, 9],
    'orracem': [9],
    'mrace3': [9],
    'dmeduc': [99],
    'dmar': [9],  # assuming if 9 exists as unknown
    'adequacy': [4],
    'nlbnl': [99],
    'totord9': [9],
    'monpre': [99],
    'nprevist': [99],
    'disllb': [999],
    'isllb10': [10],
    'dfage': [99],
    'orfath': [9],
    'frace4': [4],
    'dfeduc': [99],
    'dgestat': [99],
    'dbrwt': [9999],
    'omaps': [99],
    'fmaps': [99],
    'clingest': [99],
    'delmeth5': [5],
    'cigar': [99],
    'alcohol': [9],
    'drink': [99],
    'wgain': [99],
    'preterm': [9],
    'phyper': [9],
    'chyper': [9],
    'herpes': [9],
    'diabetes': [9],
    'lung': [9],
    'cardiac': [9],
    'anemia': [9]
}

# Drop rows with "unknown" values
for col, unknown_vals in unknown_values.items():
    df = df[~df[col].isin(unknown_vals)]

df['adequacy'] = df['adequacy'].replace({1: 1, 2: 0, 3: 0})

# Columns to map (1, 2) to (0, 1)
binary_columns = [
    'rectype', 'restatus', 'pldel3', 'birattnd', 'dmar', 'anemia',
    'cardiac', 'lung', 'diabetes', 'herpes', 'chyper', 'phyper', 'pre4000', 
    'preterm', 'tobacco', 'alcohol'
]

# Remap (1, 2) to (0, 1) for binary columns
# 0 means use it, 1 means don't use
# let's remap this to 0 means dont use, 1 means use
df[binary_columns] = df[binary_columns].replace({1: 1, 2: 0})

# Drop unnecessary columns
columns_to_keep = ['dbrwt', 'tobacco', 'dmage', 'alcohol', 'csex', 'lung', 'cigar', 'wgain', 'pldel3', 'dmeduc', 'adequacy', 'nlbnl', 'monpre', 'nprevist', 'isllb10']
df_filtered = df[columns_to_keep]

# Save the cleaned data to a new CSV file
df_filtered.to_csv('cleaned_data.csv', index=False)

print("Data cleaned and saved to 'cleaned_data.csv'")
