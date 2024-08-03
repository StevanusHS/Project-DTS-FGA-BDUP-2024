import tkinter as tk
from tkinter import messagebox
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Menghubungkan ke database MySQL dan mengambil data dari tabel marriage_data
def fetch_data():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='dts'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT year, marriage_count, age_range, marriages_in_age_range FROM marriage_data")
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Membuat grafik jumlah pernikahan per tahun dari database yang diambil
def show_yearly_visualization():
    data = fetch_data()
    if not data:
        return

    years = sorted(set(row[0] for row in data))
    yearly_counts = {year: 0 for year in years}

    for row in data:
        yearly_counts[row[0]] += row[1]

    fig, ax = plt.subplots()
    ax.plot(years, [yearly_counts[year] for year in years], marker='o', linestyle='-', color='b')
    ax.set_title('Angka Pernikahan di Indonesia dari Tahun 2000 hingga 2024')
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Jumlah Pernikahan')
    ax.grid(True)

    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    yearly_btn.config(text="Close Yearly Visualization", command=close_visualization)

# Membuat grafik jumlah pernikahan berdasarkan rentang usia dari database yang diambil
def show_age_range_visualization():
    data = fetch_data()
    if not data:
        return

    age_ranges = sorted(set(row[2] for row in data))
    years = sorted(set(row[0] for row in data))
    age_range_counts = {age_range: [0] * len(years) for age_range in age_ranges}

    for row in data:
        year_index = years.index(row[0])
        age_range_counts[row[2]][year_index] += row[3]

    fig, ax = plt.subplots()
    for age_range in age_ranges:
        ax.plot(years, age_range_counts[age_range], marker='o', linestyle='-', label=age_range)

    ax.set_title('Pernikahan Berdasarkan Rentang Usia dari Tahun 2000 hingga 2024')
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Jumlah Pernikahan')
    ax.grid(True)
    ax.legend()

    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    age_range_btn.config(text="Close Age Range Visualization", command=close_visualization)

# Menutup visualisasi yang sedang ditampilkan dan mengembalikan tombol ke fungsinya semula untuk menampilkan visualisasi
def close_visualization():
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()
        canvas = None

    yearly_btn.config(text="Show Yearly Visualization", command=show_yearly_visualization)
    age_range_btn.config(text="Show Age Range Visualization", command=show_age_range_visualization)

# Menghapus visualisasi yang sedang ditampilkan tanpa menutup aplikasi, dan juga mengembalikan tombol ke default
def clear_visualization():
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()
        canvas = None

    yearly_btn.config(text="Show Yearly Visualization", command=show_yearly_visualization)
    age_range_btn.config(text="Show Age Range Visualization", command=show_age_range_visualization)

# Mengatur tampilan antarmuka pengguna program
root = tk.Tk()
root.title("Data Visualization Program")

canvas = None

title_label = tk.Label(root, text="Selamat datang di program visualisasi data", font=("Arial", 16))
title_label.pack(pady=10)


data_frame = tk.Frame(root)
data_frame.pack(pady=5)

data_label = tk.Label(data_frame, text="Data Name: ")
data_label.pack(side=tk.LEFT)

data_entry = tk.Entry(data_frame)
data_entry.insert(0, " ")
data_entry.pack(side=tk.LEFT, padx=5)


button_frame = tk.Frame(root)
button_frame.pack(pady=10)

yearly_btn = tk.Button(button_frame, text="Show Yearly Visualization", command=show_yearly_visualization)
yearly_btn.pack(side=tk.LEFT, padx=10)

age_range_btn = tk.Button(button_frame, text="Show Age Range Visualization", command=show_age_range_visualization)
age_range_btn.pack(side=tk.LEFT, padx=10)

clear_btn = tk.Button(root, text="Clear", command=clear_visualization)
clear_btn.pack(pady=10)

root.mainloop()
