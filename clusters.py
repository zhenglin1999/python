import numpy as np
from matplotlib import pyplot as plt
from sklearn.mixture import  GaussianMixture
import math
import random

def load_data(file_name):
    f = open(file_name,'r')
    data = f.readlines()
    f.close()
    feature_list = []
    for line in data:
        tmp = line.split('\t')
        feature_list.append([tmp[0],tmp[1]])
    features = np.array(feature_list)
    features = features.astype('float')
    return features

def result_show(features, labels, centers, K=2):
    color_list = ['ob','oy','oc','om','or','og','ok','sb','sy','sc','sm','sr','sg']
    x = []
    y = []
    for i in range(K+1):
        x.append([])
        y.append([])
    for i in range(len(features)):
        x[labels[i]].append(features[i,0])
        y[labels[i]].append(features[i,1])
    for j in range(len(centers)):
        x[K].append(centers[j,0])
        y[K].append(centers[j,1])
    for i in range(len(x)):
        plt.plot(x[i],y[i],color_list[i])
    plt.show()
    return

def draw_DBSCAN(clusters):
    color_list = ['r','b','g','y','k','c','m','w','aqua','beige','brown','cadetblue','darkorchid']
    for i in range(len(clusters)):
        x = []
        y = []
        for j in range(len(clusters[i])):
            x.append(clusters[i][j][0])
            y.append(clusters[i][j][1])
        plt.scatter(x,y,color = color_list[i%len(color_list)])
    plt.show()
    return

def KMEANS(data_set,init_centers):
    centers = init_centers
    k = len(centers)
    cnt=0
    while(1):
        cnt= cnt+1
        clusters={}
        result={}
        for i in range(k):
            clusters[i]=[]
        for i in range(len(data_set)):
            order = 0
            mini=9999
            for it in range(k):
                dis = math.sqrt((data_set[i][0] - centers[it][0]) * \
                    (data_set[i][0] - centers[it][0]) + \
                    (data_set[i][1] - centers[it][1]) * (data_set[i][1] - centers[it][1]))
                if dis < mini:
                    order = it
                    mini = dis
            clusters[order].append(data_set[i])
            result[i] = order
        centers_new=[]
        dif = 0
        for i in range(k):
            sumx = 0
            sumy = 0
            for j in range(len(clusters[i])):
                sumx = sumx + clusters[i][j][0]
                sumy = sumy + clusters[i][j][1]
            centers_new.append(np.array([sumx/len(clusters[i]),sumy/len(clusters[i])]))
        for i in range(k):
            dif = dif + abs(centers[i][0]-centers_new[i][0]) +abs(centers[i][1]-centers_new[i][1])
        if dif < 10**(-4) or cnt > 50:
            return clusters,result
        else:
            centers=centers_new


def DBSCAN(_data_set,Eps,MinPts):
    data_set = []
    for i in _data_set:
        data_set.append(tuple(i))
    T = set()
    k = 0
    clusters = []
    unvisited = set(data_set)
    for i in data_set:
        if len([j for j in data_set if math.sqrt((i[0] - j[0])*(i[0] - j[0]) + \
                    (i[1] - j[1]) * (i[1] - j[1])) <= Eps])>= MinPts:
            T.add(i)
    c0 = list(unvisited - T)
    clusters.append(c0)
    while len(T):
        prev = unvisited
        o = list(T)[np.random.randint(0,len(T))]
        unvisited = unvisited - set(o)
        queue = [o]
        while len(queue):
            q = queue[0]
            nb = [i for i in data_set if math.sqrt((i[0] - q[0])*(i[0] - q[0]) + \
                    (i[1] - q[1]) * (i[1] - q[1])) <= Eps] 
            if len(nb) >= MinPts:
                s = unvisited & set(nb)
                unvisited = unvisited - s
                queue = queue + list(s)
            queue.remove(q)
        k = k + 1
        ck = list(prev - unvisited)
        T = T - set(ck)
        clusters.append(ck)
    return clusters






if __name__ == "__main__":
    sample = load_data('Restaurant_Data_Beijing.txt')
    gmm=GaussianMixture(n_components=3, covariance_type='tied')#gmm methods
    result_GMM = gmm.fit_predict(sample)
    center=gmm.means_
    result_show(sample, result_GMM, center,6)
    cluster,result_KMEANS = KMEANS(sample,center)#kmeans methods
    result_show(sample, result_KMEANS, center,3)
    clusters = DBSCAN(sample,0.010,7)#DBSCAN methods
    draw_DBSCAN(clusters)
