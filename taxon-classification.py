import pandas as pd
from datetime import datetime

# Read in cleaned-up data file
outputs_dir = 'outputs'
today = datetime.now().strftime('%Y%m%d') 
df = pd.read_csv(f'{outputs_dir}/{today}_df-with-taxonomy-annotated.csv') 

# Currently, there are 54 maximum ranks
cols_to_check = df.loc[:, '0':'53'].columns
ranks = ['Animalia', 'Bilateria', 'Deuterostomia', 'Protostomia', 'Arthropoda', 'Chordata', 'Vertebrata', 'Actinopterygii', 'Chondrichthyes', 'Tetrapoda', 'Amniota', 'Diapsida', 'Synapsida', 'Therapsida', 'Sauropsida', 'Archosauromorpha', 'Pseudosuchia', 'Dinosauromorpha', 'Dinosauria', 'Ornithischia', 'Saurischia', 'Mammaliaformes', 'Marsupialiformes', 'Placentalia', 'Theria', 'Avialae', 'Aves']
for rank in ranks:
    df[rank] = df[cols_to_check].apply(lambda row: rank in row.values, axis=1)

## Double condition classifications

condition = (df['Animalia'] == True) & (df['Bilateria'] == False)
df.loc[condition, 'classification'] = 'Non-bilaterian metazoans'
condition = (df['Protostomia'] == True) & (df['Arthropoda'] == False)
df.loc[condition, 'classification'] = 'Non-arthropod protostomes'
condition = (df['Deuterostomia'] == True) & (df['Chordata'] == False)
df.loc[condition, 'classification'] = 'Non-chordate deuterostomes'
condition = (df['Chordata'] == True) & (df['Vertebrata'] == False)
df.loc[condition, 'classification'] = 'Non-vertebrate chordates'
condition = (df['Protostomia'] == True) & (df['Chordata'] == False)
df.loc[condition, 'classification'] = 'Protostomes'
condition = (df['Vertebrata'] == True) & (df['Tetrapoda'] == False)
df.loc[condition, 'classification'] = 'Fish (misc. fish)'
condition = (df['Tetrapoda'] == True) & (df['Amniota'] == False)
df.loc[condition, 'classification'] = 'Amphibians and friends'
condition = (df['Amniota'] == True) & (df['Diapsida'] == False)
df.loc[condition, 'classification'] = 'Non-diapsid amniotes'
condition = (df['Therapsida'] == True) & (df['Mammaliaformes'] == False)
df.loc[condition, 'classification'] = 'Non-mammaliaform therapsid'
condition = (df['Mammaliaformes'] == True) & (df['Theria'] == False)
df.loc[condition, 'classification'] = 'Non-therian mammaliaforms'
condition = (df['Diapsida'] == True) & (df['Archosauromorpha'] == False)
df.loc[condition, 'classification'] = 'Non-archosauromorph diapsids'
condition = (df['Archosauromorpha'] == True) & ((df['Dinosauromorpha'] == False) | (df['Pseudosuchia'] == False))
df.loc[condition, 'classification'] = 'Non-archosaur archosauromorphs'
condition = (df['Dinosauromorpha'] == True) & (df['Dinosauria'] == False)
df.loc[condition, 'classification'] = 'Non-dinosaur dinosauromorphs'
condition = (df['Saurischia'] == True) & (df['Avialae'] == False)
df.loc[condition, 'classification'] = 'Dinosaurs (non-avian saurischians)'
condition = (df['Sauropsida'] == True) & (df['Diapsida'] == False)
df.loc[condition, 'classification'] = 'Non-diapsid sauropsids'

## Single condition classifications
condition = (df['Animalia'] == False)
df.loc[condition, 'classification'] = 'Non-metazoans'
condition = (df['Theria'] == True)
df.loc[condition, 'classification'] = 'Mammals (misc. therian mammals)'
condition = (df['Arthropoda'] == True)
df.loc[condition, 'classification'] = 'Invertebrates (arthropods)'
condition = (df['Avialae'] == True) | (df['Aves'] == True)
df.loc[condition, 'classification'] = 'Dinosaurs (birds)'
condition = (df['Placentalia'] == True)
df.loc[condition, 'classification'] = 'Placental mammals'
condition = (df['Actinopterygii'] == True)
df.loc[condition, 'classification'] = 'Fish (actinopterygians)'
condition = (df['Chondrichthyes'] == True)
df.loc[condition, 'classification'] = 'Fish (chondrichthyans)'
condition = (df['Ornithischia'] == True)
df.loc[condition, 'classification'] = 'Dinosaurs (ornithischians)'
condition = (df['Pseudosuchia'] == True)
df.loc[condition, 'classification'] = 'Crocodiles and friends'
condition = (df['Marsupialiformes'] == True)
df.loc[condition, 'classification'] = 'Mammals (marsupials, etc.)'

df.to_csv(f'{outputs_dir}/{today}_df-classified.csv')

print('Analysis concluded.\n')