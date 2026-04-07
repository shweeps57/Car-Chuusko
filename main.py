from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


DATA_FILE = Path(__file__).with_name("carData.csv")
cars_df = pd.read_csv(DATA_FILE)


def update_transmission():
    fuel = fuel_var.get()

    menu = trans_menu["menu"]
    menu.delete(0, "end")

    if fuel == "EV":
        menu.add_command(label="Automatic", command=lambda: trans_var.set("Automatic"))
        trans_var.set("Automatic")
    else:
        options = ["Any", "Manual", "Automatic"]
        for opt in options:
            menu.add_command(label=opt, command=lambda value=opt: trans_var.set(value))
        trans_var.set("Any")


def create_card(parent):
    frame = tk.Frame(parent, bg="#132B5B", bd=1, relief="solid")
    frame.pack(padx=20, pady=10, fill="x")
    return frame



def show_comparison(car1, car2):
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#0A1F44")


    tk.Label(root, text="Car Comparison", font=("Arial", 18, "bold"),
             bg="#0A1F44", fg="white").pack(pady=10)


    top_frame = tk.Frame(root, bg="#0A1F44")
    top_frame.pack(pady=10)


    tk.Label(top_frame, text="", bg="#0A1F44", width=20).grid(row=0, column=0)

    tk.Label(top_frame, text=car1["Name"], font=("Arial", 14, "bold"),
             bg="#0A1F44", fg="white", width=20).grid(row=0, column=1)

    tk.Label(top_frame, text=car2["Name"], font=("Arial", 14, "bold"),
             bg="#0A1F44", fg="white", width=20).grid(row=0, column=2)

    # MATCH %
    tk.Label(top_frame, text="Match %", bg="#0A1F44", fg="white").grid(row=1, column=0)
    tk.Label(top_frame, text=f"{car1['Match %']:.1f}%", fg="lightgreen", bg="#0A1F44").grid(row=1, column=1)
    tk.Label(top_frame, text=f"{car2['Match %']:.1f}%", fg="lightgreen", bg="#0A1F44").grid(row=1, column=2)

    # PRICE
    tk.Label(top_frame, text="Price", bg="#0A1F44", fg="white").grid(row=2, column=0)
    tk.Label(top_frame, text=f"₹{car1['MinPrice']:} - ₹{car1['MaxPrice']:}", bg="#0A1F44", fg="white").grid(row=2, column=1)
    tk.Label(top_frame, text=f"₹{car2['MinPrice']:} - ₹{car2['MaxPrice']:}", bg="#0A1F44", fg="white").grid(row=2, column=2)

    # Info
    card = create_card(root)
    info_frame = tk.Frame(card, bg="#132B5B")
    info_frame.pack(pady=10)

    attrs = ["FuelType", "Transmission", "bodyType"]

    for i, attr in enumerate(attrs):
        tk.Label(info_frame, text=attr, bg="#0A1F44",
                 fg="white", width=20).grid(row=i, column=0, padx=5, pady=3)

        tk.Label(info_frame, text=str(car1[attr]),
                 bg="#1A2E5A", fg="white", width=20).grid(row=i, column=1, padx=5)

        tk.Label(info_frame, text=str(car2[attr]),
                 bg="#1A2E5A", fg="white", width=20).grid(row=i, column=2, padx=5)

    # Performance table
    tk.Label(root, text="Performance Comparison",
             bg="#0A1F44", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

    card = create_card(root)
    table_frame = tk.Frame(card, bg="#132B5B")
    table_frame.pack(pady=10)

    attrs = ["Performance", "Comfort", "Features", "Safety", "Mileage"]

    for i, attr in enumerate(attrs):
        tk.Label(table_frame, text=attr, bg="#0A1F44",
                 fg="white", width=20).grid(row=i, column=0, pady=3)

        tk.Label(table_frame, text=str(car1[attr]),
                 bg="#1A2E5A", fg="white", width=15).grid(row=i, column=1)

        tk.Label(table_frame, text=str(car2[attr]),
                 bg="#1A2E5A", fg="white", width=15).grid(row=i, column=2)

    # Other Specs
    tk.Label(root, text="Other Stats",
             bg="#0A1F44", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

    card = create_card(root)
    extra_frame = tk.Frame(card, bg="#132B5B")
    extra_frame.pack(pady=10)

    extra_attrs = ["MaintenanceRating", "ResaleValue"]

    for i, attr in enumerate(extra_attrs):
        tk.Label(extra_frame, text=attr, bg="#0A1F44",
                 fg="white", width=20).grid(row=i, column=0, pady=3)

        tk.Label(extra_frame, text=str(car1[attr]),
                 bg="#1A2E5A", fg="white", width=15).grid(row=i, column=1)

        tk.Label(extra_frame, text=str(car2[attr]),
                 bg="#1A2E5A", fg="white", width=15).grid(row=i, column=2)


    # Matplotlib part
    tk.Label(root, text="Visual Comparison",
             bg="#0A1F44", fg="white",
             font=("Arial", 14, "bold")).pack(pady=15)

    chart_frame = tk.Frame(root, bg="#0A1F44")
    chart_frame.pack()

    categories = ["Performance", "Comfort", "Features", "Safety", "Mileage"]

    values1 = [car1[c] for c in categories]
    values2 = [car2[c] for c in categories]

   
    values1 += values1[:1]
    values2 += values2[:1]

    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig = plt.Figure(figsize=(4, 4), facecolor="#0A1F44")
    ax = fig.add_subplot(111, polar=True)
    ax.set_facecolor("#0A1F44")
    ax.tick_params(colors="white")

    # plot
    ax.plot(angles, values1, linewidth=2, label=car1["Name"])
    ax.fill(angles, values1, alpha=0.1)

    ax.plot(angles, values2, linewidth=2, label=car2["Name"])
    ax.fill(angles, values2, alpha=0.1)

    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    ax.set_title("")

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


selected_cars = []


def show_results(ranked):
    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(root, text="Top Car Recommendations:", font=("Arial", 17),bg="#0A1F44")
    title.pack(pady=10)



    top4 = ranked.head(4)
    bottom4 = ranked.tail(4)

    for _, row in top4.iterrows():
        text = f"{row['Name']} ({row['Brand']})\nMatch: {row['Match %']:.1f}%"

        card = tk.Frame(
            root,
            bg="#1F7A1F",
            bd=2,
            relief="ridge",
            padx=10,
            pady=5
        )
        card.pack(pady=5, fill="x", padx=10)

        label = tk.Label(
            card,
            text=text,
            font=("Arial", 15),
            bg="#1F7A1F",
            fg="white",
            anchor="w",
            justify="left"
        )
        label.pack(fill="x")

        var = tk.IntVar()

        def on_select(r=row, v=var):
            name = r["Name"]

            if v.get() == 1:
                if len(selected_cars) >= 2:
                    messagebox.showerror("Limit", "You can only select 2 cars")
                    v.set(0)
                    return

                if name not in selected_cars:
                    selected_cars.append(name)
            else:
                if name in selected_cars:
                    selected_cars.remove(name)

        checkbox = tk.Checkbutton(
            card,
            text="Select",
            variable=var,
            command=on_select,
            bg=card["bg"],
            fg="white",
            activebackground=card["bg"],
            activeforeground="white"
        )
        checkbox.pack(anchor="e")

    title = tk.Label(root, text="Not Recommended:", font=("Arial", 17), bg="#0A1F44")
    title.pack(pady=10)

    for _, row in bottom4.iterrows():
        text = f"{row['Name']} ({row['Brand']})\nMatch: {row['Match %']:.1f}%"

        card = tk.Frame(
            root,
            bg="#7F1D1D",
            bd=2,
            relief="ridge",
            padx=10,
            pady=5
        )
        card.pack(pady=5, fill="x", padx=10)

        label = tk.Label(
            card,
            text=text,
            font=("Arial", 15),
            bg="#7F1D1D",
            fg="white",
            anchor="w",
            justify="left"
        )
        label.pack(fill="x")

    def compare():
        if len(selected_cars) != 2:
            messagebox.showerror("Error", "Select exactly 2 cars")
            return

        car1 = ranked[ranked["Name"] == selected_cars[0]].iloc[0]
        car2 = ranked[ranked["Name"] == selected_cars[1]].iloc[0]

        show_comparison(car1, car2)

    tk.Button(root, text="Compare", command=compare).pack(pady=20)




def calculate_score(cars, user_weights):
    scores = []
    for _, car in cars.iterrows():
        score = 0
        for category in ["Performance", "Comfort", "Features", "Safety", "Mileage"]:
                difference = abs(user_weights[category] - car[category])
                match_score = 5 - difference
                score += match_score * user_weights[category]

        budget = user_weights["Budget"]

        if car["MinPrice"] <= budget <= car["MaxPrice"]:
            budget_score = 5
        elif (car["MinPrice"] <= budget + 200000) and (car["MaxPrice"] >= budget - 200000):
            budget_score = 4
        elif (car["MinPrice"] <= budget + 400000) and (car["MaxPrice"] >= budget - 400000):
            budget_score = 3
        elif (car["MinPrice"] <= budget + 700000) and (car["MaxPrice"] >= budget - 700000):
            budget_score = 2
        else:
            budget_score = 1

        score += budget_score* user_weights["BudgetPriority"]
        scores.append(score)

    cars = cars.copy()
    cars["Score"] = scores
    max_score = (
        5 * user_weights["Performance"] + 5 * user_weights["Comfort"]+ 5 * user_weights["Features"]+ 5 * user_weights["Safety"]+ 5 * user_weights["Mileage"]+ 5 * user_weights["BudgetPriority"]
    )
    cars["Match %"] = (cars["Score"]/ max_score) * 100
    return cars.sort_values("Score", ascending=False)


def recommend_cars():

    user_weights = {
        "Performance": performance_scale.get(),
        "Comfort": comfort_scale.get(),
        "Features": features_scale.get(),
        "Safety": safety_scale.get(),
        "Mileage": mileage_scale.get(),
        "BudgetPriority": budget_priority_scale.get(),
    }
    user_fuel = fuel_var.get()
    user_trans = trans_var.get()
    user_seater = seater_var.get()

    budget = simpledialog.askinteger("Budget", "Enter your budget:")

    if budget is None:
        return

    user_weights["Budget"] = budget

    lower = user_weights["Budget"] * 0.7
    upper = user_weights["Budget"] * 1.3

    filtered_cars = cars_df[
        (cars_df["MinPrice"] >= lower) & (cars_df["MinPrice"] <= upper)
    ]

    # Fuel filter
    if user_fuel != "Any":
        filtered_cars = filtered_cars[filtered_cars["FuelType"] == user_fuel]

    # Transmission filter
    if user_trans != "Any":
        filtered_cars = filtered_cars[filtered_cars["Transmission"] == user_trans]

    # Seater filter
    if user_seater != "Any":
        filtered_cars = filtered_cars[filtered_cars["Seater"] == int(user_seater)]

    if filtered_cars.empty:
        messagebox.showinfo("No results", "No cars found in your budget range.")
        return

    ranked = calculate_score(filtered_cars, user_weights)

    show_results(ranked)


root = tk.Tk()
root.configure(bg="#0A1F44")  # dark blue
root.title("Car Chuusko")
root.geometry("650x980")

label = tk.Label(root, text="Enter your car preferences:",bg="#0A1F44")
label.pack(pady=10)




tk.Label(root, text="Fuel Type:",bg="#0A1F44").pack(pady=5)
fuel_var = tk.StringVar(value="Any")

fuel_menu = tk.OptionMenu(
    root,
    fuel_var,
    "Any", "Petrol", "Diesel", "EV",
    command=lambda x: update_transmission()
)
fuel_menu.pack()



trans_label = tk.Label(root, text="Transmission:",bg="#0A1F44")
trans_label.pack(pady=5)
trans_var = tk.StringVar(value="Any")
trans_menu = tk.OptionMenu(root, trans_var, "Any", "Manual", "Automatic")
trans_menu.pack()


seater_label = tk.Label(root, text="Seater:",bg="#0A1F44")
seater_label.pack(pady=5)
seater_var = tk.StringVar(value="Any")
seater_menu = tk.OptionMenu(root, seater_var, "Any", "5", "7")
seater_menu.pack()



performance_label = tk.Label(root, text="Performance:",bg="#0A1F44")
performance_label.pack(pady=10)
performance_scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL)
performance_scale.pack()




comfort_label = tk.Label(root, text="Comfort:",bg="#0A1F44")
comfort_label.pack(pady=10)
comfort_scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL)
comfort_scale.pack()




features_label = tk.Label(root, text="Features:",bg="#0A1F44")
features_label.pack(pady=10)
features_scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL)
features_scale.pack()




safety_label = tk.Label(root, text="Safety:",bg="#0A1F44")
safety_label.pack(pady=10)
safety_scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL)
safety_scale.pack()




mileage_label = tk.Label(root, text="Mileage:",bg="#0A1F44")
mileage_label.pack(pady=10)
mileage_scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL)
mileage_scale.pack()




budget_priority_label = tk.Label(root, text="Budget Priority:",bg="#0A1F44")
budget_priority_label.pack(pady=10)
budget_priority_scale = tk.Scale(root, from_=1, to=5, orient=tk.HORIZONTAL)
budget_priority_scale.pack()



recommend_button = tk.Button(root, text="Recommend", command=recommend_cars)
recommend_button.pack(pady=10)

# print(pd.__version__)

root.mainloop()



