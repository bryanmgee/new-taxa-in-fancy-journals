import geopandas as gpd
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read in cleaned-up data file
outputs_dir = 'outputs'
today = datetime.now().strftime('%Y%m%d') 
df_classified = pd.read_csv(f'{outputs_dir}/{today}_df-classified.csv') 

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
fancy = df_classified[df_classified['journal'] != 'JVP']
jvp = df_classified[df_classified['journal'] == 'JVP']

dfs_dict = {
    'nature-science': fancy,
    'jvp': jvp
}
axis_dict = {
    'nature-science': 'Nature/Science',
    'jvp': 'JVP'
}

### PLOTTING
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

    # By animal/not animal
    plot_filename = f'{today}_{name}_animalia.{plot_format}'
    clade_count = df['Animalia'].value_counts(ascending=True)
        
    fig, ax = plt.subplots(figsize=(4.5, 8))
    bars = ax.bar(clade_count.index.astype(str), clade_count.values, color="#4ca06e", edgecolor='black')
    ax.set_xlabel('', fontsize=15)
    ax.set_ylabel('')
    ax.set_title(f'Is it an animal? ({label})', fontsize=16)
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
    plot_filename = f'{today}_{name}_vertebrata.{plot_format}'
    clade_count = df['Vertebrata'].value_counts(ascending=True)

    fig, ax = plt.subplots(figsize=(4.5, 8))
    bars = ax.bar(clade_count.index.astype(str), clade_count.values, color="#dceb5b", edgecolor='black')
    ax.set_xlabel('', fontsize=15)
    ax.set_ylabel('')
    ax.set_title(f'Is it a vertebrate? ({label})', fontsize=16)
    ax.set_facecolor('#f7f7f7')
    ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
    ax.tick_params(axis='both', which='major', labelsize=14)
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
        
    fig, ax = plt.subplots(figsize=(8, 8))
    bars = ax.barh(clade_count.index.astype(str), clade_count.values, color="#e65cd6", edgecolor='black')
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
        
    fig, ax = plt.subplots(figsize=(8, 8))
    bars = ax.barh(time_count.index.astype(str), time_count.values, color="#831717", edgecolor='black')
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


    