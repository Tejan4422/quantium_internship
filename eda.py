import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('QVI_purchase_behaviour.csv')
df1 = pd.read_excel('QVI_transaction_data.xlsx', sheet_name = 'in')
df1.isna().sum()

merged_df = pd.merge(df1, df, on = ['LYLTY_CARD_NBR'])
merged_df.isna().sum()
merged_df.LIFESTAGE.unique()
merged_df.LIFESTAGE.nunique()

merged_df.PREMIUM_CUSTOMER.unique()
merged_df.PREMIUM_CUSTOMER.nunique()

merged_df['premium'] = merged_df.apply(lambda x: x.TOT_SALES if x.PREMIUM_CUSTOMER == 'Premium' else 0, axis = 1)
merged_df['budget'] = merged_df.apply(lambda x: x.TOT_SALES if x.PREMIUM_CUSTOMER == 'Budget' else 0, axis = 1)
merged_df['mainstream'] = merged_df.apply(lambda x: x.TOT_SALES if x.PREMIUM_CUSTOMER == 'Mainstream' else 0, axis = 1)
#Customer type with bought quantity
merged_df['premium_qty'] = merged_df.apply(lambda x: x.PROD_QTY if x.PREMIUM_CUSTOMER == 'Premium' else 0, axis = 1)
merged_df['budget_qty'] = merged_df.apply(lambda x: x.PROD_QTY if x.PREMIUM_CUSTOMER == 'Budget' else 0, axis = 1)
merged_df['mainstream_qty'] = merged_df.apply(lambda x: x.PROD_QTY if x.PREMIUM_CUSTOMER == 'Mainstream' else 0, axis = 1)

merged_df.dtypes

data = [{'values' : merged_df['budget'].sum(), 'quantity' : merged_df['budget_qty'].sum()}, {'values': merged_df['premium'].sum(),
         'quantity' : merged_df['premium_qty'].sum()}, 
         {'values' : merged_df['mainstream'].sum(), 'quantity' : merged_df['mainstream_qty'].sum()}]

total_sales = pd.DataFrame(data, index = ['budget', 'premium', 'mainstream'])

#LIFESTAGE DATAFRAME
merged_df.LIFESTAGE.unique()
merged_df['young_cpl_sales'] = merged_df.apply(lambda x: x.TOT_SALES if x.LIFESTAGE == 'YOUNG SINGLES/COUPLES' else 0, axis = 1)
merged_df['midage_cpl_sales'] = merged_df.apply(lambda x: x.TOT_SALES if x.LIFESTAGE == 'MIDAGE SINGLES/COUPLES' else 0, axis = 1)
merged_df['new_fam_sales'] = merged_df.apply(lambda x: x.TOT_SALES if x.LIFESTAGE == 'NEW FAMILIES' else 0, axis = 1)
merged_df['older_fam_sales'] = merged_df.apply(lambda x: x.TOT_SALES if x.LIFESTAGE == 'OLDER FAMILIES' else 0, axis = 1)
merged_df['older_cpl_sales'] = merged_df.apply(lambda x: x.TOT_SALES if x.LIFESTAGE == 'OLDER SINGLES/COUPLES' else 0, axis = 1)
merged_df['retirees_sales'] = merged_df.apply(lambda x: x.TOT_SALES if x.LIFESTAGE == 'RETIREES' else 0, axis = 1)
merged_df['young_fml_sales'] = merged_df.apply(lambda x: x.TOT_SALES if x.LIFESTAGE == 'YOUNG FAMILIES' else 0, axis = 1)

#lifestage type with bought quantity
merged_df['young_cpl_qty'] = merged_df.apply(lambda x: x.PROD_QTY if x.LIFESTAGE == 'YOUNG SINGLES/COUPLES' else 0, axis = 1)
merged_df['midage_cpl_qty'] = merged_df.apply(lambda x: x.PROD_QTY if x.LIFESTAGE == 'MIDAGE SINGLES/COUPLES' else 0, axis = 1)
merged_df['new_fam_qty'] = merged_df.apply(lambda x: x.PROD_QTY if x.LIFESTAGE == 'NEW FAMILIES' else 0, axis = 1)
merged_df['older_fam_qty'] = merged_df.apply(lambda x: x.PROD_QTY if x.LIFESTAGE == 'OLDER FAMILIES' else 0, axis = 1)
merged_df['older_cpl_qty'] = merged_df.apply(lambda x: x.PROD_QTY if x.LIFESTAGE == 'OLDER SINGLES/COUPLES' else 0, axis = 1)
merged_df['retirees_qty'] = merged_df.apply(lambda x: x.PROD_QTY if x.LIFESTAGE == 'RETIREES' else 0, axis = 1)
merged_df['young_fml_qty'] = merged_df.apply(lambda x: x.PROD_QTY if x.LIFESTAGE == 'YOUNG FAMILIES' else 0, axis = 1)

merged_df.dtypes
#merged_df.to_csv('cleaned_data.csv', index = False)

data = [{'values' : merged_df['budget'].sum(), 'quantity' : merged_df['budget_qty'].sum()}, {'values': merged_df['premium'].sum(),
         'quantity' : merged_df['premium_qty'].sum()}, 
         {'values' : merged_df['mainstream'].sum(), 'quantity' : merged_df['mainstream_qty'].sum()}]

total_sales = pd.DataFrame(data, index = ['budget', 'premium', 'mainstream'])

merged_df['PREMIUM_CUSTOMER'].value_counts()
merged_df['LIFESTAGE'].value_counts()

colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
total_sales.plot(kind = 'pie', y = 'values', colors = colors, autopct='%1.0f%%', legend = False)
plt.title('SALES DISTRIBUTION BY CUSTOMER CATEGORIES')
plt.savefig('piechart_sales_dist.png', dpi = 100)
plt.show()  

colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
total_sales.plot(kind = 'pie', y = 'quantity', colors = colors, autopct='%1.0f%%', legend = False)
plt.title('QUANTITY DISTRIBUTION BY CUSTOMER CATEGORIES')
plt.savefig('piechart_qty_dist.png', dpi = 100)
plt.show()  


total_sales.plot(kind = 'bar', y = 'values')
plt.title('SALES DISTRIBUTION VS CUSTOMER TYPE')
plt.xticks(rotation = 0)
plt.savefig('bar_sales_dist.png', dpi = 100)


fig, ax = plt.subplots(figsize = (16,8))
sns.boxplot(x = 'LIFESTAGE', y = 'TOT_SALES', data = merged_df, ax = ax)
plt.savefig('outliers.png', dpi = 100)

merged_df.groupby(['LIFESTAGE'])['TOT_SALES'].mean().plot(kind='bar',figsize=(17,7))
plt.xticks(rotation = 0)
plt.title('LIFESTAGE VS TOTAL SALES (MEAN')
plt.savefig('bar_lifestage_vs_sales_mean.png', dpi = 100)

merged_df.groupby(['LIFESTAGE'])['TOT_SALES'].max().plot(kind='bar',figsize=(17,7))
plt.xticks(rotation = 0)
plt.title('LIFESTAGE VS TOTAL SALES (MAX)')
plt.savefig('bar_lifestage_vs_sales_max.png', dpi = 100)

merged_df.groupby(['LIFESTAGE'])['TOT_SALES'].min().plot(kind='bar',figsize=(17,7))
plt.xticks(rotation = 0)
plt.title('LIFESTAGE VS TOTAL SALES (MIN')
plt.savefig('bar_lifestage_vs_sales_min.png', dpi = 100)

data_qty = [{'values' : merged_df['young_cpl_sales'].sum(), 'quantity' : merged_df['young_cpl_qty'].sum()}, {'values': merged_df['midage_cpl_sales'].sum(),
         'quantity' : merged_df['midage_cpl_qty'].sum()}, 
         {'values' : merged_df['new_fam_sales'].sum(), 'quantity' : merged_df['new_fam_qty'].sum()},
         {'values' : merged_df['older_fam_sales'].sum(), 'quantity' : merged_df['older_fam_qty'].sum()},
         {'values' : merged_df['older_cpl_sales'].sum(), 'quantity' : merged_df['older_cpl_qty'].sum()},
         {'values' : merged_df['retirees_sales'].sum(), 'quantity' : merged_df['retirees_qty'].sum()},
         {'values' : merged_df['young_fml_sales'].sum(), 'quantity' : merged_df['young_fml_qty'].sum()}         
]

total_sales_lifestage = pd.DataFrame(data_qty, index = ['young_cpl', 'midage_cpl', 'new_fam', 'older_fam',
                                          'older_cpl','retirees', 'ypung_fml'])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
total_sales_lifestage.plot(kind = 'pie', y = 'values', colors = colors, autopct='%1.0f%%', legend = False)
plt.title('SALES DISTRIBUTION BY CUSTOMER LIFESTAGE')
plt.savefig('piechart_sales_dist_lifestage.png', dpi = 100)
plt.show()  

colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
total_sales_lifestage.plot(kind = 'pie', y = 'quantity', colors = colors, autopct='%1.0f%%', legend = False)
plt.title('QUANTITY DISTRIBUTION BY CUSTOMER LIFESTAGE')
plt.savefig('piechart_qty_dist_lifestage.png', dpi = 100)
plt.show()  

total_sales_lifestage.plot(kind = 'bar', y = 'values')
plt.xticks(rotation = 0)
plt.title('LIFESTAGE VS TOTAL SALES')
plt.savefig('bar_sales_dist_lifestage.png', dpi = 100)


data_qty_means = [{'values' : merged_df['young_cpl_sales'].mean(), 'quantity' : merged_df['young_cpl_qty'].mean()}, {'values': merged_df['midage_cpl_sales'].mean(),
         'quantity' : merged_df['midage_cpl_qty'].mean()}, 
         {'values' : merged_df['new_fam_sales'].mean(), 'quantity' : merged_df['new_fam_qty'].mean()},
         {'values' : merged_df['older_fam_sales'].mean(), 'quantity' : merged_df['older_fam_qty'].mean()},
         {'values' : merged_df['older_cpl_sales'].mean(), 'quantity' : merged_df['older_cpl_qty'].mean()},
         {'values' : merged_df['retirees_sales'].mean(), 'quantity' : merged_df['retirees_qty'].mean()},
         {'values' : merged_df['young_fml_sales'].mean(), 'quantity' : merged_df['young_fml_qty'].mean()}         
]

mean_df = pd.DataFrame(data_qty_means, index = ['young_cpl', 'midage_cpl', 'new_fam', 'older_fam',
                                          'older_cpl','retirees', 'ypung_fml'])

mean_df.plot(kind = 'bar', y = 'values')
plt.title('TOTAL SALES BEHAVIOUR BY LIFESTAGE(MEAN)')
plt.xticks(rotation = 0)
plt.savefig('bar_sales_mean_lifestage.png', dpi = 100)

mean_df.plot(kind = 'bar', y = 'quantity')
plt.title('TOTAL QUANTITY BOUGHT BEHAVIOUR BY LIFESTAGE(MEAN)')
plt.xticks(rotation = 0)
plt.savefig('bar_quantity_mean_lifestage.png', dpi = 100)



