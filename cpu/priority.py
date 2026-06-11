def get_priority(process):
    return process.priority

def priority(processes):
    processes.sort(key=get_priority)
    current_time = 0
    gantt = []

    for p in processes:
        if current_time < p.arrival:
            current_time = p.arrival

        p.response_time = current_time - p.arrival  # ← هنا

        p.waiting = current_time - p.arrival
        current_time += p.burst
        p.turnaround = current_time - p.arrival

        gantt.append((p.pid, p.burst, current_time - p.burst))

    return gantt