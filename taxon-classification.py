import pandas as pd
from datetime import datetime

# Read in cleaned-up data file
outputs_dir = 'outputs'
today = datetime.now().strftime('%Y%m%d') 
df = pd.read_csv(f'{outputs_dir}/{today}_df-with-taxonomy-annotated.csv') 

# Currently, there are 56 maximum ranks
cols_to_check = df.loc[:, '0':'55'].columns
ranks = ['Plantae', 'Animalia', 'Bilateria', 'Deuterostomia', 'Protostomia', 'Brachiopoda', 'Echinodermata', 'Gastropoda', 'Mollusca', 'Arthropoda', 'Insecta', 'Ostracoda', 'Trilobita', 'Chordata', 'Vertebrata', 'Actinopterygii', 'Chondrichthyes', 'Tetrapodomorpha', 'Tetrapoda', 'Amniota', 'Diapsida', 'Synapsida', 'Therapsida', 'Sauropsida', 'Squamata', 'Archosauromorpha', 'Testudinata', 'Pseudosuchia', 'Pterosauria', 'Dinosauromorpha', 'Dinosauria', 'Ornithischia', 'Saurischia', 'Theropoda', 'Mammaliaformes', 'Marsupialiformes', 'Placentalia', 'Primates', 'Carnivora', 'Rodentia', 'Artiodactyla', 'Perissodactyla', 'Theria', 'Avialae', 'Aves']
for rank in ranks:
    df[rank] = df[cols_to_check].apply(lambda row: rank in row.values, axis=1)

# Fine-grained classification
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
df.loc[condition, 'classification'] = 'Protostomes (other)'
condition = (df['Vertebrata'] == True) & (df['Tetrapoda'] == False)
df.loc[condition, 'classification'] = 'Fish (misc. fish)'
condition = (df['Tetrapodomorpha'] == True) & (df['Tetrapoda'] == False)
df.loc[condition, 'classification'] = 'Stem tetrapods'
condition = (df['Tetrapoda'] == True) & (df['Amniota'] == False)
df.loc[condition, 'classification'] = 'Amphibians and friends'
condition = (df['Amniota'] == True) & (df['Diapsida'] == False)
df.loc[condition, 'classification'] = 'Non-diapsid amniotes'
condition = (df['Therapsida'] == True) & (df['Mammaliaformes'] == False)
df.loc[condition, 'classification'] = 'Non-mammaliaform therapsids'
condition = (df['Mammaliaformes'] == True) & (df['Theria'] == False)
df.loc[condition, 'classification'] = 'Non-therian mammaliaforms'
condition = (df['Diapsida'] == True) & (df['Archosauromorpha'] == False)
df.loc[condition, 'classification'] = 'Non-archosauromorph diapsids'
condition = (df['Archosauromorpha'] == True) & ((df['Dinosauromorpha'] == False) | (df['Pseudosuchia'] == False))
df.loc[condition, 'classification'] = 'Early archosauromorphs'
condition = (df['Dinosauromorpha'] == True) & (df['Dinosauria'] == False)
df.loc[condition, 'classification'] = 'Non-dinosaur dinosauromorphs'
condition = (df['Saurischia'] == True) & (df['Theropoda'] == False)
df.loc[condition, 'classification'] = 'Dinosaurs, saurischians (non-theropods)'
condition = (df['Theropoda'] == True) & (df['Avialae'] == False)
df.loc[condition, 'classification'] = 'Dinosaurs, saurischians (theropods)'
condition = (df['Sauropsida'] == True) & (df['Diapsida'] == False)
df.loc[condition, 'classification'] = 'Non-diapsid sauropsids'

## Single condition classifications
condition = (df['Animalia'] == False)
df.loc[condition, 'classification'] = 'Other non-metazoans'
condition = (df['Plantae'] == True)
df.loc[condition, 'classification'] = 'Plants'
condition = (df['Brachiopoda'] == True)
df.loc[condition, 'classification'] = 'Invertebrates (brachiopods)'
condition = (df['Echinodermata'] == True)
df.loc[condition, 'classification'] = 'Invertebrates (echinoderms)'
condition = (df['Gastropoda'] == True)
df.loc[condition, 'classification'] = 'Invertebrates (gastropods)'
condition = (df['Mollusca'] == True)
df.loc[condition, 'classification'] = 'Invertebrates (molluscs)'
condition = (df['Theria'] == True)
df.loc[condition, 'classification'] = 'Mammals (misc. therian mammals)'
condition = (df['Arthropoda'] == True)
df.loc[condition, 'classification'] = 'Invertebrates (other arthropods)'
condition = (df['Insecta'] == True)
df.loc[condition, 'classification'] = 'Invertebrates (insects)'
condition = (df['Trilobita'] == True)
df.loc[condition, 'classification'] = 'Invertebrates (trilobites)'
condition = (df['Ostracoda'] == True)
df.loc[condition, 'classification'] = 'Invertebrates (ostracods)'
condition = (df['Avialae'] == True) | (df['Aves'] == True)
df.loc[condition, 'classification'] = 'Dinosaurs, saurischians (avians)'
condition = (df['Placentalia'] == True)
df.loc[condition, 'classification'] = 'Mammals, placental (other)'
condition = (df['Primates'] == True)
df.loc[condition, 'classification'] = 'Mammals, placental (primates)'
condition = (df['Actinopterygii'] == True)
df.loc[condition, 'classification'] = 'Fish (actinopterygians)'
condition = (df['Chondrichthyes'] == True)
df.loc[condition, 'classification'] = 'Fish (chondrichthyans)'
condition = (df['Ornithischia'] == True)
df.loc[condition, 'classification'] = 'Dinosaurs, ornithischians'
condition = (df['Pterosauria'] == True)
df.loc[condition, 'classification'] = 'Pterosaurs'
condition = (df['Squamata'] == True)
df.loc[condition, 'classification'] = 'Squamates'
condition = (df['Testudinata'] == True)
df.loc[condition, 'classification'] = 'Turtles'
condition = (df['Pseudosuchia'] == True)
df.loc[condition, 'classification'] = 'Pseudosuchians'
condition = (df['Marsupialiformes'] == True)
df.loc[condition, 'classification'] = 'Mammals, marsupials'
condition = (df['Carnivora'] == True)
df.loc[condition, 'classification'] = 'Mammals, placental (carnivorans)'
condition = (df['Rodentia'] == True)
df.loc[condition, 'classification'] = 'Mammals, placental (rodents)'
condition = (df['Artiodactyla'] == True)
df.loc[condition, 'classification'] = 'Mammals, placental (artiodactyls)'
condition = (df['Perissodactyla'] == True)
df.loc[condition, 'classification'] = 'Mammals, placental (perissodactyls)'

## Create time bins
### Skipping 2025 to group present year into previous bin
bins = [1999, 2000, 2005, 2010, 2015, 2020, 2027]
labels = ['1995-1999', '2000-2004', '2005-2009', '2010-2014', '2015-2019', '2020-2026']

df['publication_year_bin'] = pd.cut(df['year'], bins=bins, labels=labels, right=False)

df.to_csv(f'{outputs_dir}/{today}_df-classified.csv')

print('Analysis concluded.\n')