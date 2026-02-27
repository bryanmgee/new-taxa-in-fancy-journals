import os
import pandas as pd
import requests
from datetime import datetime

# To test with small number of taxa against API (to make sure the call works)
test = False

# Read in latest version of file
df = pd.read_csv('input-data.csv')
print(f'Imported file with {len(df)} entries.\n')

# Write time-stamped input file for archival purposes
today = datetime.now().strftime('%Y%m%d') 
df.to_csv(f'outputs/{today}_input-data.csv')

# Create outputs directory
if os.path.isdir('outputs'):
        print('outputs directory found - no need to recreate.\n')
else:
    os.mkdir('outputs')
    print('outputs directory has been created.\n')
outputs_dir = 'outputs'

# Remove articles with no actual new species
df_clean = df.dropna(subset='novel_taxon', ignore_index=True)
print(f'Processing file with {len(df_clean)} entries.\n')

# Extract genus
df_clean['genus'] = df_clean['novel_taxon'].str.split().str[0]

## Deduplicate for counts
df_unique = df_clean.drop_duplicates(subset=['genus'])
print(f'Retrieving information on {len(df_unique)} genera.\n')
if test:
    df_unique = df_unique.head(5)

results = []
for clade in df_clean['genus']:
    print(f'Retrieving taxonomy of {clade}...\n')
    try:
        response = requests.get(f'https://paleobiodb.org/data1.2/taxa/list.json?name={clade}&rel=all_parents')
        data = response.json()
        records = data['records']
        names = [d['nam'] for d in records]
        results.append(names)
    except requests.RequestException as e:
        print(f'Error retrieving page: {e}')

df_taxonomic_ranks = pd.DataFrame(results)

df_taxonomic_ranks['genus'] = df_clean['genus']
df_taxonomic_ranks.to_csv(f'{outputs_dir}/{today}_df-ranks-taxonomy.csv', index=False)

df_expanded = pd.merge(df_clean, df_taxonomic_ranks, left_index=True, right_index=True)
df_expanded.to_csv(f'{outputs_dir}/{today}_df-with-taxonomy.csv', index=False)

print('Analysis concluded.\n')