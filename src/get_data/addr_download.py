
from utils.os_client import getOSClient
import pandas as pd
from pathlib import Path

os_client = getOSClient()

def scroll_search(index, query, scroll='3m', size=10000):
    all_hits = []
    response = os_client.search(
        body = query,
        index = index,
        size=size,
        scroll=scroll,
    )
    scroll_id = response['_scroll_id']
    hits = response['hits']['hits']
    all_hits.extend(hits)
    while len(hits) > 0:
        response = os_client.scroll(scroll_id=scroll_id, scroll=scroll)
        scroll_id = response['_scroll_id']
        hits = response['hits']['hits']
        all_hits.extend(hits)
    return [hit['_source'] for hit in all_hits]

def build_query(col_addr, col_country):
    return {
      "_source": [col_addr, col_country],
      "query": {
          "bool": {
              "must": [
                  {
                      "exists": {
                          "field": col_addr
                      }
                  },
                  {
                      "bool": {
                          "must_not": [
                              {"term": {col_addr: ""}},
                              {"term": {col_addr: ",,,,"}},
                              {"term": {col_addr: "na"}},
                              {"term": {col_addr: "n/a"}},
                              {"term": {col_addr: "NaN"}},
                              {"term": {col_addr: "nan"}},
                              {"term": {col_addr: "NaNNaN"}}
                          ]
                      }
                  }
              ]
          }
      }
  }

# pull raw data
hits1 = scroll_search('Watchlist_Alias', build_query('Entity Address', 'Entity Country'))
hits2 = scroll_search('BITE_List_BITE_List_Alias', build_query('Entity Address in Trade Data', 'Entity Country'))

# convert to df
df1 = pd.DataFrame(hits1)
df2 = pd.DataFrame(hits2)

# rename cols
df1.rename(columns={'Entity Address': 'address', 'Entity Country': 'country'}, inplace=True)
df2.rename(columns={'Entity Address in Trade Data': 'address', 'Entity Country': 'country'}, inplace=True)

# combine dfs and store as csv
df = pd.concat([df1, df2], ignore_index=True)

data_dir = Path(__file__).resolve().parent.parent.parent / 'data'
df.to_csv(data_dir / 'addr_raw.csv', index=False)