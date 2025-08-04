import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox

# === Setup Tkinter Window ===
root = Tk()
root.title("Weather Forecast Dashboard")
root.geometry("500x400")
root.configure(bg="#f0f2f5")

# === WeatherAPI Details ===
API_KEY = "0daf785eeb784735b19162250250408"
DAYS = 5

# === Function to Fetch and Plot Weather ===
def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Required", "Please enter a city name.")
        return

    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days={DAYS}&aqi=no&alerts=no"
    response = requests.get(url)

    if response.status_code != 200:
        messagebox.showerror("API Error", f"Could not fetch data: {response.text}")
        return

    data = response.json()
    forecast = data['forecast']['forecastday']

    df = pd.DataFrame({
        'Date': [day['date'] for day in forecast],
        'AvgTemp_C': [day['day']['avgtemp_c'] for day in forecast]
    })

    # === Plotting with Seaborn ===
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=df, x='Date', y='AvgTemp_C', marker='o', color='teal')
    plt.title(f"{city.title()} - {DAYS}-Day Average Temperature Forecast", fontsize=13)
    plt.xlabel("Date")
    plt.ylabel("Avg Temperature (°C)")
    plt.tight_layout()
    plt.savefig("forecast_plot.png")
    plt.show()

# === GUI Layout ===
Label(root, text="Weather Forecast", font=("Helvetica", 16, "bold"), bg="#f0f2f5", fg="#333").pack(pady=20)

frame = Frame(root, bg="#f0f2f5")
frame.pack()

Label(frame, text="Enter City Name:", font=("Helvetica", 12), bg="#f0f2f5").grid(row=0, column=0, padx=10, pady=10)
city_entry = Entry(frame, font=("Helvetica", 12), width=25)
city_entry.grid(row=0, column=1, padx=10, pady=10)

Button(root, text="Get Forecast", font=("Helvetica", 12), command=get_weather, bg="#007acc", fg="white", width=20).pack(pady=20)

Label(root, text="Developed with WeatherAPI.com", font=("Helvetica", 10), bg="#f0f2f5", fg="#777").pack(side=BOTTOM, pady=10)

# === Main Loop ===
root.mainloop()
