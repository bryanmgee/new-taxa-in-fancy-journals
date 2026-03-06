import json
import os
import pandas as pd
import pyalex
import requests
from datetime import datetime

# Toggle for quick test runs with n=10 (set to TRUE if you want that)
test = False

# Read in latest version of file
df = pd.read_csv('20260306_df-classified.csv')
print(f'Imported file with {len(df)} entries.\n')

# Read in configuration file
with open('config.json', 'r') as file:
    config = json.load(file)
pyalex.config.api_key = config['KEYS']['openalexToken']

# Create outputs directory
if os.path.isdir('outputs'):
        print('outputs directory found - no need to recreate.\n')
else:
    os.mkdir('outputs')
    print('outputs directory has been created.\n')

# Date for filename
today = datetime.now().strftime('%Y%m%d') 

# Remove blanks
df_clean = df.dropna(subset='novel_taxon', ignore_index=True)
print(f'Processing file with {len(df_clean)} entries.\n')
df_clean_dedup = df_clean.drop_duplicates(subset=['doi'])
print(f'Processing {len(df_clean_dedup)} articles.\n')

# Loop through Open Alex API
## Currently only want data on high-profile journals
if test:
    df_clean_dedup = df_clean_dedup.head(10)
else:
    df_clean_dedup = df_clean_dedup[(df_clean_dedup['journal'] == 'Science') | (df_clean_dedup['journal'] == 'Nature')]

articles = []
for doi in df_clean_dedup['doi']:
    try:
        response = pyalex.Works()[f'https://doi.org/{doi}']
        print(f'Retrieving {doi}...')
        articles.append(response)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        articles.append('Did not locate')

# If you need to inspect the output of one article to determine how to subset
## You can also do this in a web browser since these calls don't require an API key
# output_filename = 'api_response.json'
# with open(output_filename, 'w', encoding='utf-8') as f:
#     json.dump(articles, f, ensure_ascii=False, indent=4)

# Subset response for specific fields
data_select_openalex = [] 
for item in articles:
    doi = item.get('doi', None)
    pub_year = item.get('publication_year', None)
    authors = item.get('authorships', None)
    author_names = []
    author_positions = []
    author_corresponding = []
    author_institutions = []
    author_countries = []
    author_orcids = []
    original_affiliations = []
    author_formatted = []
    for author in authors:
        author_position = author.get('author_position', '')
        corresponding = author.get('is_corresponding', '')
        author_info = author.get('author', '')
        institution_info = author.get('institutions', '')
        raw_affiliation = author.get('raw_affiliation_strings', '')
        author_name = author_info.get('display_name')
        author_orcid = author_info.get('orcid', '')
        name_and_orcid = f'{author_name} ({author_orcid})'
        rors = []
        countries = []
        for institution in institution_info:
            author_ror = institution.get('ror', '')
            author_ror_country = institution.get('country_code', '')
            rors.append(author_ror)
            countries.append(author_ror_country)
        author_names.append(author_name)
        author_orcids.append(author_orcid)
        original_affiliations.append(raw_affiliation)
        author_institutions.append(author_ror)
        author_countries.append(author_ror_country)
        author_institutions_unique = set(author_institutions)
        author_countries_unique = set(author_countries)
        author_formatted.append(name_and_orcid)
        author_positions.append(author_position)
        author_corresponding.append(corresponding)
    author_count = len(author_names)
    countries_count = item.get('countries_distinct_count', 0)
    countries_count_unique = len(author_countries_unique)
    institutions_count = item.get('institutions_distinct_count', 0)
    institutions_count_unique = len(author_institutions_unique)
         
    data_select_openalex.append({
        'doi': doi,
        'publication_year': pub_year,
        'authors': authors,
        'author_count': author_count,
        'author_position': author_positions,
        'author_corresponding': author_corresponding,
        'names': author_names,
        'orcids': author_orcids,
        'names_and_orcids': author_formatted,
        'original_affiliations': original_affiliations,
        'institutions': author_institutions,
        'institutions_unique': author_institutions_unique,
        'countries': author_countries,
        'countries_unique': author_countries_unique,
        'country_count': countries_count,
        'country_count_unique': countries_count_unique,
        'institution_count': institutions_count,
        'institution_count_unique': institutions_count_unique,
        'source': 'OpenAlex'
    })

df_openalex = pd.json_normalize(data_select_openalex)
df_openalex['doi'] = df_openalex['doi'].str.replace('https://doi.org/', '')
df_openalex.to_csv(f'outputs/{today}_openalex-articles.csv', index=False, encoding='utf-8-sig')

# Exploding on author name and affiliation
df_authors_individual = df_openalex.explode(['names', 'orcids', 'names_and_orcids', 'original_affiliations', 'institutions', 'countries'])
df_authors_individual.to_csv(f'outputs/{today}_openalex-authors-list.csv', index=False, encoding='utf-8-sig')

df_authors_unique_orcid = df_authors_individual.value_counts('orcids').rename_axis('author').reset_index(name='counts')
print(df_authors_unique_orcid)

df_authors_unique_names = df_authors_individual.value_counts('names').rename_axis('author').reset_index(name='counts')
print(df_authors_unique_names)

print('Analysis concluded.\n')