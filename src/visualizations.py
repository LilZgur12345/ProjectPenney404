import matplotlib.pyplot as plt
import seaborn as sns

def heatmap(df, title):
    plt.figure(figsize=(12, 10))
    sns.heatmap(df, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title(title)
    plt.show()

