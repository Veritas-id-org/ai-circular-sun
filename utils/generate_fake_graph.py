# importing package
import matplotlib.pyplot as plt
  
# create data
x = ['Syndey','Melbourne','Perth','Brisbane','Hobart', 'Adeliade', 'Darwin']
y1 = [1.06,0.98,1.20,1.14,0.95,1.14,1.20]
y2 = [5.20,4.89,5.98,5.71,4.75,5.71,5.98]
y3 = [10.60,9.78,11.95,11.41,9.51,11.41,11.95]
y4 = [21.19,19.56,23.91,22.82,19.02,22.82,23.91]
y5 = [105.96,97.81,119.55,114.11,95.10,114.11,119.55]
  
# plot lines
plt.figure(figsize=(20,6))
plt.plot(x, y1, label = "1KW")
plt.plot(x, y2, label = "5KW")
plt.plot(x, y3, label = "10KW")
plt.plot(x, y4, label = "20KW")
plt.plot(x, y5, label = "100KW")
plt.legend(loc='best')
plt.title('Annual Co2 Reduction (Tons) on Different Solar Sizes (KW)')
plt.show()