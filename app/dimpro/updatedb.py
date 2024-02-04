from alegra.client import Client
import pandas as pd



client = Client("dimproiluminacion@gmail.com", "63329e8f711dc6dbecbc")

n = 90 // 30
items = []
for i in range(n):

    dictu = client.list_items(start=(n * 10 * i), order="ASC")
    items = items + dictu
    

itemsf = pd.json_normalize(items, sep='.')
sorteditems = itemsf.sort_values(by=["id"], ascending=True)

print(sorteditems)
