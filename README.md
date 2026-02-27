# README
This repository contains code, data, and visualizations for a random side project examining taxonomic patterns of publications in Nature or Science that name at least one new species based on fossil material (i.e. extinct taxa). It is only a food-for-thought retrospective analysis and is not intended to be used as some sort of predictive tool for which high-profile journal might be preferable for aiming a novel taxon manuscript.

## Metadata
Author: Bryan M. Gee ([ORCID: 0000-0003-4517-3290](https://orcid.org/0000-0003-4517-3290))
Email: bryangee.temnospondyli@gmail.com
Version: 1.0.0
Last updated: 2026/02/27

## Contents
There are three scripts in this repository:
1. *taxonomy-retrieval.py*: This script takes the input file with the list of new species and their associated bibliographic information and retrieves information from the PBDB API on taxonomic ranks. 
2. *taxon-classification.py*: This script takes the manually annotated output file from the first script and then applies a series of classifications to bin species into more logical bins for comparison.
3. *plots.py*: This script generates the plots.

There are two data files in this repository:
1. *input-data.csv*: This is the data in the original collected format. You will need this if you want to re-run the code.
2. *df-classified.csv*: This is the data in the final output version after taxonomic rank information has been compiled, manual clean-up and augmentation has been performed, and the semi-haphazard classification scheme described below has been applied. You don't need this to re-run the code unless you skip to the plotting part. It will otherwise be regenerated if you run the first two scripts.

## Methods
### Article identification
I first made web queries for the phrase 'sp. nov. fossil' in *Nature* and *Science*'s websites, **restricting the search to articles published between 2016 and 2016, inclusive**. The links are:
* [Nature](https://www.nature.com/search?q=sp.+nov.+fossil&order=relevance&journal=nature&article_type=research&date_range=2010-2026)
* [Science](https://www.science.org/action/doSearch?AllField=sp.+nov.+fossil&SeriesKey=science&startPage=&ConceptID=505154&AfterYear=2010&BeforeYear=2027&queryID=52%2F9564754844)

These searches have to be done through the journals' site, rather than through a public resource like the Crossref API, because they have to be able to search the entire text, which is often paywalled, not just the publicly available title and abstract.

Because the sample size is a little low, and these journals are atypical, I wanted a representative of a more "normal" journal. I went with the *Journal of Vertebrate Paleontology* for two reasons: (1) Journal of Paleontology's date filters get messed up for old articles that were digitized (these are filtered by their date of being put online, not the original publication date) and (2) most high-profile extinct taxa naming papers are on vertebrates. The link for [JVP](https://www.tandfonline.com/action/doSearch?AllField=sp.+nov.&SeriesKey=ujvp20&content=standard&dateRange=[20100101+TO+20261231]&target=default&sortBy=Earliest_desc&startPage=&pageSize=50). As a note, there are almost 750 articles returned for JVP in this time range, so the data for JVP is only through 2020, inclusive.

### Article assessment
I then examined each article manually and extracted basic information about novel taxa at the species level: journal, article title, publication year, DOI, taxon name, country the holotype was discovered in, and geologic era and period. Two *Nature* articles were excluded, [Zeng et al., 2026](https://www.nature.com/articles/s41586-025-10030-0), which described a speciose Cambrian assemblage in which more than half of the >150 recognized species are considered new, as the authors did not formalize names for new species (probably due to Nature's page limits), and [Moore et al., 2024](https://www.nature.com/articles/s41586-024-07919-7), which is about a parasitoid wasp in modern *Drosophila*. One *Science* article was excluded, [Miao et al., 2022](https://doi.org/10.1126/science.abo2475), which improperly used 'sp. nov.' in reference to a species named in 2008 and which invokes no taxonomic act. Similar issues are found in JVP articles but are too numerous to list here. JVP's search results also seem to return hits if 'sp. nov.' is in the references. Any article where a new species was not formalized was omitted in the downstream scripting process.

### Taxonomic assessment
In order to standardize how information about the taxonomic ranks of each novel taxon were treated, I utilized the [Paleobiology Database (PBDB) REST API](https://paleobiodb.org/data1.2/). This is not a perfect mechanism, and I am well-aware of the PBDB's limitations, but the only real alternative that could ensure coverage for all sampled taxa was Wikipedia - a lot of papers truncate the systematic paleontology or depict ranks not equivalent to those in other papers. A dynamic resource is also preferable to the original paper, as the taxonomy of some recently named taxa may have shifted to a different consensus over time.

The PBDB doesn't always have data for taxa, so after retrieving information on the taxa that do, I used a combination of Wikipedia and the PBDB to identify slightly higher ranks (e.g., family) that might be listed in the PBDB. Anyone re-running the script would need to do the same manual steps for missing data. I also did some minor cleaning up to account for a few genera that needed to be replaced due to preoccupation, a weird frameshift in which the PBDB output was frameshifted by one somewhere in the middle of the merged dataframe (still trying to figure this out, but it has no functional import at this point), and changed 'United States' listings to 'United States of America' to prepare it for *geopandas* specifically.

### Classification
To make the plots slightly more comprehensible and more focused on disparities between clades, I created a series of Boolean columns based on whether a taxon was listed as belonging to a clade (e.g., 'Vertebrata') and then used those columns to create conditional categorizations (e.g., if a taxon was listed as a tetrapodomorph but not as an amniote, it is classifed as 'Amphibians and friends'). These categories are hardly asymmetrical, don't always hew to Linnaean ranks, are sometimes referring to paraphyletic clades, and will probably be tweaked in the future.

### Future development
This is just a fun side project for me, but it would be easy to either expand the temporal range for sampling journal articles (or maybe to just skip to a decade-long time bin from a few decades ago) or to expand the journal scope (e.g., Proc B, PNAS, Current Biology). If you find this interesting and want to contribute, feel free to fork (and make a PR if you want to merge back).

#### Author assessment
*I have this scoped but it's not quite ready yet*
In order to gain insight into trends by publishing authors on these papers, I utilized the [OpenAlex REST API](https://developers.openalex.org/). For those not familiar with the resource, OpenAlex is a freely available bibliographic resource that ingests and standardizes metadata from Crossref (the people who mint DOIs for journal articles) and DataCite (the people who mint DOIs for datasets and software). Information on ROR-standardized affiliations and country were extracted. For those not familiar with [ROR](https://ror.org/), this is a global registry of research institution names intended to mitigate problems of writing the same institution's name in many different ways (sort of like ORCID but for institutions).

## Licensing of materials
Metadata about journal publications and taxonomic classifications is typically regarded as non-creative and thus not eligible to be held in copyright. All data included here are thus treated as being in the public domain (CC0 license waiver). The code is licensed under MIT, which basically allows anyone to do anything with it as long as they credit the original (read the License file for more). The visualizations are creative, but I see no point in copyrighting them since anyone can regenerate them on their own with my code and dataset.

### Re-use and requirements
Anyone should feel free to re-use and re-purpose these materials. If you make use of public APIs, please make sure to use best practices for making polite requests to REST APIs. You will need to install various Python modules not in the standard library: *geopandas*, *matplotlib*, *pandas* and *requests*. These are all standard, widely used modules available on PyPi. If you want to produce the map plots, you will need to get the shapefile from: [https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/](https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/).