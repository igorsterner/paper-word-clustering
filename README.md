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
- [Examples](#example-output)


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

### Visualisation

```
python src/tools/similarity-tree.py --word money
python src/tools/thesaurus.py --find_rnns 1
```

#### Examples

Similarity tree:

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

RNNs, like in paper:

```txt
[(('1960s', '1970s'), 0.47),
 (('weeks', 'months'), 0.45),
 (('summer', 'winter'), 0.36),
 (('radio', 'television'), 0.33),
 (('%', 'percent'), 0.32),
 (('temperature', 'pressure'), 0.31),
 (('levels', 'temperatures'), 0.31),
 (('month', 'week'), 0.3),
 (('hours', 'minutes'), 0.3),
 (('city', 'town'), 0.29),
 (('report', 'study'), 0.29),
 (('air', 'water'), 0.28),
 (('people', 'men'), 0.27),
 (('letters', 'words'), 0.27),
 (('models', 'versions'), 0.27),
 (('brother', 'wife'), 0.27),
 (('data', 'information'), 0.26),
 (('army', 'forces'), 0.26),
 (('company', 'government'), 0.25),
 (('development', 'growth'), 0.25),
 (('games', 'films'), 0.25),
 (('issues', 'problems'), 0.25),
 (('education', 'training'), 0.24),
 (('animals', 'plants'), 0.24),
 (('system', 'network'), 0.24),
 (('version', 'edition'), 0.24),
 (('children', 'child'), 0.24),
 (('security', 'health'), 0.24),
 (('art', 'music'), 0.24),
 (('song', 'album'), 0.24),
 (('types', 'schools'), 0.24),
 (('software', 'applications'), 0.24),
 (('team', 'band'), 0.23),
 (('economy', 'industry'), 0.23),
 (('period', 'season'), 0.23),
 (('man', 'woman'), 0.22),
 (('name', 'title'), 0.22),
 (('position', 'status'), 0.22),
 (('access', 'ability'), 0.22),
 (('characters', 'features'), 0.22),
 (('release', 'election'), 0.21),
 (('metal', 'rock'), 0.21),
 (('century', 'era'), 0.21),
 (('method', 'theory'), 0.21),
 (('body', 'cell'), 0.21),
 (('surface', 'ground'), 0.21),
 (('aircraft', 'ships'), 0.2),
 (('computer', 'video'), 0.2),
 (('species', 'groups'), 0.2),
 (('quality', 'performance'), 0.2),
 (('form', 'style'), 0.19),
 (('area', 'region'), 0.19),
 (('concept', 'idea'), 0.19),
 (('color', 'sound'), 0.19),
 (('lack', 'fact'), 0.19),
 (('society', 'culture'), 0.19),
 (('operation', 'project'), 0.19),
 (('plan', 'rules'), 0.19),
 (('cities', 'regions'), 0.19),
 (('services', 'operations'), 0.18),
 (('countries', 'states'), 0.18),
 (('agreement', 'decision'), 0.18),
 (('example', 'evidence'), 0.18),
 (('way', 'means'), 0.16),
 (('light', 'signal'), 0.15)]
```