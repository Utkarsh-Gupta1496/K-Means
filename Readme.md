This Repository contains implementation of **K_Means Algorithm** from scratch in numpy.

**Dataset Used** : 50,000 Images from CIFAR 10 Dataset
  1. Load the data from the following link:
     https://www.cs.toronto.edu/~kriz/cifar.html
     
**Features(Generated for each CIFAR Image):**
  1. Every ML technique requires a carefully crafted features on which that particular algorithm is trained, Similarly our K_Means Algorithm will require some appropriate feature vector.
  2. Feature Generation(For KMeans):
       a) Convert images to grayscale images.\
       b) Find the histograms and get a 10-dimensional representation of each images\
       c) For each image, find the histogram with bin size 25 (last bin of 30;i.e.225-255;giving you 10 bins)\
       d) Data Matrix = Datapoints x Feature Size = 5000 x 10
       
**Distance-Metric utilized here in K-Means Algorithm**: L2-Distance

**Value of K used for demonstration :** 5 (5 Clusters)

**Visulization** : Principal Component Analysis (PCA) 

**Sample Ouput**: ![](/images/output.png.png)

