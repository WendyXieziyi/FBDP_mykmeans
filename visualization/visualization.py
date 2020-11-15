import matplotlib.pyplot as plt

path = "D:\classes\大四上\金融大数据处理技术\实验\作业七\MyKmeans\output"
filename = path+"\clusteredInstances\part-m-00000"

cluster = []
X = []
Y = []

with open(filename, "rt") as f:
    lines = f.readlines()
    for line in lines:
        print(line)
        cluster.append(line[-2])
        line = line[:-3]
        temp = [int(t) for t in line.split(',')]
        X.append(temp[0])
        Y.append(temp[1])

plt.xlabel('X')
plt.ylabel('Y')
colors = ['r', 'g', 'b']

for j in range(len(cluster)):
    plt.scatter(X[j], Y[j], c=colors[int(cluster[j])-1], alpha=0.4)
# plt.show()
plt.savefig(path+"/result.png")
