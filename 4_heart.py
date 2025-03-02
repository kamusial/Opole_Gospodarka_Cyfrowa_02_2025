import pandas as pd

df = pd.read_csv('heart.csv', comment='#')
print(df.head().to_string())