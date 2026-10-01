import glob
import json
import os
import pandas as pd
import pypandoc
import re
import requests
from datetime import datetime
from rich.progress import track

# Read in cleaned-up data file
outputs_dir = 'outputs'
today = datetime.now().strftime('%Y%m%d') 
file_pattern = f'{outputs_dir}/*_dataset-classified.csv'

try:
    most_recent_file = max(glob.iglob(file_pattern), key=os.path.getmtime)
    df = pd.read_csv(most_recent_file, dtype='str')
    if df is not None:
        print(f'Imported data file: {most_recent_file} with {len(df)} entries.\n') 

except ValueError:
    print(f'No files matched the given pattern ({file_pattern}).')

df = df.sort_values(by='genus')
## Restrict to unique articles
df_articles = df.drop_duplicates(subset=['doi'], keep='first')

# To run small batch
test = False
if test:
    df_articles = df_articles.head(400)

# Create empty lists
## To store API response
jsons = []
## To store any DOIs that fail
errors = []
for doi in track(df_articles['doi'], description=f'Retrieving citations for {len(df_articles)} articles...'):
    try:
        url = f'https://api.crossref.org/works/{doi}'
        response = requests.get(url)
        if response.status_code == 200:
            new_data = response.json()
        jsons.append(new_data)
    except requests.exceptions.Timeout:
        print(f'Error retrieving citation for {doi}: {e}')

        errors.append(doi)
    except requests.RequestException as e:
        print(f'Error retrieving citation for {doi}: {e}')
        errors.append(doi)

# Function to get first letter from first name(s)
## Will get each letter from hyphenated name (e.g., Bob-Jones -> B.-J.)
def get_first_letters(text):
    pattern = r'\b\w|-'
    tokens = re.findall(pattern, text)
    result = ''.join(tokens)
    return re.sub(r'-+', '-', result).strip('-')

with open(f'{today}_crossref_response.json', 'w', encoding='utf-8') as file:
    json.dump(jsons, file)

# Subset API response
data_select_crossref = []
for article in jsons:
    item = article.get('message', None)
    journal_field = item.get('container-title', None)
    journal_name = journal_field[0] if journal_field else None
    publisher = item.get('publisher', None)
    doi = item.get('DOI', None)
    title_field = item.get('title', [])
    title = title_field[0] if title_field else None
    volume = item.get('volume', 'No volume')
    issue_field = item.get('journal-issue', None)
    issue = issue_field.get('issue', None) if issue_field else None
    article = item.get('article-number', None)
    page = item.get('page', None)
    if article:
        pagination = article
    else:
        pagination = page
    published = item.get('published-print', '')
    if isinstance(published, str): #no print publication
        published_online = item.get('published-online', '')
        published_year = published_online.get('date-parts', [])[0][0]
    else:
        published_year = published.get('date-parts', [])[0][0]
    authors = item.get('author', [])
    author_names_list = []
    for author in authors:
        family = author.get('family', '')
        given = author.get('given', '')
        given_initials = get_first_letters(given)
        given_initials_str = '.'.join(given_initials)
        author_names = family + ', ' + given_initials_str + '.'
        author_names_list.append(author_names)
        # Add ampersand before last name if 2+ authors
        author_names_str = ' & '.join([', '.join(author_names_list[:-1]),author_names_list[-1]] if len(author_names_list) > 2 else author_names_list)

    data_select_crossref.append({
        'doi': doi,
        'journal': journal_name,
        'volume': volume,
        'issue': issue,
        'pagination': pagination,
        'publication_year': published_year,
        'title': title,
        'authors': author_names_str
        })

df_data_select_crossref = pd.DataFrame(data_select_crossref)
df_data_select_crossref.to_csv(f'{today}_crossref_filtered_df.csv', index=False, encoding='utf-8-sig')

## Casing
### Convert author names to title case
df_data_select_crossref['authors'] = df_data_select_crossref['authors'].str.title()
### Remove period if ending the string of authors to avoid double period
df_data_select_crossref['authors'] = df_data_select_crossref['authors'].str.replace(r'\.$', '', regex=True)
## Replace HTML tags with markdown syntax
df_data_select_crossref['title'] = df_data_select_crossref['title'].str.replace('<i>', '*', regex=False)
df_data_select_crossref['title'] = df_data_select_crossref['title'].str.replace('</i>', '*', regex=False)
## Replace hyphens with en-dashes in pagination
df_data_select_crossref['pagination'] = df_data_select_crossref['pagination'].str.replace('-', '–', regex=False)

markdown_text = '# References\n\n'

for index, row in df_data_select_crossref.iterrows():
    # Conditionally display issue if it exists
    if pd.notnull(row['issue']):
        ref = (f'{row['authors']}. ({row['publication_year']}). {row['title']}. *{row['journal']}*, *{row['volume']}*({row['issue']}): {row['pagination']}. DOI: [{row['doi']}](https://doi.org/{row['doi']})')
    else:
        ref = (f'{row['authors']}. ({row['publication_year']}). {row['title']}. *{row['journal']}*, *{row['volume']}*: {row['pagination']}. DOI: [{row['doi']}](https://doi.org/{row['doi']})')
    markdown_text += f'- {ref}\n'

# print(markdown_text)

args = ['--reference-doc=ref-doc.docx']

pypandoc.convert_text(
    source=markdown_text,
    to='docx',
    format='md',
    outputfile=f'{today}_formatted_dataset_refs.docx',
    extra_args=args
)

print('Document exported successfully.\n')

if errors:
    print(errors)
else:
    print('No DOIs failed retrieval.\n')