import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

df = pd.read_csv(r"C:\Users\DR.ARSHIA\Desktop\AMR Insight\asts.csv")
print(df["Resistance phenotype"].value_counts())
print("-------------------------------------------------------------")
print(df["Antibiotic"].value_counts())
print("-------------------------------------------------------------")
# Number of resistant results for each antibiotic
result_for_specific_antibiotic = (
    (df["Resistance phenotype"] == "resistant")
    .groupby(df["Antibiotic"])
    .sum()
    .reset_index(name = "Resistant count")
    )
print(result_for_specific_antibiotic)
print("-------------------------------------------------------------")
# Resistance rate for each antibiotic
total = df.groupby("Antibiotic").size().reset_index(name = "total")
result = pd.merge(
    result_for_specific_antibiotic,
    total,
    on = "Antibiotic"
    )

result["Resistance Rate"] = (
    result["Resistant count"] / result["total"] * 100
    )
print(result)
print("-------------------------------------------------------------")
# Which antibiotic has the highest resistance rate?
print(result.loc[result['Resistance Rate'].idxmax()])
print("-------------------------------------------------------------")
# Number of susceptible results for each antibiotic
susceptible_count = (
    (df["Resistance phenotype"] == "susceptible")
    .groupby(df["Antibiotic"])
    .sum()
    .reset_index(name = "susceptible count")
    )
print(susceptible_count)    
print("-------------------------------------------------------------")
# Susceptibility rate for each antibiotic
total = df.groupby("Antibiotic").size().reset_index(name = "total")
result1 = pd.merge(
    susceptible_count,
    total,
    on = "Antibiotic"
    )
result1["susceptibility rate"] = (
    result1["susceptible count"] / result1["total"] * 100
    )
print(result1) 
print("-------------------------------------------------------------")
# Which bacterial species has the highest overall resistance rate?
resistant_count_bacteria = (
    (df["Resistance phenotype"] == "resistant")
    .groupby(df["Scientific name"])
    .sum()
    .reset_index(name = "resistant_count_bacteria")
    )
print(resistant_count_bacteria)
print("-------------------------------------------------------------")
total_bacteria = df.groupby('Scientific name').size().reset_index(name = 'total')
result2 = pd.merge(
    resistant_count_bacteria,
    total_bacteria,
    on = "Scientific name"
    )
result2['Resistance Rate'] = (
    result2['resistant_count_bacteria'] / result2['total'] * 100
    )
print(result2)
print("-------------------------------------------------------------")
print(result.loc[result['Resistance Rate'].idxmax()])
print("-------------------------------------------------------------")
# Do resistance patterns differ among bacterial species?
##bacteria_antibiotic = df.groupby(['Scientific name', 'Antibiotic'])
resistant_count = (
    (df['Resistance phenotype'] == "resistant")
    .groupby([df["Scientific name"], df['Antibiotic']])
    .sum()
    .reset_index(name = 'resistant_count')
    )
print(resistant_count)
print("-------------------------------------------------------------")
total_bacteria_antibiotic = df.groupby(["Scientific name", 'Antibiotic']).size().reset_index(name = "total")
result3 = pd.merge(
    resistant_count,
    total_bacteria_antibiotic,
    on = ["Scientific name", "Antibiotic"]
    )
result3['Resistance Rate'] = (
    result3['resistant_count'] / result3['total'] * 100
    )
print(result3)
#print(total_bacteria_antibiotic)
print("-------------------------------------------------------------")
# Number of intermediate results for each antibiotic
intermediate_count = (
    (df["Resistance phenotype"] == 'intermediate')
    .groupby(df['Antibiotic'])
    .sum()
    .reset_index(name = 'intermediate_count')
    )
print(intermediate_count)
print("-------------------------------------------------------------")
intermediate_antibiotic = df.groupby('Antibiotic').size().reset_index(name = 'total')
result4 = pd.merge(
    intermediate_count,
    intermediate_antibiotic,
    on = 'Antibiotic'
    )
result4['intermediate rate'] = (
    result4['intermediate_count'] / result4['total'] * 100
    )
print(result4)
print("-------------------------------------------------------------")
# Final results table
final_result = pd.merge(
    result,
    result1,
    on = 'Antibiotic'
    )
final_result = pd.merge(
    final_result,
    result4,
    on = 'Antibiotic'
    )
final_result = final_result[
    [
        "Antibiotic",
        "Resistant count",
        "Resistance Rate",
        "susceptible count",
        "susceptibility rate",
        "intermediate_count",
        "intermediate rate"
    ]
]

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_rows", None)

print(final_result)
print("-------------------------------------------------------------")
final_result["Total Rate"] = (
    final_result["Resistance Rate"]
    + final_result["susceptibility rate"]
    + final_result["intermediate rate"]
)

print(final_result[
    ["Antibiotic",
     "Resistance Rate",
     "susceptibility rate",
     "intermediate rate",
     "Total Rate"]
])
print("-------------------------------------------------------------")
# Antibiotic resistance profile

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(final_result['Antibiotic']))

width = 0.25

bars1 = ax.bar(
    x - width,
    final_result["Resistance Rate"],
    width,
    label="Resistance"
)

bars2 = ax.bar(
    x,
    final_result["susceptibility rate"],
    width,
    label="Susceptibility"
)

bars3 = ax.bar(
    x + width,
    final_result["intermediate rate"],
    width,
    label="Intermediate"
)

ax.set_xticks(x)
ax.set_xticklabels(final_result["Antibiotic"])

ax.set_xlabel('Antibiotic')
ax.set_ylabel('Percentage (%)')

ax.set_title('Antibiotic Resistance Profile')

ax.set_ylim(0, 100)


ax.legend()
ax.grid(
    axis='y',
    linestyle= '--',
    alpha=0.5
)

ax.bar_label(bars1, fmt="%.1f%%")
ax.bar_label(bars2, fmt="%.1f%%")
ax.bar_label(bars3, fmt="%.1f%%")

fig.tight_layout()

os.makedirs(
    r"C:\Users\DR.ARSHIA\Desktop\py project\figures",
    exist_ok=True
)

fig.savefig(
    r"C:\Users\DR.ARSHIA\Desktop\py project\figures\antibiotic_resistance_profile.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
print("-------------------------------------------------------------")
# Identify duplicate sample-antibiotic records
print(df["BioSample"].head(10))

print(df["BioSample"].nunique())

duplicates_rows = df[
    df.duplicated(
        subset=["BioSample", "Antibiotic"],
        keep=False
    )
]

print(
    duplicates_rows[
        ["BioSample", "Antibiotic", "Resistance phenotype"]
    ].sort_values(
        ["BioSample", "Antibiotic"]
    )
)

print(دارند؟
    duplicates_rows.groupby(
        ["BioSample", "Antibiotic"]
    )["Resistance phenotype"].nunique()
)
print("-------------------------------------------------------------")
# Determine how many different antibiotics were tested for each sample
antibiotic_per_sample = (
    df.groupby('BioSample')['Antibiotic']
    .nunique()
)

print(antibiotic_per_sample.value_counts().sort_index())
print("-------------------------------------------------------------")
# Do some antibiotics have similar resistance patterns? 
complete_samples = antibiotic_per_sample[
    antibiotic_per_sample == 5
].index

df_complete = df[
    df["BioSample"].isin(complete_samples)
]

print(df_complete["BioSample"].nunique())

print(
    df_complete.groupby(
        ['BioSample', 'Antibiotic']
    )['Resistance phenotype']
    .nunique()
    .value_counts()
    .sort_index()
)


ambiguous = (
    df_complete.groupby(
        ["BioSample", "Antibiotic"]
    )["Resistance phenotype"]
    .nunique()
)

ambiguous = ambiguous[ambiguous > 1]

print(ambiguous)

print(
    df_complete[
        df_complete.set_index(
            ["BioSample", "Antibiotic"]
        ).index.isin(ambiguous.index)
    ][
        ["BioSample", "Antibiotic", "Resistance phenotype"]
    ]
)
print("-------------------------------------------------------------")
resistant_per_sample = (
    (df_complete["Resistance phenotype"] == "resistant")
    .groupby(
        [df_complete["BioSample"], df_complete["Antibiotic"]]
    )
    .any()
    .reset_index(name="resistant")
)

print(resistant_per_sample.head(10))
print("-------------------------------------------------------------")
# Pivot the data to create a sample-antibiotic resistance matrix
resistance_matrix = resistant_per_sample.pivot(
    index = 'BioSample',
    columns = 'Antibiotic',
    values = 'resistant' 
)

print(resistance_matrix.head())
print("-------------------------------------------------------------")
resistance_matrix = resistance_matrix.astype(int)
print(resistance_matrix.head())
print(resistance_matrix.shape)
print("-------------------------------------------------------------")
correlation_matrix = resistance_matrix.corr()
print(correlation_matrix)
print("-------------------------------------------------------------")
# Correlation heatmap
fig, ax = plt.subplots(figsize=(9, 7))

im = ax.imshow(
    correlation_matrix,
    vmin=-1,
    vmax=1
)

ax.set_xticks(range(len(correlation_matrix.columns)))
ax.set_xticklabels(
    correlation_matrix.columns,
    rotation=45,
    ha="right"
)

ax.set_yticks(range(len(correlation_matrix.index)))
ax.set_yticklabels(correlation_matrix.index)

ax.set_title("Antibiotic Resistance Correlation")

fig.colorbar(im, ax=ax, label="Correlation")

for i in range(len(correlation_matrix)):
    for j in range(len(correlation_matrix.columns)):
        ax.text(
            j,
            i,
            f"{correlation_matrix.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

fig.tight_layout()

os.makedirs(
    r"C:\Users\DR.ARSHIA\Desktop\py project\figures",
    exist_ok = True
)

fig.savefig(
     r"C:\Users\DR.ARSHIA\Desktop\py project\figures\antibiotic_resistance_correlation_heatmap.png",
     dpi = 300,
     bbox_inches = 'tight'
)

plt.show()

print("-------------------------------------------------------------")
# Is a bacterial sample resistant to multiple antibiotics simultaneously?
resistance_count_per_sample = (
    resistance_matrix.sum(axis=1)
)

print(resistance_count_per_sample.head())

resistance_distribution = (
    resistance_count_per_sample
    .value_counts()
    .sort_index()
)
print(resistance_distribution)
print("-------------------------------------------------------------")
# Resistance distribution plot
fig, ax = plt.subplots(figsize= (8, 5))

x = (resistance_distribution.index)

bars = ax.bar(
    x, 
    resistance_distribution, 
    label = 'resistance count per sample'
)

ax.set_xlabel('Number of Resistant Antibiotics')
ax.set_ylabel('sample count')

ax.set_title("Distribution of Antibiotic Resistance per Sample")

ax.bar_label(bars, fmt='%d')
ax.grid(
    axis = 'y',
    linestyle = '--',
    alpha = 0.3
)

os.makedirs(
    r"C:\Users\DR.ARSHIA\Desktop\py project\figures",
    exist_ok=True
)

fig.savefig(
    r"C:\Users\DR.ARSHIA\Desktop\py project\figures\resistance_distribution.png",
    dpi = 300,
    bbox_inches = 'tight'
)

plt.show()
print("-------------------------------------------------------------")
# Can we create a resistance profile for each sample?

resistance_matrix["Resistance Profile"] = resistance_matrix.apply(
    lambda row: "No resistance" if ", ".join(row[row == 1].index) == "" 
    else ", ".join(row[row == 1].index),
    axis=1
)

print(resistance_matrix.head(100))

#(df.columns.tolist())
#print(df.head())
#print(df.shape)
#print(df.columns)
#print(df)