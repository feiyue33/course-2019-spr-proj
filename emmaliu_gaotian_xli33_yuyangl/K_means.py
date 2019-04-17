import random as rand
import math as math
import matplotlib.pyplot as plt
import json


class Point:
    def __init__(self, latit_, longit_):
        self.latit = latit_
        self.longit = longit_
        
        
class clustering:
    def __init__(self, geo_locs_, k_):
        self.geo_locations = geo_locs_
        self.k = k_
        self.clusters = []  
        self.means = []    



    def next_node(self, index, points, clusters):
        
        dist = {}
        for point_1 in points:
            for cluster in clusters.values():
                point_2 = cluster[0]
                if point_1 not in dist:
                    dist[point_1] = math.sqrt(math.pow(point_1.latit - point_2.latit,2.0) + math.pow(point_1.longit - point_2.longit,2.0))       
                else:
                    dist[point_1] += math.sqrt(math.pow(point_1.latit - point_2.latit,2.0) + math.pow(point_1.longit - point_2.longit,2.0))
        count_ = 0
        max_ = 0
        for key, value in dist.items():
            if count_ == 0:
                max_ = value
                max_point = key
                count_ += 1
            else:
                if value > max_:
                    max_ = value
                    max_point = key
        return max_point
    
    
    def means_init(self, points):
        point_ = rand.choice(points)
        clusters = dict()
        clusters.setdefault(0, []).append(point_)
        points.remove(point_)
       
        for i in range(1, self.k):
            point_ = self.next_node(i, points, clusters)
            clusters.setdefault(i, []).append(point_)
            points.remove(point_)
      
        self.means = self.compute_mean(clusters)
       
            
            
    def compute_mean(self, clusters):
        means = []
        for cluster in clusters.values():
            mean_point = Point(0.0, 0.0)
            cnt = 0.0
            for point in cluster:
                mean_point.latit += point.latit
                mean_point.longit += point.longit
                cnt += 1.0
            mean_point.latit = mean_point.latit/cnt
            mean_point.longit = mean_point.longit/cnt
            means.append(mean_point)
        return means
   
    
    def assign_points(self, points):
        clusters = dict()
        for point in points:
            dist = []
            
            for mean in self.means:
                dist.append(math.sqrt(math.pow(point.latit - mean.latit,2.0) + math.pow(point.longit - mean.longit,2.0)))
          
            cnt_ = 0
            index = 0
            min_ = dist[0]
            for d in dist:
                if d < min_:
                    min_ = d
                    index = cnt_
                cnt_ += 1
         
            clusters.setdefault(index, []).append(point)
        return clusters
    
    
    def update_means(self, means, threshold):
        for i in range(len(self.means)):
            mean_1 = self.means[i]
            mean_2 = means[i]
            
            if math.sqrt(math.pow(mean_1.latit - mean_2.latit,2.0) + math.pow(mean_1.longit - mean_2.longit,2.0)) > threshold:
                return False
        return True
    
  
    def print_clusters(self, clusters):
        cluster_cnt = 1
        for cluster in clusters.values():
            print("nodes in cluster #%d" % cluster_cnt)
            cluster_cnt += 1
            for point in cluster:
                print("point(%f,%f)" % (point.latit, point.longit))
  
    
    def print_means(self, means):
        for point in means:
            print("%f %f" % (point.latit, point.longit))
    
    
    def k_means(self, plot_flag):
        if len(self.geo_locations) < self.k:
            return -1  
        
        points_ = [point for point in self.geo_locations]
        self.means_init(points_)
        
        stop = False
        while not stop:
            points_ = [point for point in self.geo_locations]
            clusters = self.assign_points(points_)
            means = self.compute_mean(clusters)
            stop = self.update_means(means, 0.01)
            if not stop:
                self.means = []
                self.means = means
        self.clusters = clusters
       
        
        if plot_flag:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            markers = ['o', 'd', 'x', 'h', 'H', 7, 4, 5, 6, '8', 'p', ',', '+', '.', 's', '*', 3, 0, 1, 2]
            colors = ['r', 'k', 'b', [0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]
            cnt = 0
            for cluster in clusters.values():
                latits = []
                longits = []
                for point in cluster:
                    latits.append(point.latit)
                    longits.append(point.longit)
                ax.scatter(longits, latits, s=60, c=colors[cnt], marker=markers[cnt])
                cnt += 1
            plt.show()
        return 0


def loadTweets():
     with open("/Users/mac/Desktop/tweets_amman.json", 'r') as f:
         temp=json.loads(f.read())
         #length=len(temp)
         place=[]
         bounding=[]
         location=[]
         position=[]
         
         for i in range(0,len(temp)):
             if temp[i]['place']!=None:
                 place.append(temp[i]['place'])
         for j in range(0,len(place)):
             if place[j]['bounding_box']!=None:
                 bounding.append(place[j]['bounding_box'])
         for k in range(0,len(bounding)):
             if bounding[k]['coordinates']!=None:
                 location.append(bounding[k]['coordinates'])

                 
         for m in range (0,len(location)):
             for n in range (0,len(location[m][0])):
                 position.append(location[m][0][n])
                     
         #print(len(position))
         return position

def main():
    geo_locs = []
    #loc=loadTweets()  #get data from the json file
    loc=[[35.518228, 31.7117874],[35.8958489, 31.7117874],[35.8958489, 32.2482657],[35.518228, 32.2482657],[35.6797295, 31.2567877],[37.2500185, 31.2567877],[37.2500185, 32.088612],[35.6797295, 32.088612],[35.8771149, 31.5084006],[37.789607, 31.5084006],[37.789607, 32.2290518],[35.8771149, 32.2290518],[34.266924, 29.393973],[35.669933, 29.393973],[35.669933, 33.290533],[34.266924, 33.290533],[35.6762878, 32.1214959],[35.9993981, 32.1214959],[35.9993981, 32.4054203],[35.6762878, 32.4054203],[35.546435, 32.247619],[36.0871758, 32.247619],[36.0871758, 32.7553607],[35.546435, 32.7553607]]

    for i in range(0,len(loc)):
        loc_ = Point(float(loc[i][0]),float(loc[i][1]))
        geo_locs.append(loc_)
    
    cluster = clustering(geo_locs, 3 )
    flag = cluster.k_means(False)
    if flag == -1:
        print("Error in arguments!")
    else:
        print("clustering results:")
        cluster.print_clusters(cluster.clusters)
        means=cluster.compute_mean(cluster.clusters)
        print("clustering means:")
        cluster.print_means(means)
        cluster.k_means(True)
        cluster.print_means
        
if __name__ == "__main__":
    main()
