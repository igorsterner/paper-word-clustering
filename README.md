# Paper Implementation - "Automatic Retrieval and Clustering of Similar Words" (Lin, 1998)

This repo contains an implementation of [Automatic Retrieval and Clustering of Similar Words](https://aclanthology.org/P98-2127/) by Dekang Lin.

## Citation

```sql
@inproceedings{lin-1998-automatic-retrieval,
    title = "Automatic Retrieval and Clustering of Similar Words",
    author = "Lin, Dekang",
    booktitle = "36th Annual Meeting of the Association for Computational Linguistics and 17th International Conference on Computational Linguistics, Volume 2",
    month = aug,
    year = "1998",
    address = "Montreal, Quebec, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P98-2127",
    doi = "10.3115/980691.980696",
    pages = "768--774",
}
```

## Table of Contents

- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Visualisation](#visualisation)
- [Example Output](#example-output)


### Dataset

```
mkdir data
cd data
wget https://downloads.wortschatz-leipzig.de/corpora/eng_news-typical_2016_1M.tar.gz 
tar -xvzf eng_news-typical_2016_1M.tar.gz
```

### Installation

```
pip install -r requirements.txt
```

### Usage

First parse the data.
```
python src/tools/dependency-parser.py
```

Then run the main script.
```
python src/main.py
```

### Visualisations

```
python src/tools/similarity-tree.py --word money
```

#### Example output

```txt
money
 |___ energy
 |    |___ information
 |    |___ power
 |    |    |___ authority
 |    |    |___ space
 |    |    |___ support
 |    |    |___ knowledge
 |    |    |___ property
 |    |___ value
 |    |    |___ amount
 |    |    |___ price
 |    |    |___ word
 |    |    |    |___ name
 |    |___ heat
 |    |___ sense
 |    |    |___ decision
 |    |    |___ interest
 |    |    |    |___ efforts
 |    |    |    |___ issues
 |    |    |    |    |___ problems
 |    |    |    |___ ability
 |    |    |    |    |___ access
 |    |    |    |___ place
 |    |___ water
 |    |    |___ family
 |    |    |    |___ army
 |    |    |    |___ country
 |    |___ food
 |    |    |___ game
 |    |    |    |___ life
 |    |    |    |___ character
 |    |    |    |___ music
 |    |    |    |    |___ style
 |    |    |___ rest
 |    |    |    |___ weeks
 |    |    |    |___ majority
 |    |    |    |___ cards
 |    |___ resources
 |    |    |___ soldiers
 |    |    |    |___ men
```