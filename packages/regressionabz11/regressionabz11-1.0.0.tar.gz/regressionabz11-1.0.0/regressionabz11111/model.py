#importing Matplotlib for plotting
import matplotlib.pyplot as plt
import numpy as np
from regression import LinearRegression
 
#Loding the data
df = pd.read_csv('data_LinearRegression.csv')
 
#Preparing the data
x = np.array(df.iloc[:,0])
y = np.array(df.iloc[:,1])
 
#Creating the class object
regressor = LinearRegression(x,y)
 
#Training the model with .fit method
regressor.fit(1000 , 0.0001) # epochs-1000 , learning_rate - 0.0001
 
#Prediciting the values
y_pred = regressor.predict(x)
 
#Plotting the results
plt.figure(figsize = (10,6))
plt.scatter(x,y , color = 'green')
plt.plot(x , y_pred , color = 'k' , lw = 3)
plt.xlabel('x' , size = 20)
plt.ylabel('y', size = 20)
plt.show()