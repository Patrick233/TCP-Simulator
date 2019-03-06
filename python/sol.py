import os

def compute(file):
    with open(file) as f:
        lines = f.readlines()

    startTime = -1
    endTime = -1
    dataSize = 0
    packetNum = 0
    dropNum = 0

    latencyCount = 0
    latencySum = 0
    packetDict = {}

    for line in lines:
        arr = line.split(" ")
        if(line[0]=="r"):
            if(startTime==-1): startTime = float(arr[1])
            else: endTime = float(arr[1])
            dataSize += int(arr[5])
            if(packetDict.get(arr[10], -1)!=-1):
                latencySum += (float(arr[1])-packetDict.get(arr[10]))
                latencyCount+=1
        if(line[0]=="+"):
            packetDict[arr[10]] = float(arr[1])
            packetNum+=1
        if (line[0] == "d"):
            dropNum+=1
        # print(line)

    throughput = dataSize*8/(1000000*(endTime-startTime))

    print("Throughput: ")
    print(str(throughput)+" Mbps")

    print("Latency: ")
    print(str(latencySum/latencyCount)+" s")

    print("Drop rate: ")
    print(str(dropNum*1.0/packetNum)+"%")

for file in os.listdir("./results"):
    arr = file.split("_")
    try:
        print "Computing {} TCP with {} bandwidth and packet size {}".format(arr[2], arr[1], arr[-1])
    except:
        print "Invalid filename: " + file

    compute("./results/" + file)
