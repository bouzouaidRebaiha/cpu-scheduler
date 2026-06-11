from collections import deque

def get_arrival(process):
    return process.arrival

def rr(processes, quantum):
    processes.sort(key=get_arrival)
    current_time = 0
    gantt = []
    ready_queue = deque()
    i = 0

    while ready_queue or i < len(processes):
        while i < len(processes) and processes[i].arrival <= current_time:
            ready_queue.append(processes[i])
            i += 1

        if not ready_queue:
            current_time = processes[i].arrival
            continue

        p = ready_queue.popleft()

        if p.response_time == -1:              # ← هنا
            p.response_time = current_time - p.arrival

        execution_time = min(p.remaining, quantum)
        gantt.append((p.pid, execution_time, current_time))
        current_time += execution_time
        p.remaining -= execution_time

        while i < len(processes) and processes[i].arrival <= current_time:
            ready_queue.append(processes[i])
            i += 1

        if p.remaining == 0:
            p.completion = current_time
            p.turnaround = p.completion - p.arrival
            p.waiting = p.turnaround - p.burst
        else:
            ready_queue.append(p)

    return gantt