import geopandas as gpd
import glob
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read in cleaned-up data file
outputs_dir = 'outputs'
today = datetime.now().strftime('%Y%m%d') 

file_pattern_dict = {
                    'df_classified': f'{outputs_dir}/*_dataset-classified.csv',
                    'df_names': f'{outputs_dir}/*_openalex-authors-summary-name-only.csv', 
                    'df_orcids': f'{outputs_dir}/*_openalex-authors-summary-orcid-only.csv', 
                    'df_names_orcids': f'{outputs_dir}/*_openalex-authors-summary-name-orcid.csv'
                    }

## Create empty dict to store
df_dict = {}

for k, v in file_pattern_dict.items():
    try:
        most_recent_file = max(glob.iglob(v), key=os.path.getmtime)
        df_dict[k] = pd.read_csv(most_recent_file, low_memory=False)
        if df_dict[k] is not None:
                print(f'Imported data file: {most_recent_file} with {len(df_dict[k])} entries.\n') 
        print(df_dict[k].head())
        
    except ValueError:
        print(f'No files matched the given pattern ({df_dict[v]}).')

## Assign as local variables
### Order *MUST* match that of the file_pattern_dict
df_classified, df_names, df_orcids, df_names_orcids = df_dict.values()
total = len(df_classified)

## Set blanks for age to 'unknown'
### At least some bounds are known for most species with blanks in 'age2' (see 'age1'), but boundary-crossing localities may be blank for both
## Set blanks for geography to 'not defined'
df_classified.fillna({'age1': 'Unknown', 'age2': 'Unknown', 'geography': 'Not defined'}, inplace=True)

# Create plots and summaries directories
if os.path.isdir('plots'):
        print('plots directory found - no need to recreate.\n')
else:
    os.mkdir('plots')
    print('plots directory has been created.\n')
if os.path.isdir('summaries'):
        print('summaries directory found - no need to recreate.\n')
else:
    os.mkdir('summaries')
    print('summaries directory has been created.\n')

plots_dir = 'plots'
summaries_dir = 'summaries'

# Standardized plot variables
plot_format = 'png'
dpi = 300
img_height = 5.5
img_width = 6.5
axis_font = 9
title_font = 10
tick_font = 9
label_font = 9
legend_font = 9
alpha = 0.8
bg_col = '#F8F8F8'

names_dict = {
    'Nature': 'Nature',
    'Science': 'Science',
    'Science Advances': 'Sci Adv',
    'Nature Communications': 'Nat Commun',
    'Nature Ecology & Evolution': 'Nat Ecol Evol',
    'Current Biology': 'Curr Biol',
    'Gondwana Research': 'Gondwana Res',
    'PNAS': 'Proc Natl Acad Sci USA',
    'Journal of Vertebrate Paleontology': 'J Vert Paleontol',
    'Journal of Paleontology': 'J Paleontol',
    'Journal of Systematic Palaeontology': 'J Syst Palaeontol',
    'Palaeontology': 'Palaeontology',
    'Papers in Palaeontology': 'Pap Palaeontol'
}

# Replace journal names with ISO 4
df_classified['journal'] = df_classified['journal'].replace(names_dict)

# Color map for all 20 categories
cat_order = ['Other', 'Plants and fungi', 'Non-bilaterian metazoans', 'Molluscs', 'Lophophorates', 'Non-insect pan-arthropods', 'Insects', 'Non-chordate deuterostomes', 'Fish (chondrichthyans)', 'Fish (actinopterygians)', 'Fish (other)', 'Amphibians', 'Lepidosauromorphs', 'Pseudosuchians', 'Pantestudines', 'Non-avian avemetatarsalians', 'Avians', 'Non-primate mammaliamorphs', 'Primates', 'Other amniotes']
# all_categories = sorted(df_classified['classification'].dropna().unique())
cmap = plt.get_cmap('tab20_r')
color_mapping_groups = {val: cmap(i) for i, val in enumerate(cat_order)}
## Set order of categories


# Color map for time bins
color_mapping_ages = {
    'Unknown': "#DFDFDF",
    'pre-Ediacaran': '#f74370',
    'Ediacaran': '#FED96A',
    'Cambrian': '#7FA056',
    'Ordovician': '#009270',
    'Silurian': '#B3E1B6',
    'Devonian': '#CB8C37',
    'Carboniferous': '#67A599',
    'Permian': '#F04028',
    'Triassic': '#812B92',
    'Jurassic': '#34B2C9',
    'Cretaceous': '#7FC64E',
    'Paleogene': '#FD9A52',
    'Neogene': '#FFE619',
    'Quaternary': '#F9F97F'
}
## Set order of time bins
age_order = ['Unknown', 'pre-Ediacaran','Ediacaran','Cambrian','Ordovician', 'Silurian', 'Devonian', 'Carboniferous', 'Permian', 'Triassic', 'Jurassic', 'Cretaceous', 'Paleogene', 'Neogene', 'Quaternary']

# Color map for countries
## Because the list of top 10 varies by journal, only certain countries are colored
default_color = '#DDDDDD'
color_mapping = {
                #  'Argentina': '#74ACDF',
                #  'Australia': '#00843D',
                #  'Canada': '#D80621',
                 'China': '#EE1C25',
                #  'France': '#000091', 
                 'Myanmar': '#FFCD00',
                 'United States of America': '#0A3161'}
color_mapping_geo = {val: color_mapping.get(val, default_color) for val in df_classified['geography']}

# Color map for journals
## Based on Okabe-Ito
color_mapping_journals = {
    'Nature': "#E69F00",
    'Science': '#E69F00',
    'Nat Commun': '#009E73',
    'Sci Adv': '#009E73',
    'Curr Biol': '#009E73',
    'Proc Natl Acad Sci USA': '#009E73',
    'Gondwana Res': '#009E73',
    'Nat Ecol Evol': '#009E73',
    'J Vert Paleontol': '#0072B2',
    'J Paleontol': '#0072B2',
    'J Syst Palaeontol': '#0072B2',
    'Palaeontology': '#0072B2',
    'Pap Palaeontol': '#0072B2'
}

# Subset df
tier1 = ['Nature', 'Science']
tier1_df = df_classified[df_classified['journal'].isin(tier1)]
tier2 = ['Curr Biol', 'Gondwana Res', 'Nat Commun', 'Nat Ecol Evol', 'Proc Natl Acad Sci USA', 'Sci Adv']
tier2_df = df_classified[df_classified['journal'].isin(tier2)]
control = ['J Paleontol', 'J Syst Palaeontol', 'J Vert Paleontol', 'Palaeontology', 'Pap Palaeontol']
control_df = df_classified[df_classified['journal'].isin(control)]

dfs_dict = {
    'High-JIF': tier1,
    'Medium-JIF': tier2,
    'Control': control
}
axis_dict = {
    'High-JIF': 'Nature/Science',
    'Medium-JIF': 'PNAS/Current Bio/Nature Comms/Nature Eco Evo/Sci Adv',
    'Control': 'Control'
}

tiers = [tier1, tier2, control]

# Create subsetted dfs for later
rank_columns = df_classified.loc[:, '0':'70'].columns
## Arthropods
df_arthropoda = df_classified[df_classified['Panarthropoda']]
## Insects
df_insecta = df_classified[df_classified['Insecta']]
## Mammaliamorphs
df_mammal = df_classified[df_classified['Mammaliamorpha']]
## Avemetatarsalians
df_avemet = df_classified[df_classified['Avemetatarsalia']]
## 'Amphibians'
df_amphibian = df_classified[df_classified['classification'] == 'Amphibians']

# Create PBDB dfs
pbdb_initial_missing_species = df_classified[(df_classified['source'].str.contains('manually added', case=False)
                                            & ~df_classified['source'].str.contains('paper')
                                            & ~df_classified['source'].str.contains('PBDB API', case=False))] 
genera_unique = df_classified.drop_duplicates(subset=['genus'], keep='first')
pbdb_initial_missing_genera = genera_unique[(genera_unique['source'].str.contains('manually added', case=False))]

pbdb_failed_retrieval_species = df_classified[(df_classified['source'].str.contains('failed API', case=False) 
                                 | df_classified['source'].str.contains('should have been retrieved')
                                 | df_classified['source'].str.contains('typo'))]
pbdb_failed_retrieval_genera = pbdb_failed_retrieval_species.drop_duplicates(subset=['genus'], keep='first')


pbdb_synonymy_species = df_classified[(df_classified['source'].str.contains('in PBDB as subgenus'))]
pbdb_synonymy_genera = pbdb_synonymy_species.drop_duplicates(subset=['genus'], keep='first')

pbdb_truly_missing_species = df_classified[(df_classified['source'].str.contains('manually added', case=False) 
                                 & ~df_classified['source'].str.contains('should have been retrieved')
                                 & ~df_classified['source'].str.contains('typo')
                                 & ~df_classified['source'].str.contains('in PBDB as subgenus', case=False)
                                 & ~df_classified['source'].str.contains('PBDB API', case=False)
                                 & ~df_classified['source'].str.contains('in PBDB as junior synonym', case=False)
                                 & ~df_classified['source'].str.contains('paper'))]
pbdb_truly_missing_genera = pbdb_truly_missing_species.drop_duplicates(subset=['genus'], keep='first')

pbdb_truly_missing_species_count = len(pbdb_truly_missing_species) 
pbdb_truly_missing_genera_count  = len(pbdb_truly_missing_genera)

pbdb_edited_species = df_classified[(df_classified['source'].str.contains('manually edited'))]
pbdb_edited_genera = pbdb_edited_species.drop_duplicates(subset=['genus'], keep='first')






genera_counts = genera_unique['classification'].value_counts().reindex(cat_order, fill_value=0).reset_index(name='count')
genera_counts['percentage'] = (genera_counts['count'] / len(genera_unique)) * 100

papers_unique = df_classified.drop_duplicates(subset=['doi'], keep='first')
papers_counts = papers_unique['journal'].value_counts().reset_index(name='count')

pbdb_truly_missing_species_2026 = pbdb_truly_missing_species[pbdb_truly_missing_species['year'] < 2026]
pbdb_truly_missing_genera_2026 = pbdb_truly_missing_genera[pbdb_truly_missing_genera['year'] < 2026]
pbdb_truly_missing_species_2016 = pbdb_truly_missing_species[pbdb_truly_missing_species['year'] < 2016]
pbdb_truly_missing_genera_2016 = pbdb_truly_missing_genera[pbdb_truly_missing_genera['year'] < 2016]


missing_pbdb_df_dois = pbdb_truly_missing_genera.drop_duplicates(subset=['doi'], keep='first')
missing_doi_count = missing_pbdb_df_dois['journal'].value_counts().reset_index(name='count')
missing_doi_count['percentage'] = (missing_doi_count['count'] / len(missing_pbdb_df_dois)) * 100
missing_doi_count = missing_doi_count.sort_values(by='percentage', ascending=True)

missing_pbdb_df_unique = pbdb_truly_missing_genera.drop_duplicates(subset=['genus'], keep='first')
print(f'There are {len(missing_pbdb_df_unique)} unique genera that were not found in the PBDB and that appear to be legitimately absent. This includes genera with multiple species.\n')

pbdb_counts = missing_pbdb_df_unique['classification'].value_counts().reindex(cat_order, fill_value=0).reset_index(name='count')
pbdb_counts['percentage'] = (pbdb_counts['count'] / len(missing_pbdb_df_unique)) * 100

############# SUMMARY PRINT STATEMENTS ##################
print('Writing text summary file.\n')
now = datetime.now()

with open(f'{summaries_dir}/{today}_summary.txt', 'w') as file:
    file.write(f'This is the summary text file for {today}, initialized on {now}.\n\n')

    file.write('----- General dataset attributes -----.\n\n')
    file.write(f'There are {df_classified['novel_taxon'].nunique()} unique species distributed among {df_classified['genus'].nunique()} unique genera from {df_classified['geography'].nunique()} geographic regions, and published in {df_classified['doi'].nunique()} unique papers in the dataset.\n\n')

    file.write('----- Journal attributes -----.\n\n')
    for journal, subset_df in df_classified.groupby('journal'):
        file.write(f'There are {subset_df['novel_taxon'].nunique()} unique species distributed among {subset_df['genus'].nunique()} unique genera from {subset_df['geography'].nunique()} geographic regions, and published in {subset_df['doi'].nunique()} unique papers for {journal}.\n\n')

    file.write('----- Category / time / country combinations -----.\n\n')
    for journal, subset_df in df_classified.groupby('journal'):
        group = subset_df[['classification']].value_counts().idxmax()
        file.write(f'The most common category for {journal} is {group}.\n')
        age_group = subset_df[['age2', 'classification']].value_counts().idxmax()
        file.write(f'The most common category-age combination for {journal} is {age_group}.\n')
        age_group_geo = subset_df[['age2', 'classification', 'geography']].value_counts().idxmax()
        file.write(f'The most common category-age-geography combination for {journal} is {age_group_geo}.\n')
        age_geo = subset_df[['age2', 'geography']].value_counts().idxmax()
        file.write(f'The most common age-geography combination for {journal} is {age_geo}.\n\n')

    file.write('----- Common category percents -----.\n\n')
    print_cats = ['Eukaryota', 'Animalia', 'Deuterostomia', 'Protostomia', 'Chordata', 'Vertebrata', 'Amniota', 'Dinosauria', 'Aves', 'Avialae', 'Mammaliamorpha', 'Mammalia']
    for clade in print_cats:
        df_subset = df_classified[df_classified[clade]]
        count = len(df_subset)
        percent = round(count/total, 4) * 100
        file.write(f'There are {count} ({percent}%) species classified as {clade}.\n')

    file.write('----- PBDB data -----.\n\n')
    file.write('----- PBDB source -----.\n')
    # Subtraction of 1 is related to manual addition of one paper (one species, one genus)
    file.write(f'There are {len(pbdb_initial_missing_species)} species ({(len(pbdb_initial_missing_species))/(len(df_classified)-1) * 100})% belonging to genera that were not initially retrieved from the PBDB, belong to {len(pbdb_initial_missing_genera)-1} unique genera ({(len(pbdb_initial_missing_genera)-1)/(len(genera_unique)-1) * 100}%). This includes API failures and entries that should/could have been retrieved. \n')
    file.write(f'There are {len(pbdb_failed_retrieval_species)} species ({(len(pbdb_failed_retrieval_species))/(len(df_classified)-1) * 100})% belonging to genera that should have been retrieved from the PBDB, belong to {len(pbdb_failed_retrieval_genera)} unique genera ({(len(pbdb_failed_retrieval_genera))/(len(genera_unique)-1) * 100}%).\n')
    file.write(f'There are {len(pbdb_synonymy_species)} species ({(len(pbdb_synonymy_species))/(len(df_classified)-1) * 100})% belonging to genera that are listed as subgenera of another genus, with {len(pbdb_synonymy_genera)} unique genera ({(len(pbdb_synonymy_genera))/(len(genera_unique)-1) * 100}%).\n')
    file.write(f'There are thus {pbdb_truly_missing_species_count} unique species (({pbdb_truly_missing_species_count/(len(df_classified)-1) * 100})%) belonging to {pbdb_truly_missing_genera_count} unique genera (({pbdb_truly_missing_genera_count/(len(genera_unique)-1) * 100})%) that are considered truly missing\n\n') 
    file.write(f'Of those {len(pbdb_truly_missing_species)} species, {len(pbdb_truly_missing_species_2026)} were published prior to 2026, and of those {len(pbdb_truly_missing_genera)} genera, {len(pbdb_truly_missing_genera_2026)} were published prior to 2026 .\n')
    file.write(f'Of those {len(pbdb_truly_missing_species)} species, {len(pbdb_truly_missing_species_2016)} were published prior to 2016, and of those {len(pbdb_truly_missing_genera)} genera, {len(pbdb_truly_missing_genera_2016)} were published prior to 2016 .\n')
    file.write(f'{len(pbdb_edited_species)} species among {len(pbdb_edited_genera)} genera were manually edited for information.\n')


    # file.write('----- Species-level -----.\n')
    # counts_str = df_classified['source'].value_counts().to_string()
    # file.write(counts_str)







## Quick counts
journal_counts = df_classified.groupby('journal')['classification'].value_counts()
journal_counts.to_csv(f'{summaries_dir}/{today}_journal-category-count.csv')

journals_by_cat_20 = df_classified.groupby(['journal', 'classification']).size().reset_index(name='count')

pivot_df = journals_by_cat_20.pivot(index='journal', columns='classification', values='count').fillna(0)
pivot_df = pivot_df.sort_index(ascending=False)

# Calculate percentages (relative counts)
pivot_pct = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

# Sort by defined order
pivot_pct = pivot_pct[cat_order]

# ############################################
# ###             PLOTS                    ###
# ############################################

# ##### Full dataset (no filtering) #####
# print(f'Creating graphs for full dataset.\n')
# # By category
# all_counts = df_classified['classification'].value_counts().reindex(cat_order, fill_value=0).reset_index(name='count')
# all_counts['percentage'] = (all_counts['count'] / len(df_classified)) * 100

# plot_filename = f'{today}_all-journals_groups.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# ax.barh(all_counts['classification'], all_counts['percentage'], color=[color_mapping_groups[x] for x in all_counts['classification']], edgecolor='black', linewidth=1.2)

# for i, pct in enumerate(all_counts['percentage']):
#     ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

# ax.set_yticks(all_counts['classification'])
# ax.set_xlabel('Percent of new species', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# ax.set_title('Category distribution of new species (all journals)', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.set_axisbelow(True)
# ax.set_xlim(0, all_counts['percentage'].max() * 1.5)
# ax.set_facecolor(bg_col)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# # By age
# all_ages = df_classified['age2'].value_counts().reindex(age_order, fill_value=0).reset_index(name='count')
# all_ages['percentage'] = (all_ages['count'] / len(df_classified)) * 100

# plot_filename = f'{today}_all-journals_ages.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# ax.barh(all_ages['age2'], all_ages['percentage'], color=[color_mapping_ages[x] for x in all_ages['age2']], edgecolor='black', linewidth=1.2)

# for i, pct in enumerate(all_ages['percentage']):
#     ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

# ax.set_yticks(all_ages['age2'])
# ax.set_xlabel('Percent of new species', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# ax.set_title('Time period distribution of new species (all journals)', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.set_axisbelow(True)
# ax.set_xlim(0, all_ages['percentage'].max() * 1.5)
# ax.set_facecolor(bg_col)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# # By country
# all_countries = df_classified['geography'].value_counts().reset_index(name='count')
# all_countries['percentage'] = (all_countries['count'] / len(df_classified)) * 100

# ## Restrict to top X
# cut = 20
# all_countries = all_countries.head(cut)

# plot_filename = f'{today}_all-journals_countries_top-{cut}.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# ax.barh(all_countries['geography'], all_countries['percentage'], color=[color_mapping_geo[x] for x in all_countries['geography']], edgecolor='black', linewidth=1.2)

# for i, pct in enumerate(all_countries['percentage']):
#     ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

# ax.set_yticks(all_countries['geography'])
# ax.set_xlabel('Percent of new species', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# ax.set_title(f'Geographic distribution of new species (top {cut}, all journals)', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.set_axisbelow(True)
# ax.set_xlim(0, all_countries['percentage'].max() * 1.5)
# ax.invert_yaxis()
# ax.set_facecolor(bg_col)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# ##### Recursive plots #####

# for name, tier in dfs_dict.items():

#     ##### ------------ Groups ------------  #####
#     ####### ------------ Journals parsed within tier ------------  #######
#     print(f'Creating graphs for {name} journals.\n')
#     plot_filename = f'{today}_{name}_groups_separate.{plot_format}'
#     if tier == tier1:
#         fig, axs = plt.subplots(1, 2, figsize=(img_width, img_height))
#     else:
#         fig, axs = plt.subplots(3, 2, figsize=(img_width, img_height*1.8))
#     axs_flat = axs.flatten()

#     for i, journal in enumerate(tier):
#         ax = axs_flat[i]
#         df_subset = df_classified[df_classified['journal'] == journal]
#         total = len(df_subset)
#         groups = df_subset['classification'].value_counts().reindex(cat_order, fill_value=0).rename_axis('group').reset_index(name='count')
#         groups['percentage'] = (groups['count'] / total) * 100

#         ax.barh(groups['group'], groups['percentage'], color=[color_mapping_groups[x] for x in groups['group']], edgecolor='black', linewidth=1.2)

#         for i, pct in enumerate(groups['percentage']):
#             ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

#         # ax.set_yticks(groups['group'])
#         ax.set_yticklabels([])
#         # ax.legend(title='', bbox_to_anchor=(0.38, -0.15), loc='upper center', fontsize=legend_font, ncol=2)
#         ax.set_xlabel('Percent of new species', fontsize=axis_font, fontweight='bold')
#         ax.set_ylabel('', fontsize=axis_font)
#         ax.set_title(journal, fontsize=title_font, style='italic')
#         ax.tick_params(labelsize=tick_font)
#         # for row in range(1):
#         #     for col in range(1):
#         #         # Check if the current subplot is in the rightmost column (index 1 for a 2-column grid)
#         #         if col == 1:
#         #             # Option A: Hides just the text labels, keeps tick marks
#         #             axs[row, col].set_yticklabels([])
                    
#         #             # Option B: Hides the entire y-axis (labels, tick marks, and axis line)
#         #             # axs[row, col].get_yaxis().set_visible(False)
#         ax.set_facecolor(bg_col)
#         ax.set_xlim(0, 45)

#     # Drop blank subplot for control group (n=5)
#     if name == 'control':
#         for j in range(len(control), len(axs_flat)):
#             fig.delaxes(axs_flat[j])

#     plt.subplots_adjust(wspace=0.3)
#     plt.tight_layout()
#     # plt.show()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     ####### ------------ Journals combined within tier ------------  #######
#     plot_filename = f'{today}_{name}_groups_grouped.{plot_format}'

#     tier_df = df_classified[df_classified['journal'].isin(tier)]
#     tier_counts = tier_df['classification'].value_counts().reindex(cat_order, fill_value=0).reset_index(name='count')
#     tier_counts['percentage'] = (tier_counts['count'] / len(tier_df)) * 100

#     fig, ax = plt.subplots(figsize=(img_width, img_height))

#     ax.barh(tier_counts['classification'], tier_counts['percentage'], color=[color_mapping_groups[x] for x in tier_counts['classification']], edgecolor='black', linewidth=1.2)

#     for i, pct in enumerate(tier_counts['percentage']):
#         ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

#     ax.set_yticks(tier_counts['classification'])
#     ax.set_xlabel('Percent of new species', fontsize=axis_font, fontweight='bold')
#     ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
#     ax.set_title(f'Category distribution of new species ({name})', fontsize=title_font, fontweight='bold')
#     ax.tick_params(labelsize=tick_font)
#     ax.set_axisbelow(True)
#     ax.set_xlim(0, 30)
#     ax.set_facecolor(bg_col)

#     plt.tight_layout()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     if tier == tier1 or tier == tier2:
#         control_counts = control_df['classification'].value_counts().reindex(cat_order, fill_value=0).reset_index(name='count')
#         control_counts['percentage'] = (control_counts['count'] / len(df_classified)) * 100
#         merged_df = pd.merge(control_counts, tier_counts, on='classification')
#         merged_df = merged_df.rename(columns={'count_x': f'count_all', 'percentage_x': f'percentage_all', 'count_y': f'count_{name}', 'percentage_y': f'percentage_{name}'})
#         merged_df['difference'] = merged_df[f'percentage_{name}'] - merged_df['percentage_all']
#         merged_df['magnitude'] = merged_df['difference'] / merged_df['percentage_all']

#         plot_filename = f'{today}_{name}_groups_differential.{plot_format}'

#         fig, ax = plt.subplots(figsize=(img_width, img_height))

#         ax.barh(merged_df['classification'], merged_df['difference'], color=[color_mapping_groups[x] for x in merged_df['classification']], edgecolor='black', linewidth=1.2)

#         for i, pct in enumerate(merged_df['difference']):
#             position = 'left' if pct > 0 else 'right'
#             x_pos = pct + 0.1 if pct > 0 else pct - 0.15
#             ax.text(x_pos, i, f' {pct:.1f}%', ha=position, va='center', fontsize=label_font)

#         ax.set_yticks(merged_df['classification'])
#         ax.set_xlabel('Percent difference', fontsize=axis_font, fontweight='bold')
#         ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
#         ax.set_title(f'Category distribution of new species ({name})', fontsize=title_font, fontweight='bold')
#         ax.tick_params(labelsize=tick_font)
#         ax.set_axisbelow(True)
#         ax.set_xlim(-25, 25)
#         ax.set_facecolor(bg_col)

#         plt.axvline(x=0, color='black', linestyle='--', linewidth=1)
#         plt.tight_layout()
#         plot_path = os.path.join(plots_dir, plot_filename)
#         plt.savefig(plot_path, format=plot_format, dpi=dpi)
#         plt.close(fig)

#         plot_filename = f'{today}_{name}_groups_magnitude.{plot_format}'
        
#         fig, ax = plt.subplots(figsize=(img_width, img_height))

#         ax.barh(merged_df['classification'], merged_df['magnitude'], color=[color_mapping_groups[x] for x in merged_df['classification']], edgecolor='black', linewidth=1.2)

#         for i, pct in enumerate(merged_df['magnitude']):
#             position = 'left' if pct > 0 else 'right'
#             x_pos = pct + 0.1 if pct > 0 else pct - 0.3
#             ax.text(x_pos, i, f' {pct:.1f}x', ha=position, va='center', fontsize=label_font)

#         ax.set_yticks(merged_df['classification'])
#         ax.set_xlabel('Percent magnitude', fontsize=axis_font, fontweight='bold')
#         ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
#         ax.set_title(f'Category distribution of new species ({name})', fontsize=title_font, fontweight='bold')
#         ax.tick_params(labelsize=tick_font)
#         ax.set_axisbelow(True)
#         if tier == tier1:
#             ax.set_xlim(-15, 50)
#         else:
#             ax.set_xlim(-15, 15)
#         ax.set_facecolor(bg_col)

#         plt.axvline(x=0, color='black', linestyle='--', linewidth=1)
#         plt.tight_layout()
#         plot_path = os.path.join(plots_dir, plot_filename)
#         plt.savefig(plot_path, format=plot_format, dpi=dpi)
#         plt.close(fig)
        

#     ##### ------------ Ages ------------  #####
#     ####### ------------ Journals parsed within tier ------------  #######
#     plot_filename = f'{today}_{name}_ages_separate.{plot_format}'

#     if tier == tier1:
#         fig, axs = plt.subplots(1, 2, figsize=(12, 7))
#     else:
#         fig, axs = plt.subplots(3, 2, figsize=(12, 15))
#     axs_flat = axs.flatten()

#     for i, journal in enumerate(tier):
#         ax = axs_flat[i]
#         df_subset = df_classified[df_classified['journal'] == journal]
#         total = len(df_subset)
#         groups = df_subset['age2'].value_counts().reindex(age_order, fill_value=0).rename_axis('age').reset_index(name='count')
#         groups['percentage'] = (groups['count'] / total) * 100

#         ax.barh(groups['age'], groups['percentage'], color=[color_mapping_ages[x] for x in groups['age']], edgecolor='black', linewidth=1.2)

#         for i, pct in enumerate(groups['percentage']):
#             ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

#         ax.set_yticks(groups['age'])
#         # ax.set_xlabel('Percent of new species', fontsize=axis_font, fontweight='bold')
#         ax.set_ylabel('', fontsize=axis_font)
#         ax.set_title(journal, fontsize=title_font, style='italic')
#         ax.tick_params(labelsize=tick_font)
#         # ax.grid(axis='y', alpha=alpha, linestyle='--')
#         # ax.set_axisbelow(True)
#         ax.set_facecolor(bg_col)
#         ax.set_xlim(0, 55)

#     # Drop blank subplot for control group (n=5)
#     if name == 'control':
#         for j in range(len(control), len(axs_flat)):
#             fig.delaxes(axs_flat[j])

#     plt.subplots_adjust(wspace=0.3)
#     plt.tight_layout()
#     # plt.show()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     ####### ------------ Journals combined within tier ------------  #######
#     plot_filename = f'{today}_{name}_ages_grouped.{plot_format}'
    
#     tier_df = df_classified[df_classified['journal'].isin(tier)]
#     tier_counts = tier_df['age2'].value_counts().reindex(age_order, fill_value=0).reset_index(name='count')
#     tier_counts['percentage'] = (tier_counts['count'] / len(tier_df)) * 100

#     fig, ax = plt.subplots(figsize=(img_width, img_height))

#     ax.barh(tier_counts['age2'], tier_counts['percentage'], color=[color_mapping_ages[x] for x in tier_counts['age2']], edgecolor='black', linewidth=1.2)

#     for i, pct in enumerate(tier_counts['percentage']):
#         ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

#     ax.set_yticks(tier_counts['age2'])
#     ax.set_xlabel('Percent of new species', fontsize=axis_font, fontweight='bold')
#     ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
#     ax.set_title(f'Time period distribution of new species ({name})', fontsize=title_font, fontweight='bold')
#     ax.tick_params(labelsize=tick_font)
#     ax.set_axisbelow(True)
#     ax.set_xlim(0, 45)
#     ax.set_facecolor(bg_col)

#     plt.tight_layout()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     ##### ------------ Countries ------------  #####
#     ####### ------------ Journals parsed within tier ------------  #######
#     plot_filename = f'{today}_{name}_countries_separate.{plot_format}'

#     if tier == tier1:
#         fig, axs = plt.subplots(1, 2, figsize=(12, 6))
#     else:
#         fig, axs = plt.subplots(3, 2, figsize=(12, 14))    
#     axs_flat = axs.flatten()

#     for i, journal in enumerate(tier):
#         ax = axs_flat[i]
#         df_subset = df_classified[df_classified['journal'] == journal]
#         total = len(df_subset)
#         groups = df_subset['geography'].value_counts().rename_axis('geography').reset_index(name='count')
#         groups['percentage'] = (groups['count'] / total) * 100
#         groups_top = groups.head(10)

#         ax.barh(groups_top['geography'], groups_top['percentage'], color=[color_mapping_geo[x] for x in groups['geography']], edgecolor='black', linewidth=1.2)

#         for i, pct in enumerate(groups_top['percentage']):
#             ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

#         ax.set_yticks(groups_top['geography'])
#         # ax.set_xlabel('Percent of new species', fontsize=axis_font, fontweight='bold')
#         ax.set_ylabel('', fontsize=axis_font)
#         ax.set_title(journal, fontsize=title_font, style='italic')
#         ax.tick_params(labelsize=tick_font)
#         # ax.grid(axis='y', alpha=alpha, linestyle='--')
#         # ax.set_axisbelow(True)
#         ax.set_facecolor(bg_col)
#         ax.set_xlim(0, 50)
#         ax.invert_yaxis()

#     # Drop blank subplot for control group (n=5)
#     if name == 'control':
#         for j in range(len(control), len(axs_flat)):
#             fig.delaxes(axs_flat[j])

#     plt.subplots_adjust(wspace=0.3)
#     plt.tight_layout()
#     # plt.show()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     ####### ------------ Journals combined within tier ------------  #######
#     plot_filename = f'{today}_{name}_countries_grouped.{plot_format}'
    
#     tier_df = df_classified[df_classified['journal'].isin(tier)]
#     tier_counts = tier_df['geography'].value_counts().rename_axis('geography').reset_index(name='count')
#     tier_counts['percentage'] = (tier_counts['count'] / len(tier_df)) * 100
#     tier_counts_top = tier_counts.head(15)

#     fig, ax = plt.subplots(figsize=(img_width, img_height))

#     ax.barh(tier_counts_top['geography'], tier_counts_top['percentage'], color=[color_mapping_geo[x] for x in tier_counts_top['geography']], edgecolor='black', linewidth=1.2)

#     for i, pct in enumerate(tier_counts_top['percentage']):
#         ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

#     ax.set_yticks(tier_counts_top['geography'])
#     ax.set_xlabel('Percent of new species', fontsize=axis_font, fontweight='bold')
#     ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
#     ax.set_title(f'Geographic distribution of new species ({name})', fontsize=title_font, fontweight='bold')
#     ax.tick_params(labelsize=tick_font)
#     ax.set_axisbelow(True)
#     ax.set_xlim(0, 50)
#     ax.invert_yaxis()
#     ax.set_facecolor(bg_col)

#     plt.tight_layout()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

# ###############################################
# #### ---------- ONE-OFF GRAPHS ---------- #####
# ###############################################

# print('Creating singleton graphs.\n')

# ##### ---------- PBDB graphs ---------- #####

# plot_filename = f'{today}_pbdb-missing_groups_percent.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# ax.barh(pbdb_counts['classification'], pbdb_counts['percentage'], color=[color_mapping_groups[x] for x in pbdb_counts['classification']], edgecolor='black', linewidth=1.2)

# for i, pct in enumerate(pbdb_counts['percentage']):
#     ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

# ax.set_yticks(pbdb_counts['classification'])
# ax.set_xlabel('Percent of genera', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# ax.set_title('Category distribution of new species', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.set_axisbelow(True)
# ax.set_xlim(0, pbdb_counts['percentage'].max() * 1.5)
# ax.set_facecolor(bg_col)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# plot_filename = f'{today}_pbdb-missing_groups_count.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# ax.barh(pbdb_counts['classification'], pbdb_counts['count'], color=[color_mapping_groups[x] for x in pbdb_counts['classification']], edgecolor='black', linewidth=1.2)

# for i, pct in enumerate(pbdb_counts['count']):
#     ax.text(pct, i, f' {pct:.1f}', ha='left', va='center', fontsize=label_font)

# ax.set_yticks(pbdb_counts['classification'])
# ax.set_xlabel('Number of genera', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# ax.set_title('Category distribution of genera', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.set_axisbelow(True)
# ax.set_xlim(0, pbdb_counts['count'].max() * 1.5)
# ax.set_facecolor(bg_col)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# merged_df = pd.merge(genera_counts, pbdb_counts, on='classification')
# merged_df = merged_df.rename(columns={'count_x': 'count_all', 'percentage_x': 'percentage_all', 'count_y': 'count_pbdb', 'percentage_y': 'percentage_pbdb'})
# merged_df['difference'] = merged_df['percentage_pbdb'] - merged_df['percentage_all']
# merged_df['magnitude'] = merged_df['difference'] / merged_df['percentage_all']

# plot_filename = f'{today}_pbdb_groups_differential.{plot_format}'

# fig, ax = plt.subplots(figsize=(img_width, img_height))

# ax.barh(merged_df['classification'], merged_df['difference'], color=[color_mapping_groups[x] for x in merged_df['classification']], edgecolor='black', linewidth=1.2)

# for i, pct in enumerate(merged_df['difference']):
#     position = 'left' if pct > 0 else 'right'
#     x_pos = pct + 0.1 if pct > 0 else pct - 0.15
#     ax.text(x_pos, i, f' {pct:.1f}%', ha=position, va='center', fontsize=label_font)

# ax.set_yticks(merged_df['classification'])
# ax.set_xlabel('Percent difference', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# ax.set_title(f'Category distribution of new species with genera missing from the PBDB', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.set_axisbelow(True)
# ax.set_xlim(-25, 25)
# ax.set_facecolor(bg_col)

# plt.axvline(x=0, color='black', linestyle='--', linewidth=1)
# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# plot_filename = f'{today}_pbdb-missing_dois_percent_inter.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# ax.barh(missing_doi_count['journal'], missing_doi_count['percentage'], color=[color_mapping_journals[x] for x in missing_doi_count['journal']], edgecolor='black', linewidth=1.2)

# for i, pct in enumerate(missing_doi_count['percentage']):
#     ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

# ax.set_yticks(missing_doi_count['journal'])
# ax.set_xlabel('Percent of articles', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# ax.set_title('Proportion of missing genera', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.set_axisbelow(True)
# ax.set_xlim(0, missing_doi_count['percentage'].max() * 1.5)
# ax.set_facecolor(bg_col)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# merged_df = pd.merge(papers_counts, missing_doi_count, on='journal')
# merged_df = merged_df.rename(columns={'count_x': 'count_all', 'count_y': 'count_missing'})
# merged_df['percentage_all'] = (merged_df['count_missing'] / merged_df['count_all']) * 100
# merged_df = merged_df.sort_values(by='percentage_all', ascending=True)

# plot_filename = f'{today}_pbdb-missing_dois_percent_intra.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# ax.barh(merged_df['journal'], merged_df['percentage_all'], color=[color_mapping_journals[x] for x in merged_df['journal']], edgecolor='black', linewidth=1.2)

# for i, pct in enumerate(merged_df['percentage_all']):
#     ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

# ax.set_yticks(merged_df['journal'])
# ax.set_xlabel('Percent of articles', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# for label in ax.get_yticklabels():
#     label.set_fontstyle('italic')
# ax.set_title('Proportion of articles with missing genus', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.set_axisbelow(True)
# ax.set_xlim(0, merged_df['percentage_all'].max() * 1.5)
# ax.set_facecolor(bg_col)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# ##### ---------- Burmese amber graphs ---------- #####
# df_myanmar = df_classified[df_classified['geography'] == 'Myanmar']
# print(f'There are {len(df_myanmar)} species from Myanmar.\n')

# ## By category
# myanmar_counts = df_myanmar['classification'].value_counts().reindex(cat_order, fill_value=0).reset_index(name='count')
# myanmar_counts['percentage'] = (myanmar_counts['count'] / len(df_myanmar)) * 100

# plot_filename = f'{today}_myanmar_groups.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# ax.barh(myanmar_counts['classification'], myanmar_counts['percentage'], color=[color_mapping_groups[x] for x in all_counts['classification']], edgecolor='black', linewidth=1.2)

# for i, pct in enumerate(myanmar_counts['percentage']):
#     ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

# ax.set_yticks(myanmar_counts['classification'])
# ax.set_xlabel('Percent of new species', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# ax.set_title('Category distribution of new species from Myanmar', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.set_axisbelow(True)
# ax.set_xlim(0, 100)
# ax.set_facecolor(bg_col)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# ## By country
# all_countries = df_insecta['geography'].value_counts().reset_index(name='count')
# all_countries['percentage'] = (all_countries['count'] / len(df_insecta)) * 100
# cut = 20
# all_countries = all_countries.head(cut)

# plot_filename = f'{today}_insects_countries_top-{cut}.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# ax.barh(all_countries['geography'], all_countries['percentage'], color=[color_mapping_geo[x] for x in all_countries['geography']], edgecolor='black', linewidth=1.2)

# for i, pct in enumerate(all_countries['percentage']):
#     ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

# ax.set_yticks(all_countries['geography'])
# ax.set_xlabel('Percent of new species', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# ax.set_title(f'Geographic distribution of new insect species (top {cut})', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.set_axisbelow(True)
# ax.set_xlim(0, all_countries['percentage'].max() * 1.5)
# ax.invert_yaxis()
# ax.set_facecolor(bg_col)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# ## By time
# years_order = list(range(2000, 2027))
# myanmar_years = df_myanmar['year'].value_counts().reindex(years_order, fill_value=0).reset_index(name='count')

# plot_filename = f'{today}_myanmar_time.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# ax.barh(myanmar_years['year'], myanmar_years['count'], color='#7faf40', edgecolor='black', linewidth=1.2)

# ax.set_yticks(myanmar_years['year'])
# ax.set_xlabel('Count', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# ax.set_title('New species from Myanmar', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.grid(axis='x', alpha=alpha, linestyle='--')
# ax.set_axisbelow(True)
# ax.set_xlim(0, 25)
# ax.set_facecolor(bg_col)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# # ########################## CLADE-BASED SUMMARIES AND GRAPHS ################################




# # ##################
# # ### ARTHROPODA ###
# # ##################

# # Additional ranks to add
# ranks = ['Deuteropoda', 'Radiodonta', 'Trilobita', 'Chelicerata', 'Arachnida', 'Ostracoda', 'Decapoda']
# for rank in ranks:
#     df_arthropoda[rank] = df_arthropoda[rank_columns].apply(lambda row: rank in row.values, axis=1)

# condition = (df_arthropoda['Deuteropoda'] == False)
# df_arthropoda.loc[condition, 'classification_arth'] = 'Non-deuteropod pan-arthopods'
# condition = (df_arthropoda['Radiodonta'] == True)
# df_arthropoda.loc[condition, 'classification_arth'] = 'Radiodonts'
# condition = (df_arthropoda['Trilobita'] == True)
# df_arthropoda.loc[condition, 'classification_arth'] = 'Trilobites'
# condition = (df_arthropoda['Arachnida'] == True)
# df_arthropoda.loc[condition, 'classification_arth'] = 'Arachnids'
# condition = (df_arthropoda['Chelicerata'] == True) & (df_arthropoda['Arachnida'] == False)
# df_arthropoda.loc[condition, 'classification_arth'] = 'Non-arachnid chelicerates'
# condition = (df_arthropoda['Ostracoda'] == True)
# df_arthropoda.loc[condition, 'classification_arth'] = 'Ostracods'
# condition = (df_arthropoda['Decapoda'] == True)
# df_arthropoda.loc[condition, 'classification_arth'] = 'Decapods'
# condition = (df_arthropoda['Insecta'] == True)
# df_arthropoda.loc[condition, 'classification_arth'] = 'Insects'
# ## Catch-all for anything remaining
# condition = (df_arthropoda['Deuteropoda'] == True) & (df_arthropoda['classification_arth'].isna())
# df_arthropoda.loc[condition, 'classification_arth'] = 'Other deuteropods'

# arth_order = ['Non-deuteropod pan-arthopods', 'Radiodonts', 'Trilobites', 'Arachnids', 'Non-arachnid chelicerates', 'Ostracods', 'Decapods', 'Insects', 'Other deuteropods']
# journal_order = ['Nature', 'Science', 'Curr Biol', 'Gondwana Res', 'Nat Commun', 'Nat Ecol Evol', 'Proc Natl Acad Sci USA', 'Sci Adv', 'J Paleontol', 'J Syst Palaeontol', 'Palaeontology', 'Pap Palaeontol']

# arth_count = df_arthropoda.groupby(['journal', 'classification_arth']).size().reset_index(name='count')
# arth_count['classification_arth'] = pd.Categorical(arth_count['classification_arth'], categories=arth_order, ordered=True)
# arth_count = arth_count.sort_values('classification_arth')

# pivot_df = arth_count.pivot(index='journal', columns='classification_arth', values='count').fillna(0)
# pivot_df = pivot_df.loc[journal_order[::-1]]
# pivot_pct = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

# # Color map
# select_categories = sorted(arth_count['classification_arth'].dropna().unique())
# cmap_arth = plt.get_cmap('Set1')
# colors_arth = cmap_arth(np.arange(len(select_categories)))

# plot_filename = f'{today}_panarthropoda_relative-proportions.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# pivot_pct.plot(kind='barh', stacked=True, ax=ax, color=colors_arth, edgecolor='black', linewidth=0.5)

# # Labels, etc.
# ax.set_xlabel('Percentage (%)', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# for label in ax.get_yticklabels():
#     label.set_fontstyle('italic')
# ax.set_title('Relative Proportion of Pan-Arthropoda by Journal', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.legend(title='', bbox_to_anchor=(0.38, -0.15), loc='upper center', fontsize=legend_font, ncol=2)
# ax.grid(axis='x', alpha=alpha, linestyle='--')
# ax.set_axisbelow(True)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# # ###############
# # ### INSECTA ###
# # ###############

# # Additional ranks to add
# ranks = ['Archaeognatha', 'Hydropalaeoptera', 'Polyneoptera', 'Lepidoptera', 'Coleoptera', 'Hemiptera', 'Hymenoptera', 'Diptera', 'Antliophora', 'Panorpida', 'Neuroptera', 'Neoneuroptera', 'Myrmeleontiformia']
# for rank in ranks:
#     df_insecta[rank] = df_insecta[rank_columns].apply(lambda row: rank in row.values, axis=1)

# condition = (df_insecta['Archaeognatha'] == True)
# df_insecta.loc[condition, 'classification_insect'] = 'Archaeognathans'
# condition = (df_insecta['Hydropalaeoptera'] == True)
# df_insecta.loc[condition, 'classification_insect'] = 'Paleopterans'
# condition = (df_insecta['Polyneoptera'] == True)
# df_insecta.loc[condition, 'classification_insect'] = 'Polyneopterans'
# condition = (df_insecta['Lepidoptera'] == True)
# df_insecta.loc[condition, 'classification_insect'] = 'Lepidopterans'
# condition = (df_insecta['Coleoptera'] == True)
# df_insecta.loc[condition, 'classification_insect'] = 'Coleopterans'
# condition = (df_insecta['Hemiptera'] == True)
# df_insecta.loc[condition, 'classification_insect'] = 'Hemipterans'
# condition = (df_insecta['Hymenoptera'] == True)
# df_insecta.loc[condition, 'classification_insect'] = 'Hymenopterans'
# condition = (df_insecta['Diptera'] == True)
# df_insecta.loc[condition, 'classification_insect'] = 'Dipterans'
# condition = (df_insecta['Myrmeleontiformia'] == True)
# df_insecta.loc[condition, 'classification_insect'] = 'Myrmeleontiformians'
# condition = (df_insecta['Diptera'] == False) & (df_insecta['Antliophora'] == True)
# df_insecta.loc[condition, 'classification_insect'] = 'Other antliophorans'
# condition = (df_insecta['Panorpida'] == True) & (df_insecta['classification_insect'].isna())
# df_insecta.loc[condition, 'classification_insect'] = 'Other panorpidans'
# condition = (df_insecta['Neoneuroptera'] == True) & (df_insecta['classification_insect'].isna())
# df_insecta.loc[condition, 'classification_insect'] = 'Other neoneuropterans'
# condition = (df_insecta['Neuroptera'] == True) & (df_insecta['classification_insect'].isna())
# df_insecta.loc[condition, 'classification_insect'] = 'Other neuropterans'
# ## Catch-all for anything remaining
# condition = (df_insecta['classification_insect'].isna())
# df_insecta.loc[condition, 'classification_insect'] = 'Other insects'

# insect_order = ['Archaeognathans', 'Paleopterans', 'Polyneopterans', 'Lepidopterans', 'Hemipterans', 'Hymenopterans', 'Other panorpidans', 'Coleopterans', 'Dipterans', 'Other antliophorans', 'Myrmeleontiformians', 'Other neoneuropterans', 'Other neuropterans', 'Other insects']
# journal_order = ['Nature', 'Science', 'Curr Biol', 'Gondwana Res', 'Nat Commun', 'Proc Natl Acad Sci USA', 'Sci Adv', 'J Paleontol', 'J Syst Palaeontol', 'Palaeontology', 'Pap Palaeontol']

# insect_count = df_insecta.groupby(['journal', 'classification_insect']).size().reset_index(name='count')
# insect_count['classification_insect'] = pd.Categorical(insect_count['classification_insect'], categories=insect_order, ordered=True)
# insect_count = insect_count.sort_values('classification_insect')

# pivot_df = insect_count.pivot(index='journal', columns='classification_insect', values='count').fillna(0)
# pivot_df = pivot_df.loc[journal_order[::-1]]
# pivot_pct = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

# # Color map
# select_categories = sorted(insect_count['classification_insect'].dropna().unique())
# cmap_arth = plt.get_cmap('tab20c')
# colors_arth = cmap_arth(np.arange(len(select_categories)))

# plot_filename = f'{today}_insecta_relative-proportions.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# pivot_pct.plot(kind='barh', stacked=True, ax=ax, color=colors_arth, edgecolor='black', linewidth=0.5)

# # Labels, etc.
# ax.set_xlabel('Percentage (%)', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# for label in ax.get_yticklabels():
#     label.set_fontstyle('italic')
# ax.set_title('Relative Proportion of Insecta by Journal', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.legend(title='', bbox_to_anchor=(0.38, -0.15), loc='upper center', fontsize=legend_font, ncol=2)
# ax.grid(axis='x', alpha=alpha, linestyle='--')
# ax.set_axisbelow(True)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# # ######################
# # ### MAMMALIAMORPHA ###
# # ######################

# # Additional ranks to add
# ranks = ['Eutriconodonta', 'Allotheria', 'Multituberculata', 'Metatheria', 'Monotremata', 'Afrotheria', 'Carnivora', 'Xenarthra', 'Euungulata', 'Chiroptera', 'Rodentia']
# for rank in ranks:
#     df_mammal[rank] = df_mammal[rank_columns].apply(lambda row: rank in row.values, axis=1)

# condition = (df_mammal['Mammaliamorpha'] == True) & (df_mammal['Mammalia'] == False)
# df_mammal.loc[condition, 'classification_mamm'] = 'Non-mammalian mammaliamorphs'
# condition = (df_mammal['Eutriconodonta'] == True)
# df_mammal.loc[condition, 'classification_mamm'] = 'Eutriconodonts'
# condition = (df_mammal['Primates'] == True)
# df_mammal.loc[condition, 'classification_mamm'] = 'Primates'
# condition = (df_mammal['Afrotheria'] == True)
# df_mammal.loc[condition, 'classification_mamm'] = 'Afrotherians'
# condition = (df_mammal['Metatheria'] == True)
# df_mammal.loc[condition, 'classification_mamm'] = 'Metatherians'
# condition = (df_mammal['Allotheria'] == True)
# df_mammal.loc[condition, 'classification_mamm'] = 'Other allotherians'
# condition = (df_mammal['Multituberculata'] == True)
# df_mammal.loc[condition, 'classification_mamm'] = 'Multituberculates'
# condition = (df_mammal['Monotremata'] == True)
# df_mammal.loc[condition, 'classification_mamm'] = 'Monotremes'
# condition = (df_mammal['Rodentia'] == True)
# df_mammal.loc[condition, 'classification_mamm'] = 'Rodents'
# condition = (df_mammal['Xenarthra'] == True)
# df_mammal.loc[condition, 'classification_mamm'] = 'Xenarthrans'
# condition = (df_mammal['Euungulata'] == True)
# df_mammal.loc[condition, 'classification_mamm'] = 'Ungulates'
# condition = (df_mammal['Carnivora'] == True)
# df_mammal.loc[condition, 'classification_mamm'] = 'Carnivorans'
# condition = (df_mammal['Chiroptera'] == True)
# df_mammal.loc[condition, 'classification_mamm'] = 'Chiropterans'
# condition = (df_mammal['Placentalia'] == True) & (df_mammal['classification_mamm'].isna())
# df_mammal.loc[condition, 'classification_mamm'] = 'Other placental mammals'
# condition = (df_mammal['Mammalia'] == True) & (df_mammal['classification_mamm'].isna())
# df_mammal.loc[condition, 'classification_mamm'] = 'Other non-placental mammals'
# ## Catch-all for anything remaining
# condition = (df_mammal['classification_mamm'].isna())
# df_mammal.loc[condition, 'classification_mamm'] = 'Other'

# mammal_order = ['Non-mammalian mammaliamorphs', 'Eutriconodonts', 'Monotremes', 'Metatherians', 'Multituberculates', 'Other allotherians', 'Afrotherians', 'Rodents', 'Chiropterans', 'Xenarthrans', 'Ungulates', 'Carnivorans', 'Primates', 'Other placental mammals', 'Other non-placental mammals', 'Other']
# journal_order = ['Nature', 'Science', 'Curr Biol', 'Gondwana Res', 'Nat Commun', 'Nat Ecol Evol', 'Proc Natl Acad Sci USA', 'Sci Adv', 'J Paleontol', 'J Syst Palaeontol', 'J Vert Paleontol', 'Palaeontology', 'Pap Palaeontol']

# mammal_count = df_mammal.groupby(['journal', 'classification_mamm']).size().reset_index(name='count')
# mammal_count['classification_mamm'] = pd.Categorical(mammal_count['classification_mamm'], categories=mammal_order, ordered=True)
# mammal_count = mammal_count.sort_values('classification_mamm')

# pivot_df = mammal_count.pivot(index='journal', columns='classification_mamm', values='count').fillna(0)
# pivot_df = pivot_df.loc[journal_order[::-1]]
# pivot_pct = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

# # Color map
# select_categories = sorted(mammal_count['classification_mamm'].dropna().unique())
# cmap_mamm = plt.get_cmap('tab20')
# colors_mamm = cmap_mamm(np.arange(len(select_categories)))

# plot_filename = f'{today}_mammalia_relative-proportions.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# pivot_pct.plot(kind='barh', stacked=True, ax=ax, color=colors_mamm, edgecolor='black', linewidth=0.5)

# # Labels, etc.
# ax.set_xlabel('Percentage (%)', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# for label in ax.get_yticklabels():
#     label.set_fontstyle('italic')
# ax.set_title('Relative Proportion of Mammaliamorpha by Journal', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.legend(title='', bbox_to_anchor=(0.38, -0.15), loc='upper center', fontsize=legend_font, ncol=2)
# ax.grid(axis='x', alpha=alpha, linestyle='--')
# ax.set_axisbelow(True)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)


# #######################
# ### AVEMETATARSALIA ###
# #######################

# # Additional ranks to add
# ranks = ['Pterosauria', 'Sauropodomorpha', 'Marginocephalia', 'Ornithopoda', 'Thyreophora', 'Enantiornithes', 'Euornithes']
# for rank in ranks:
#     df_avemet[rank] = df_avemet[rank_columns].apply(lambda row: rank in row.values, axis=1)

# # condition = (df_avemet['Dinosauromorpha'] == True) & (df_avemet['Dinosauria'] == False)
# # df_avemet.loc[condition, 'classification_avemet'] = 'Non-dinosaur dinosauromorphs'
# condition = (df_avemet['Pterosauria'] == True)
# df_avemet.loc[condition, 'classification_avemet'] = 'Pterosaurs'
# condition = (df_avemet['Sauropodomorpha'] == True)
# df_avemet.loc[condition, 'classification_avemet'] = 'Saurischia (sauropodomorphs)'
# condition = (df_avemet['Marginocephalia'] == True)
# df_avemet.loc[condition, 'classification_avemet'] = 'Ornithischia (marginocephalians)'
# condition = (df_avemet['Thyreophora'] == True)
# df_avemet.loc[condition, 'classification_avemet'] = 'Ornithischia (thyreophorans)'
# condition = (df_avemet['Ornithopoda'] == True)
# df_avemet.loc[condition, 'classification_avemet'] = 'Ornithischia (ornithopods)'
# condition = (df_avemet['Ornithischia'] == True) & (df_avemet['classification_avemet'].isna())
# df_avemet.loc[condition, 'classification_avemet'] = 'Ornithischia (other)'
# condition = (df_avemet['Enantiornithes'] == True)
# df_avemet.loc[condition, 'classification_avemet'] = 'Saurischia (enantiornithines)'
# condition = (df_avemet['Aves'] == True)
# df_avemet.loc[condition, 'classification_avemet'] = 'Saurischia (euornithines)'
# condition = ((df_avemet['Avialae'] == True) | (df_avemet['Aves'] == True)) & (df_avemet['classification_avemet'].isna())
# df_avemet.loc[condition, 'classification_avemet'] = 'Saurischia (other avians)'
# condition = (df_avemet['Theropoda'] == True) & (df_avemet['classification_avemet'].isna())
# df_avemet.loc[condition, 'classification_avemet'] = 'Saurischia (non-avian theropods)'
# condition = (df_avemet['Saurischia'] == True) & (df_avemet['classification_avemet'].isna())
# df_avemet.loc[condition, 'classification_avemet'] = 'Saurischia (other)'
# ## Catch-all for anything remaining
# condition = (df_avemet['classification_avemet'].isna())
# df_avemet.loc[condition, 'classification_avemet'] = 'Other non-dinosaurs'

# avemet_order = ['Pterosaurs', 'Other non-dinosaurs', 'Saurischia (sauropodomorphs)', 'Saurischia (non-avian theropods)', 'Saurischia (enantiornithines)', 'Saurischia (euornithines)', 'Saurischia (other avians)', 'Saurischia (other)', 'Ornithischia (marginocephalians)', 'Ornithischia (thyreophorans)', 'Ornithischia (ornithopods)', 'Ornithischia (other)']
# journal_order = ['Nature', 'Science', 'Curr Biol', 'Gondwana Res', 'Nat Commun', 'Nat Ecol Evol', 'Proc Natl Acad Sci USA', 'Sci Adv', 'J Paleontol', 'J Syst Palaeontol', 'J Vert Paleontol', 'Palaeontology', 'Pap Palaeontol']

# avemet_count = df_avemet.groupby(['journal', 'classification_avemet']).size().reset_index(name='count')
# avemet_count['classification_avemet'] = pd.Categorical(avemet_count['classification_avemet'], categories=avemet_order, ordered=True)
# avemet_count = avemet_count.sort_values('classification_avemet')

# pivot_df = avemet_count.pivot(index='journal', columns='classification_avemet', values='count').fillna(0)
# pivot_df = pivot_df.loc[journal_order[::-1]]
# pivot_pct = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

# # Color map
# select_categories = sorted(avemet_count['classification_avemet'].dropna().unique())
# cmap_avemet = plt.get_cmap('Paired')
# colors_avemet = cmap_avemet(np.arange(len(select_categories)))

# plot_filename = f'{today}_avemetatarsalia_relative-proportions.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# pivot_pct.plot(kind='barh', stacked=True, ax=ax, color=colors_avemet, edgecolor='black', linewidth=0.5)

# # Labels, etc.
# ax.set_xlabel('Percentage (%)', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# for label in ax.get_yticklabels():
#     label.set_fontstyle('italic')
# ax.set_title('Relative Proportion of Avemetatarsalia by Journal', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.legend(title='', bbox_to_anchor=(0.38, -0.15), loc='upper center', fontsize=legend_font, ncol=2)
# ax.grid(axis='x', alpha=alpha, linestyle='--')
# ax.set_axisbelow(True)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# ## non-avian dinosaurs
# non_bird_dinos = df_avemet[(df_avemet['Dinosauria']) & (~df_avemet['Aves']) & (~df_avemet['Avialae'])]
# print(f'There are {len(non_bird_dinos)} non-avian dinosaurs in the dataset.\n')

# non_bird_dinos_count = non_bird_dinos.groupby('journal').size().reset_index(name='count')
# print(non_bird_dinos_count)

# # pivot_df = non_bird_dinos_count.pivot(index='journal', columns='classification_avemet', values='count').fillna(0)
# # pivot_df = pivot_df.sort_index(ascending=False)
# # pivot_pct = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

# # # Color map
# # select_categories = sorted(df_avemet['journal'].dropna().unique())
# # cmap_avemet = plt.get_cmap('tab20b')
# # colors_avemet = cmap_avemet(np.arange(len(select_categories)))

# # plot_filename = f'{today}_non-avian-dinosaurs_relative-proportions.{plot_format}'
# # fig, ax = plt.subplots(figsize=(img_width, img_height))

# # pivot_pct.plot(kind='barh', stacked=True, ax=ax, color=colors_avemet, edgecolor='black', linewidth=0.5)

# # # Labels, etc.
# # ax.set_xlabel('Percentage (%)', fontsize=axis_font, fontweight='bold')
# # ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# # ax.set_title('Relative Proportion of Avemetatarsalia by Journal', fontsize=title_font, fontweight='bold')
# # ax.tick_params(labelsize=tick_font)
# # ax.legend(title='', bbox_to_anchor=(0.38, -0.15), loc='upper center', fontsize=legend_font, ncol=2)
# # ax.grid(axis='x', alpha=alpha, linestyle='--')
# # ax.set_axisbelow(True)

# # plt.tight_layout()
# # plot_path = os.path.join(plots_dir, plot_filename)
# # plt.savefig(plot_path, format=plot_format, dpi=dpi)
# # plt.close(fig)

# # #### Since 2020 only ####
# # df_avemet_2020 = df_avemet[df_avemet['year'] >= 2020]

# # avemet_count_2020 = df_avemet_2020.groupby(['journal', 'classification_avemet']).size().reset_index(name='count')

# # pivot_df = avemet_count_2020.pivot(index='journal', columns='classification_avemet', values='count').fillna(0)
# # pivot_df = pivot_df.sort_index(ascending=False)
# # pivot_pct = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

# # # Color map
# # select_categories = sorted(df_avemet['journal'].dropna().unique())
# # cmap_avemet = plt.get_cmap('tab20b')
# # colors_avemet = cmap_avemet(np.arange(len(select_categories)))

# # plot_filename = f'{today}_avemetatarsalia_relative-proportions_2020-present.{plot_format}'
# # fig, ax = plt.subplots(figsize=(img_width, img_height))

# # pivot_pct.plot(kind='barh', stacked=True, ax=ax, color=colors_avemet, edgecolor='black', linewidth=0.5)

# # # Labels, etc.
# # ax.set_xlabel('Percentage (%)', fontsize=axis_font, fontweight='bold')
# # ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# # ax.set_title('Relative Proportion of Avemetatarsalia by Journal', fontsize=title_font, fontweight='bold')
# # ax.tick_params(labelsize=tick_font)
# # ax.legend(title='', bbox_to_anchor=(0.38, -0.15), loc='upper center', fontsize=legend_font, ncol=2)
# # ax.grid(axis='x', alpha=alpha, linestyle='--')
# # ax.set_axisbelow(True)

# # plt.tight_layout()
# # # plt.show()
# # plot_path = os.path.join(plots_dir, plot_filename)
# # plt.savefig(plot_path, format=plot_format, dpi=dpi)
# # plt.close(fig)


# # ##################
# # ### AMPHIBIANS ###
# # ##################

# # Additional ranks to add
# ranks = ['Lissamphibia', 'Temnospondyli']
# for rank in ranks:
#     df_amphibian[rank] = df_amphibian[rank_columns].apply(lambda row: rank in row.values, axis=1)

# condition = (df_amphibian['Lissamphibia'] == True)
# df_amphibian.loc[condition, 'classification_amphib'] = 'Lissamphibians'
# condition = (df_amphibian['Tetrapoda'] == False)
# df_amphibian.loc[condition, 'classification_amphib'] = 'Stem tetrapods'
# condition = (df_amphibian['Temnospondyli'] == True) & (df_amphibian['Lissamphibia'] == False)
# df_amphibian.loc[condition, 'classification_amphib'] = 'Non-lissamphibian temnospondyls'
# ## Catch-all for anything remaining
# condition = (df_amphibian['classification_amphib'].isna())
# df_amphibian.loc[condition, 'classification_amphib'] = 'Other early tetrapods'

# amphib_order = ['Stem tetrapods', 'Non-lissamphibian temnospondyls', 'Lissamphibians', 'Other early tetrapods']
# journal_order = ['Nature', 'Science', 'Gondwana Res', 'Nat Commun', 'Nat Ecol Evol', 'Proc Natl Acad Sci USA', 'J Paleontol', 'J Syst Palaeontol', 'J Vert Paleontol', 'Palaeontology', 'Pap Palaeontol']

# amphib_count = df_amphibian.groupby(['journal', 'classification_amphib']).size().reset_index(name='count')
# amphib_count['classification_amphib'] = pd.Categorical(amphib_count['classification_amphib'], categories=amphib_order, ordered=True)
# amphib_count = amphib_count.sort_values('classification_amphib')

# pivot_df = amphib_count.pivot(index='journal', columns='classification_amphib', values='count').fillna(0)
# pivot_df = pivot_df.loc[journal_order[::-1]]
# pivot_pct = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

# # Color map
# select_categories = sorted(amphib_count['classification_amphib'].dropna().unique())
# cmap_arth = plt.get_cmap('Dark2')
# colors_arth = cmap_arth(np.arange(len(select_categories)))

# plot_filename = f'{today}_amphibians_relative-proportions.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# pivot_pct.plot(kind='barh', stacked=True, ax=ax, color=colors_arth, edgecolor='black', linewidth=0.5)

# # Labels, etc.
# ax.set_xlabel('Percentage (%)', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# for label in ax.get_yticklabels():
#     label.set_fontstyle('italic')
# ax.set_title('Relative Proportion of Amphibians by Journal', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.legend(title='', bbox_to_anchor=(0.38, -0.15), loc='upper center', fontsize=legend_font, ncol=2)
# ax.grid(axis='x', alpha=alpha, linestyle='--')
# ax.set_axisbelow(True)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)


####################### multi-species vs. single-species descriptions ###############
single = []
multiple = []
journals = []
invert_count = []
all_count = []
columns = ['journal', 'single', 'multiple', 'invert_count', 'all_count']
df_species = pd.DataFrame(columns=columns)

for journal, subset_df in df_classified.groupby('journal'):
        multi_species = (subset_df['doi'].value_counts() > 1).sum()
        single_species = (subset_df['doi'].value_counts() == 1).sum()
        print(f'There are {multi_species} papers that describe more than one species and {single_species} papers that describe only one species in {journal}.\n')
        invert = (~subset_df['Vertebrata']).sum()
        all = len(subset_df)
        single.append(single_species)
        multiple.append(multi_species)
        journals.append(journal)
        invert_count.append(invert)
        all_count.append(all)

df_species['journal'] = journals
df_species['single'] = single
df_species['multiple'] = multiple
df_species['invert_count'] = invert_count
df_species['all_count'] = all_count
df_species['percent_multiple'] = (df_species['multiple'] / (df_species['multiple'] + df_species['single'])) * 100
df_species['percent_invert'] = (df_species['invert_count'] / df_species['all_count']) * 100

print(df_species)
journal_order = ['Nature', 'Science', 'Curr Biol', 'Gondwana Res', 'Nat Commun', 'Nat Ecol Evol', 'Proc Natl Acad Sci USA', 'Sci Adv', 'J Paleontol', 'J Syst Palaeontol', 'J Vert Paleontol', 'Palaeontology', 'Pap Palaeontol']
df_species['journal'] = pd.Categorical(df_species['journal'], categories=reversed(journal_order), ordered=True)
df_species = df_species.sort_values(by='journal')

plot_filename = f'{today}_journals_multi-species.{plot_format}'
fig, ax = plt.subplots(figsize=(img_width, img_height))

ax.barh(df_species['journal'], df_species['percent_multiple'], color=[color_mapping_journals[x] for x in df_species['journal']], edgecolor='black', linewidth=1.2)

for i, pct in enumerate(df_species['percent_multiple']):
    ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

ax.set_yticks(df_species['journal'])
ax.set_xlabel('Percent of articles', fontsize=axis_font, fontweight='bold')
ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
for label in ax.get_yticklabels():
    label.set_fontstyle('italic')
ax.set_title('Proportion of articles with multiple new species', fontsize=title_font, fontweight='bold')
ax.tick_params(labelsize=tick_font)
ax.set_axisbelow(True)
ax.set_xlim(0, df_species['percent_multiple'].max() * 1.5)
ax.set_facecolor(bg_col)

plt.tight_layout()
plot_path = os.path.join(plots_dir, plot_filename)
plt.savefig(plot_path, format=plot_format, dpi=dpi)
plt.close(fig)

# Drop JVP from next graph
df_species_invert = df_species.drop(df_species[df_species['journal'] == 'J Vert Paleontol'].index)
color_mapping_journals_12 = {key: val for key, val in color_mapping_journals.items() if key != 'J Vert Paleontol'}
colors = df_species_invert['journal'].map(color_mapping_journals_12)

plot_filename = f'{today}_journals_invert-vs-multi.{plot_format}'
fig, ax = plt.subplots(figsize=(img_width, img_height))
ax.scatter(df_species_invert['percent_invert'], df_species_invert['percent_multiple'], color=colors, s=50)
ax.set_title('Comparison of non-vertebrate composition and multi-species description', fontsize=title_font, fontweight='bold')
ax.set_xlabel('Percent of species that are non-vertebrates', fontsize=axis_font, fontweight='bold')
ax.set_ylabel('Percent of articles that describe multiple species', fontsize=axis_font, fontweight='bold')
ax.grid(axis='both', alpha=alpha, linestyle='--')
ax.set_axisbelow(True)
ax.set_facecolor(bg_col)
ax.set_ylim(0, 50)

# Add trendline
coefficients = np.polyfit(df_species_invert['percent_invert'], df_species_invert['percent_multiple'], deg=1)
trendline_equation = np.poly1d(coefficients)
x_sorted = np.sort(df_species_invert['percent_invert'])
plt.plot(x_sorted, trendline_equation(x_sorted), color="red", linestyle="--", linewidth=2, label=f"{trendline_equation}")

# slope, intercept, r_value, p_value, std_err = stats.linregress(df_species_invert['percent_invert'], df_species_invert['percent_multiple'])
# r2_value = r_value ** 2
# print(r2_value)
# plt.plot(df_species_invert['percent_invert'], slope * df_species_invert['percent_invert'] + intercept, color='red', linewidth=2, 
#          label=f'Fit: $R^2$ = {r2_value:.2f}')

plt.tight_layout()
plot_path = os.path.join(plots_dir, plot_filename)
plt.savefig(plot_path, format=plot_format, dpi=dpi)
plt.close(fig)

####################### AUTHOR FREQUENCY IN NATURE AND SCIENCE ###############
pub_bins = [0, 2, 5, 50]
pub_labels = ['1 article', '2-4 articles', '>5 articles']
# frequencies = df_names['count'].value_counts(bins=pub_bins, sort=False).reset_index()
# print(f'There are {len(df_names)} unique names in the focal journals.\n')
# print(frequencies)

# frequencies = df_orcids['count'].value_counts(bins=pub_bins, sort=False).reset_index()
# print(f'There are {len(df_orcids)} unique ORCIDs in the focal journals.\n')
# print(frequencies)

# frequencies = df_names_orcids['count'].value_counts(bins=pub_bins, sort=False).reset_index()
# print(f'There are {len(df_names_orcids)} unique name-ORCIDs in the focal journals.\n')
# print(frequencies)

authors_dict = {
    'Names-only': df_names,
    'ORCIDs-only': df_orcids,
    'Names-ORCIDS': df_names_orcids
}

authors_variables_dict = {
    'names': df_names,
    'orcids': df_orcids,
    'names_and_orcids': df_names_orcids
}

for variable, df in authors_variables_dict.items():
    nature = df[df['journal'] == 'Nature']
    science = df[df['journal'] == 'Science']

    df['count_bin'] = pd.cut(df['count'], bins=pub_bins, labels=pub_labels)

    grouped_df = df.groupby(['journal', 'count_bin'], observed=False).size().reset_index(name='count')
    grouped_df['percentage'] = np.where(grouped_df['journal'] == 'Science', (grouped_df['count']/(len(science))) * 100, (grouped_df['count']/(len(nature)))*100)
    nature_results = grouped_df[grouped_df['journal'] == 'Nature']
    science_results = grouped_df[grouped_df['journal'] == 'Science']

    nature_percents=nature_results['percentage']
    science_percents=science_results['percentage']

    plot_filename = f'{today}_repeat_authorship_{variable}_separated.{plot_format}'
    fig, ax = plt.subplots(figsize=(img_width, img_height/2))

    # ax.barh(result['count'], result['percentage'], color=bar_colors, edgecolor='black', linewidth=1.2)
    # y=np.arange(2)
    # height = 0.35
    # rects1 = ax.barh(y - height/2, nature_percents, height, label='Nature', color='#1f77b4')
    # rects2 = ax.barh(y + height/2, science_percents, height, label='Science', color='#ff7f0e')

    ax = grouped_df.plot(x='percentage', y=['journal', 'count_bin'], kind='barh', width=0.8)

    # for i, pct in enumerate(result['percentage']):
    #     ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

    ax.set_xlabel('Percent of unique authors', fontsize=axis_font, fontweight='bold')
    ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
    ax.set_title('Proportion of authors listed on multiple Nature or Science articles', fontsize=title_font, fontweight='bold')
    ax.tick_params(labelsize=tick_font)
    ax.grid(axis='x', alpha=alpha, linestyle='--')
    ax.set_axisbelow(True)
    ax.set_xlim(0, 100)
    ax.set_facecolor(bg_col)

    plt.tight_layout()
    plot_path = os.path.join(plots_dir, plot_filename)
    plt.savefig(plot_path, format=plot_format, dpi=dpi)
    plt.close(fig)

    # frequencies = pd.cut(df['count'], bins=pub_bins, labels=pub_labels).value_counts().reset_index(name='size')
    # print(f'There are {len(df)} unique values across the focal journals for {variable} (author names are divided by journal).\n')
    # frequencies['percentage'] = (frequencies['size']/len(df)) * 100

    # plot_filename = f'{today}_repeat_authorship_{variable}_separated.{plot_format}'
    # fig, ax = plt.subplots(figsize=(img_width, img_height/2))

    # ax.barh(frequencies['count'], frequencies['percentage'], color="#884747", edgecolor='black', linewidth=1.2)

    # for i, pct in enumerate(frequencies['percentage']):
    #     ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

    # ax.set_xlabel('Percent of unique authors', fontsize=axis_font, fontweight='bold')
    # ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
    # ax.set_title('Proportion of authors listed on multiple Nature or Science articles', fontsize=title_font, fontweight='bold')
    # ax.tick_params(labelsize=tick_font)
    # ax.grid(axis='x', alpha=alpha, linestyle='--')
    # ax.set_axisbelow(True)
    # ax.set_xlim(0, 100)
    # ax.set_facecolor(bg_col)

    # plt.tight_layout()
    # plot_path = os.path.join(plots_dir, plot_filename)
    # plt.savefig(plot_path, format=plot_format, dpi=dpi)
    # plt.close(fig)

    # df_combined = df.groupby(variable)['count'].sum().reset_index().reset_index()
    # print(f'There are {len(df_combined)} unique values across the focal journals (author names are grouped between journal).\n')
    # frequencies = pd.cut(df_combined['count'], bins=pub_bins, labels=pub_labels).value_counts().reset_index(name='size')
    # frequencies['percentage'] = (frequencies['size']/len(df_combined)) * 100

    # plot_filename = f'{today}_repeat_authorship_{variable}_grouped.{plot_format}'
    # fig, ax = plt.subplots(figsize=(img_width, img_height/2))

    # ax.barh(frequencies['count'], frequencies['percentage'], color="#884747", edgecolor='black', linewidth=1.2)

    # for i, pct in enumerate(frequencies['percentage']):
    #     ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

    # ax.set_xlabel('Percent of unique authors', fontsize=axis_font, fontweight='bold')
    # ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
    # ax.set_title('Proportion of authors listed on multiple Nature or Science articles', fontsize=title_font, fontweight='bold')
    # ax.tick_params(labelsize=tick_font)
    # ax.grid(axis='x', alpha=alpha, linestyle='--')
    # ax.set_axisbelow(True)
    # ax.set_xlim(0, 100)
    # ax.set_facecolor(bg_col)

    # plt.tight_layout()
    # plot_path = os.path.join(plots_dir, plot_filename)
    # plt.savefig(plot_path, format=plot_format, dpi=dpi)
    # plt.close(fig)
    

    

# df_names_combined = df_names.groupby('names')['count'].sum().reset_index()
# df_orcids_combined = df_names.groupby('orcids')['count'].sum().reset_index()
# df_names_orcids_combined = df_names_orcids.groupby('names_orcids')['count'].sum().reset_index()

# author_dfs = ['df_names_combined', 'df_orcids_combined', 'df_names_orcids_combined']
# for df in author_dfs:
#     # frequencies = df['count'].value_counts(bins=pub_bins, sort=False).reset_index()
#     print(f'There are {len(df)} unique values across the focal journals for {df} (author names are divided by journal).\n')
#     print(frequencies)



# single = []
# multiple = []
# journals = []
# invert_count = []
# all_count = []
# columns = ['journal', 'single', 'multiple', 'invert_count', 'all_count']
# df_species = pd.DataFrame(columns=columns)

# for journal, subset_df in df_classified.groupby('journal'):
#         multi_species = (subset_df['doi'].value_counts() > 1).sum()
#         single_species = (subset_df['doi'].value_counts() == 1).sum()
#         print(f'There are {multi_species} papers that describe more than one species and {single_species} papers that describe only one species in {journal}.\n')
#         invert = (~subset_df['Vertebrata']).sum()
#         all = len(subset_df)
#         single.append(single_species)
#         multiple.append(multi_species)
#         journals.append(journal)
#         invert_count.append(invert)
#         all_count.append(all)

# df_species['journal'] = journals
# df_species['single'] = single
# df_species['multiple'] = multiple
# df_species['invert_count'] = invert_count
# df_species['all_count'] = all_count
# df_species['percent_multiple'] = (df_species['multiple'] / (df_species['multiple'] + df_species['single'])) * 100
# df_species['percent_invert'] = (df_species['invert_count'] / df_species['all_count']) * 100

# print(df_species)
# journal_order = ['Nature', 'Science', 'Curr Biol', 'Gondwana Res', 'Nat Commun', 'Nat Ecol Evol', 'Proc Natl Acad Sci USA', 'Sci Adv', 'J Paleontol', 'J Syst Palaeontol', 'J Vert Paleontol', 'Palaeontology', 'Pap Palaeontol']
# df_species['journal'] = pd.Categorical(df_species['journal'], categories=reversed(journal_order), ordered=True)
# df_species = df_species.sort_values(by='journal')

# plot_filename = f'{today}_journals_multi-species.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# ax.barh(df_species['journal'], df_species['percent_multiple'], color=[color_mapping_journals[x] for x in df_species['journal']], edgecolor='black', linewidth=1.2)

# for i, pct in enumerate(df_species['percent_multiple']):
#     ax.text(pct, i, f' {pct:.1f}%', ha='left', va='center', fontsize=label_font)

# ax.set_yticks(df_species['journal'])
# ax.set_xlabel('Percent of articles', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# for label in ax.get_yticklabels():
#     label.set_fontstyle('italic')
# ax.set_title('Proportion of articles with multiple new species', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.set_axisbelow(True)
# ax.set_xlim(0, df_species['percent_multiple'].max() * 1.5)
# ax.set_facecolor(bg_col)

# plt.tight_layout()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

print('Graphing complete.\n')

# #####################################


# plot_filename = f'{today}_20-cat_relative-proportions.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# # Map colors to the columns in pivot_pct
# # plot_colors = [colors[journal] for journal in pivot_pct.columns]

# pivot_pct.plot(kind='barh', stacked=True, ax=ax, color=colors, edgecolor='black', linewidth=0.5)

# # Labels, etc.
# ax.set_xlabel('Percentage (%)', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# ax.set_title('Relative Proportion of Clades by Journal', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.legend(title='', bbox_to_anchor=(0.38, -0.15), loc='upper center', fontsize=legend_font, ncol=2)
# ax.grid(axis='x', alpha=alpha, linestyle='--')
# ax.set_axisbelow(True)

# plt.tight_layout()
# # plt.show()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# ###############################################################################

## Combine some categories
df_classified['classification_consolidated'] = 'Other'
df_classified.loc[df_classified['classification'] == 'Non-avian avemetatarsalians', 'classification_consolidated'] = 'Non-avian avemetatarsalians'
df_classified.loc[df_classified['classification'] == 'Non-primate mammaliamorphs', 'classification_consolidated'] = 'Non-primate mammaliamorphs'
df_classified.loc[df_classified['classification'] == 'Primates', 'classification_consolidated'] = 'Primates'
df_classified.loc[df_classified['classification'] == 'Avians', 'classification_consolidated'] = 'Avians'

# Color map
select_categories = sorted(df_classified['classification'].dropna().unique())
cmap_5 = plt.get_cmap('Accent')
colors_5 = cmap_5(np.arange(len(select_categories)))

## Quick counts
journals_by_cat_5 = df_classified.groupby(['journal', 'classification_consolidated']).size().reset_index(name='count')

pivot_df = journals_by_cat_5.pivot(index='journal', columns='classification_consolidated', values='count').fillna(0)
pivot_df = pivot_df.sort_index(ascending=False)
journal_order = ['Nature', 'Science', 'Curr Biol', 'Gondwana Res', 'Nat Commun', 'Nat Ecol Evol', 'Proc Natl Acad Sci USA', 'Sci Adv', 'J Paleontol', 'J Syst Palaeontol', 'J Vert Paleontol', 'Palaeontology', 'Pap Palaeontol']
pivot_df = pivot_df.loc[journal_order[::-1]]
# Calculate percentages (relative counts)
pivot_pct = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100


# Set order
cat_order = ['Avians', 'Non-avian avemetatarsalians', 'Primates', 'Non-primate mammaliamorphs', 'Other']
pivot_pct = pivot_pct[cat_order]

plot_filename = f'{today}_5-cat_relative-proportions.{plot_format}'
fig, ax = plt.subplots(figsize=(img_width, img_height))
pivot_pct.plot(kind='barh', stacked=True, ax=ax, color=colors_5, edgecolor='black', linewidth=0.5)

# Labels, etc.
ax.set_xlabel('Percentage (%)', fontsize=axis_font, fontweight='bold')
ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
for label in ax.get_yticklabels():
    label.set_fontstyle('italic')
ax.set_title('Relative Proportion of Charismatic Clades by Journal', fontsize=title_font, fontweight='bold')
ax.tick_params(labelsize=tick_font)
ax.legend(title='', bbox_to_anchor=(0.38, -0.15), loc='upper center', fontsize=legend_font, ncol=2)
ax.grid(axis='x', alpha=alpha, linestyle='--')
ax.set_axisbelow(True)

plt.tight_layout()
# plt.show()
plot_path = os.path.join(plots_dir, plot_filename)
plt.savefig(plot_path, format=plot_format, dpi=dpi)
plt.close(fig)

# ###############################################################################

# ## Combine some categories
# df_classified['classification_consolidated'] = 'Other'
# df_classified.loc[df_classified['classification'] == 'Non-avian avemetatarsalians', 'classification_consolidated'] = 'Non-avian avemetatarsalians'
# df_classified.loc[df_classified['classification'] == 'Non-primate mammaliamorphs', 'classification_consolidated'] = 'Non-primate mammaliamorphs'
# df_classified.loc[df_classified['classification'] == 'Primates', 'classification_consolidated'] = 'Primates'
# df_classified.loc[df_classified['classification'] == 'Avians', 'classification_consolidated'] = 'Avians'

# # Color map
# select_categories = sorted(df_classified['journal'].dropna().unique())
# cmap_5 = plt.get_cmap('tab20c')
# colors_5 = cmap_5(np.arange(len(select_categories)))

# ## Quick counts
# journals_by_cat_5 = df_classified.groupby(['journal', 'Insecta']).size().reset_index(name='count')

# pivot_df = journals_by_cat_5.pivot(index='journal', columns='Insecta', values='count').fillna(0)
# pivot_df = pivot_df.sort_index(ascending=False)
# # Calculate percentages (relative counts)
# pivot_pct = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

# plot_filename = f'{today}_journals-insecta.{plot_format}'
# fig, ax = plt.subplots(figsize=(img_width, img_height))

# pivot_pct.plot(kind='barh', stacked=True, ax=ax, color=colors_5, edgecolor='black', linewidth=0.5)

# # Labels, etc.
# ax.set_xlabel('Percentage (%)', fontsize=axis_font, fontweight='bold')
# ax.set_ylabel('', fontsize=axis_font, fontweight='bold')
# ax.set_title('Relative Proportion of Insect Species by Journal', fontsize=title_font, fontweight='bold')
# ax.tick_params(labelsize=tick_font)
# ax.legend(title='', bbox_to_anchor=(0.38, -0.15), loc='upper center', fontsize=legend_font, ncol=2)
# ax.grid(axis='x', alpha=alpha, linestyle='--')
# ax.set_axisbelow(True)

# plt.tight_layout()
# # plt.show()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)



# ### Quick numerical summaries

# ### PLOTTING

# # Create color map for fine-grained classification
# clade_color_map = {'Plants': "#4FBD4B",
#             'Other non-metazoans': "#82997F",
#             'Non-bilaterian metazoans': '#000000',
#             'Non-chordate deuterostomes': '#000000',
#             'Non-vertebrate chordates': '#000000',
#             'Fish (actinopterygians)': "#5F79B1",
#             'Fish (chondrichthyans)': '#5F79B1',
#             'Fish (misc. fish)': '#5F79B1',
#             'Amphibians and friends': "#764397",
#             'Stem tetrapods': '#764397',
#             'Dinosaurs, ornithischians': "#C55F5F",
#             'Dinosaurs, saurischians (avians)': '#C55F5F',
#             'Dinosaurs, saurischians (non-theropods)': '#C55F5F',
#             'Dinosaurs, saurischians (theropods)': '#C55F5F',
#             'Early archosauromorphs': "#AA742D",
#             'Pseudosuchians': '#AA742D',
#             'Pterosaurs': '#AA742D',
#             'Turtles': "#FDEB47",
#             'Squamates': '#FDEB47',
#             'Non-diapsid sauropsids': '#FDEB47',
#             'Non-archosauromorph diapsids': '#FDEB47',
#             'Mammals (misc. therian mammals)': "#D834E7",
#             'Mammals, marsupials': '#D834E7',
#             'Mammals, placental (artiodactyls)': '#D834E7',
#             'Mammals, placental (carnivorans)': '#D834E7',
#             'Mammals, placental (other)': '#D834E7',
#             'Mammals, placental (perissodactyls)': '#D834E7',
#             'Mammals, placental (primates)': '#D834E7',
#             'Mammals, placental (rodents)': '#D834E7',
#             'Non-therian mammaliaforms': '#D834E7',
#             'Non-mammaliaform therapsids': '#D834E7',
#             'Protostomes (other)': "#A39B9B",
#             'Invertebrates (other arthropods)': "#CCCCCC",
#             'Invertebrates (brachiopods)': '#CCCCCC',
#             'Invertebrates (echinoderms)': '#CCCCCC',
#             'Invertebrates (insects)': '#CCCCCC',
#             'Invertebrates (molluscs)': '#CCCCCC',
#             'Invertebrates (ostracods)': '#CCCCCC',
#             'Invertebrates (trilobites)': '#CCCCCC'
# }

# time_color_map = {'pre-Ediacaran': '#F73563',
#                   'Ediacaran': '#F73563',
#                   'Cambrian': '#99C08D',
#                   'Ordovician': '#99C08D',
#                   'Silurian': '#99C08D',
#                   'Devonian': '#99C08D',
#                   'Carboniferous': '#99C08D',
#                   'Permian': '#99C08D',
#                   'Triassic': '#67C5CA',
#                   'Jurassic': '#67C5CA',
#                   'Cretaceous': '#67C5CA',
#                   'Paleocene': '#F2F91D',
#                   'Eocene': '#F2F91D',
#                   'Oligocene': '#F2F91D',
#                   'Miocene': '#F2F91D',
#                   'Pliocene': '#F2F91D',
#                   'Pleistocene': '#F2F91D'
# }

# year_color_map = {'1995-1999': "#f8e7d8",
#                 '2000-2004': "#f7d5b7",
#                 '2005-2009': "#f5ae70",
#                 '2010-2014': "#f78e32",
#                 '2015-2019': "#fc7500",
#                 '2020-2026': "#a04e05",
# }

# # By animal/not animal
# plot_filename = f'{today}_nature-science_animalia.{plot_format}'
# clade_count = fancy['Animalia'].value_counts(ascending=True)
    
# fig, ax = plt.subplots(figsize=(4.5, 8))
# bars = ax.bar(clade_count.index.astype(str), clade_count.values, color="#4ca06e", edgecolor='black')
# ax.set_xlabel('', fontsize=15)
# ax.set_ylabel('')
# ax.set_title(f'Is it an animal? (Nature/Science)', fontsize=16)
# ax.set_facecolor('#f7f7f7')
# ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
# ax.tick_params(axis='both', which='major', labelsize=14)
# ax.set_axisbelow(True)
# plt.tight_layout()
# # plt.show()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# # By vertebrate/not vertebrate
# plot_filename = f'{today}_nature-science_vertebrata.{plot_format}'
# clade_count = fancy['Vertebrata'].value_counts(ascending=True)

# fig, ax = plt.subplots(figsize=(4.5, 8))
# bars = ax.bar(clade_count.index.astype(str), clade_count.values, color="#dceb5b", edgecolor='black')
# ax.set_xlabel('', fontsize=15)
# ax.set_ylabel('')
# ax.set_title(f'Is it a vertebrate? (Nature/Science)', fontsize=16)
# ax.set_facecolor('#f7f7f7')
# ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
# ax.tick_params(axis='both', which='major', labelsize=14)
# ax.set_axisbelow(True)
# plt.tight_layout()
# # plt.show()
# plot_path = os.path.join(plots_dir, plot_filename)
# plt.savefig(plot_path, format=plot_format, dpi=dpi)
# plt.close(fig)

# # # Restrict to most common clades only and then do by time bin
# # plot_filename = f'{today}_nature-science_clades-over-time.{plot_format}'

# # focal_taxa = ['Mammals, placental (primates)', 'Non-therian mammaliaforms', 'Dinosaurs, saurischians (theropods)', 'Fish (misc. fish)', 'Amphibians and friends']
# # pattern = '|'.join(focal_taxa)
# # df_prominent = fancy[fancy['classification'].str.contains(pattern, na=False)]
# # df_prominent_counts = df_prominent.groupby('publication_year_bin')['classification'].value_counts().unstack(fill_value=0)
# # df_prominent_flipped = df_prominent_counts.T
# # colors = [year_color_map[col] for col in df_prominent_flipped.columns]

# # df_prominent_flipped.plot(kind='barh', figsize=(8,8), color=colors)
# # plt.xlabel('Count')
# # plt.ylabel('')
# # plt.title(f'New species description by time bin (Nature/Science)')
# # plt.tight_layout()
# # # plt.show()
# # plot_path = os.path.join(plots_dir, plot_filename)
# # plt.savefig(plot_path, format=plot_format, dpi=dpi)
# # plt.close(fig)

# for name, df in dfs_dict.items():
#     # Create conditional label for journals to differentiate in title
#     label = axis_dict.get(name, 'Journal')

#     # Only unique articles
#     df_expanded_dedup = df.drop_duplicates(subset=['doi', 'geography'])

#     # How many species in a journal
#     plot_filename = f'{today}_{name}_species-per-journal.{plot_format}'
#     species_counts = df['journal'].value_counts(ascending=True)
    
#     fig, ax = plt.subplots(figsize=(4.5, 8))
#     bars = ax.bar(species_counts.index, species_counts.values, color='#00a9b7', edgecolor='black')
    
#     ax.set_ylabel('')
#     ax.set_title(f'Species by journal ({label})', fontsize=16)
#     ax.set_facecolor('#f7f7f7')
#     ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
#     ax.tick_params(axis='both', which='major', labelsize=14)
#     ax.set_xticks(species_counts.index.astype(str))
#     ax.set_axisbelow(True)
#     plt.tight_layout()
#     # plt.show()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     # How many species-naming articles per journal (less than # of species due to multi-species descriptions)
#     plot_filename = f'{today}_{name}_article-per-journal.{plot_format}'
#     species_counts = df_expanded_dedup['journal'].value_counts(ascending=True)
        
#     fig, ax = plt.subplots(figsize=(4.5, 8))
#     bars = ax.bar(species_counts.index, species_counts.values, color='#00a9b7', edgecolor='black')
#     ax.set_xlabel('', fontsize=15)
#     ax.set_ylabel('')
#     ax.set_title(f'Descrip. by journal ({label})', fontsize=16)
#     ax.set_facecolor('#f7f7f7')
#     ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
#     ax.tick_params(axis='both', which='major', labelsize=14)
#     ax.set_axisbelow(True)
#     plt.tight_layout()
#     # plt.show()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     # How many new species per country
#     plot_filename = f'{today}_{name}_species-per-country_species.{plot_format}'
#     article_counts = df_classified['geography'].value_counts(ascending=True)
        
#     fig, ax = plt.subplots(figsize=(4.5, 8))
#     bars = ax.barh(article_counts.index, article_counts.values, color='#00a9b7', edgecolor='black')
#     ax.set_xlabel('', fontsize=15)
#     ax.set_ylabel('')
#     ax.set_title(f'Holotype country ({label})', fontsize=16)
#     ax.set_facecolor('#f7f7f7')
#     ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
#     ax.tick_params(axis='both', which='major', labelsize=10)
#     ax.set_axisbelow(True)
#     plt.tight_layout()
#     # plt.show()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     # How many species-naming articles per country (less than # of species due to multi-species descriptions)
#     plot_filename = f'{today}_{name}_species-per-country_articles.{plot_format}'
#     article_counts = df_expanded_dedup['geography'].value_counts(ascending=True)
        
#     fig, ax = plt.subplots(figsize=(4.5, 8))
#     bars = ax.barh(article_counts.index, article_counts.values, color='#00a9b7', edgecolor='black')
#     ax.set_xlabel('', fontsize=15)
#     ax.set_ylabel('')
#     ax.set_title(f'Holotype country ({label})', fontsize=16)
#     ax.set_facecolor('#f7f7f7')
#     ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
#     ax.tick_params(axis='both', which='major', labelsize=10)
#     ax.set_axisbelow(True)
#     plt.tight_layout()
#     # plt.show()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     # By tetrapod/not tetrapod
#     plot_filename = f'{today}_{name}_tetrapoda.{plot_format}'
#     clade_count = df['Tetrapoda'].value_counts(ascending=True)

#     fig, ax = plt.subplots(figsize=(4.5, 8))
#     bars = ax.bar(clade_count.index.astype(str), clade_count.values, color="#b566c6", edgecolor='black')
#     ax.set_xlabel('', fontsize=15)
#     ax.set_ylabel('')
#     ax.set_title(f'Is it a tetrapod? ({label})', fontsize=16)
#     ax.set_facecolor('#f7f7f7')
#     ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
#     ax.tick_params(axis='both', which='major', labelsize=14)
#     ax.set_axisbelow(True)
#     plt.tight_layout()
#     # plt.show()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     # By mammaliaformes/not mammaliaformes
#     plot_filename = f'{today}_{name}_mammaliaformes.{plot_format}'
#     clade_count = df['Mammaliaformes'].value_counts(ascending=True)
        
#     fig, ax = plt.subplots(figsize=(4.5, 8))
#     bars = ax.bar(clade_count.index.astype(str), clade_count.values, color="#905d7c", edgecolor='black')
#     ax.set_xlabel('', fontsize=15)
#     ax.set_ylabel('')
#     ax.set_title(f'Is it a mammaliaform? ({label})', fontsize=16)
#     ax.set_facecolor('#f7f7f7')
#     ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
#     ax.tick_params(axis='both', which='major', labelsize=14)
#     ax.set_axisbelow(True)
#     plt.tight_layout()
#     # plt.show()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     # By dinosaur/not dinosaur
#     plot_filename = f'{today}_{name}_dinosauria.{plot_format}'
#     clade_count = df['Dinosauria'].value_counts(ascending=True)
        
#     fig, ax = plt.subplots(figsize=(4.5, 8))
#     bars = ax.bar(clade_count.index.astype(str), clade_count.values, color="#b97b47", edgecolor='black')
#     ax.set_xlabel('', fontsize=15)
#     ax.set_ylabel('')
#     ax.set_title(f'Is it a dinosaur? ({label})', fontsize=16)
#     ax.set_facecolor('#f7f7f7')
#     ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
#     ax.tick_params(axis='both', which='major', labelsize=14)
#     ax.set_axisbelow(True)
#     plt.tight_layout()
#     # plt.show()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     # Compare all clades
#     plot_filename = f'{today}_{name}_all-clades.{plot_format}'
#     clade_count = df['classification'].value_counts(ascending=True)

#     colors = [clade_color_map.get(clade, '#cccccc') for clade in clade_count.index]
        
#     fig, ax = plt.subplots(figsize=(8, 8))
#     bars = ax.barh(clade_count.index.astype(str), clade_count.values, color=colors, edgecolor='black')
#     ax.set_xlabel('', fontsize=15)
#     ax.set_ylabel('')
#     ax.set_title(f'Clade comparison ({label})', fontsize=16)
#     ax.set_facecolor('#f7f7f7')
#     ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
#     ax.tick_params(axis='both', which='major', labelsize=14)
#     ax.set_axisbelow(True)
#     plt.tight_layout()
#     # plt.show()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     # Compare time bins
#     plot_filename = f'{today}_{name}_time-bins.{plot_format}'
#     time_count = df['age2'].value_counts(ascending=True)

#     colors = [time_color_map.get(bin, '#cccccc') for bin in time_count.index]
        
#     fig, ax = plt.subplots(figsize=(8, 8))
#     bars = ax.barh(time_count.index.astype(str), time_count.values, color=colors, edgecolor='black')
#     ax.set_xlabel('', fontsize=15)
#     ax.set_ylabel('')
#     ax.set_title(f'Time bin comparison ({label})', fontsize=16)
#     ax.set_facecolor('#f7f7f7')
#     ax.grid(True, which='both', color='white', linestyle='-', linewidth=1.5)
#     ax.tick_params(axis='both', which='major', labelsize=14)
#     ax.set_axisbelow(True)
#     plt.tight_layout()
#     # plt.show()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     #### GEOPANDAS CHLOROPLETH

#     # Read in shapefile
#     world = gpd.read_file('ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')
#     country_counts = df['geography'].value_counts().reset_index()
#     country_counts.columns = ['NAME', 'count']

#     # Merge counts with world map shapefile
#     world = world.merge(country_counts, on='NAME', how='left')
#     world['count'] = world['count'].fillna(0)

#     # Plot
#     plot_filename = f'{today}_{name}_holotype_country_chloropleth.{plot_format}'
#     fig, ax = plt.subplots(figsize=(12, 8))
#     world.plot(column='count', cmap='viridis', legend=True, ax=ax)
#     plt.title(f'New species occurrence (chloropleth)  ({label})')
#     # plt.show()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)

#     ### BINARY PRESENCE/ABSENCE
#     # Load world map
#     world = gpd.read_file('ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')
#     countries = df['geography'].unique().tolist()

#     # Map to shapefile
#     world['selected'] = world['NAME'].isin(countries)

#     # Plot
#     plot_filename = f'{today}_{name}_holotype_country_binary.{plot_format}'
#     fig, ax = plt.subplots(figsize=(12, 8))
#     world.plot(column='selected', cmap='Pastel1_r', legend=True, ax=ax)
#     plt.title(f'New species occurrence (binary) ({label})')
#     # plt.show()
#     plot_path = os.path.join(plots_dir, plot_filename)
#     plt.savefig(plot_path, format=plot_format, dpi=dpi)
#     plt.close(fig)