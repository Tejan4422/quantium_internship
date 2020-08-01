import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('cleaned_data.csv')
df.columns
df['pkg_weight'] = df['PROD_NAME'].apply(lambda x: int(''.join(x for x in x if x.isdigit())))

heatmap_df = df[['PROD_QTY','TOT_SALES','LIFESTAGE','PREMIUM_CUSTOMER', 'pkg_weight']].copy()

dum = pd.get_dummies(heatmap_df)

h_labels = [x.replace('_', ' ').title() for x in 
            list(dum.select_dtypes(include=['number', 'bool']).columns.values)]
corr = dum.corr()
fig, ax = plt.subplots(figsize=(10,6))
sns_plot = sns.heatmap(corr, annot=True, xticklabels=h_labels, yticklabels=h_labels, cmap=sns.cubehelix_palette(as_cmap=True), ax=ax)
sns_plot.figure.savefig('heatmap.png')

dum['pkg_weight'].nunique()

ax = sns.barplot(x="pkg_weight", y="TOT_SALES", data=dum)
plt.xticks(rotation = 90)
plt.title('SALES DISTRIBUTION vs PACKAGE WEIGHT')
plt.savefig('bar_sales_pkg.png', dpi = 100)