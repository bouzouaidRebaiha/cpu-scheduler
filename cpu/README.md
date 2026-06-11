# 🌸 CPU Scheduler Simulator

A desktop application that simulates and compares CPU scheduling algorithms with an animated GUI built with Python and CustomTkinter.

---

## ✨ Supported Algorithms

| Algorithm | Description |
|---|---|
| **FCFS** | First Come First Served |
| **SJF** | Shortest Job First (Non-preemptive) |
| **SRTF** | Shortest Remaining Time First (Preemptive SJF) |
| **Priority** | Priority-based Scheduling |
| **RR** | Round Robin with configurable time quantum |

---

## 🖥️ Features

- Input any number of processes with custom PID, Arrival Time, Burst Time, and Priority
- Animated **Gantt Chart** with color-coded processes
- Per-process results: Waiting Time, Turnaround Time, Response Time
- **Algorithm Comparison Table** — runs all algorithms on the same input automatically
- Smart recommendation for the best algorithm based on your data 

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install customtkinter Pillow
```

### Run
```bash
python main.py
```

---

## 📁 Project Structure

```
cpu-scheduler/
├── main.py          # Main GUI application
├── process.py       # Process class definition
├── fcfs.py          # FCFS algorithm
├── sjf.py           # SJF algorithm
├── priority.py      # Priority Scheduling algorithm
├── rr.py            # Round Robin algorithm

```

---

## 📊 Output

After entering processes and selecting an algorithm, the app displays:
- Animated Gantt Chart
- Results table per process
- Average Waiting, Turnaround, and Response Times
- CPU Utilization %
- Side-by-side comparison of all algorithms

---

## 🛠️ Requirements

- Python 3.x
- customtkinter
- Pillow


