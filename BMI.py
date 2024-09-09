import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import random

# Spoonacular API configuration
API_KEY = "66a3ac5a78884af3b3e02e5e4379a370"  # Replace with your own API key
API_URL = "https://api.spoonacular.com/mealplanner/generate"

# Data storage for progress
bmi_progress = {}

# Function to calculate BMI
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get()) / 100  # Convert height from cm to meters
        bmi = round(weight / (height ** 2), 2)
        result_label.config(text=f"Your BMI is: {bmi}")

        # Save current date and BMI to progress data
        current_date = datetime.now().strftime("%Y-%m-%d")
        bmi_progress[current_date] = bmi

        # Show suggestions based on aim
        suggest_food_exercise(bmi, aim_combo.get())

    except ValueError:
        ttk.Messagebox.show_error("Input Error", "Please enter valid numbers for weight and height.")

# Function to fetch food recommendations from Spoonacular API
def fetch_food_suggestions(goal):
    try:
        if goal == "Gain Weight":
            target_calories = 3000
        elif goal == "Gain Muscle":
            target_calories = 2500
        elif goal == "Reduce Weight":
            target_calories = 1500
        else:
            target_calories = 2000

        response = requests.get(API_URL, params={
            'apiKey': API_KEY,
            'targetCalories': target_calories,
            'timeFrame': 'day'
        })

        if response.status_code == 200:
            meal_data = response.json()
            meals = meal_data.get("meals", [])
            food_recommendation = f"Recommended Meals: " + ", ".join([meal["title"] for meal in meals])
            return food_recommendation
        else:
            return "Error fetching food suggestions"

    except Exception as e:
        return f"Error fetching data: {str(e)}"

# Placeholder AI logic for suggesting exercise
def suggest_food_exercise(bmi, aim):
    food_suggestion = fetch_food_suggestions(aim)

    if aim == "Gain Weight":
        exercise = ["Strength Training", "Weight Lifting"]
    elif aim == "Gain Muscle":
        exercise = ["Bodybuilding", "Resistance Training"]
    elif aim == "Reduce Weight":
        exercise = ["Cardio", "HIIT"]
    else:
        exercise = ["General Fitness"]

    exercise_recommendation = f"Recommended Exercise: {', '.join(random.sample(exercise, len(exercise)))}"

    suggestion_label.config(text=f"{food_suggestion}\n{exercise_recommendation}")

# Show BMI progress graph
def show_bmi_progress():
    if len(bmi_progress) == 0:
        ttk.Messagebox.show_info("No Data", "No BMI data to display yet.")
        return

    dates = list(bmi_progress.keys())
    bmi_values = list(bmi_progress.values())

    plt.figure()
    plt.plot(dates, bmi_values, marker='o', color='blue')
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title("BMI Progress")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Tkinter GUI setup using ttkbootstrap
root = ttk.Window(themename="darkly")  # Choose a theme (e.g., darkly, flatly, etc.)
root.title("BMI Calculator with AI Suggestions")
root.geometry('400x400')

# Style and layout configuration
style = ttk.Style()
style.configure("TLabel", padding=5)
style.configure("TButton", padding=5)

# Labels and entry fields for weight and height
ttk.Label(root, text="Enter your weight (kg):", bootstyle=INFO).grid(row=0, column=0, padx=10, pady=10)
weight_entry = ttk.Entry(root, bootstyle=INFO)
weight_entry.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(root, text="Enter your height (cm):", bootstyle=INFO).grid(row=1, column=0, padx=10, pady=10)
height_entry = ttk.Entry(root, bootstyle=INFO)
height_entry.grid(row=1, column=1, padx=10, pady=10)

# Dropdown for selecting fitness aim
ttk.Label(root, text="Select your aim:", bootstyle=INFO).grid(row=2, column=0, padx=10, pady=10)
aim_combo = ttk.Combobox(root, values=["Gain Weight", "Gain Muscle", "Reduce Weight"], bootstyle=INFO)
aim_combo.grid(row=2, column=1, padx=10, pady=10)

# Button to calculate BMI
calculate_btn = ttk.Button(root, text="Calculate BMI", command=calculate_bmi, bootstyle=SUCCESS)
calculate_btn.grid(row=3, column=0, columnspan=2, pady=10)

# Label to show BMI result
result_label = ttk.Label(root, text="Your BMI will appear here.", bootstyle=INFO)
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Label to show AI suggestions
suggestion_label = ttk.Label(root, text="AI Suggestions for food and exercise will appear here.", bootstyle=INFO)
suggestion_label.grid(row=5, column=0, columnspan=2, pady=10)

# Button to show BMI progress graph
progress_btn = ttk.Button(root, text="Show BMI Progress", command=show_bmi_progress, bootstyle=PRIMARY)
progress_btn.grid(row=6, column=0, columnspan=2, pady=10)

# Run the app
root.mainloop()