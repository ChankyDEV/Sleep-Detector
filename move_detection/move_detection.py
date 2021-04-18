import csv
import matplotlib.pyplot as plt
from scipy import ndimage
from position_data_processing import filterByConfidence
from position_data_processing import averagePerSecond
from position_data_processing import differentiation
from csv_reader import read_csv

name = 'LAnkle'
filmname = 'film_2'

x,y,conf = read_csv('data/'+filmname+'_points/'+name+'.csv')
filteredX, filteredY = filterByConfidence(x,y,conf,0.75)

# Średnie w każdej sekundzie
avgX = averagePerSecond(filteredX)
avgY = averagePerSecond(filteredY)

# Filtracja medianowa
medianX=ndimage.median_filter(input=avgX,size=5)
medianY=ndimage.median_filter(input=avgY,size=5)
frames = list(range(0, len(medianX)))

fig, (ax1, ax2,ax3,ax4) = plt.subplots(4,1)
fig.suptitle(f'{name}')

diffX = differentiation(avgX)
diffY = differentiation(avgY)

ax1.plot(range(len(avgX)), avgX)
ax1.set_title('Filtered X')

ax2.plot(range(len(avgY)), avgY)
ax2.set_title('Filtered Y')

ax3.plot(range(len(diffX)), diffX)
ax3.set_title('diff X')

ax4.plot(range(len(diffX)), diffX)
ax4.set_title('diff Y')

plt.show()