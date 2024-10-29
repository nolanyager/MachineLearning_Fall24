# %%
# Import Packages Test: 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%
#Current WD:
import os
cwd = os.getcwd()
print(cwd)

# %%
# Loading NRI data and specifying STCOFIPS as a string column
nri_data = pd.read_csv("../data/raw/NRI_Data_By_County.csv", dtype={'STCOFIPS': str})

# Subsetting: 
columns_to_keep = ['STCOFIPS'] + [col for col in nri_data.columns if col.endswith('_AFREQ') or col.endswith('_RISKR')]
nri_subset = nri_data[columns_to_keep]

# %%
# Loading SVI data and telling python FIPS is a string 
svi_data = pd.read_csv("../data/raw/SVI_2022_Data_By_County.csv", dtype={'FIPS': str})


# %%
# Subsetting SVI data
columns_to_keep = [
    'ST', 'STATE', 'ST_ABBR', 'STCNTY', 'COUNTY', 'FIPS', 'LOCATION', 'AREA_SQMI',
    'E_TOTPOP', 'EP_POV150', 'EP_UNEMP', 'EP_HBURD', 'EP_NOHSDP', 'EP_UNINSUR', 
    'EP_AGE65', 'EP_AGE17', 'EP_DISABL', 'EP_SNGPNT', 'EP_LIMENG', 'EP_MINRTY', 
    'EP_MUNIT', 'EP_MOBILE', 'EP_CROWD', 'EP_NOVEH', 'EP_GROUPQ', 'EP_NOINT', 
    'EP_AFAM', 'EP_HISP', 'EP_ASIAN', 'EP_AIAN', 'EP_NHPI', 'EP_TWOMORE', 'EP_OTHERRACE'
]

# %%
# Creating the subset: 
svi_subset = svi_data[columns_to_keep]


# %%
# Extracting both FIPS codes as sets: 
nri_fips = set(nri_subset['STCOFIPS'])
svi_fips = set(svi_subset['FIPS'])

# %%
# FIPS in NRI, but not in SVI data: 
fips_in_nri_not_svi = nri_fips - svi_fips

# %%
# Vice versa: FIPS in SVI, but not in NRI: 
fips_in_svi_not_nri = svi_fips - nri_fips

# %%
# Printing both: 
print(f"FIPS codes in NRI but not in SVI: {fips_in_nri_not_svi}")
print(f"FIPS codes in SVI but not in NRI: {fips_in_svi_not_nri}")

# %%
# Renaming STCOFIPS in NRI to FIPS (simpler, aligned with SVI data)
nri_subset = nri_subset.rename(columns={'STCOFIPS': 'FIPS'})

# %%
# Perform outer join on the FIPS code 
nri_svi_merged = pd.merge(nri_subset, svi_subset, on='FIPS', how='outer')

# %%
# Printing it to check: 
print(nri_svi_merged.head())

nri_svi_merged.to_csv('../data/processed/nri_svi_merged.csv', index=False)
