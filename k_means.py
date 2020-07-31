"""
Created on Fri Feb  7 15:37:04 2020

@author: Utkarsh
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
#%%

# Data Pre-processing
def unpickle(file):
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

def load_cifar_10_data(data_dir, negatives=False):
    """
    Return train_data, train_filenames, train_labels, test_data, test_filenames, test_labels
    """

    # get the meta_data_dict
    # num_cases_per_batch: 1000
    # label_names: ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    # num_vis: :3072

    meta_data_dict = unpickle(data_dir + "/batches.meta")
    cifar_label_names = meta_data_dict[b'label_names']
    cifar_label_names = np.array(cifar_label_names)

    # training data
    cifar_train_data = None
    cifar_train_filenames = []
    cifar_train_labels = []

    # cifar_train_data_dict
    # 'batch_label': 'training batch 5 of 5'
    # 'data': ndarray
    # 'filenames': list
    # 'labels': list

    for i in range(1, 6):
        cifar_train_data_dict = unpickle(data_dir + "/data_batch_{}".format(i))
        if i == 1:
            cifar_train_data = cifar_train_data_dict[b'data']
        else:
            cifar_train_data = np.vstack((cifar_train_data, cifar_train_data_dict[b'data']))
        cifar_train_filenames += cifar_train_data_dict[b'filenames']
        cifar_train_labels += cifar_train_data_dict[b'labels']

    cifar_train_data = cifar_train_data.reshape((len(cifar_train_data), 3, 32, 32))
    if negatives:
        cifar_train_data = cifar_train_data.transpose(0, 2, 3, 1).astype(np.float32)
    else:
        cifar_train_data = np.rollaxis(cifar_train_data, 1, 4)
    cifar_train_filenames = np.array(cifar_train_filenames)
    cifar_train_labels = np.array(cifar_train_labels)


    cifar_test_data_dict = unpickle(data_dir + "/test_batch")
    cifar_test_data = cifar_test_data_dict[b'data']
    cifar_test_filenames = cifar_test_data_dict[b'filenames']
    cifar_test_labels = cifar_test_data_dict[b'labels']

    cifar_test_data = cifar_test_data.reshape((len(cifar_test_data), 3, 32, 32))
    if negatives:
        cifar_test_data = cifar_test_data.transpose(0, 2, 3, 1).astype(np.float32)
    else:
        cifar_test_data = np.rollaxis(cifar_test_data, 1, 4)
    cifar_test_filenames = np.array(cifar_test_filenames)
    cifar_test_labels = np.array(cifar_test_labels)

    return cifar_train_data, cifar_train_filenames, cifar_train_labels, \
        cifar_test_data, cifar_test_filenames, cifar_test_labels, cifar_label_names
        
        
#Directory where dataset is stored        
cifar_10_dir = './Utkarsh/DLCV_assignment/DLCV_Assignment1\cifar-10-python/cifar-10-batches-py'

train_data, train_filenames, train_labels, test_data, test_filenames, test_labels, label_names =\
load_cifar_10_data(cifar_10_dir)
#%%

# Generating DataMatrix(Each data point is represented by a feature matrix)
"Converting CIFAR 10 DATA SET INTO Grayscale"
train_data_final=[]
histogram_train=[]
for i in range(50000):
    temp=train_data[i]
    temp1=cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
    train_data_final.append(temp1)
    
test_data_final=[]
histogram_test=[]
for i in range(10000):
    temp=test_data[i]
    temp1=cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
    test_data_final.append(temp1)

image=train_data_final[0]
  
def bins_grayscale(image):
    vec_image=image.flatten()
    #bin 0-25
    x1=len(np.where(vec_image<=25)[0])
    #bin 25-50
    x2=len(np.where(vec_image<=50)[0])-len(np.where(vec_image<=25)[0])
    #bin 50-75
    x3=len(np.where(vec_image<=75)[0])-len(np.where(vec_image<=50)[0])
    #bin 75-100
    x4=len(np.where(vec_image<=100)[0])-len(np.where(vec_image<=75)[0])
    #bin 100-125
    x5=len(np.where(vec_image<=125)[0])-len(np.where(vec_image<=100)[0])
    #bin 125-150
    x6=len(np.where(vec_image<=150)[0])-len(np.where(vec_image<=125)[0])
    #bin 150-175
    x7=len(np.where(vec_image<=175)[0])-len(np.where(vec_image<=150)[0])
    #bin 175-200
    x8=len(np.where(vec_image<=200)[0])-len(np.where(vec_image<=175)[0])
    #bin 200-225
    x9=len(np.where(vec_image<=225)[0])-len(np.where(vec_image<=200)[0])
    #bin 225-255
    x10=len(np.where(vec_image<=255)[0])-len(np.where(vec_image<=225)[0])
    temp=[]
    temp=[x1,x2,x3,x4,x5,x6,x7,x8,x9,x10]
    temp=np.array(temp).reshape(1,10)
    return temp

# creating a data matrix (50000 * 10)
feature_matrix=np.zeros((1,10))
for i in train_data_final:
    
    temp=bins_grayscale(i)
    feature_matrix=np.vstack((feature_matrix,temp))
    
feature_matrix=feature_matrix[1:50001,:]

feature_matrix=feature_matrix.transpose()   
#%%
# Standardize the data

X_std = StandardScaler().fit_transform(feature_matrix) 
#%%   
# Initializize Number of Clusters 
K=5

# Initialize random means
def inital_mean(K,dimmension):
    mean={}
    for i in range(K):
        mean[i]=(np.random.rand(dimmension)*2)
        
    return mean

mean=inital_mean(K,10)

def updated_mean(feature_matrix,K,classes):
    # feature matrix is (feature) x (datapoints)
    mean={}
    temp=np.array(classes)
    for i in range(K):
        mean[i]=np.mean(feature_matrix[:,np.where(temp==i)[0]],1)
        
    return mean
    
#%%         
def l2_distance(feature_matrix,mean,K1):
    #feature matrix is (feature) x (datapoints)
    classes=[]
    for i in range(feature_matrix.shape[1]):
        temp=np.linalg.norm(mean[0]-feature_matrix[:,i])
        temp1=0
        for j in range(K1):
            temp2=np.linalg.norm(mean[j]-feature_matrix[:,i])
            if temp2 < temp:
                temp1=j
                temp=temp2
        classes.append(temp1)
    mean=updated_mean(feature_matrix,K1,classes)
    return classes,mean
#%%
#K means K=5   
for i in range(10):
    labels,mean=l2_distance(feature_matrix,mean,K)
#%%
labels=np.array(labels)    

#Visulatization of Clusters using PCA

pca = PCA(n_components=2)
         
principalComponents = pca.fit_transform(np.transpose(feature_matrix))
#PCs:50000 x 2
fig = plt.figure()
plt.xlabel('Principal Component 1', fontsize = 15)
plt.ylabel('Principal Component 2', fontsize = 15)
plt.title('K Means (K=5), DataPoints:50,000,PCA Visualization', fontsize = 20)

targets = ['0', '1', '2','3','4']
colors = ['r', 'g', 'b','y','k']

for target, color in zip(targets,colors):
    print (target)
    temp=np.where(labels==int(target))[0]
    # print(temp)
    plt.scatter(principalComponents[temp,0],principalComponents[temp,1],c = color)
    
plt.legend(targets)
plt.grid()
