import os
import csv
SRC_NUM = 8
DEST_NUM = 9
PACKET_SIZE = 1000

throughput_dict = {}

def parse_file(file):
    with open(file) as f:
        lines = f.readlines()

    drop_num = 0

    #Global start/end time
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
        if(arr[SRC_NUM] != "0.0" or arr[DEST_NUM] != "3.0"):
            continue
        time = float(arr[1])
        if start_time == -1:
            start_time = time
        else:
            end_time = time

        # If we've seen this packet before, then update end time
        if arr[10] in packet_dict:
            packet_dict[arr[10]][1] = time
        # If we never seen this packet before, set time as start time
        else:
            packet_dict[arr[10]] = [time, -1]

        if (line[0] == "d"):
            print "packet drop"
            drop_num+=1

    name_arr = file.split("_")
    tcp_v = name_arr[2]
    band_width = int(name_arr[1][0])

    if tcp_v not in throughput_dict:
        throughput_dict[tcp_v] = []

    throughput_dict[tcp_v].append(compute_throughput(packet_dict, start_time, end_time))
    compute_avg_latency(packet_dict)
    compute_drop_rate(packet_dict, drop_num)

def compute_throughput(packet_dict, start_time, end_time):
    packet_num = len(packet_dict)
    data_size = packet_num*PACKET_SIZE
    throughput = data_size*8/(1000000*(end_time-start_time))
    print("Throughput: {} Mps".format(throughput))
    return str(throughput)


def compute_avg_latency(packet_dict):
    sum = 0
    for value in packet_dict.values():
        sum += value[1]-value[0]
    print("Latency: {}s".format(sum/ len(packet_dict)))
    return sum/ len(packet_dict)

def compute_drop_rate(packet_dict, drop_num):
    print("Drop rate: {}%".format(drop_num*1.0/len(packet_dict)))
    return drop_num*1.0/len(packet_dict)


for file in sorted(os.listdir("./results")):
    arr = file.split("_")
    if arr[-1] == "12000.tr":
        continue
    try:
        print "Computing {} TCP with {} bandwidth and packet size {}".format(arr[2], arr[1], arr[-1])
    except:
        print "Invalid filename: " + file

    parse_file("./results/" + file)

with open('dict.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in throughput_dict.items():
        str = ';'.join(value)
        writer.writerow([key, str])
print throughput_dict
