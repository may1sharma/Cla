import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import math

def main():
    outFile = "Path.txt"
    if len(sys.argv) < 2:
        print " Please specify input txt file"
    elif len(sys.argv) >2:
        outFile = sys.argv[2]

    heatmap = defaultdict(float)
    unvisited = set()

    # Read Input file
    with open(sys.argv[1], 'r') as file:
        for line in file:
            params = line.split(" ")
            probability = float(params[2])
            heatmap[(int(params[0]), int(params[1]))] = probability
            if probability > 0:
                unvisited.add((int(params[0]), int(params[1]), float(params[2])))

    # print heatmap
    # print "Total non zero nodes ", len(unvisited)

    # Closest non-zero valued node
    node = min(unvisited, key= lambda x: (math.pow(x[0], 2) + math.pow(x[1], 2)))
    # print "Closest node ",  node
    closest = int(math.ceil(math.sqrt(math.pow(node[0], 2) + math.pow(node[1], 2))))
    # print closest
    idealPath = sorted(unvisited, key= lambda x: x[2], reverse = True)

    # Initialization
    node = (0, 0)
    cdp = []
    time = []
    cdp.append(heatmap[node])
    time.append(0)
    if (0, 0, heatmap[node]) in unvisited:
        unvisited.remove((0,0, heatmap[node]))
    direction = 0
    calc_direction = {(-1, -1): 1, (-1, 0): 2, (-1, 1): 3, (0, 1): 4, (1, 1): 5, (1, 0): 6, (1, -1): 7, (0, -1): 8}
    output = []
    # output.append(node)

    while unvisited:
        destination = max(unvisited, key= lambda x: (x[2], -math.pow(x[0]-node[0], 2) - math.pow(x[1]-node[1], 2)))

        # Traverse to destination
        while not (node[0] == destination[0] and node[1] == destination[1]):
            x = node[0]
            y = node[1]

            # Shifting x coordinate
            if destination[0] > node[0]:
                nx = x + 1
            elif destination[0] < node[0]:
                nx = x - 1

            # Shifting y coordinate
            if destination[1] > node[1]:
                ny = y + 1
            elif destination[1] < node[1]:
                ny = y - 1

            node = (nx, ny)

            climb = []
            for d in calc_direction.keys():
                if (x + d[0], y + d[1], heatmap[(x + d[0], y + d[1])]) in unvisited:
                    climb.append((x + d[0], y + d[1]))
            # if nx != x and ny != y:
            #     if (nx, y, heatmap[(nx, y)]) in unvisited:
            #         climb.append((nx, y))
            #     if (x, ny, heatmap[(x, ny)]) in unvisited:
            #         climb.append((x, ny))
            #     if (nx, ny, heatmap[(nx, ny)]) in unvisited:
            #         climb.append((nx, ny))

            # print climb
            if climb:
                node = max(climb, key=lambda x:(heatmap[x],
                                                -math.pow(x[0]-destination[0], 2) - math.pow(x[1]-destination[1], 2)))

            # Append way-point to output if direction is changed
            ndir = calc_direction[(node[0] - x, node[1] - y)]
            if ndir != direction:
                output.append((x, y))
                direction = ndir

            if ndir in [1, 3, 5, 7]:
                time.append(time[-1] + math.sqrt(2))
            else:
                time.append(time[-1] + 1)

            # Traverse the node if unvisited
            if (node[0], node[1], heatmap[node]) in unvisited:
                cdp.append(cdp[-1] + heatmap[node])
                unvisited.remove((node[0], node[1], heatmap[node]))
            else:
                cdp.append(cdp[-1])
    # Append Last node to output
    output.append(node)

    # print "All waypoints ", len(output)
    # print "Unique waypoints ", len(set(output))
    # print output
    # Write output to file
    with open(outFile, 'w') as file:
        for line in output:
            file.write(str(line[0]) + " " + str(line[1]) + "\n")

    # Compute Efficiency-LB
    T = [100, 200, 300, 600, 900]
    effLB = []

    for t in T:
        B = 0
        for i in range(t+1-closest):
            B += idealPath[i][2]
        # print B
        i = 0
        while time[i] < t:
            i += 1
        effLB.append(cdp[i]/B)
        # print cdp[i]

    print
    print "----------------------- Table: Efficiency-LB vs Time -----------------------"
    print
    print "     Time         \t        Efficiency-LB"
    print
    for i in range(len(T)):
        print "    ", T[i], "        \t       ", effLB[i]

    # Plot of CDP vs Time
    plt.plot(time, cdp)
    plt.xlabel('Flight Time')
    plt.ylabel('CDP')
    plt.title('CDP vs Flight Time')
    plt.show()


if __name__ == "__main__":
    main()
