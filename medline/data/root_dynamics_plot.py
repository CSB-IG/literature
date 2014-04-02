import numpy as np
import matplotlib.pyplot as plt


#data = np.genfromtxt('SN_GN_data.txt', delimiter=',', usecols=(0, 1), names=['x', 'y'])
data = np.genfromtxt('root_dynamics_plotting.txt', delimiter=',', usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), names=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'z'])


fig = plt.figure()
fig.suptitle('Dynamic evolution of MeSH-tree headings', fontsize=16, fontweight='bold', family='serif')

ax1 = fig.add_subplot(111)

ax1.plot(data['a'], data['b'], marker='o', linestyle='-', color='#0000FF', label='A')

ax1.set_title("Headings", fontsize=14,fontweight='bold', family='serif')    
ax1.set_xlabel('Years',fontsize=13, style='italic', family='serif')
ax1.set_ylabel('Prorportions',fontsize=13, style='italic', family='serif' )

ax2 = fig.add_subplot(111)
ax2.plot(data['a'], data['c'], marker='p', linestyle='-', color='#A52A2A', label='B')

ax3 = fig.add_subplot(111)
ax3.plot(data['a'], data['d'], marker='|', linestyle='-', color='#5F9EA0', label='C')

ax4 = fig.add_subplot(111)
ax4.plot(data['a'], data['e'], marker='s', linestyle='-', color='#7FFF00', label='D')

ax5 = fig.add_subplot(111)
ax5.plot(data['a'], data['f'], marker='^', linestyle='-', color='#D2691E', label='E')

ax6 = fig.add_subplot(111)
ax6.plot(data['a'], data['g'], marker='>', linestyle='-', color='#6495ED', label='F')

ax7 = fig.add_subplot(111)
ax7.plot(data['a'], data['h'], marker='*', linestyle='-', color='#DC143C', label='G')

ax8 = fig.add_subplot(111)
ax8.plot(data['a'], data['i'], marker='h', linestyle='-', color='#006400', label='H')

ax9 = fig.add_subplot(111)
ax9.plot(data['a'], data['j'], marker='D', linestyle='-', color='#8B0000', label='I')

ax10 = fig.add_subplot(111)
ax10.plot(data['a'], data['k'], marker='v', linestyle='-', color='#DAA520', label='J')

ax11 = fig.add_subplot(111)
ax11.plot(data['a'], data['l'], marker='1', linestyle='-', color='#808080', label='K')

ax12 = fig.add_subplot(111)
ax12.plot(data['a'], data['m'], marker='3', linestyle='-', color='#008000', label='L')

ax13 = fig.add_subplot(111)
ax13.plot(data['a'], data['n'], marker='.', linestyle='-', color='#00FF00', label='M')

ax14 = fig.add_subplot(111)
ax14.plot(data['a'], data['o'], marker='<', linestyle='-', color='#00FA9A', label='N')

ax15 = fig.add_subplot(111)
ax15.plot(data['a'], data['z'], marker='H', linestyle='-', color='#FF4500', label='Z')

"""
data = np.genfromtxt('root_dynamics_plotting.txt', delimiter=',', usecols=(0, 2), names=['x', 'y'])
ax2 = fig.add_subplot(111)
ax2.plot(data['x'], data['y'], marker='p', linestyle='-', color='b', label='nodes')

"""
leg = ax1.legend(loc='upper right')

plt.axis([1985, 2017, 0, 0.35])

plt.show()
