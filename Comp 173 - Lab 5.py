#!/usr/bin/python
import sys
import copy


class Process:
    def __init__(self, PID, Arrival, Burst, Start, End, Wait):
        self.PID = PID
        self.Arrival = Arrival
        self.Burst = Burst
        self.Start = Start
        self.End = End
        self.Wait = Wait

    def process_info(self):
        print("PID: %d\t Arrival Time: %d\t Start Time: %d\t End Time: %d\t Running Time: %d\t Wait Time: %d"
              % (self.PID, self.Arrival, self.Start, self.End, self.Burst, self.Wait))

    def index(vector, format, key):
        if format == "PID":
            for index in range(len(vector)):
                if vector[index].PID == key:
                    return index
        elif format == "Arrival":
            for index in range(len(vector)):
                if vector[index].Arrival == key:
                    return index
        elif format == "Burst":
            for index in range(len(vector)):
                if vector[index].Burst == key:
                    return index

    def Update_Burst(self, value):
        self.Burst = value

    def fcfs(process_count, processes):
        queue = []; check = []
        check = copy.deepcopy(processes)

        for index in range(len(check)):
            if check[index].Burst == 0:
                del check[index]
                process_count = process_count - 1

        for y in range(process_count):
            small = check[0].Arrival
            for x in range(len(check)):
                if check[x].Arrival < small:
                    small = check[x].Arrival
            index = Process.index(processes, "Arrival", small)
            queue.append(processes[index])
            del check[Process.index(check, "Arrival", small)]

        print("Job Queue:")
        for size in range(len(queue)):
            queue[size].process_info()

        ready = []; wait = copy.deepcopy(queue); clock = 0; current = None

        while clock >= 0:
            print("Time: %d" % clock)

            # Completion Check
            if len(wait) == 0 and len(ready) == 0:
                break

            # Move to Ready if Available / Delete Incorrect Processes
            for index in range(len(wait)):
                if index < len(wait):
                    if wait[index].Burst == 0:
                        print("Bad Process!")
                        del wait[index]

                    if wait[index].Arrival <= clock:
                        ready.append(copy.copy(wait[index]))
                        del wait[index]

            if len(ready) > 0:
                current = ready[0]

            # Kill Completed Processes
            for index in range(len(ready)):
                if index < len(ready):
                    if ready[index].Burst == 0:
                        print("\n---------Process %d Complete---------" % ready[index].PID)
                        update = Process.index(processes, "PID", ready[index].PID)
                        processes[update].End = clock
                        temp = processes[update]
                        temp.Wait = (temp.End - (temp.Arrival + temp.Burst))
                        del ready[index]
                        clock = clock - 1

            # User Info Output
            print("Working on PID: %d" % current.PID)
            current.process_info()
            current.Update_Burst(current.Burst-1)

            temp = Process.index(processes, "PID", current.PID)
            if processes[temp].Arrival != 0 and processes[temp].Start == 0:
                processes[temp].Start = clock

            clock += 1

        print("\n---------Final Time: %d---------" % clock)
        del ready; del check; Avg_Wait = 0
        for index in range(len(processes)):
            processes[index].process_info()
            Avg_Wait += processes[index].Wait
        Avg_Wait = (Avg_Wait/(len(processes)))
        print("---------Average Wait Time: %.2f---------" % Avg_Wait)

    def rr(process_count, processes, quantum):
        quantum = int(quantum[0])
        if quantum <= 0:
            print("Incorrect Time Quantum")
            exit(1)

        queue = []; check = []; i = 0; time = 0
        check = copy.deepcopy(processes)

        for index in range(len(check)):
            if check[index].Burst == 0:
                del check[index]
                process_count = process_count - 1

        for y in range(process_count):
            small = check[0].Arrival
            for x in range(len(check)):
                if check[x].Arrival < small:
                    small = check[x].Arrival
            index = Process.index(processes, "Arrival", small)
            queue.append(processes[index])
            del check[Process.index(check, "Arrival", small)]

        print("Job Queue:")
        for size in range(len(queue)):
            queue[size].process_info()

        ready = []; wait = copy.deepcopy(queue); clock = 0; current = None

        while clock >= 0:
            print("Time: %d" % clock, end='\t')

            # Completion Check
            if len(wait) == 0 and len(ready) == 0:
                break

            # Move to Ready if Available / Delete Incorrect Processes
            for index in range(len(wait)):
                if index < len(wait):
                    if wait[index].Arrival <= clock:
                        ready.append(copy.copy(wait[index]))
                        del wait[index]

            if current is None:
                current = ready[0]

            if time == quantum or current.Burst == 0:
                if (i + 1) < len(ready):
                    i = i + 1
                else:
                    i = 0
                current = ready[i]
                time = 0

            # Kill Completed Processes
            for index in range(len(ready)):
                if index < len(ready):
                    if ready[index].Burst == 0:
                        print("\n---------Process %d Complete---------" % ready[index].PID)
                        update = Process.index(processes, "PID", ready[index].PID)
                        processes[update].End = clock
                        temp = processes[update]
                        temp.Wait = (temp.End - (temp.Arrival + temp.Burst))
                        del ready[index]

            # User Info Output
            print("Working on PID: %d" % current.PID)
            current.Update_Burst(current.Burst-1)

            temp = Process.index(processes, "PID", current.PID)
            if processes[temp].Arrival != 0 and processes[temp].Start == 0:
                processes[temp].Start = clock

            clock += 1
            time += 1

        print("\n---------Final Time: %d---------" % (clock - 1))
        del ready; del wait; Avg_Wait = 0
        for index in range(len(processes)):
            processes[index].process_info()
            Avg_Wait += processes[index].Wait
        Avg_Wait = (Avg_Wait/(len(processes)))
        print("---------Average Wait Time: %.2f---------" % Avg_Wait)

    def sjf(process_count, processes):
        queue = []; check = []
        check = copy.deepcopy(processes)

        # for index in range(len(check)):
        #     if check[index].Burst == 0:
        #         del check[index]

        for y in range(len(check)):
            small = check[0].Burst
            for x in range(len(check)):
                if check[x].Burst < small:
                    small = check[x].Burst
            index = Process.index(processes, "Burst", small)
            queue.append(processes[index])
            del check[Process.index(check, "Burst", small)]

        print("Job Queue:")
        for size in range(len(queue)):
            queue[size].process_info()

        ready = []; wait = copy.deepcopy(queue); clock = 0; current = None

        while clock >= 0:
            print("Time: %d" % clock)

            # Completion Check
            if len(wait) == 0 and len(ready) == 0:
                break

            # Move to Ready if Available / Delete Incorrect Processes
            for index in range(len(wait)):
                if index < len(wait):
                    if wait[index].Burst == 0:
                        print("Bad Process!")
                        del wait[index]

                    if wait[index].Arrival <= clock:
                        ready.append(copy.copy(wait[index]))
                        del wait[index]

            if len(ready) > 0:
                current = ready[0]

            # Kill Completed Processes
            for index in range(len(ready)):
                if index < len(ready):
                    if ready[index].Burst == 0:
                        print("\n---------Process %d Complete---------" % ready[index].PID)
                        update = Process.index(processes, "PID", ready[index].PID)
                        processes[update].End = clock
                        temp = processes[update]
                        temp.Wait = (temp.End - (temp.Arrival + temp.Burst))
                        del ready[index]

            # Assign Current Process
            for index in range(len(ready)):
                if current.Burst > ready[index].Burst:
                    current = ready[index]

            # User Info Output
            print("Working on PID: %d" % current.PID)
            current.process_info()
            current.Update_Burst(current.Burst-1)

            temp = Process.index(processes, "PID", current.PID)
            if processes[temp].Arrival != 0 and processes[temp].Start == 0:
                processes[temp].Start = clock

            clock += 1

        print("\n---------Final Time: %d---------" % (clock - 1))
        del ready; del check; del wait; Avg_Wait = 0
        for index in range(len(processes)):
            processes[index].process_info()
            Avg_Wait += processes[index].Wait
        Avg_Wait = (Avg_Wait/(len(processes)))
        print("---------Average Wait Time: %.2f---------" % Avg_Wait)


def main():
    info = open(sys.argv[1], 'r')  # Take command line arguments

    process_count = int(info.readline().strip())  # Read number of processes

    print("Number of processes: %d" % process_count)

    pid = []; arrival = []; burst = []

    for row in range(process_count):
        tasks = info.readline().strip()
        tasks = tasks.split()

        pid.append(int(tasks[0]))
        arrival.append(int(tasks[1]))
        burst.append(int(tasks[2]))

    processes = []
    for items in range(process_count):
        new_process = Process(pid[items], arrival[items], burst[items], 0, 0, 0)
        processes.append(new_process)
        # Process.process_info(Processes[items])

    if sys.argv[2].upper() == "FCFS":
        print("Wants to run FCFS")
        Process.fcfs(process_count, processes)
    elif sys.argv[2].upper() == "RR":
        print("Wants to run RR")
        Process.rr(process_count, processes, sys.argv[3])
    elif sys.argv[2].upper() == "SJF":
        print("Wants to run SJF")
        Process.sjf(process_count, processes)
    else:
        print("Improper Scheduling Algorithm, Exiting")
        exit(1)


main()
