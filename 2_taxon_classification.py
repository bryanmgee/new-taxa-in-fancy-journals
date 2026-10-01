import glob
import pandas as pd
import os
from datetime import datetime

# Read in cleaned-up data file
outputs_dir = 'outputs'
today = datetime.now().strftime('%Y%m%d') 

file_pattern = f'{outputs_dir}/*_dataset-with-taxonomy_edited.csv'

try:
    most_recent_file = max(glob.iglob(file_pattern), key=os.path.getmtime)
    df = pd.read_csv(most_recent_file, dtype='str')
    if df is not None:
        print(f'Imported data file: {most_recent_file}.\n') 
        total = len(df)

except ValueError:
    print(f'No files matched the given pattern ({file_pattern}).')

# Summarize all taxa counts
## Currently, there are 71 maximum ranks
rank_columns = df.loc[:, '0':'70'].columns

ranks = ['Problematica', 'Eukaryota', 'Plantae', 'Fungi', 'Prokaryota', 'Protozoa', 'Chromalveolata', 'Animalia', 'Bilateria', 'Cyclostomi', 'Deuterostomia', 'Protostomia', 'Lophophorata', 'Mollusca', 'Panarthropoda', 'Insecta', 'Chordata', 'Vertebrata', 'Gnathostomata', 'Actinopterygii', 'Sarcopterygii', 'Chondrichthyes', 'Tetrapodomorpha', 'Tetrapoda', 'Amphibia', 'Amniota', 'Lepidosauromorpha', 'Archosauromorpha', 'Pantestudines', 'Pseudosuchia', 'Avemetatarsalia', 'Dinosauromorpha', 'Dinosauria', 'Ornithischia', 'Saurischia', 'Theropoda', 'Mammaliamorpha', 'Mammaliaformes', 'Mammalia', 'Marsupialiformes', 'Placentalia', 'Primates', 'Theria', 'Avialae', 'Aves']
for rank in ranks:
    df[rank] = df[rank_columns].apply(lambda row: rank in row.values, axis=1)

# Categorization
condition = (df['Plantae'] == True) | (df['Fungi'] == True)
df.loc[condition, 'classification'] = 'Plants and fungi'
condition = (df['Animalia'] == True) & (df['Bilateria'] == False)
df.loc[condition, 'classification'] = 'Non-bilaterian metazoans'
condition = (df['Lophophorata'] == True)
df.loc[condition, 'classification'] = 'Lophophorates'
condition = (df['Insecta'] == True)
df.loc[condition, 'classification'] = 'Insects'
condition = (df['Panarthropoda'] == True) & (df['classification'].isna())
df.loc[condition, 'classification'] = 'Non-insect pan-arthropods'
condition = (df['Mollusca'] == True)
df.loc[condition, 'classification'] = 'Molluscs'
condition = (df['Deuterostomia'] == True) & (df['Chordata'] == False)
df.loc[condition, 'classification'] = 'Non-chordate deuterostomes'
condition = (df['Actinopterygii'] == True)
df.loc[condition, 'classification'] = 'Fish (actinopterygians)'
condition = (df['Chondrichthyes'] == True)
df.loc[condition, 'classification'] = 'Fish (chondrichthyans)'
condition = (df['Chordata'] == True) & (df['Tetrapodomorpha'] == False) & ((df['Vertebrata'] == True) | (df['Cyclostomi'] == True)) & (df['classification'].isna())
df.loc[condition, 'classification'] = 'Fish (other)'
condition = (df['Tetrapodomorpha'] == True) & ((df['Amphibia'] == False) & (df['Amniota'] == False))
df.loc[condition, 'classification'] = 'Amphibians'
condition = (df['Amphibia'] == True)
df.loc[condition, 'classification'] = 'Amphibians'
condition = (df['Lepidosauromorpha'] == True)
df.loc[condition, 'classification'] = 'Lepidosauromorphs'
condition = (df['Pantestudines'] == True)
df.loc[condition, 'classification'] = 'Pantestudines'
condition = (df['Pseudosuchia'] == True)
df.loc[condition, 'classification'] = 'Pseudosuchians'
condition = (df['Mammaliamorpha'] == True)
df.loc[condition, 'classification'] = 'Non-primate mammaliamorphs'
condition = (df['Primates'] == True)
df.loc[condition, 'classification'] = 'Primates'
condition = (df['Avemetatarsalia'] == True)
df.loc[condition, 'classification'] = 'Non-avian avemetatarsalians'
condition = (df['Avialae'] == True) | (df['Aves'] == True)
df.loc[condition, 'classification'] = 'Avians'
condition = (df['Amniota'] == True) & (df['classification'].isna())
df.loc[condition, 'classification'] = 'Other amniotes'
condition = (df['2'].isna())
df.loc[condition, 'classification'] = 'Other'

## Catch-all for anything remaining
condition = (df['classification'].isna())
df.loc[condition, 'classification'] = 'Other'

unclassified = df['classification'].isna().sum()
print(f'Number of unclassified taxa: {unclassified} (includes multi-species genera).\n')

df.to_csv(f'{outputs_dir}/{today}_dataset-classified.csv', index=False, encoding='utf-8-sig')

print('Taxonomic re-classification concluded.\n')