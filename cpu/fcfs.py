def fcfs(processes):
    processes.sort(key=lambda p: p.arrival)
    current_time = 0
    gantt = []

    for p in processes:
        if current_time < p.arrival:
            current_time = p.arrival

        p.response_time = current_time - p.arrival
        p.waiting       = current_time - p.arrival
        current_time   += p.burst
        p.completion    = current_time
        p.turnaround    = current_time - p.arrival

        gantt.append((p.pid, p.burst, current_time - p.burst))

    return gantt