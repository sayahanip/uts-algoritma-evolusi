import tkinter as tk
from tkinter import scrolledtext, messagebox
import math

def sigmoid(v):
    return 1 / (1 + math.exp(-v))

def bin_to_int(bits):
    return int("".join(str(int(b)) for b in bits), 2)

def str_to_bits(s):
    return [int(x) for x in s]

# Fitness sesuai soal
def f(x):
    return (x - 5)**2 + 10


# =====================================================
#                  PSO CORE FUNCTION
# =====================================================
def run_pso():
    try:
        # Ambil input dari GUI
        w = float(entry_w.get())
        c1 = float(entry_c1.get())
        c2 = float(entry_c2.get())
        iterasi_total = int(entry_iter.get())

        # r1, r2, random check (dipisah koma)
        r1 = [float(x) for x in entry_r1.get().split(",")]
        r2 = [float(x) for x in entry_r2.get().split(",")]
        random_check = [float(x) for x in entry_rc.get().split(",")]

        # partikel (masukkan biner per baris)
        particle_lines = text_particles.get("1.0", tk.END).strip().split("\n")
        particles = [str_to_bits(line.replace(" ", "")) for line in particle_lines]
        
        vel = [0.0 for _ in particles]

        output = ""

        # hitung pBest awal
        pbest = [bin_to_int(p) for p in particles]
        gbest = min(pbest, key=lambda x: f(x))

        output += "==== Iterasi 0 (Awal) ====\n"
        for i, p in enumerate(pbest):
            output += f"Partikel {i+1}: x={p}, fitness={f(p)}\n"
        output += f"gBest = {gbest} | fitness = {f(gbest)}\n\n"


        # =====================================================
        #                  PROSES ITERASI
        # =====================================================
        for it in range(1, iterasi_total + 1):
            output += f"==== Iterasi {it} ====\n"

            for i in range(len(particles)):
                x_now = bin_to_int(particles[i])
                p_best = pbest[i]

                vel[i] = (
                    w * vel[i]
                    + c1 * r1[i] * (p_best - x_now)
                    + c2 * r2[i] * (gbest - x_now)
                )

                # update posisi binary
                new_bits = []
                s = sigmoid(vel[i])
                for chk in random_check:
                    new_bits.append(1 if s > chk else 0)

                particles[i] = new_bits
                x_new = bin_to_int(particles[i])

                # update pBest
                if f(x_new) < f(p_best):
                    pbest[i] = x_new

                output += (
                    f"Partikel {i+1}: v={vel[i]:.4f}, "
                    f"x={x_new}, fitness={f(x_new)}\n"
                )

            gbest = min(pbest, key=lambda x: f(x))
            output += f"gBest = {gbest}, fitness = {f(gbest)}\n\n"

        # tampilkan ke GUI
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, output)

    except Exception as e:
        messagebox.showerror("Error", f"Input tidak valid!\n{str(e)}")



# =====================================================
#                     SECTION
# =====================================================
root = tk.Tk()
root.title("PSO Input – Kalkulator PSO")
root.geometry("750x680")


# ========== Frame Input ==========
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="w:").grid(row=0, column=0)
entry_w = tk.Entry(frame, width=10)
entry_w.insert(0, "0.5")
entry_w.grid(row=0, column=1)

tk.Label(frame, text="c1:").grid(row=1, column=0)
entry_c1 = tk.Entry(frame, width=10)
entry_c1.insert(0, "1")
entry_c1.grid(row=1, column=1)

tk.Label(frame, text="c2:").grid(row=2, column=0)
entry_c2 = tk.Entry(frame, width=10)
entry_c2.insert(0, "1")
entry_c2.grid(row=2, column=1)

tk.Label(frame, text="Iterasi:").grid(row=3, column=0)
entry_iter = tk.Entry(frame, width=10)
entry_iter.insert(0, "2")
entry_iter.grid(row=3, column=1)

# ======================
# R1, R2, Random Check
# ======================
tk.Label(frame, text="r1 (pisahkan koma):").grid(row=0, column=2, padx=10)
entry_r1 = tk.Entry(frame, width=20)
entry_r1.insert(0, "0.2,0.4,0.6")
entry_r1.grid(row=0, column=3)

tk.Label(frame, text="r2 (pisahkan koma):").grid(row=1, column=2)
entry_r2 = tk.Entry(frame, width=20)
entry_r2.insert(0, "0.9,0.7,0.5")
entry_r2.grid(row=1, column=3)

tk.Label(frame, text="random check:").grid(row=2, column=2)
entry_rc = tk.Entry(frame, width=20)
entry_rc.insert(0, "0.7,0.2,0.8")
entry_rc.grid(row=2, column=3)


# =======================
# Input partikel
# =======================
tk.Label(root, text="Masukkan Posisi Partikel (biner per baris):").pack()

text_particles = scrolledtext.ScrolledText(root, width=40, height=5)
text_particles.insert(tk.END, "0010\n1000\n1110")
text_particles.pack(pady=5)


# =======================
# Tombol Run
# =======================
btn_run = tk.Button(root, text="JALANKAN PSO", font=("Arial", 12, "bold"),
                    command=run_pso, width=20, bg="#5cb85c", fg="white")
btn_run.pack(pady=10)


# =======================
# Output
# =======================
text_output = scrolledtext.ScrolledText(root, width=80, height=22, font=("Consolas", 10))
text_output.pack(pady=10)

root.mainloop()
