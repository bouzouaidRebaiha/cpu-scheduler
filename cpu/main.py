import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import copy
import math
import random

from process     import Process
from fcfs        import fcfs
from sjf         import sjf
from priority    import priority
from rr import rr


# ── Theme ──────────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BG         = "#fff0f5"
PINK       = "#e75480"
LIGHT_PINK = "#ffd6e7"
FG         = "#4a0030"
COLORS     = ["#ffadc7", "#ffd6e7", "#c9b8ff", "#b8e0ff", "#c8f7c5", "#ffe4b5"]

# ── Root ───────────────────────────────────────────────
root = ctk.CTk()
root.title("🌸 CPU Scheduler 🌸")
root.geometry("980x900")
root.configure(fg_color=BG)

# ── Background Canvas ──────────────────────────────────
bg_canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

def draw_flower(canvas, cx, cy, size, color):
    for i in range(6):
        angle = math.radians(i * 60)
        px = cx + size * math.cos(angle)
        py = cy + size * math.sin(angle)
        canvas.create_oval(px - size*0.5, py - size*0.5,
                           px + size*0.5, py + size*0.5,
                           fill=color, outline="")
    canvas.create_oval(cx - size*0.4, cy - size*0.4,
                       cx + size*0.4, cy + size*0.4,
                       fill="#fff9c4", outline="")

for _ in range(18):
    draw_flower(bg_canvas,
                random.randint(20, 960),
                random.randint(20, 880),
                random.randint(8, 18),
                random.choice(["#ffb6c1","#ff69b4","#dda0dd","#e6e6fa","#ffc0cb"]))

sparkles      = [[random.randint(0,980), random.randint(0,900),
                  random.uniform(2,4), random.uniform(0.3,0.8)] for _ in range(40)]
sparkle_items = [bg_canvas.create_oval(s[0], s[1], s[0]+s[2], s[1]+s[2],
                  fill="#ffb6c1", outline="") for s in sparkles]

def animate():
    for i, s in enumerate(sparkles):
        s[1] += s[3]
        if s[1] > 900:
            s[1] = 0
            s[0] = random.randint(0, 980)
        bg_canvas.coords(sparkle_items[i], s[0], s[1], s[0]+s[2], s[1]+s[2])
    root.after(30, animate)

animate()

# ── Images ────────────────────────────────────────────
try:
    gojo_img   = Image.open("cute_gojo.jpg").resize((250, 250))
    gojo_photo = ImageTk.PhotoImage(gojo_img)
    bg_canvas.create_image(980, 125, image=gojo_photo, anchor="e")
except Exception:
    pass

try:
    poster_img   = Image.open("poster.jpg").resize((250, 150))
    poster_photo = ImageTk.PhotoImage(poster_img)
    bg_canvas.create_image(130, 850, image=poster_photo, anchor="center")
except Exception:
    pass

# ── Scrollable Main Frame ──────────────────────────────
main_scroll = ctk.CTkScrollableFrame(root, fg_color="transparent", width=940)
main_scroll.pack(fill="both", expand=True, padx=10, pady=5)

# ── Title ──────────────────────────────────────────────
ctk.CTkLabel(main_scroll, text="🌸 CPU Scheduler 🌸",
             font=ctk.CTkFont(size=26, weight="bold"),
             text_color=PINK, fg_color="transparent").pack(pady=15)

# ── Algorithm Selection ────────────────────────────────
algo_var   = ctk.StringVar(value="FCFS")
algo_frame = ctk.CTkFrame(main_scroll, fg_color=LIGHT_PINK, corner_radius=20)
algo_frame.pack(pady=5, padx=20)

ctk.CTkLabel(algo_frame, text="Algorithm:",
             font=ctk.CTkFont(size=13),
             text_color=FG, fg_color="transparent").pack(side="left", padx=10)

for algo_name in ["FCFS", "SJF", "Priority", "RR", "SRTF"]:
    ctk.CTkRadioButton(algo_frame, text=algo_name,
                       variable=algo_var, value=algo_name,
                       font=ctk.CTkFont(size=13, weight="bold"),
                       text_color=FG, fg_color=PINK,
                       hover_color=LIGHT_PINK).pack(side="left", padx=8, pady=8)

ctk.CTkLabel(algo_frame, text="Quantum:",
             font=ctk.CTkFont(size=13),
             text_color=FG, fg_color="transparent").pack(side="left", padx=5)
quantum_entry = ctk.CTkEntry(algo_frame, width=50,
                              font=ctk.CTkFont(size=13),
                              fg_color=LIGHT_PINK, text_color=FG,
                              border_color=PINK, corner_radius=10)
quantum_entry.pack(side="left", padx=5, pady=8)

# ── Input ──────────────────────────────────────────────
input_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
input_frame.pack(pady=8)

ctk.CTkLabel(input_frame, text="Number of Processes:",
             font=ctk.CTkFont(size=13),
             text_color=FG, fg_color="transparent").grid(row=0, column=0, padx=5)
n_entry = ctk.CTkEntry(input_frame, width=60,
                        font=ctk.CTkFont(size=13),
                        fg_color=LIGHT_PINK, text_color=FG,
                        border_color=PINK, corner_radius=10)
n_entry.grid(row=0, column=1, padx=5)

table_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
table_frame.pack(pady=5)
entries   = []
processes = []

def create_table():
    for w in table_frame.winfo_children():
        w.destroy()
    entries.clear()
    n = int(n_entry.get())
    for j, h in enumerate(["PID", "Arrival", "Burst", "Priority"]):
        ctk.CTkLabel(table_frame, text=h,
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=PINK, fg_color=LIGHT_PINK,
                     corner_radius=8, width=100).grid(row=0, column=j, padx=4, pady=3)
    for i in range(n):
        row_entries = []
        for j in range(4):
            e = ctk.CTkEntry(table_frame, width=100,
                             font=ctk.CTkFont(size=12),
                             fg_color="#fff0f5", text_color=FG,
                             border_color=PINK, corner_radius=8)
            e.grid(row=i+1, column=j, padx=4, pady=4)
            row_entries.append(e)
        entries.append(row_entries)

ctk.CTkButton(input_frame, text="🌸 Create Table",
              font=ctk.CTkFont(size=13, weight="bold"),
              fg_color=PINK, hover_color="#c71585",
              text_color="white", corner_radius=15,
              command=create_table).grid(row=0, column=2, padx=10)

# ── Gantt Canvas ───────────────────────────────────────
gantt_canvas = tk.Canvas(main_scroll, bg="#fff0f5", height=120, width=900,
                          highlightthickness=2, highlightbackground=PINK)
gantt_canvas.pack(pady=10, padx=20)

# ── Results Frame ──────────────────────────────────────
result_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
result_frame.pack(pady=5)

# ── Stats Frame ────────────────────────────────────────
stats_frame = ctk.CTkFrame(main_scroll, fg_color=LIGHT_PINK, corner_radius=20)
stats_frame.pack(pady=8, padx=20, fill="x")

# ── Helper Functions ───────────────────────────────────
def clone(p):
    new_p              = copy.copy(p)
    new_p.remaining    = p.burst
    new_p.waiting      = 0
    new_p.turnaround   = 0
    new_p.completion   = 0
    new_p.response_time = -1
    return new_p

def reset_and_run(algo_name, original_processes):
    procs = [clone(p) for p in original_processes]
    try:
        q = int(quantum_entry.get()) if quantum_entry.get() else 2
    except ValueError:
        q = 2
    if algo_name == "FCFS":
        fcfs(procs)
    elif algo_name == "SJF":
        sjf(procs)
    elif algo_name == "Priority":
        priority(procs)
    elif algo_name == "RR":
        rr(procs, q)
    return procs

def recommend_algorithm(procs):
    n                = len(procs)
    bursts           = [p.burst    for p in procs]
    prios            = [p.priority for p in procs]
    avg_burst        = sum(bursts) / n
    burst_range      = max(bursts) - min(bursts)
    priority_variance = max(prios) - min(prios)

    if priority_variance >= 3:
        return "Priority", f"Priorities vary widely (range {priority_variance})"
    elif burst_range <= 2:
        return "FCFS",     f"Burst times are similar (range {burst_range})"
    elif avg_burst <= 5:
        return "SJF",      f"Low average burst ({avg_burst:.1f})"
    elif n >= 4 and avg_burst >= 6:
        return "RR",       f"Many processes ({n}) with long bursts → interactive"
    else:
        return "SJF",      "General case favours SJF"

# ── Statistics ─────────────────────────────────────────
def show_statistics(gantt_data):
    for w in stats_frame.winfo_children():
        w.destroy()

    if not processes:
        return

    n              = len(processes)
    avg_waiting    = sum(p.waiting       for p in processes) / n
    avg_turnaround = sum(p.turnaround    for p in processes) / n
    avg_response   = sum(p.response_time for p in processes) / n
    total_time     = max(p.completion    for p in processes)
    busy_time      = sum(p.burst         for p in processes)
    throughput     = n / total_time
    cpu_util       = (busy_time / total_time) * 100

    ctk.CTkLabel(stats_frame, text="📊 Statistics",
                 font=ctk.CTkFont(size=15, weight="bold"),
                 text_color=PINK, fg_color="transparent").pack(pady=(10,5))

    # ── Metric Cards ──
    cards_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
    cards_frame.pack(padx=15, pady=5)

    metrics = [
        ("⏳ Avg Waiting",     f"{avg_waiting:.2f}"),
        ("🔄 Avg Turnaround",  f"{avg_turnaround:.2f}"),
        ("⚡ Avg Response",    f"{avg_response:.2f}"),
        ("📈 Throughput",      f"{throughput:.3f} p/u"),
        ("💻 CPU Utilization", f"{cpu_util:.1f}%"),
    ]

    for col, (label, value) in enumerate(metrics):
        box = ctk.CTkFrame(cards_frame, fg_color="#fff0f5",
                           corner_radius=12, border_color=PINK, border_width=1)
        box.grid(row=0, column=col, padx=8, pady=5, ipadx=8, ipady=5)
        ctk.CTkLabel(box, text=label,
                     font=ctk.CTkFont(size=11),
                     text_color=FG, fg_color="transparent").pack()
        ctk.CTkLabel(box, text=value,
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=PINK, fg_color="transparent").pack()

   # ── Comparison Table ──
    ctk.CTkLabel(stats_frame, text="🌸 Algorithm Comparison",
                 font=ctk.CTkFont(size=14, weight="bold"),
                 text_color=PINK, fg_color="transparent").pack(pady=(12,6))

    comp_outer = ctk.CTkFrame(stats_frame, fg_color="#ffe4f0",
                               corner_radius=20, border_color=PINK, border_width=2)
    comp_outer.pack(padx=20, pady=4, fill="x")

    comp_table = ctk.CTkFrame(comp_outer, fg_color="transparent")
    comp_table.pack(padx=12, pady=10)

    # ── Header ──
    header_icons = ["🎀", "⏳", "🔄", "⚡", "📈", "💻"]
    headers      = ["Algorithm", "Avg Waiting", "Avg Turnaround",
                    "Avg Response", "Throughput", "CPU Util%"]

    for col, (icon, h) in enumerate(zip(header_icons, headers)):
        cell = ctk.CTkFrame(comp_table, fg_color=PINK, corner_radius=10)
        cell.grid(row=0, column=col, padx=4, pady=4, ipadx=6, ipady=4)
        ctk.CTkLabel(cell, text=f"{icon} {h}",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="white", fg_color="transparent").pack(padx=6)

    best_algo, reason = recommend_algorithm(processes)

    row_colors = ["#fff0f5", "#fde8f0"]   # تبادل ألوان الصفوف

    for row_i, name in enumerate(["FCFS", "SJF", "Priority", "RR", "SRTF"]):
        try:
            temp_procs = reset_and_run(name, processes)
            aw  = sum(p.waiting        for p in temp_procs) / n
            at  = sum(p.turnaround     for p in temp_procs) / n
            ar  = sum(p.response_time  for p in temp_procs) / n
            tt  = max(p.completion     for p in temp_procs)
            bt  = sum(p.burst          for p in temp_procs)
            tp  = n / tt
            cpu = (bt / tt) * 100

            is_best  = (name == best_algo)
            bg_color = "#ffc0d9" if is_best else row_colors[row_i % 2]
            prefix   = "🏆 "    if is_best else "   "

            values = [f"{prefix}{name}",
                      f"{aw:.2f}", f"{at:.2f}",
                      f"{ar:.2f}", f"{tp:.3f}", f"{cpu:.1f}%"]

            for col, val in enumerate(values):
                cell = ctk.CTkFrame(comp_table, fg_color=bg_color,
                                    corner_radius=8)
                cell.grid(row=row_i+1, column=col, padx=4, pady=3,
                          ipadx=6, ipady=5)
                ctk.CTkLabel(cell, text=val,
                             font=ctk.CTkFont(size=11,
                                              weight="bold" if is_best else "normal"),
                             text_color=PINK if is_best else FG,
                             fg_color="transparent").pack(padx=8)
        except Exception:
            pass

    # ── Recommendation Badge ──
    badge_frame = ctk.CTkFrame(stats_frame, fg_color=PINK, corner_radius=15)
    badge_frame.pack(pady=(8,4), padx=20)
    ctk.CTkLabel(badge_frame,
                 text=f"🏆  Best Algorithm: {best_algo}",
                 font=ctk.CTkFont(size=13, weight="bold"),
                 text_color="white", fg_color="transparent").pack(
                     padx=20, pady=6)

    reason_frame = ctk.CTkFrame(stats_frame, fg_color="#fff0f5",
                                 corner_radius=10, border_color=PINK, border_width=1)
    reason_frame.pack(pady=(0,12), padx=20)
    ctk.CTkLabel(reason_frame,
                 text=f"💡  {reason}",
                 font=ctk.CTkFont(size=11),
                 text_color=FG, fg_color="transparent").pack(padx=15, pady=6)

# ── Run Scheduler ──────────────────────────────────────
def run_scheduler():
    gantt_canvas.delete("all")
    for w in result_frame.winfo_children():
        w.destroy()
    for w in stats_frame.winfo_children():
        w.destroy()
    processes.clear()

    for row in entries:
        pid          = int(row[0].get())
        arrival      = int(row[1].get())
        burst        = int(row[2].get())
        priority_val = int(row[3].get())
        processes.append(Process(pid, arrival, burst, priority_val))

    for p in processes:
        p.remaining     = p.burst
        p.response_time = -1

    algo = algo_var.get()
    if algo == "FCFS":
        gantt_data = fcfs(processes)
    elif algo == "SJF":
        gantt_data = sjf(processes)
    elif algo == "Priority":
        gantt_data = priority(processes)
    else:
        quantum    = int(quantum_entry.get())
        gantt_data = rr(processes, quantum)

    # ── Results Table ──
    for j, h in enumerate(["PID", "Arrival", "Burst",
                             "Waiting", "Turnaround", "Response"]):
        ctk.CTkLabel(result_frame, text=h,
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=PINK, fg_color=LIGHT_PINK,
                     corner_radius=8, width=110).grid(
                         row=0, column=j, padx=3, pady=3)

    for i, p in enumerate(processes):
        for j, v in enumerate([p.pid, p.arrival, p.burst,
                                p.waiting, p.turnaround, p.response_time]):
            ctk.CTkLabel(result_frame, text=str(v),
                         font=ctk.CTkFont(size=12),
                         text_color=FG, fg_color="#ffe4f0",
                         corner_radius=8, width=110).grid(
                             row=i+1, column=j, padx=3, pady=3)

    # ── Gantt Chart ──
    scale = 28
    x_pos = [10]
    y     = 20

    def draw_block(i):
        if i >= len(gantt_data):
            _, burst, start = gantt_data[-1]
            gantt_canvas.create_text(x_pos[0], y+75,
                                      text=str(start + burst),
                                      fill=PINK, font=("Arial", 9, "bold"))
            show_statistics(gantt_data)
            return

        pid, burst, start = gantt_data[i]

        prev_end = 0
        if i > 0:
            _, pb, ps = gantt_data[i-1]
            prev_end  = ps + pb

        if start > prev_end:
            idle_w = (start - prev_end) * scale
            gantt_canvas.create_rectangle(x_pos[0], y,
                                           x_pos[0]+idle_w, y+60,
                                           fill="#f0f0f0", outline=PINK, width=1)
            gantt_canvas.create_text(x_pos[0]+idle_w//2, y+30,
                                      text="idle", fill="#aaa",
                                      font=("Arial", 10, "italic"))
            gantt_canvas.create_text(x_pos[0], y+75,
                                      text=str(prev_end),
                                      fill=PINK, font=("Arial", 9, "bold"))
            x_pos[0] += idle_w

        width = burst * scale
        color = COLORS[i % len(COLORS)]
        gantt_canvas.create_rectangle(x_pos[0], y,
                                       x_pos[0]+width, y+60,
                                       fill=color, outline=PINK, width=2)
        gantt_canvas.create_text(x_pos[0]+width//2, y+30,
                                  text=f"🌸 P{pid}", fill=FG,
                                  font=("Arial", 12, "bold"))
        gantt_canvas.create_text(x_pos[0], y+75,
                                  text=str(start),
                                  fill=PINK, font=("Arial", 9, "bold"))
        x_pos[0] += width
        root.after(800, draw_block, i+1)

    root.after(300, draw_block, 0)

# ── Run Button ─────────────────────────────────────────
ctk.CTkButton(main_scroll, text="🌸 Run Scheduler 🌸",
              font=ctk.CTkFont(size=15, weight="bold"),
              fg_color=PINK, hover_color="#c71585",
              text_color="white", corner_radius=20,
              width=200, height=45,
              command=run_scheduler).pack(pady=8)

root.mainloop()