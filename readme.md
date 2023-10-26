# Deep Lifelog Data Analysis
[Data Visualization Demo](https://lifelog.streamlit.app/)
## Introduction
This is my first serious data analysis project. The project spans from data collection and formatting to presentation. The repo is intended for exhibition and demo hosting only, not for forking or application to other projects. Most of the functionality is data wrangling of very specific non-generalizable idiosyncracies. Individual codebase elements like the custom query language may be adaptable to other purposes.

Since I started grad school in September 2017, I've collected continuous time series tabular data on my daily activities. It started as a small productivity exercise to track my academic tasks,
but as my data obsession kicked in the scope ballooned out of control.

I was inspired by [r/dataisbeautiful content like this](https://www.reddit.com/r/dataisbeautiful/comments/ab4uzz/i_recorded_every_hour_of_my_2018_and_17_oc/),
but I wanted to track way more detail than a single categorical variable over fixed intervals.

Though it was suited fine for the original small productivity exercise, the scope of data features has blown way past what the app that I use for data collection, [timesheet.io](https://timesheet.io/), was intended for. Most of the juicy information, included that for all of the features listed above, is all collected in a single string entry. So about 90% of this project has been feature engineering: designing data structures to represent one's day-to-day life, parsing that one string, unpacking the mess of shortcuts I've used to streamline collection, and fixing a litany of rookie mistakes.

I implemented a hybrid `pandas`/OOP framework for the project.  My focus in development was on scalability and maintainability over performance. This is because the dataset is small, and I expect to continue adding features over time.

## Where's the Data?
Separating all sensitive information from the public codebase has been one of the challenges of the project. Due to the sensitive nature of the data, only a limited amount of data is shared in this repo:
- Small sample of raw data
  - `RAW_CSVs/sample_RAW_PUBLIC.csv`
  - Be aware that all the raw data is collected in Spanish, which was it's own challenge
- Intermediate `Catalog` yaml files for all implemented `Collectible` leaf classes except for `Person` and `Location`
  -`catalogs/Catalog_*.yaml`
- Graphics used by the [Demo](https://lifelog.streamlit.app/)
  - `VS_Persistent/figs_PUBL.pkl`

## Data Features
Raw data features:
- Time interval
- Project
- Tags
- Description
- Mood

Implemented in feature engineering:
- Media (`TVShow`, `Movie`, `Podcast`, `Audiobook`)
- `Person`
- `Food`

Data is logged, but further feature engineering needed:
- Media (`Software`, `VideoGame`, `TabletopGame`)
- `Location`
- `SubjectMatter`: topics discussed and researched
## Codebase Features
- Custom query language built with `antlr` for readable and maintainable query and update statements
  - `tsqparser/independent.tsqy`: Primary query file used for data cleaning
  - `tsqparser/TimesheetQuery.g4`: Grammar file
- `Collectible` class hierarchy structuring shared features of `Audiobook`, `Podcast`, `Food`, and `Person` classes, among others
- `HierarchicalEnum` an `Enum`-like abstract base class where enum members are organized in a hierarchy   
  - Implemented via pure python class inheritance to represent any directed acyclic graph hierarchy
  - Ex: `Genre`, `SocialGroup`, and `SubjectMatter`
- Internationalization and localization (partially implemented) to translate Spanish raw and `Enum` data into English.
- Key libraries:
  - pandas
  - numpy
  - antlr
  - yamlable
  - matplotlib
  - streamlit