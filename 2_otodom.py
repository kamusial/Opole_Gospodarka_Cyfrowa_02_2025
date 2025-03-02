import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('otodom.csv')
print(df.head().to_string())   # wyświetl 5 pierwszych wierszy

print(df.describe().T.to_string())
sns.heatmap(df.iloc[:, 1:].corr(), annot=True)
plt.show()
