import json
import pandas as pd
import matplotlib.pyplot as plt

# Read JSON data from file
with open("C:/Users/extracted_data.json", "r") as file:
    data = json.load(file)

# Create a dictionary to store the ratings for each country
ratings_by_country = {}

for entry in data:
    country = entry["Country"]
    rating = entry["Rating"]
    if country not in ratings_by_country:
        ratings_by_country[country] = {}
    ratings_by_country[country][rating] = ratings_by_country[country].get(rating, 0) + 1

# Convert the ratings_by_country dictionary into a DataFrame
df = pd.DataFrame(ratings_by_country).T

# Sort the DataFrame by the sum of ratings in ascending order
df["Total"] = df.sum(axis=1)
df = df.sort_values(by="Total", ascending=True)

# Plot the grouped bar plot
plt.figure(figsize=(12, 8))
df.drop(columns=["Total"]).plot(kind="bar", stacked=True, cmap="viridis")
plt.xlabel("Country")
plt.ylabel("Frequency")
plt.title("Country-wise Distribution of Ratings")
plt.legend(title="Rating")
plt.tight_layout()

# Show the plot
plt.show()
