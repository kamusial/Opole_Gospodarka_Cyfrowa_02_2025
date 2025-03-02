import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

moj_plik = pd.read_csv('weight-height.csv')
print(moj_plik)
print(type(moj_plik))

print(moj_plik.head(3))
print(moj_plik.Gender.value_counts())    # policz wartosic w kolumnie Gender
moj_plik.Height = moj_plik.Height * 2.54
# moj_plik.Height *= 2.54    # linia 9 i 10  borią to samo
moj_plik.Weight /= 2.2
print(f'Po zmianie jednostek')
print(moj_plik.head(10))

# plt.hist(moj_plik.Weight)   # przygotuj histram z danyhc "Weight"
# plt.show()
# sns.histplot(moj_plik.Weight)
# plt.show()
#
# sns.histplot(moj_plik.query("Gender=='Male'").Weight)
# sns.histplot(moj_plik.query("Gender=='Female'").Weight)
# plt.show()

moj_plik = pd.get_dummies(moj_plik)   # usuwam dane nienumeryczne, zamienia na numeryczne
print(moj_plik.head())
del moj_plik['Gender_Male']    # usuwa kolumne
moj_plik.rename(columns={'Gender_Female': 'Gender'}, inplace=True)   # wykonaj w locie
print(moj_plik)
# Gender  0 - mezczyzna,     1 - kobieta
