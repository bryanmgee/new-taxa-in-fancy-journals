import geopandas as gpd
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read in cleaned-up data file
outputs_dir = 'outputs'
today = datetime.now().strftime('%Y%m%d') 
df_classified = pd.read_csv(f'{outputs_dir}/{today}_df-classified.csv')
if df_classified is not None:
    print('Imported data file.\n') 

# Create plots directory
if os.path.isdir('plots'):
        print('plots directory found - no need to recreate.\n')
else:
    os.mkdir('plots')
    print('plots directory has been created.\n')
plots_dir = 'plots'

# Define plot output format
plot_format = 'png'
dpi = 300

# Subset df
fancy = df_classified[(df_classified['journal'] == 'Science') | (df_classified['journal'] == 'Nature')]
sorta_fancy = df_classified[(df_classified['journal'] == 'PNAS') | (df_classified['journal'] == 'Current Biology')]
jvp = df_classified[df_classified['journal'] == 'JVP']
palaeo = df_classified[df_classified['journal'] == 'Palaeontology']

dfs_dict = {
    'nature-science': fancy,
    'pnas-currentbio': sorta_fancy,
    # 'jvp': jvp,
    'palaeontology': palaeo
}
axis_dict = {
    'nature-science': 'Nature/Science',
    'pnas-currentbio': 'PNAS/Current Bio',
    # 'jvp': 'JVP',
    'palaeo': 'Palaeontology'
}

### PLOTTING

# Create color map for fine-grained classification
clade_color_map = {'Plants': "#4FBD4B",
            'Other non-metazoans': "#82997F",
            'Non-bilaterian metazoans': '#000000',
            'Non-chordate deuterostomes': '#000000',
            'Non-vertebrate chordates': '#000000',
            'Fish (actinopterygians)': "#5F79B1",
            'Fish (chondrichthyans)': '#5F79B1',
            'Fish (misc. fish)': '#5F79B1',
            'Amphibians and friends': "#764397",
            'Stem tetrapods': '#764397',
            'Dinosaurs, ornithischians': "#C55F5F",
            'Dinosaurs, saurischians (avians)': '#C55F5F',
            'Dinosaurs, saurischians (non-theropods)': '#C55F5F',
            'Dinosaurs, saurischians (theropods)': '#C55F5F',
            'Early archosauromorphs': "#AA742D",
            'Pseudosuchians': '#AA742D',
            'Pterosaurs': '#AA742D',
            'Turtles': "#FDEB47",
            'Squamates': '#FDEB47',
            'Non-diapsid sauropsids': '#FDEB47',
            'Non-archosauromorph diapsids': '#FDEB47',
            'Mammals (misc. therian mammals)': "#D834E7",
            'Mammals, marsupials': '#D834E7',
            'Mammals, placental (artiodactyls)': '#D834E7',
            'Mammals, placental (carnivorans)': '#D834E7',
            'Mammals, placental (other)': '#D834E7',
            'Mammals, placental (perissodactyls)': '#D834E7',
            'Mammals, placental (primates)': '#D834E7',
            'Mammals, placental (rodents)': '#D834E7',
            'Non-therian mammaliaforms': '#D834E7',
            'Non-mammaliaform therapsids': '#D834E7',
            'Protostomes (other)': "#A39B9B",
            'Invertebrates (other arthropods)': "#CCCCCC",
            'Invertebrates (brachiopods)': '#CCCCCC',
            'Invertebrates (echinoderms)': '#CCCCCC',
            'Invertebrates (insects)': '#CCCCCC',
            'Invertebrates (molluscs)': '#CCCCCC',
            'Invertebrates (ostracods)': '#CCCCCC',
            'Invertebrates (trilobites)': '#CCCCCC'
}

time_color_map = {'pre-Ediacaran': '#F73563',
                  'Ediacaran': '#F73563',
                  'Cambrian': '#99C08D',
                  'Ordovician': '#99C08D',
                  'Silurian': '#99C08D',
                  'Devonian': '#99C08D',
                  'Carboniferous': '#99C08D',
                  'Permian': '#99C08D',
                  'Triassic': '#67C5CA',
                  'Jurassic': '#67C5CA',
                  'Cretaceous': '#67C5CA',
                  'Paleocene': '#F2F91D',
                  'Eocene': '#F2F91D',
                  'Oligocene': '#F2F91D',
                  'Miocene': '#F2F91D',
                  'Pliocene': '#F2F91D',
                  'Pleistocene': '#F2F91D'
}

year_color_map = {'1995-1999': "#f8e7d8",
                '2000-2004': "#f7d5b7",
                '2005-2009': "#f5ae70",
                '2010-2014': "#f78e32",
                '2015-2019': "#fc7500",
                '2020-2026': "#a04e05",
}

# By animal/not animal
plot_filename = f'{today}_nature-science_animalia.{plot_format}'
clade_count = fancy['Animalia'].value_counts(ascending=True)
    
fig, ax = plt.subplots(figsize=(4.5, 8))
bars = ax.bar(clade_count.index.astype(str), clade_count.values, color="#4ca06e", edgecolor='black')
ax.set_xlabel('', fontsize=15)
ax.set_ylabel('')
ax.set_title(f'Is it an animal? (Nature/Science)', fontsize=16)
ax.set_facecolor('#f7f7f7')
ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
ax.tick_params(axis='both', which='major', labelsize=14)
ax.set_axisbelow(True)
plt.tight_layout()
# plt.show()
plot_path = os.path.join(plots_dir, plot_filename)
plt.savefig(plot_path, format=plot_format, dpi=dpi)
plt.close(fig)

# By vertebrate/not vertebrate
plot_filename = f'{today}_nature-science_vertebrata.{plot_format}'
clade_count = fancy['Vertebrata'].value_counts(ascending=True)

fig, ax = plt.subplots(figsize=(4.5, 8))
bars = ax.bar(clade_count.index.astype(str), clade_count.values, color="#dceb5b", edgecolor='black')
ax.set_xlabel('', fontsize=15)
ax.set_ylabel('')
ax.set_title(f'Is it a vertebrate? (Nature/Science)', fontsize=16)
ax.set_facecolor('#f7f7f7')
ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
ax.tick_params(axis='both', which='major', labelsize=14)
ax.set_axisbelow(True)
plt.tight_layout()
# plt.show()
plot_path = os.path.join(plots_dir, plot_filename)
plt.savefig(plot_path, format=plot_format, dpi=dpi)
plt.close(fig)

# # Restrict to most common clades only and then do by time bin
# plot_filename = f'{today}_nature-science_clades-over-time.{plot_format}'

# focal_taxa = ['Mammals, placental (primates)', 'Non-therian mammaliaforms', 'Dinosaurs, saurischians (theropods)', 'Fish (misc. fish)', 'Amphibians and friends']
# pattern = '|'.join(focal_taxa)
# df_prominent = fancy[fancy['classification'].str.contains(pattern, na=False)]
# df_prominent_counts = df_prominent.groupby('publication_year_bin')['classification'].value_counts().unstack(fill_value=0)
# df_prominent_flipped = df_prominent_counts.T
# colors = [year_color_map[col] for col in df_prominent_flipped.columns]

# df_prominent_flipped.plot(kind='barh', figsize=(8,8), color=colors)
# plt.xlabel('Count')
# plt.ylabel('')
# plt.title(f'New species description by time bin (Nature/Science)')
# plt.tight_layout()
# # plt.show()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

for name, df in dfs_dict.items():
    # Create conditional label for journals to differentiate in title
    label = axis_dict.get(name, 'Journal')

    # Only unique articles
    df_expanded_dedup = df.drop_duplicates(subset=['doi', 'geography'])

    # How many species in a journal
    plot_filename = f'{today}_{name}_species-per-journal.{plot_format}'
    species_counts = df['journal'].value_counts(ascending=True)
    
    fig, ax = plt.subplots(figsize=(4.5, 8))
    bars = ax.bar(species_counts.index, species_counts.values, color='#00a9b7', edgecolor='black')
    
    ax.set_ylabel('')
    ax.set_title(f'Species by journal ({label})', fontsize=16)
    ax.set_facecolor('#f7f7f7')
    ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_xticks(species_counts.index.astype(str))
    ax.set_axisbelow(True)
    plt.tight_layout()
    # plt.show()
    plot_path = os.path.join(plots_dir, plot_filename)
    plt.savefig(plot_path, format=plot_format, dpi=dpi)
    plt.close(fig)

    # How many species-naming articles per journal (less than # of species due to multi-species descriptions)
    plot_filename = f'{today}_{name}_article-per-journal.{plot_format}'
    species_counts = df_expanded_dedup['journal'].value_counts(ascending=True)
        
    fig, ax = plt.subplots(figsize=(4.5, 8))
    bars = ax.bar(species_counts.index, species_counts.values, color='#00a9b7', edgecolor='black')
    ax.set_xlabel('', fontsize=15)
    ax.set_ylabel('')
    ax.set_title(f'Descrip. by journal ({label})', fontsize=16)
    ax.set_facecolor('#f7f7f7')
    ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_axisbelow(True)
    plt.tight_layout()
    # plt.show()
    plot_path = os.path.join(plots_dir, plot_filename)
    plt.savefig(plot_path, format=plot_format, dpi=dpi)
    plt.close(fig)

    # How many new species per country
    plot_filename = f'{today}_{name}_species-per-country_species.{plot_format}'
    article_counts = df_classified['geography'].value_counts(ascending=True)
        
    fig, ax = plt.subplots(figsize=(4.5, 8))
    bars = ax.barh(article_counts.index, article_counts.values, color='#00a9b7', edgecolor='black')
    ax.set_xlabel('', fontsize=15)
    ax.set_ylabel('')
    ax.set_title(f'Holotype country ({label})', fontsize=16)
    ax.set_facecolor('#f7f7f7')
    ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.set_axisbelow(True)
    plt.tight_layout()
    # plt.show()
    plot_path = os.path.join(plots_dir, plot_filename)
    plt.savefig(plot_path, format=plot_format, dpi=dpi)
    plt.close(fig)

    # How many species-naming articles per country (less than # of species due to multi-species descriptions)
    plot_filename = f'{today}_{name}_species-per-country_articles.{plot_format}'
    article_counts = df_expanded_dedup['geography'].value_counts(ascending=True)
        
    fig, ax = plt.subplots(figsize=(4.5, 8))
    bars = ax.barh(article_counts.index, article_counts.values, color='#00a9b7', edgecolor='black')
    ax.set_xlabel('', fontsize=15)
    ax.set_ylabel('')
    ax.set_title(f'Holotype country ({label})', fontsize=16)
    ax.set_facecolor('#f7f7f7')
    ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.set_axisbelow(True)
    plt.tight_layout()
    # plt.show()
    plot_path = os.path.join(plots_dir, plot_filename)
    plt.savefig(plot_path, format=plot_format, dpi=dpi)
    plt.close(fig)

    # By tetrapod/not tetrapod
    plot_filename = f'{today}_{name}_tetrapoda.{plot_format}'
    clade_count = df['Tetrapoda'].value_counts(ascending=True)

    fig, ax = plt.subplots(figsize=(4.5, 8))
    bars = ax.bar(clade_count.index.astype(str), clade_count.values, color="#b566c6", edgecolor='black')
    ax.set_xlabel('', fontsize=15)
    ax.set_ylabel('')
    ax.set_title(f'Is it a tetrapod? ({label})', fontsize=16)
    ax.set_facecolor('#f7f7f7')
    ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_axisbelow(True)
    plt.tight_layout()
    # plt.show()
    plot_path = os.path.join(plots_dir, plot_filename)
    plt.savefig(plot_path, format=plot_format, dpi=dpi)
    plt.close(fig)

    # By mammaliaformes/not mammaliaformes
    plot_filename = f'{today}_{name}_mammaliaformes.{plot_format}'
    clade_count = df['Mammaliaformes'].value_counts(ascending=True)
        
    fig, ax = plt.subplots(figsize=(4.5, 8))
    bars = ax.bar(clade_count.index.astype(str), clade_count.values, color="#905d7c", edgecolor='black')
    ax.set_xlabel('', fontsize=15)
    ax.set_ylabel('')
    ax.set_title(f'Is it a mammaliaform? ({label})', fontsize=16)
    ax.set_facecolor('#f7f7f7')
    ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_axisbelow(True)
    plt.tight_layout()
    # plt.show()
    plot_path = os.path.join(plots_dir, plot_filename)
    plt.savefig(plot_path, format=plot_format, dpi=dpi)
    plt.close(fig)

    # By dinosaur/not dinosaur
    plot_filename = f'{today}_{name}_dinosauria.{plot_format}'
    clade_count = df['Dinosauria'].value_counts(ascending=True)
        
    fig, ax = plt.subplots(figsize=(4.5, 8))
    bars = ax.bar(clade_count.index.astype(str), clade_count.values, color="#b97b47", edgecolor='black')
    ax.set_xlabel('', fontsize=15)
    ax.set_ylabel('')
    ax.set_title(f'Is it a dinosaur? ({label})', fontsize=16)
    ax.set_facecolor('#f7f7f7')
    ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_axisbelow(True)
    plt.tight_layout()
    # plt.show()
    plot_path = os.path.join(plots_dir, plot_filename)
    plt.savefig(plot_path, format=plot_format, dpi=dpi)
    plt.close(fig)

    # Compare all clades
    plot_filename = f'{today}_{name}_all-clades.{plot_format}'
    clade_count = df['classification'].value_counts(ascending=True)

    colors = [clade_color_map.get(clade, '#cccccc') for clade in clade_count.index]
        
    fig, ax = plt.subplots(figsize=(8, 8))
    bars = ax.barh(clade_count.index.astype(str), clade_count.values, color=colors, edgecolor='black')
    ax.set_xlabel('', fontsize=15)
    ax.set_ylabel('')
    ax.set_title(f'Clade comparison ({label})', fontsize=16)
    ax.set_facecolor('#f7f7f7')
    ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_axisbelow(True)
    plt.tight_layout()
    # plt.show()
    plot_path = os.path.join(plots_dir, plot_filename)
    plt.savefig(plot_path, format=plot_format, dpi=dpi)
    plt.close(fig)

    # Compare time bins
    plot_filename = f'{today}_{name}_time-bins.{plot_format}'
    time_count = df['age2'].value_counts(ascending=True)

    colors = [time_color_map.get(bin, '#cccccc') for bin in time_count.index]
        
    fig, ax = plt.subplots(figsize=(8, 8))
    bars = ax.barh(time_count.index.astype(str), time_count.values, color=colors, edgecolor='black')
    ax.set_xlabel('', fontsize=15)
    ax.set_ylabel('')
    ax.set_title(f'Time bin comparison ({label})', fontsize=16)
    ax.set_facecolor('#f7f7f7')
    ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_axisbelow(True)
    plt.tight_layout()
    # plt.show()
    plot_path = os.path.join(plots_dir, plot_filename)
    plt.savefig(plot_path, format=plot_format, dpi=dpi)
    plt.close(fig)

    #### GEOPANDAS CHLOROPLETH

    # Read in shapefile
    world = gpd.read_file('ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')
    country_counts = df['geography'].value_counts().reset_index()
    country_counts.columns = ['NAME', 'count']

    # Merge counts with world map shapefile
    world = world.merge(country_counts, on='NAME', how='left')
    world['count'] = world['count'].fillna(0)

    # Plot
    plot_filename = f'{today}_{name}_holotype_country_chloropleth.{plot_format}'
    fig, ax = plt.subplots(figsize=(12, 8))
    world.plot(column='count', cmap='viridis', legend=True, ax=ax)
    plt.title(f'New species occurrence (chloropleth)  ({label})')
    # plt.show()
    plot_path = os.path.join(plots_dir, plot_filename)
    plt.savefig(plot_path, format=plot_format, dpi=dpi)
    plt.close(fig)

    ### BINARY PRESENCE/ABSENCE
    # Load world map
    world = gpd.read_file('ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')
    countries = df['geography'].unique().tolist()

    # Map to shapefile
    world['selected'] = world['NAME'].isin(countries)

    # Plot
    plot_filename = f'{today}_{name}_holotype_country_binary.{plot_format}'
    fig, ax = plt.subplots(figsize=(12, 8))
    world.plot(column='selected', cmap='Pastel1_r', legend=True, ax=ax)
    plt.title(f'New species occurrence (binary) ({label})')
    # plt.show()
    plot_path = os.path.join(plots_dir, plot_filename)
    plt.savefig(plot_path, format=plot_format, dpi=dpi)
    plt.close(fig)