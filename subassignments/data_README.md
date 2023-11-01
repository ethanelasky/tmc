# Data Source Documentation Assignment
## Prompt
Identify data source for your research project, and document aspects of this data source. 
Data provenance, and explanation of how the data was or will be gathered should be documented.  
Ownership of the data, including licensing issues for dataset and possible outputs should be discussed. 
Possibilities for bias or censoring in the data should be explored.
## Response
### Data source and provenance
My corpus for analysis will come from American and Taiwanese news outlets and will consist of all articles published between 2013 and 2023. 
For American news, I will use ProQuest’s US Major Dailies (the five most important newspapers in the country, comprised of the New York Times, the Washington Post, the Wall Street Journal, the Chicago Tribune, and the Los Angeles Times). This database is available on ProQuest’s [TDMStudio](https://tdmstudio.proquest.com), which is free for Berkeley affiliates. 
More details on TDMStudio data available [here](notebooks/Extracting_data_from_TDM_Studio.ipynb).
For Taiwanese news, I will scrape all online news articles within the given timeframe from the island’s three major dailies ([Liberty Times](https://www.ltn.com.tw), [United Daily News](https://udn.com/news/index), [China Times](https://www.chinatimes.com)). These sites’ news is publicly available without login, although they may contain diff
Scrapers for each site can be found in the `scrapers` folder, and an in-depth explanation of how I will deploy them can be found [here](scrapers/scraping_README.md).
Finally, to develop a list of seed words, which find articles relevant to China among the entire corpus of all articles, I may collect links and associated words from posts in [PTT](https://www.ptt.cc/bbs/index.html), which is like Reddit but Taiwanese.
### Data rights and ownership concerns
American newspaper data is available through license via ProQuest. Taiwanese online newspaper data will be obtained through web scraping. Use of these articles is permitted under the research clause of fair use (合理使用) both in America and in Taiwan.
Web versions of news articles may differ from their print versions; to maintain consistency with my approach to scraping Taiwanese news, I will only use Web versions of news articles.
### Censorship and bias
The United States and Taiwan each [rank]( https://freedomhouse.org/country/united-states/freedom-net/2021#B) [highly](https://freedomhouse.org/country/taiwan/freedom-net/2021#B)  in terms of lack of censorship and content restrictions. 
In terms of bias, my data may leave out news articles that are not linked to within the news website (e.g. not accessible via search). Additionally, my search of PTT articles for seed words may not be exhaustive, meaning that I may miss a few terms that demonstrate relevance to China. 

