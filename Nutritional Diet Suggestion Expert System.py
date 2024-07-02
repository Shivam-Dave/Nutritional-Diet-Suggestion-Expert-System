#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Define the knowledge base and combine nutrients
knowledge_base = {
    "non_vegetarian": {
        "protein": {
            "chicken breast": 31,
            "salmon": 22,
            "turkey": 30,
            "shrimp": 20,
            "tofu": 8,
            "lentils": 9,
            "black beans": 7,
            "cottage cheese": 11,
        },
        "carbohydrates": {
            "brown rice": 45,
            "quinoa": 39,
            "sweet potato": 27,
            "whole wheat bread": 18,
            "oats": 17,
        },
        "fats": {
            "avocado": 15,
            "almonds": 14,
            "peanut butter": 8,
            "olive oil": 0,
            "chia seeds": 5,
            "cottage cheese": 9,
        },
        "vitamins and minerals": {
            "spinach": 145,
            "kale": 200,
            "broccoli": 81,
            "bell pepper": 95,
            "carrot": 41,
        }
    },
    "vegetarian": {
        "protein": {
            "tofu": 8,
            "lentils": 9,
            "black beans": 7,
            "cottage cheese": 11,
        },
        "carbohydrates": {
            "brown rice": 45,
            "quinoa": 39,
            "sweet potato": 27,
            "whole wheat bread": 18,
            "oats": 17,
        },
        "fats": {
            "avocado": 15,
            "almonds": 14,
            "chia seeds": 5,
            "cottage cheese": 9,
        },
        "vitamins and minerals": {
            "spinach": 145,
            "kale": 200,
            "broccoli": 81,
            "bell pepper": 95,
            "carrot": 41,
        }
    },
    "vegan": {
        "protein": {
            "tofu": 8,
            "lentils": 9,
            "black beans": 7,
        },
        "carbohydrates": {
            "brown rice": 45,
            "quinoa": 39,
            "sweet potato": 27,
            "oats": 17,
        },
        "fats": {
            "avocado": 15,
            "almonds": 14,
            "chia seeds": 5,
        },
        "vitamins and minerals": {
            "spinach": 145,
            "kale": 200,
            "broccoli": 81,
            "bell pepper": 95,
            "carrot": 41,
        }
    }
}

# Combine nutrients
def combine_nutrients():
    for nutrient_category in ["protein", "carbohydrates", "fats", "vitamins and minerals"]:
        # Combine vegan and vegetarian into non-vegetarian
        non_veg_set = set(knowledge_base["non_vegetarian"][nutrient_category].keys())
        veg_set = set(knowledge_base["vegetarian"][nutrient_category].keys())
        vegan_set = set(knowledge_base["vegan"][nutrient_category].keys())

        # Add vegan to vegetarian
        knowledge_base["vegetarian"][nutrient_category] = {
            **knowledge_base["vegetarian"][nutrient_category],
            **{key: knowledge_base["vegan"][nutrient_category][key] for key in vegan_set if key not in veg_set}
        }
        
        # Add vegetarian and vegan to non-vegetarian
        combined_set = veg_set.union(vegan_set)
        knowledge_base["non_vegetarian"][nutrient_category] = {
            **knowledge_base["non_vegetarian"][nutrient_category],
            **{key: knowledge_base["vegetarian"][nutrient_category][key] for key in combined_set if key not in non_veg_set}
        }

combine_nutrients()

# Suggest diet based on user information
def suggest_diet(weight, height, age, gender):
    # Calculate basal metabolic rate (BMR)
    if gender.lower() == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    # Calculate daily caloric needs
    daily_caloric_needs = bmr * 1.2  # Assuming sedentary lifestyle

    # Calculate nutrient recommendations
    recommendations = {}
    for nutrient in ["protein", "carbohydrates", "fats", "vitamins and minerals"]:
        total_nutrient_content = 0
        for food_type in knowledge_base.values():
            total_nutrient_content += sum(food_type[nutrient].values())

        recommendations[nutrient] = total_nutrient_content * daily_caloric_needs / 2000  # Based on a 2000-calorie diet
    return recommendations

# Suggest meal plan based on diet type and number of courses
def suggest_meal_plan(diet_type, num_courses):
    meal_plan = []

    if diet_type.lower() in knowledge_base:
        # Retrieve food options based on the diet type
        food_options = knowledge_base[diet_type.lower()]

        for _ in range(num_courses):
            course = {}
            for nutrient, foods in food_options.items():
                random_food = random.choice(list(foods.keys()))
                course[nutrient] = random_food
            meal_plan.append(course)
    else:
        messagebox.showerror("Error", "Invalid diet type entered. Please try again.")
    
    return meal_plan

# Create the GUI using Tkinter
class DietSuggestionApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set title and configure window size
        self.title("Nutritional Diet Suggestion App")
        self.geometry("800x600")

        # Center the window
        self.center_window()

        # Load background image using Pillow
        try:
            # Load the background image
            self.bg_img = Image.open("Nutritional Diet Suggestion Expert System.png")  # Specify the path of your image file
            self.bg_img = ImageTk.PhotoImage(self.bg_img)
            
            # Create a label for the background
            self.bg_label = tk.Label(self, image=self.bg_img)
            self.bg_label.place(relwidth=1, relheight=1)
            self.update_background_image()
        except Exception as e:
            print(f"Error loading background image: {e}")

        # Font styles
        self.title_font = ("Helvetica", 16, "bold")
        self.label_font = ("Helvetica", 12, "bold")
        self.button_font = ("Helvetica", 12, "bold")
        self.error_font = ("Arial", 12, "bold")

        # Main frame
        self.main_frame = tk.Frame(self, bg="white")  # Use white background color
        self.main_frame.pack(padx=10, pady=10, expand=True, fill="both")

        # Title label
        self.title_label = tk.Label(self.main_frame, text="Diet Suggestion App", font=self.title_font, bg="white", fg="black")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # User input fields
        self.create_input_fields()

        # Buttons
        self.create_buttons()

        # Output frame with text box and scrollbar
        self.create_output_frame()

        # Bind the window resizing event to the update_background_image function
        self.bind("<Configure>", self.update_background_image)

    def update_background_image(self, event=None):
        """Resize the background image with respect to window size."""
        if hasattr(self, 'bg_img'):
            self.bg_label.config(width=self.winfo_width(), height=self.winfo_height())
            self.bg_label.place(relwidth=1, relheight=1)

    def center_window(self):
        """Centers the GUI window on the screen."""
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Get window width and height
        window_width = 800
        window_height = 600

        # Calculate x and y coordinates for centering
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the window geometry
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Validate inputs when generating a meal plan or calculating recommendations
    def validate_inputs(self):
        """Validate height, weight, age, and number of courses inputs."""
        valid = True

        # Validate height
        if not self.validate_height():
            valid = False

        # Validate weight
        if not self.validate_weight():
            valid = False

        # Validate age
        if not self.validate_age():
            valid = False

        # Validate number of courses
        if not self.validate_num_courses():
            valid = False

        return valid

    # Create input fields and validation
    def create_input_fields(self):
        # Create labels and entries for input fields
        self.weight_label = tk.Label(self.main_frame, text="Weight (kg):", font=self.label_font, bg="white", fg="black")
        self.weight_label.grid(row=1, column=0, pady=5, sticky="e")
        self.weight_entry = tk.Entry(self.main_frame, font=self.label_font, bg="white", fg="black")
        self.weight_entry.grid(row=1, column=1, pady=5)

        self.height_label = tk.Label(self.main_frame, text="Height (cm):", font=self.label_font, bg="white", fg="black")
        self.height_label.grid(row=2, column=0, pady=5, sticky="e")
        self.height_entry = tk.Entry(self.main_frame, font=self.label_font, bg="white", fg="black")
        self.height_entry.grid(row=2, column=1, pady=5)

        self.age_label = tk.Label(self.main_frame, text="Age (years):", font=self.label_font, bg="white", fg="black")
        self.age_label.grid(row=3, column=0, pady=5, sticky="e")
        self.age_entry = tk.Entry(self.main_frame, font=self.label_font, bg="white", fg="black")
        self.age_entry.grid(row=3, column=1, pady=5)

        self.gender_label = tk.Label(self.main_frame, text="Gender:", font=self.label_font, bg="white", fg="black")
        self.gender_label.grid(row=4, column=0, pady=5, sticky="e")
        self.gender_var = tk.StringVar()
        self.gender_combobox = ttk.Combobox(self.main_frame, textvariable=self.gender_var, font=self.label_font,
                                            values=["Male", "Female"], state="readonly")
        self.gender_combobox.grid(row=4, column=1, pady=5)
        self.gender_combobox.set("Male")

        self.diet_type_label = tk.Label(self.main_frame, text="Diet Type:", font=self.label_font, bg="white", fg="black")
        self.diet_type_label.grid(row=5, column=0, pady=5, sticky="e")
        self.diet_type_var = tk.StringVar()
        self.diet_type_combobox = ttk.Combobox(self.main_frame, textvariable=self.diet_type_var, font=self.label_font,
                                               values=["Choose", "Vegan", "Vegetarian", "Non-Vegetarian"], state="readonly")
        self.diet_type_combobox.grid(row=5, column=1, pady=5)
        self.diet_type_combobox.set("Choose")

        self.num_courses_label = tk.Label(self.main_frame, text="Number of Courses (max:15):", font=self.label_font,
                                          bg="white", fg="black")
        self.num_courses_label.grid(row=6, column=0, pady=5, sticky="e")
        self.num_courses_entry = tk.Entry(self.main_frame, font=self.label_font, bg="white", fg="black")
        self.num_courses_entry.grid(row=6, column=1, pady=5)

    def validate_height(self):
        """Validate height input."""
        try:
            height = float(self.height_entry.get())
            if height <= 30 or height < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Height must be greater than 30 cm and non-negative.")
            return False
        return True

    def validate_weight(self):
        """Validate weight input."""
        try:
            weight = float(self.weight_entry.get())
            if weight <= 10 or weight < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Weight must be greater than 10 kg and non-negative.")
            return False
        return True

    def validate_age(self):
        """Validate age input."""
        try:
            age = int(self.age_entry.get())
            if age <= 0 or age < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Age must be greater than 0 and non-negative.")
            return False
        return True

    def validate_num_courses(self):
        """Validate number of courses input."""
        try:
            num_courses = int(self.num_courses_entry.get())
            if num_courses <= 0 or num_courses > 15 or num_courses < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Number of courses must be between 1 and 15 and non-negative.")
            return False
        return True

    def create_buttons(self):
        # Create buttons for calculating recommendations and generating meal plans
        self.calculate_button = tk.Button(self.main_frame, text="Calculate Recommendations", font=self.button_font,
                                          command=self.calculate_recommendations, bg="white", fg="black")
        self.calculate_button.grid(row=7, column=0, pady=10, sticky="ew")

        self.generate_meal_plan_button = tk.Button(self.main_frame, text="Generate Meal Plan", font=self.button_font,
                                                   command=self.generate_meal_plan, bg="white", fg="black")
        self.generate_meal_plan_button.grid(row=7, column=1, pady=10, sticky="ew")

    def create_output_frame(self):
        """Creates the output frame with a text box and scrollbar."""
        # Create output frame
        self.output_frame = tk.Frame(self.main_frame, bg="white")
        self.output_frame.grid(row=8, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        # Create text box and scrollbar
        self.output_text = tk.Text(self.output_frame, width=80, height=15, font=self.label_font, wrap=tk.WORD, bg="white", fg="black")
        self.scrollbar = tk.Scrollbar(self.output_frame, command=self.output_text.yview)
        self.output_text.config(yscrollcommand=self.scrollbar.set)

        # Pack the text box and scrollbar
        self.output_text.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # Calculate recommendations based on user input
    def calculate_recommendations(self):
        # Validate inputs before proceeding
        if not self.validate_inputs():
            return
        
        try:
            # Retrieve input values
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            age = int(self.age_entry.get())
            gender = self.gender_var.get()

            # Calculate recommendations
            recommendations = suggest_diet(weight, height, age, gender)

            # Display recommendations
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Daily Nutrient Recommendations:\n")
            for nutrient, recommendation in recommendations.items():
                self.output_text.insert(tk.END, f"{nutrient.capitalize()}: {recommendation:.2f} g\n")

        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter numeric values for Weight, Height, and Age.")

    # Generate meal plan based on user input
    def generate_meal_plan(self):
        # Validate inputs before proceeding
        if not self.validate_inputs():
            return

        try:
            diet_type = self.diet_type_var.get()
            num_courses = int(self.num_courses_entry.get())

            if diet_type == "Choose":
                messagebox.showerror("Error", "Please select a diet type from the dropdown.")
                return

            # Generate meal plan
            meal_plan = suggest_meal_plan(diet_type, num_courses)

            # Display meal plan
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Suggested Meal Plan:\n")
            for course_num, course in enumerate(meal_plan):
                self.output_text.insert(tk.END, f"\nCourse {course_num + 1}:\n")
                for nutrient, food in course.items():
                    self.output_text.insert(tk.END, f"{nutrient.capitalize()}: {food}\n")

        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter numeric values for the number of courses.")

# Run the application
app = DietSuggestionApp()
app.mainloop()


# In[ ]:





# In[ ]:




