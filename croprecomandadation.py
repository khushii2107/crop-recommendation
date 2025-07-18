import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import threading
import time

# Global theme
is_dark = False
last_fig = None

# Load dataset
def load_data():
    return pd.read_csv('crop_data_sample.csv', parse_dates=['date'])

# Crop Recommendation
def recommend_crop():
    def task():
        try:
            loading_label.config(text="Predicting...")
            predict_btn.config(state=tk.DISABLED)
            time.sleep(1.5)

            temp = float(temperature_entry.get())
            humidity = float(humidity_entry.get())
            moisture = float(soil_moisture_entry.get())

            data = load_data()
            distances = ((data['temperature'] - temp)**2 +
                         (data['humidity'] - humidity)**2 +
                         (data['soil_moisture'] - moisture)**2)**0.5
            closest = distances.idxmin()
            crop = data.loc[closest, 'crop_recommendation']

            result_text_box.delete("1.0", tk.END)
            result_text_box.insert(tk.END, f"Recommended Crop: {crop}")
            result_text_box.tag_configure("center", justify="center")
            result_text_box.tag_add("center", "1.0", "end")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
        finally:
            predict_btn.config(state=tk.NORMAL)
            loading_label.config(text="")

    threading.Thread(target=task).start()

# Plot Graph on Tab
def plot_on_tab(tab, column, title, color):
    global last_fig
    for widget in tab.winfo_children():
        widget.destroy()

    data = load_data()
    fig, ax = plt.subplots(figsize=(6, 2.4))
    ax.plot(data['date'], data[column], color=color)

    ax.set_title(title, fontsize=10)
    ax.set_xlabel("Date", fontsize=9)
    ax.set_ylabel(column.capitalize(), fontsize=9)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    fig.autofmt_xdate(rotation=45)
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()

    last_fig = fig
    canvas = FigureCanvasTkAgg(fig, master=tab)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Export Graph
def export_graph():
    if last_fig:
        file = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG Image", "*.png"), ("PDF File", "*.pdf")])
        if file:
            last_fig.savefig(file)
            messagebox.showinfo("Saved", "Graph exported successfully!")

# Toggle Light/Dark Theme
def toggle_theme():
    global is_dark
    is_dark = not is_dark
    bg = "#212529" if is_dark else "#f8f9fa"
    fg = "white" if is_dark else "black"
    frame.config(bg=bg)
    for widget in frame.winfo_children():
        if isinstance(widget, (tk.Label, tk.Entry, tk.Button, tk.Text)):
            widget.config(bg=bg, fg=fg)

# GUI Setup
def create_gui():
    global graph_tabs, temperature_entry, humidity_entry, soil_moisture_entry
    global result_text_box, predict_btn, loading_label, frame

    window = tk.Tk()
    window.title("Crop Recommendation System")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")
    window.resizable(False, False)

    # Background
    bg_img = Image.open("background.jpg").resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_img)
    canvas = tk.Canvas(window, width=screen_width, height=screen_height)
    canvas.pack()
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Main Frame
    frame_w, frame_h = 720, 820
    frame = tk.Frame(canvas, bg='#f8f9fa', bd=2, highlightbackground="gray", highlightthickness=1)
    frame.place(x=(screen_width - frame_w)//2, y=(screen_height - frame_h)//2,
                width=frame_w, height=frame_h)
    frame.pack_propagate(False)

    # Title
    tk.Label(frame, text="Crop Recommendation System", bg='#f8f9fa',
             font=("Arial", 20, "bold")).pack(pady=10)

    # Input Fields
    def create_input(label):
        tk.Label(frame, text=label, bg='#f8f9fa', font=("Arial", 12, "bold")).pack(pady=4)
        entry = tk.Entry(frame, font=("Arial", 11), relief=tk.FLAT, bd=2,
                         highlightthickness=1, highlightbackground="#ced4da")
        entry.pack(pady=4, ipady=4, ipadx=2)
        return entry

    temperature_entry = create_input("Temperature (°C)")
    humidity_entry = create_input("Humidity (%)")
    soil_moisture_entry = create_input("Soil Moisture (%)")

    # Buttons
    predict_btn = tk.Button(frame, text="Predict Suitable Crop", bg="#4CAF50", fg="white",
                            font=("Arial", 11, "bold"), relief="flat", command=recommend_crop)
    predict_btn.pack(pady=10)

    loading_label = tk.Label(frame, text="", bg='#f8f9fa', font=("Arial", 11), fg="gray")
    loading_label.pack()

    result_text_box = tk.Text(frame, height=2, width=60, font=("Arial", 12), bg="#e9ecef", bd=0)
    result_text_box.pack(pady=5)

    # Tabs for Graphs
    tk.Label(frame, text="Data Trend Visualizations", bg='#f8f9fa',
             font=("Arial", 14, "bold")).pack(pady=10)

    graph_tabs = ttk.Notebook(frame)
    temp_tab = tk.Frame(graph_tabs, bg='white')
    humidity_tab = tk.Frame(graph_tabs, bg='white')
    soil_tab = tk.Frame(graph_tabs, bg='white')
    graph_tabs.add(temp_tab, text="Temperature")
    graph_tabs.add(humidity_tab, text="Humidity")
    graph_tabs.add(soil_tab, text="Soil Moisture")
    graph_tabs.pack(fill=tk.BOTH, expand=False, padx=10, pady=5, ipadx=10, ipady=6)

    # Load all graphs
    plot_on_tab(temp_tab, 'temperature', 'Temperature Over Time', '#007ACC')
    plot_on_tab(humidity_tab, 'humidity', 'Humidity Over Time', '#28A745')
    plot_on_tab(soil_tab, 'soil_moisture', 'Soil Moisture Over Time', '#B34D4D')

    # Export + Theme Buttons
    tk.Button(frame, text="Download Graph", font=("Arial", 11), bg="#6c757d", fg="white",
              command=export_graph).pack(pady=(10, 4))
    tk.Button(frame, text="Toggle Theme", font=("Arial", 11), bg="#343a40", fg="white",
              command=toggle_theme).pack(pady=(4, 10))

    window.mainloop()

if __name__ == "__main__":
    create_gui()
