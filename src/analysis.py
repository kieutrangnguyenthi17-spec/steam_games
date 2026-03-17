import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# LOAD DATA
df = pd.read_csv("../data/steam_games_dataset.csv")

print(df.info())
print(df.head())

# CLEAN DATA
df = df.drop_duplicates()

# Convert owners
def convert_owners(x):
    try:
        return int(str(x).split('-')[0])
    except:
        return 0

df['owners_clean'] = df['owners'].apply(convert_owners)

# Rating ratio
df['rating_ratio'] = df['positive'] / (df['positive'] + df['negative'] + 1)

sns.set_style("whitegrid")


# 1. TOP GAMES (RIÊNG)

top_games = df.sort_values(by='owners_clean', ascending=False).head(10)

plt.figure(figsize=(8,5))
sns.barplot(x='owners_clean', y='name', data=top_games)
plt.title("Top 10 Most Popular Games")
plt.tight_layout()
plt.savefig("../images/top_games.png")
plt.show()


# 2. PRICE VS RATING (RIÊNG)

plt.figure(figsize=(8,5))
sns.scatterplot(x='price', y='positive', data=df)
plt.yscale('log')
plt.title("Price vs Positive Ratings")
plt.tight_layout()
plt.savefig("../images/price_vs_rating.png")
plt.show()


# 3. TOP DEVELOPERS (THAY GENRE)

top_dev = df['developer'].value_counts().head(10)

plt.figure(figsize=(8,5))
sns.barplot(x=top_dev.values, y=top_dev.index)
plt.title("Top Developers")
plt.tight_layout()
plt.savefig("../images/top_developers.png")
plt.show()

# 4. CCU DISTRIBUTION

plt.figure(figsize=(8,5))
sns.histplot(df['ccu'], bins=50)
plt.title("CCU Distribution")
plt.tight_layout()
plt.savefig("../images/ccu_distribution.png")
plt.show()


# 5. CORRELATION HEATMAP

numeric_cols = df.select_dtypes(include=['int64', 'float64'])

plt.figure(figsize=(10,6))
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("../images/correlation_heatmap.png")
plt.show()


# DASHBOARD (TỔNG HỢP)

fig, axes = plt.subplots(3, 2, figsize=(16, 12))
fig.suptitle("Steam Games Dashboard", fontsize=16)

# 1
sns.barplot(x='owners_clean', y='name', data=top_games, ax=axes[0,0])
axes[0,0].set_title("Top Games")

# 2
sns.scatterplot(x='price', y='positive', data=df, ax=axes[0,1])
axes[0,1].set_yscale('log')
axes[0,1].set_title("Price vs Rating")

# 3
sns.barplot(x=top_dev.values, y=top_dev.index, ax=axes[1,0])
axes[1,0].set_title("Top Developers")

# 4
sns.histplot(df['ccu'], bins=50, ax=axes[1,1])
axes[1,1].set_title("CCU Distribution")

# 5
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', ax=axes[2,0])
axes[2,0].set_title("Correlation")

# hide empty
axes[2,1].set_visible(False)

plt.tight_layout()
plt.savefig("../dashboard/python_dashboard.png")
plt.show()