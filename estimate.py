# Import necessary modules for GUI, file operations, and utilities
import os
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import utils




# Global variables for the application
# Global error label variable for displaying error messages
error_label = None
# Model parameters (theta0: intercept, theta1: slope)
theta0 = 2
theta1 = 5
# Variable to store file read status label
file_read = None
# Get the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))


# Create the main Tkinter window
root = tk.Tk()
root.title("Car Price vs. Mileage")
root.geometry("1000x600")


# Function to ensure the theta parameters file exists and is valid
def ensure_local_file(filename):
    # Access global variables
    global theta0
    global theta1
    global file_read
    # Get the current directory path
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full file path
    file_path = os.path.join(current_dir, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        # Create default file if it doesn't exist
        theta0, theta1 = utils.create_default_file(file_path, filename)
    else:
        # Validate the existing file
        result = utils.local_file_valid_check(filename, file_path)
        
        if result == True:        
            # File is valid, read the parameters
            print(f"{filename} already exists ✅")
            with open(file_path, "r") as f:
                theta0, theta1 = f.read().split(",")
                theta0 = float(theta0)
                theta1 = float(theta1)
        else:
            # File is invalid, get error type and reset to defaults
            error_type = result[1]
            
            theta0, theta1 = utils.create_default_file(file_path, filename)
            print(f"{filename} reset to defaults ✅")
            
            # Display error message in the GUI
            file_read = tk.Label(root, text=f"{filename} error: {error_type} - reset to defaults", fg="red")
            file_read.pack(pady=10)
            
# Initialize the theta parameters file
ensure_local_file("thetas")

# Function to estimate car price based on mileage using linear regression
def estimate_price(mileage):
    # Print input mileage for debugging
    print("Mileage:", mileage)
    # Calculate price using linear regression formula: price = theta0 + theta1 * mileage
    result = (theta0 + theta1 * mileage)
    # Print estimated price for debugging
    print("estimated price:", result)
    return result


# Function to clear all error and status messages from the GUI
def clear_messages():
    # Access global variables
    global file_read
    # Remove file read status label if it exists
    if file_read is not None:
        file_read.destroy()
        file_read = None
    global error_label
    # Remove error label if it exists
    if error_label is not None:
        error_label.destroy()
        error_label = None

# Function called when the calculate button is pressed
def push_button():
    # Access global error label variable
    global error_label
    # Get the input value from the entry box
    input_value = box.get()
    
    # Clear any existing messages
    clear_messages()
    
    # Check if input is empty
    if (input_value.strip() == ""):
        print("Value is empty.")
        # Display error message for empty input
        error_label = tk.Label(root, text="Please enter a value.", fg="red")
        error_label.pack(pady=10)
    else:
        try:
            # Convert input to integer and calculate price
            mileage = int(input_value)
            price = estimate_price(mileage)
            # Update the result label with estimated price and model parameters
            sonuc_label.config(text=f"estimated price: {price} " + "theta0: " + str(theta0) + " theta1: " + str(theta1))
        except ValueError:
            # Handle invalid input (non-numeric)
            error_label = tk.Label(root, text="Please enter a valid number!" , fg="red")
            error_label.pack(pady=10)


# Tkinter GUI setup and configuration

# Create input label
label = tk.Label(root, text="Please enter a value:")
label.pack(pady=10)

# Create input entry box
box = tk.Entry(root, width=30)
box.pack(pady=5)

# Create calculate button
buton = tk.Button(root, text="Calculate", command=push_button)
buton.pack(pady=10)

# Create result display label
sonuc_label = tk.Label(root, text="", font=("Arial", 12))
sonuc_label.pack(pady=20)

# Start the main GUI event loop
root.mainloop()
