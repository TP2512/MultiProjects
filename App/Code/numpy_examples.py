import numpy as np
print("1d array:\n",np.array([1,2,3]))
print("2d array:\n",np.array([[1.5,2,3],[4,5,6]],dtype=float))
# print("3d array:\n",np.array([[1.5,2,3],[4,5,6]],[[1.5,2,3],[4,5,6]],dtype=float))
print("arrays of zeros:\n",np.zeros((3,4)))
print("arrays of ones:\n",np.ones((3,4),dtype=float))
print("evenly spaced values:\n",np.arange(10,50,5))
print("evenly spaced values:\n",np.linspace(1,10,6))
print("full spaced values:\n",np.full((2,2),7))
print("eye :\n",np.eye(3))
print("random values:\n",np.random.random((2,2)))
print("empty array:\n",np.empty((2,2)))
a = np.array([1,2,3])
b = np.array([[1.5,2,3],[4,5,6]],dtype=float)
np.save('my_array',a)
np.savez('array.npz',a,b)
print(np.load('my_array.npy'))
# print(np.loadtxt('test.txt'))
# print(np.loadtxt('test.txt',delimiter=","))
print(np.loadtxt('test.txt',delimiter=" "))



























