import pandas
import matplotlib
import matplotlib.pyplot as plt

df = pandas.read_csv('exsample1.csv')
df.columns = df.columns.str.replace('Unnamed: 7','Price')
df.columns = df.columns.str.replace('Unnamed: 9','Sum')
#df.drop(labels=[0], axis=0)
df['Price'] = pandas.to_numeric(df.Price)


"""df.rename(columns={
    'Unnamed: 1':'Date',
    'Unnamed: 2':'Ordererr',
    'Unnamed: 3':'City',
    'Unnamed: 4':'Region',
    'Unnamed: 5':'Category',
    'Unnamed: 6':'Product',
    'Unnamed: 7':'Price',
    'Unnamed: 8':'Quantity',
    'Unnamed: 9':'Sum',
})"""
df.to_csv('file.csv')
df['New Price'] = df['Price'] + df['Price']*0.1
df[df.Sum > 500]
print(df)

x = (df)
plt.plot(*x)
plt.show()