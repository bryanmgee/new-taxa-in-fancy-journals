import glob
import json
import os
import pandas as pd
import pyalex
import requests
from datetime import datetime
from rich.progress import track

# Read in latest version of file
outputs_dir = 'outputs'
today = datetime.now().strftime('%Y%m%d') 

file_pattern = f'{outputs_dir}/*_dataset-classified.csv'

try:
    most_recent_file = max(glob.iglob(file_pattern), key=os.path.getmtime)
    df = pd.read_csv(most_recent_file, low_memory=False)
    if df is not None:
        print(f'Imported data file: {most_recent_file} with {len(df)} entries.\n') 

except ValueError:
    print(f'No files matched the given pattern ({file_pattern}).')

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

df_clean_dedup_high_JIF = df_clean_dedup[(df_clean_dedup['journal'] == 'Science') | (df_clean_dedup['journal'] == 'Nature')]

# Toggle for quick test runs with small sample size (set to TRUE if you want that)
test = False
if test:
    df_clean_dedup_high_JIF = df_clean_dedup_high_JIF.head(15)

# Loop through Open Alex API
articles = []
errors = []
for doi in track(df_clean_dedup_high_JIF['doi'], description=f'Retrieving metadata for {len(df_clean_dedup_high_JIF)} articles...'):
    try:
        response = pyalex.Works()[f'https://doi.org/{doi}']
        print(f'Retrieving {doi}...')
        articles.append(response)
    except requests.exceptions.RequestException as e:
        print(f'An error occurred for {doi}: {e}')
        errors.append(doi)

# Subset response for specific fields
data_select_openalex = [] 
for item in articles:
    doi = item.get('doi', None)
    pub_year = item.get('publication_year', None)
    authors = item.get('authorships', None)
    journal = item.get('primary_location', '').get('source', '').get('display_name','')
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
        # corresponding = author.get('is_corresponding', '')
        author_info = author.get('author', '')
        institution_info = author.get('institutions', '')
        raw_affiliation = author.get('raw_affiliation_strings', '')
        author_name = author_info.get('display_name')
        author_orcid = author_info.get('orcid', '')
        name_and_orcid = f'{author_name} ({author_orcid})'
        # rors = []
        # countries = []
        # for institution in institution_info:
        #     author_ror = institution.get('ror', '')
        #     print(f'ROR for {author_name}: {author_ror}')
        #     author_ror_country = institution.get('country_code', '')
        #     rors.append(author_ror)
        #     print(f'ROR IDs for {author_name}: {rors}')
        #     countries.append(author_ror_country)
        author_names.append(author_name)
        author_orcids.append(author_orcid)
        original_affiliations.append(raw_affiliation)
        # author_institutions.append(rors)
        # author_institutions = list(chain.from_iterable(author_institutions))
        # author_countries.append(countries)
        # author_countries = list(chain.from_iterable(author_countries))
        # author_institutions_unique = set(author_institutions)
        # author_countries_unique = set(author_countries)
        author_formatted.append(name_and_orcid)
        # author_positions.append(author_position)
        # author_corresponding.append(corresponding)
    author_count = len(author_names)
    # countries_count = item.get('countries_distinct_count', 0)
    # countries_count_unique = len(author_countries_unique)
    # institutions_count = item.get('institutions_distinct_count', 0)
    # institutions_count_unique = len(author_institutions_unique)
         
    data_select_openalex.append({
        'doi': doi,
        'journal': journal,
        'publication_year': pub_year,
        'authors': authors,
        'author_count': author_count,
        # 'author_position': author_positions,
        # 'author_corresponding': author_corresponding,
        'names': author_names,
        'orcids': author_orcids,
        'names_and_orcids': author_formatted,
        'original_affiliations': original_affiliations,
        'institutions': author_institutions,
        # 'institutions_unique': author_institutions_unique,
        # 'countries': author_countries,
        # 'countries_unique': author_countries_unique,
        # 'country_count': countries_count,
        # 'country_count_unique': countries_count_unique,
        # 'institution_count': institutions_count,
        # 'institution_count_unique': institutions_count_unique,
        # 'source': 'OpenAlex'
    })

df_openalex = pd.json_normalize(data_select_openalex)
df_openalex['doi'] = df_openalex['doi'].str.replace('https://doi.org/', '')
# Fixing weird edge case where journal is mislabeled in OpenAlex
df_openalex['journal'] = df_openalex['journal'].str.replace('Nature Cell Biology', 'Nature', regex=False)

df_openalex.to_csv(f'outputs/{today}_openalex-articles.csv', index=False, encoding='utf-8-sig')

# Exploding on author name and affiliation
df_authors_individual = df_openalex.explode(['names', 'orcids', 'names_and_orcids', 'original_affiliations'])
df_authors_individual.to_csv(f'outputs/{today}_openalex-authors-list.csv', index=False, encoding='utf-8-sig')

## Summarize on plain name only
df_authors_name_only = df_authors_individual.groupby('journal', as_index=False)['names'].value_counts().reset_index()
df_authors_name_only.to_csv(f'outputs/{today}_openalex-authors-summary-name-only.csv', index=False, encoding='utf-8-sig')

## Summarize on ORCID only
### Remove any entries without ORCID
df_authors_with_orcid = df_authors_individual[df_authors_individual['orcids'].str.contains('orcid.org', case=True)]
df_authors_orcid_only = df_authors_with_orcid.groupby('journal', as_index=False)['orcids'].value_counts().reset_index()
df_authors_orcid_only.to_csv(f'outputs/{today}_openalex-authors-summary-orcid-only.csv', index=False, encoding='utf-8-sig')

## Summarize on name + ORCID
# df_authors_name_orcid = df_authors_with_orcid['names_and_orcids'].value_counts().reset_index()
df_authors_name_orcid = df_authors_with_orcid.groupby('journal', as_index=False)['names_and_orcids'].value_counts()
df_authors_name_orcid.to_csv(f'outputs/{today}_openalex-authors-summary-name-orcid.csv', index=False, encoding='utf-8-sig')

if errors:
    print(errors)
else:
    print('No DOIs failed retrieval.\n')

print('Analysis concluded.\n')