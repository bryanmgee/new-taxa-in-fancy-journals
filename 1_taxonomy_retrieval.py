import csv
import os
import pandas as pd
import re
import requests
import time
from datetime import datetime
from rich.progress import track

###################################################################################
### To test with small number of taxa against API (to make sure the call works) ###
###################################################################################
test = True

# Read in latest version of file
df = pd.read_csv('input-data.csv')
print(f'Imported file with {len(df)} entries.\n')

# Write time-stamped input file for archival purposes
today = datetime.now().strftime('%Y%m%d') 
df.to_csv(f'outputs/{today}_input-data.csv', encoding='utf-8-sig')

# Create outputs directory
if os.path.isdir('outputs'):
        print('outputs directory found - no need to recreate.\n')
else:
    os.mkdir('outputs')
    print('outputs directory has been created.\n')
outputs_dir = 'outputs'

# Remove articles with no actual new species
df_names = df.dropna(subset='novel_taxon', ignore_index=True)
print(f'Processing {len(df_names)} unique species names.\n')

# Basic whitespace cleaning for (potential) common issue
df_names['doi'] = df_names['doi'].str.strip()
df_names['title'] = df_names['title'].str.strip()
df_names['novel_taxon'] = df_names['novel_taxon'].str.strip()
df_names['age1'] = df_names['age1'].str.strip()
df_names['age2'] = df_names['age2'].str.strip()

# Extract genus
df_names['genus'] = df_names['novel_taxon'].str.split().str[0]
## Removing '?' around genus names (https://stackoverflow.com/questions/50444346/fast-punctuation-removal-with-pandas)
punc = re.compile(r'[^\w\s]+')
df_names['genus'] = [punc.sub('', x) for x in df_names['genus'].tolist()]

df_names.to_csv('outputs/test-cleaning.csv')

## Deduplicate for counts
df_unique = df_names.drop_duplicates(subset=['genus'])
df_unique = df_unique.sort_values(by='genus')

if test:
    df_unique = df_unique.head(50)
print(f'Retrieving taxonomic ranks for {len(df_unique)} unique genera.\n')

results = []
errors = []

for clade in track(df_unique['genus'], description='Retrieving ranks...'):
    # print(f'Retrieving taxonomy of {clade}...\n')
    try:
        response = requests.get(f'https://paleobiodb.org/data1.2/taxa/list.json?name={clade}&rel=all_parents')
        data = response.json()
        records = data['records']
        names = [d['nam'] for d in records]
        results.append(names)
        time.sleep(0.4) # Manual rate-limiting
    except requests.exceptions.Timeout:
        errors.append(clade)
    except requests.RequestException as e:
        print(f'Error retrieving data for {clade}: {e}')
        errors.append(clade)

df_taxonomic_ranks = pd.DataFrame(results)
# Print any failed retrievals (API issues)
print(f"\nNumber of failed API calls: {len(errors)}\n")
if len(errors) > 0:
    print(errors)

# Saving failed retrievals
with open(f'{outputs_dir}/{today}_failed-retrievals.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['genus']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()
    for item in errors: writer.writerow({'genus': clade})

# Extract right-most value (genus from PBDB, blank if no match in PBDB)
df_taxonomic_ranks['genus'] = df_taxonomic_ranks.ffill(axis=1).iloc[:, -1]
# Move the newly created last column (genus) to the front
cols = list(df_taxonomic_ranks.columns)
df_taxonomic_ranks = df_taxonomic_ranks[[cols[-1]] + cols[:-1]]
# Calculate number of entries for which rank info was not retrieved
missing_genera = df_taxonomic_ranks['genus'].isna().sum()
missing_prop = round((missing_genera / len(df_unique)) * 100)
print(f'Number of genera that ranks were not retrieved for: {missing_genera} out of {len(df_unique)} ({missing_prop}%)\n')
df_taxonomic_ranks = df_taxonomic_ranks.dropna(subset=['genus'])
df_taxonomic_ranks['source'] = 'PBDB API'

# Combine with input data
df_expanded = pd.merge(df_names, df_taxonomic_ranks, how='left', on='genus')
df_expanded.to_csv(f'{outputs_dir}/{today}_dataset-with-taxonomy.csv', index=False, encoding='utf-8-sig')

# Begin staging for manual editing
## Hard-coding known replacement names
df_expanded.loc[df['genus'] == 'Cabralia', 'genus'] = 'Sangaia'
df_expanded.loc[df['genus'] == 'Cerkesia', 'genus'] = 'Hamamlia'
df_expanded.loc[df['genus'] == 'Chlamyphractus', 'genus'] = 'Chlamydophractus'
df_expanded.loc[df['genus'] == 'Cooperithyris', 'genus'] = 'Sinaithyris'
df_expanded.loc[df['genus'] == 'Galanthis', 'genus'] = 'Galanthisictis'
df_expanded.loc[df['genus'] == 'Heterocladus', 'genus'] = 'Jimaodanus'
df_expanded.loc[df['genus'] == 'Laputa', 'genus'] = 'Laputavis'
df_expanded.loc[df['genus'] == 'Lyra', 'genus'] = 'Lyrakeryx'
df_expanded.loc[df['genus'] == 'Matapa', 'genus'] = 'Matapanui'
df_expanded.loc[df['genus'] == 'Palmula', 'genus'] = 'Palmulasaurus'
df_expanded.loc[df['genus'] == 'Psammorhynchus', 'genus'] = 'Priscosturion'
df_expanded.loc[df['genus'] == 'Scalaria', 'genus'] = 'Scalaridelphys'
df_expanded.loc[df['genus'] == 'Sullivania', 'genus'] = 'Sullivanosaurus'
df_expanded.loc[df['genus'] == 'Wenzia', 'genus'] = 'Swenzia'

df_expanded.to_csv(f'{outputs_dir}/{today}_dataset-with-taxonomy_edited.csv', index=False, encoding='utf-8-sig')

print('Taxonomic rank retrieval concluded.\n')