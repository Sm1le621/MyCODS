import pandas
import matplotlib
import matplotlib.pyplot as plt
import numpy



df = pandas.read_csv('exsample1.csv')
x = numpy.array(str(df))
plt.plot(x)
plt.show()