import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print("Starting data analysis...")

# Load the dataset
df = pd.read_csv("res/csv/All_Diets.csv")

print("Dataset loaded successfully")
print("Dataset shape:", df.shape)

# -------------------------
# Handle missing values
# Task 5: Replaced the 3 sepate fillna calls with a single call that fills all macronutrient columns at once using their respective means. This is more efficient and cleaner.
# -------------------------
macro_cols = ["Protein(g)", "Carbs(g)", "Fat(g)"]
df[macro_cols] = df[macro_cols].fillna(df[macro_cols].mean())

print("Missing values handled")

# -------------------------
# Average macronutrients per diet type
# -------------------------
avg_macros = df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]].mean()
print("\nAverage macronutrients:")
print(avg_macros)

# -------------------------
# Top 5 protein-rich recipes per diet type
# -------------------------
top_protein = (
    df.sort_values("Protein(g)", ascending=False)
      .groupby("Diet_type")
      .head(5)
)

print("\nTop protein recipes:")
print(top_protein[["Diet_type", "Protein(g)"]])

# -------------------------
# Derived metrics (safe division)
# -------------------------
df["Protein_to_Carbs_ratio"] = df["Protein(g)"] / df["Carbs(g)"].replace(0, 1)
df["Carbs_to_Fat_ratio"] = df["Carbs(g)"] / df["Fat(g)"].replace(0, 1)

print("Derived metrics added")

# -------------------------
# Save outputs (useful for Docker / serverless tasks)
# -------------------------
avg_macros.to_csv("res/csv/avg_macros.csv")
top_protein.to_csv("res/csv/top_protein.csv")

print("Output files saved")

# -------------------------
# Visualizations
# Task 5: Changed plt.show() to plt.close() after saving each figure. This allows the script to run in headless environments (like Docker) without issues and prevents blocking execution.
# -------------------------

# Protein bar chart
sns.barplot(x=avg_macros.index, y=avg_macros["Protein(g)"])
plt.title("Average Protein by Diet Type")
plt.ylabel("Average Protein (g)")
plt.tight_layout()
plt.savefig("res/png/protein_chart.png")
plt.close()

# Carbs bar chart
sns.barplot(x=avg_macros.index, y=avg_macros["Carbs(g)"])
plt.title("Average Carbs by Diet Type")
plt.ylabel("Average Carbs (g)")
plt.tight_layout()
plt.savefig("res/png/carbs_chart.png")
plt.close()

# Fat bar chart
sns.barplot(x=avg_macros.index, y=avg_macros["Fat(g)"])
plt.title("Average Fat by Diet Type")
plt.ylabel("Average Fat (g)")
plt.tight_layout()
plt.savefig("res/png/fat_chart.png")
plt.close()

# Heatmap
sns.heatmap(avg_macros, annot=True, cmap="YlGnBu")
plt.title("Macronutrient Content by Diet Type")
plt.xlabel("Macronutrients")
plt.tight_layout()
plt.savefig("res/png/heatmap.png")
plt.close()

# Scatter plot
sns.scatterplot(
    data=top_protein,
    x=top_protein.index,
    y="Protein(g)",
    hue="Diet_type",
    s=100
)
plt.title("Top 5 Protein-Rich Recipes by Diet Type")
plt.ylabel("Protein (g)")
plt.xlabel("Recipe Index")
plt.legend(title="Diet Type")
plt.tight_layout()
plt.savefig("res/png/scatter_plot.png")
plt.close()

print("Data analysis complete.")