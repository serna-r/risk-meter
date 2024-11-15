import matplotlib.pyplot as plt
from math import pi
from datetime import datetime
import json
import os

# Load json storing the risks
json_file_path = './flaskr/json/risks.json'
with open(json_file_path, 'r') as f: 
    JSON_RISKS = json.load(f)

# Constants for scaling the radar chart
MAX_VALUE = 35
MIN_VALUE = 0

def plot_radar_risk_dimensions(data, data_weighted, risk_type, folder):
    # Define the categories and the data points
    categories = ['Physical', 'Social', 'Resources', 'Psychological', 'Prosecution', 'Career', 'Freedom']
    values = [data[category] for category in categories]
    values += values[:1]  # Close the loop in values
    values_weighted = [data_weighted[category] for category in categories]
    values_weighted += values_weighted[:1]  # Close the loop for weighted values
    N = len(categories)

    # Create angles for the radar chart
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Complete the loop to close the chart

    # Create the figure with a single subplot
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.suptitle("Radar Plot: Risk Dimensions", fontsize=16)

    # Plot the normal risk scores
    ax.plot(angles, values, 'o-', ms=4, mec="w", linewidth=1.5, color='b', label=f"{risk_type} - Service")
    
    # Plot the weighted risk scores
    ax.plot(angles, values_weighted, 'o-', ms=4, mec="w", linewidth=1.5, color='r', label=f"{risk_type} - User modified")
    
    # Set the labels and limits
    ax.set_ylim(0, 35)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    
    # Add legend with appropriate location to ensure it displays correctly
    ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))

    # Generate a timestamp and create the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"radar_{timestamp}.png"
    path = os.path.join(folder, filename)
    os.makedirs(folder, exist_ok=True)  # Ensure the directory exists

    # Save figure with the name
    plt.savefig(path)
    plt.close(fig)

    return filename  # Return only the filename, not the full path

def calculate_risk(selected_elements, risk_appetite):
    """Calculate risks based on data stored in JSON_RISKS."""
    # Calculate the factor for risk appetite (if 4 = 1 if 7 = 0.25 if 1 = 1.75)
    risk_appetite_factor = 2 - risk_appetite / 4

    # Define the risk matrix and element index from JSON file
    risk_matrix = JSON_RISKS["risk_matrix"]
    element_index = JSON_RISKS["element_index"]

    # Initialize the risk scores for each dimension
    risk_scores = {dimension: 0 for dimension in risk_matrix}

    # Sum the values for each selected element across all dimensions
    for element in selected_elements:
        index = element_index[element]
        for dimension in risk_matrix:
            risk_scores[dimension] += risk_matrix[dimension][index]

    # Apply the weighted factor for risk appetite
    risk_scores_weighted = {dimension: value * risk_appetite_factor for dimension, value in risk_scores.items()}

    return risk_scores, risk_scores_weighted

def get_risk_color_class(score):
    if score < 30:
        return "very-low"
    elif score < 60:
        return "low"
    elif score < 90:
        return "medium"
    elif score < 120:
        return "high"
    elif score < 150:
        return "very-high"
    else:
        return "death"
    
# Evaluate based on nist policies
def evaluate_compliance(min_length, min_mask, extra_sec):
    """Function to evaluate compliance for a single service"""
    compliance = 0
    max_compliance = 3  # Total number of policies
    
    # Policy 1: Blocklist Requirement
    if extra_sec == 1:
        compliance += 1
    
    # Policy 2: Minimum Length
    compliance += min_length - 7
    
    # Policy 3: No Composition Rules
    if min_mask.lower() == 'l':  # l means no composition rules required
        compliance += 1
    
    # Calculate compliance score
    compliance_score = compliance / max_compliance
    return compliance_score


def example():
    # Example usage
    selected_elements = ["Nickname", "Email", "Location", "Subscription"]
    risk_appetite = 5  # Example risk appetite level
    risk_scores, risk_scores_weighted = calculate_risk(selected_elements, risk_appetite)
    print("Calculated Risk Scores:", risk_scores)
    print("Calculated Weighted Risk Scores:", risk_scores_weighted)

    # Plot the radar chart based on calculated risk scores
    plot_path = plot_radar_risk_dimensions(risk_scores, risk_scores_weighted, "Service Risk Profile", './')
    print("Radar plot saved to:", plot_path)

