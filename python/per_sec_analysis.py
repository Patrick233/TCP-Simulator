import os
import csv
import matplotlib.pyplot as plt

EVENT_NUM = 0
SRC_NUM = 8
DEST_NUM = 9
PACKET_TYPE = 4
TO_NODE = 3
PACKET_SIZE = 1000
# RESULT_DIR = "./result2"
RESULT_DIR = "./results"

packet_count = []

throughput_dict = {}
latency_dict = {}
droprate_dict = {}

def compute_throughput(packet_dict, start_time, end_time):
    packet_num = len(packet_dict)
    data_size = packet_num * PACKET_SIZE
    throughput = data_size * 8 / (1000000 * (end_time - start_time))
    print("Throughput: {} Mps".format(throughput))
    return str(throughput)


def parse_file(file):
    with open(file) as f:
        lines = f.readlines()

    drop_num = 0

    # Global start/end time
    start_time = -1
    end_time = -1

    # Parse each tcp packet and save in the start_time and end_time in the dict
    # e.g packet 1 starts at 1.0 and ends at 10.0, then at the end we'll have an entry {1, [1.0, 10.0]}
    packet_dict = {}

    for line in lines:
        arr = line.split(" ")

        # Since we only care about TCP packet here
        # if arr[4] == "tcp":
        #     print "Source " + arr[SRC_NUM]
        #     print "Dest " + arr[DEST_NUM]
        # print arr
        # if(arr[SRC_NUM] != "0.0" or arr[DEST_NUM] != "3.0" or arr[EVENT_NUM] != 'r' or arr[PACKET_TYPE] != 'tcp'):
        if arr[TO_NODE] == '3' and arr[PACKET_TYPE] == 'tcp' and arr[EVENT_NUM] == 'r':
            time = int(float(arr[1]) * 1)
            packet_count[time] += 1


def compute_avg_latency(packet_dict):
    sum = 0
    for value in packet_dict.values():
        sum += value[1] - value[0]
    print("Latency: {}s".format(sum / len(packet_dict)))
    return str(sum / len(packet_dict))


def compute_drop_rate(packet_dict, drop_num):
    print("Drop rate: {}%".format(drop_num * 1.0 / len(packet_dict)))
    return str(drop_num * 100.0 / len(packet_dict))


def write_to_csv(file, count):
    with open(file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for i in range(60):
            writer.writerow([i, count[i]])

def reset():
    for i in range(610):
        packet_count[i] = 0


for file in sorted(os.listdir(RESULT_DIR)):
    packet_count = []
    for i in range(61):
        packet_count.append(0)
    arr = file.split("_")
    # if arr[-1] == "12000.tr" or arr[1] == '7mb' or arr[1] == '6mb' or arr[1] == '5mb':
    if arr[-1] == "12000.tr" or arr[1] != '5mb':
        continue
    try:
        print("Computing {} TCP with {} bandwidth and packet size {}".format(arr[2], arr[1], arr[-1]))
    except:
        print("Invalid filename: " + file)

    parse_file(RESULT_DIR + "/" + file)
    plt.plot(packet_count, label=arr[2] + "_" + arr[1])
    # plt.legend(arr[2])
    plt.hold

# print throughput_dict
# parse_file('/Users/Patrizio/Desktop/neu/CS5700/NS/TCP-Simulator/result2/2_5mb_newreno_reno.tr')
# write_to_csv("per_sec.csv", packet_count)
# print latency_dict
# write_to_csv("latency2.csv", latency_dict)
# print droprate_dict
# write_to_csv("droprate2.csv", droprate_dict)

plt.legend(loc='upper right')
plt.xlabel('Number of packets received at N4 per second')
plt.ylabel('Time / seconds)')
plt.show()
