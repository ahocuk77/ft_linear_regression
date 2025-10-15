# Import necessary modules for file operations and utilities
import utils
import os
import matplotlib.pyplot as plt

# Linear Regression class for machine learning model training
class LinearRegression:
    def __init__(self):
        # Initialize model parameters
        self.theta0 = 0  # Intercept (bias term)
        self.theta1 = 0  # Slope (weight for mileage feature)
        self.learning_rate = 0.01  # Learning rate for gradient descent
        
    def read_data(self, filename="data.csv"):
        # Initialize lists to store mileage and price data
        mileages = []
        prices = []
        # Get the current directory path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full file path
        file_path = os.path.join(current_dir, filename)

        # Check if the data file exists
        if not os.path.exists(file_path):
            print(f"{filename} not found ❌")
            return False, "file not found"

        # Read and parse the CSV file
        with open(file_path, "r") as f:
            lines = f.readlines()
            # Skip the first line as it contains headers
            for line in lines[1:]:  # first line is the header
                # Validate the data format using utility function
                result = utils.csv_file_valid_check(line)
                if not result == True:
                    error_type = result[1]
                    print(f"Invalid data format in {filename} ❌ - {error_type}")
                    return False, "invalid data format"
                # Parse mileage and price from comma-separated values
                mileage, price = line.strip().split(",")
                mileages.append(float(mileage))
                prices.append(float(price))
        return mileages, prices
    
        
    def plot_regression_line(self, mileages, prices):
        """Plot the regression line on top of the data points."""
        plt.figure(figsize=(8, 6))
        plt.scatter(mileages, prices, color='blue', label='Data Points', alpha=0.6)

        # Calculate line values for regression line
        x_line = [min(mileages), max(mileages)]
        y_line = [self.theta0 + self.theta1 * x for x in x_line]

        # Draw the regression line
        plt.plot(x_line, y_line, color='red', linewidth=2, label='Regression Line')

        # Visual details
        plt.xlabel("Mileage (km)")
        plt.ylabel("Price (€)")
        plt.title("Linear Regression: Car Price vs Mileage")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.4)
        plt.tight_layout()
        plt.show()

    
    def train(self, epochs=100):
        # Read training data from CSV file
        mileages, prices = self.read_data()
        if not mileages:
            print("Training stopped ❌ — no data.")
            return
        
        
        # ✅ Data normalization for better convergence
        mean_x = sum(mileages) / len(mileages)
        std_x = (sum((x - mean_x) ** 2 for x in mileages) / len(mileages)) ** 0.5
        mileages_norm = [(x - mean_x) / std_x for x in mileages]

        # Initialize training variables
        m = len(mileages)  # Number of training examples
        prev_loss = float('inf')  # Start with infinite loss for first epoch
        tolerance = 1e-1          # Stop if loss difference is smaller than this value

        # Main training loop
        for epoch in range(epochs):
            # Calculate predictions using current model parameters
            predictions = [self.theta0 + self.theta1 * x for x in mileages_norm]
            # Calculate prediction errors
            errors = [pred - y for pred, y in zip(predictions, prices)]

            # ✅ Calculate gradients for gradient descent
            grad0 = (1 / m) * sum(errors)
            grad1 = (1 / m) * sum(e * x for e, x in zip(errors, mileages_norm))

            # ✅ Update model parameters using gradient descent
            new_theta0 = self.theta0 - self.learning_rate * grad0
            new_theta1 = self.theta1 - self.learning_rate * grad1
            self.theta0, self.theta1 = new_theta0, new_theta1

            # ✅ Calculate loss using Mean Squared Error (MSE)
            loss = (1 / (2 * m)) * sum(e ** 2 for e in errors)

            # Print training progress
            print(f"Epoch {epoch:4d}: θ0={self.theta0:.4f}, θ1={self.theta1:.4f}, loss={loss:.10f}")

            # ✅ Early stopping to prevent overfitting
            if abs(prev_loss - loss) < tolerance:
                print(f"\n⚡ Early stopping triggered at epoch {epoch} (loss={loss:.10f})\n")
                break

            # Store current loss for next iteration comparison
            prev_loss = loss

        # ✅ Denormalize thetas to work with original data scale
        self.theta1 /= std_x
        self.theta0 -= (self.theta1 * mean_x)

        # Print training completion and final parameters
        print("Training complete ✅")
        print(f"Final θ0={self.theta0:.4f}, θ1={self.theta1:.4f}")

        # ✅ Plot regression line on top of the data
        self.plot_regression_line(mileages, prices)
        # Save the trained parameters to file
        self.save_thetas()

    # Method to save trained model parameters to a file
    def save_thetas(self, filename="thetas"):
        # Get the current directory path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full file path
        file_path = os.path.join(current_dir, filename)
        try:
            # Write theta parameters to file in comma-separated format
            with open(file_path, "w") as f:
                f.write(f"{self.theta0},{self.theta1}")
            print(f"Thetas saved successfully ✅ → {filename}")
        except Exception as e:
            print(f"Error saving thetas ❌: {e}")



# Main function to run the linear regression training
def main():
    # Create a new LinearRegression instance
    first = LinearRegression()
    # Train the model with 1000 epochs
    first.train(1000)

# Entry point of the program
if __name__ == "__main__":
    main()
