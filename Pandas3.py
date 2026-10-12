import pandas
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

df = pandas.read_csv('exsample1.csv')
df.columns = df.columns.str.replace('Unnamed: 7','Price')
df.columns = df.columns.str.replace('Unnamed: 9','Sum')
df.columns = df.columns.str.replace('Unnamed: 2','Data')
df.columns = df.columns.str.replace('Unnamed: 1','Ordererr')
df.columns = df.columns.str.replace('Unnamed: 3','City')
df.columns = df.columns.str.replace('Unnamed: 8','Kilkist')
df.columns = df.columns.str.replace('Unnamed: 6','Product')
fig = plt.figure(figsize=(12, 7))
gs = GridSpec(ncols= 3, nrows = 2,figure = fig)
#df.drop(labels=[0], axis=0)
df['Price'] = pandas.to_numeric(df.Price)
df.to_numpy()
print(df.info())

dk=df
df['New Price'] = df['Price'] + df['Price'] * 0.1
#df = df[df.Sum > 3000]
df = df[df.Sum > 3000]
dk = dk[dk.Price >0]
a = df['Kilkist'].to_list()
v = df['Kilkist'].to_list()
a1 = dk['Price'].to_list()
v1 = dk['City'].to_list()



ax = fig.add_subplot(gs[0,0:4])
ax.scatter(range(0, len(a)), a, s=20, c=(0, 0.1, 0.9))
ax.xaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(v))

fig.suptitle("Sells Nigers")

ax.set_xlabel('X ')
ax.set_ylabel('Y ')
ax.annotate('Few Sells!', xy=(17.01, 550), xytext=(16.3, 2000),
            arrowprops={'facecolor':'red', 'shrink':0.1})
ax.tick_params(axis='both', which='major', labelsize=12)
ax.axis([0, 18, 0, 4000])
plt.plot(a)

ax2 = fig.add_subplot(gs[1,0:4])
ax2.scatter(range(0, len(a1)), a1, s=20, c=(0, 0.8, 0.5))
ax2.xaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(v1))
ax2.annotate('Good!', xy=(7, 7), xytext=(6, 20),
            arrowprops={'facecolor':'red', 'shrink':0.1})
ax2.axis([0, 18, 0, 50])
plt.plot(a1)







plt.show()