import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from scipy.stats import pearsonr

df = pd.read_csv('QVI_data.csv')
df.dtypes
df['STORE_NBR'].unique()

#Sorting data according to store numbers and date
lst = ['STORE_NBR', 'DATE']
df_trail = df.sort_values(by = lst)
df_trail.reset_index(inplace = True)
df_trail['BRAND'].unique()

df_trail['STORE_NBR'].nunique()

store_sales = pd.DataFrame(columns = ['STORE_NBR', 'TOT_SALES'])
store_sales['STORE_NBR'] = range(0, 272)
for i in range(0, 272):
    store_sales['TOT_SALES'][i] = np.where(df_trail['STORE_NBR']==i, df_trail['TOT_SALES'],0).sum()

df_trail['DATE'] = pd.to_datetime(df_trail['DATE'])
df_trail['MONTH'] = df_trail['DATE'].dt.month 
df_trail['YEAR'] =  df_trail['DATE'].dt.year

df_trail.dtypes

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
yr_cor = []
mon_cor = []
pkg_cor = []
life_cor = []
cust_cor = []
num = []
stores = []
for i in range(1,273):
    num.append(i)
for i in num:
    if i == 76 or i == 92:
        continue
    df_temp = df_trail[df_trail['STORE_NBR'] == i]
    df_temp['LIFESTAGE'] = le.fit_transform(df_temp['LIFESTAGE'])
    df_temp['PREMIUM_CUSTOMER'] = le.fit_transform(df_temp['PREMIUM_CUSTOMER'])
    yr_cor.append(pearsonr(df_temp['TOT_SALES'], df_temp['YEAR'])[0])
    mon_cor.append(pearsonr(df_temp['TOT_SALES'], df_temp['MONTH'])[0])
    pkg_cor.append(pearsonr(df_temp['TOT_SALES'], df_temp['PACK_SIZE'])[0])
    life_cor.append(pearsonr(df_temp['TOT_SALES'], df_temp['LIFESTAGE'])[0])
    cust_cor.append(pearsonr(df_temp['TOT_SALES'], df_temp['PREMIUM_CUSTOMER'])[0])
    stores.append(i)

pearson_df = pd.DataFrame(columns = ['STORE_NBR', 'MONTH_COR', 'YEAR_COR', 'PACK_COR',
                                     'LIFESTAGE_COR', 'CUST_COR'])
pearson_df['STORE_NBR'] = stores
pearson_df['MONTH_COR'] = mon_cor
pearson_df['YEAR_COR'] = yr_cor
pearson_df['PACK_COR'] = pkg_cor
pearson_df['LIFESTAGE_COR'] = life_cor
pearson_df['CUST_COR'] = cust_cor

pearson_df['CORRELATION_77'] = pearson_df.apply(lambda x: x.MONTH_COR + x.YEAR_COR
          + x.PACK_COR if x.MONTH_COR > 0
          and x.YEAR_COR > 0 and x.PACK_COR > 0 and x.LIFESTAGE_COR < 0 and
          x.CUST_COR < 0 else 0, axis = 1)

pearson_df['CORRELATION_86'] = pearson_df.apply(lambda x: x.MONTH_COR + x.PACK_COR
          + x.LIFESTAGE_COR if x.MONTH_COR > 0
          and x.YEAR_COR < 0 and x.PACK_COR > 0 and x.LIFESTAGE_COR > 0 and
          x.CUST_COR < 0 else 0, axis = 1)

pearson_df['CORRELATION_88'] = pearson_df.apply(lambda x: x.YEAR_COR + x.PACK_COR
          + x.CUST_COR if x.MONTH_COR < 0
          and x.YEAR_COR > 0 and x.PACK_COR > 0 and x.LIFESTAGE_COR < 0 and
          x.CUST_COR > 0 else 0, axis = 1)

str_nos = [77, 82] 
sales = []
months = []
stores = []
year = []
mean_pkg = []
monthly_customers = []
monthly_transactions = []
lst = [2, 3, 4]
monthly_sales_77 = pd.DataFrame(columns = ['STORE_NBR', 'MONTH', 'YEAR', 'SALES', 
                                        'MONTHLY_CUSTOMERS', 
                                        'MONTHLY_TRANSACTIONS', 'MEAN_PKG_SIZE'])
for i in str_nos:
    df_test = df_trail[df_trail['STORE_NBR'] == i]
    #y.append(i)
    for j in lst:    
        #print(i)
        #y = (df_test['STORE_NBR'])
        sales.append(df_test[df_test['MONTH'] == j]['TOT_SALES'].sum())
        months.append(j)
        stores.append(i)
        monthly_transactions.append(len(df_test[df_test['MONTH'] == j]))
        monthly_customers.append(df_test[df_test['MONTH'] == j]['LYLTY_CARD_NBR'].nunique())
        mean_pkg.append(df_test[df_test['MONTH'] == j]['PACK_SIZE'].mean())

df_test[df_test['MONTH'] == 6]['TOT_SALES'].sum()
df_test = df_trail[df_trail['STORE_NBR'] == 1]

monthly_sales_77['STORE_NBR'] = stores
monthly_sales_77['SALES'] = sales
monthly_sales_77['MONTH'] = months
monthly_sales_77['MONTHLY_CUSTOMERS'] = monthly_customers
monthly_sales_77['MONTHLY_TRANSACTIONS'] = monthly_transactions
monthly_sales_77['MEAN_PKG_SIZE'] = mean_pkg

mon_1 = [2, 3, 4]
monthly_sales_77['YEAR'] = monthly_sales_77.MONTH.apply(lambda x: 2019 if x in mon_1 else 2018)
monthly_sales_77['TRAN_PER_CUST'] = monthly_sales_77['MONTHLY_TRANSACTIONS']/monthly_sales_77['MONTHLY_CUSTOMERS']
monthly_sales_77['TRAN_PER_CUST'] = monthly_sales_77['TRAN_PER_CUST'].fillna(value = 0)
monthly_sales_77['MEAN_PKG_SIZE'] = monthly_sales_77['MEAN_PKG_SIZE'].fillna(value = 0)
monthly_sales_77.to_csv('final_data.csv', index = False)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="SALES", hue = "SALES", data=monthly_sales_77, palette = colors)
plt.xticks(rotation = 90)
plt.title('SALES DISTRIBUTION OF 77 VS 82 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_sales_77.png', dpi = 100)


fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="MONTHLY_CUSTOMERS", hue = "MONTHLY_CUSTOMERS", data=monthly_sales_77, palette = colors)
plt.xticks(rotation = 90)
plt.title('CUSTOMER DISTRIBUTION OF 77 VS 82 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_cust_77.png', dpi = 100)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="MONTHLY_TRANSACTIONS", hue = "MONTHLY_TRANSACTIONS", data=monthly_sales_77, palette = colors)
plt.xticks(rotation = 90)
plt.title('TRANSACTION DISTRIBUTION OF 77 VS 82 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_tran_77.png', dpi = 100)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="MEAN_PKG_SIZE", hue = "MEAN_PKG_SIZE", data=monthly_sales_77, palette = colors)
plt.xticks(rotation = 90)
plt.title('PACKAGE SIZE DISTRIBUTION OF 77 VS 82 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_pkg_77.png', dpi = 100)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="TRAN_PER_CUST", hue = "TRAN_PER_CUST", data=monthly_sales_77, palette = colors)
plt.xticks(rotation = 90)
plt.title('TRANSACTION PER CUST DISTRIBUTION OF 77 VS 82 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_tpc_77.png', dpi = 100)
 

str_nos = [86, 160] 
sales = []
months = []
stores = []
year = []
mean_pkg = []
monthly_customers = []
monthly_transactions = []
lst = [2, 3, 4]
monthly_sales_86 = pd.DataFrame(columns = ['STORE_NBR', 'MONTH', 'YEAR', 'SALES', 
                                        'MONTHLY_CUSTOMERS', 
                                        'MONTHLY_TRANSACTIONS', 'MEAN_PKG_SIZE'])
for i in str_nos:
    df_test = df_trail[df_trail['STORE_NBR'] == i]
    #y.append(i)
    for j in lst:    
        #print(i)
        #y = (df_test['STORE_NBR'])
        sales.append(df_test[df_test['MONTH'] == j]['TOT_SALES'].sum())
        months.append(j)
        stores.append(i)
        monthly_transactions.append(len(df_test[df_test['MONTH'] == j]))
        monthly_customers.append(df_test[df_test['MONTH'] == j]['LYLTY_CARD_NBR'].nunique())
        mean_pkg.append(df_test[df_test['MONTH'] == j]['PACK_SIZE'].mean())

df_test[df_test['MONTH'] == 6]['TOT_SALES'].sum()
df_test = df_trail[df_trail['STORE_NBR'] == 1]

monthly_sales_86['STORE_NBR'] = stores
monthly_sales_86['SALES'] = sales
monthly_sales_86['MONTH'] = months
monthly_sales_86['MONTHLY_CUSTOMERS'] = monthly_customers
monthly_sales_86['MONTHLY_TRANSACTIONS'] = monthly_transactions
monthly_sales_86['MEAN_PKG_SIZE'] = mean_pkg

mon_1 = [2, 3, 4]
monthly_sales_86['YEAR'] = monthly_sales_77.MONTH.apply(lambda x: 2019 if x in mon_1 else 2018)
monthly_sales_86['TRAN_PER_CUST'] = monthly_sales_86['MONTHLY_TRANSACTIONS']/monthly_sales_86['MONTHLY_CUSTOMERS']
monthly_sales_86['TRAN_PER_CUST'] = monthly_sales_86['TRAN_PER_CUST'].fillna(value = 0)
monthly_sales_86['MEAN_PKG_SIZE'] = monthly_sales_86['MEAN_PKG_SIZE'].fillna(value = 0)
monthly_sales_86.to_csv('final_data.csv', index = False) 

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="SALES", hue = "SALES", data=monthly_sales_86, palette = colors)
plt.xticks(rotation = 90)
plt.title('SALES DISTRIBUTION OF 86 VS 160 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_sales_86.png', dpi = 100)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="MONTHLY_CUSTOMERS", hue = "MONTHLY_CUSTOMERS", data=monthly_sales_86, palette = colors)
plt.xticks(rotation = 90)
plt.title('CUSTOMER DISTRIBUTION OF 86 VS 160 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_cust_86.png', dpi = 100)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="MONTHLY_TRANSACTIONS", hue = "MONTHLY_TRANSACTIONS", data=monthly_sales_86, palette = colors)
plt.xticks(rotation = 90)
plt.title('TRANSACTION DISTRIBUTION OF 86 VS 160 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_tran_86.png', dpi = 100)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="MEAN_PKG_SIZE", hue = "MEAN_PKG_SIZE", data=monthly_sales_86, palette = colors)
plt.xticks(rotation = 90)
plt.title('PACKAGE SIZE DISTRIBUTION OF 86 VS 160 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_pkg_86.png', dpi = 100)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="TRAN_PER_CUST", hue = "TRAN_PER_CUST", data=monthly_sales_86, palette = colors)
plt.xticks(rotation = 90)
plt.title('TRANSACTION PER CUST DISTRIBUTION OF 86 VS 160 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_tpc_86.png', dpi = 100)


str_nos = [88, 261] 
sales = []
months = []
stores = []
year = []
mean_pkg = []
monthly_customers = []
monthly_transactions = []
lst = [2, 3, 4]
monthly_sales_88 = pd.DataFrame(columns = ['STORE_NBR', 'MONTH', 'YEAR', 'SALES', 
                                        'MONTHLY_CUSTOMERS', 
                                        'MONTHLY_TRANSACTIONS', 'MEAN_PKG_SIZE'])
for i in str_nos:
    df_test = df_trail[df_trail['STORE_NBR'] == i]
    #y.append(i)
    for j in lst:    
        #print(i)
        #y = (df_test['STORE_NBR'])
        sales.append(df_test[df_test['MONTH'] == j]['TOT_SALES'].sum())
        months.append(j)
        stores.append(i)
        monthly_transactions.append(len(df_test[df_test['MONTH'] == j]))
        monthly_customers.append(df_test[df_test['MONTH'] == j]['LYLTY_CARD_NBR'].nunique())
        mean_pkg.append(df_test[df_test['MONTH'] == j]['PACK_SIZE'].mean())

df_test[df_test['MONTH'] == 6]['TOT_SALES'].sum()
df_test = df_trail[df_trail['STORE_NBR'] == 1]

monthly_sales_88['STORE_NBR'] = stores
monthly_sales_88['SALES'] = sales
monthly_sales_88['MONTH'] = months
monthly_sales_88['MONTHLY_CUSTOMERS'] = monthly_customers
monthly_sales_88['MONTHLY_TRANSACTIONS'] = monthly_transactions
monthly_sales_88['MEAN_PKG_SIZE'] = mean_pkg

mon_1 = [2, 3, 4]
monthly_sales_88['YEAR'] = monthly_sales_77.MONTH.apply(lambda x: 2019 if x in mon_1 else 2018)
monthly_sales_88['TRAN_PER_CUST'] = monthly_sales_88['MONTHLY_TRANSACTIONS']/monthly_sales_88['MONTHLY_CUSTOMERS']
monthly_sales_88['TRAN_PER_CUST'] = monthly_sales_88['TRAN_PER_CUST'].fillna(value = 0)
monthly_sales_88['MEAN_PKG_SIZE'] = monthly_sales_88['MEAN_PKG_SIZE'].fillna(value = 0)
monthly_sales_88.to_csv('final_data.csv', index = False)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="SALES", hue = "SALES", data=monthly_sales_88, palette = colors)
plt.xticks(rotation = 90)
plt.title('SALES DISTRIBUTION OF 88 VS 261 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_sales_88.png', dpi = 100)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="MONTHLY_CUSTOMERS", hue = "MONTHLY_CUSTOMERS", data=monthly_sales_88, palette = colors)
plt.xticks(rotation = 90)
plt.title('CUSTOMER DISTRIBUTION OF 88 VS 261 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_cust_88.png', dpi = 100)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="MONTHLY_TRANSACTIONS", hue = "MONTHLY_TRANSACTIONS", data=monthly_sales_88, palette = colors)
plt.xticks(rotation = 90)
plt.title('TRANSACTION DISTRIBUTION OF 88 VS 261 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_tran_88.png', dpi = 100)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="MEAN_PKG_SIZE", hue = "MEAN_PKG_SIZE", data=monthly_sales_88, palette = colors)
plt.xticks(rotation = 90)
plt.title('PACKAGE SIZE DISTRIBUTION OF 88 VS 261 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_pkg_88.png', dpi = 100)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
colors = ['#708090', '#A9A9A9', '#7FFFD4', '#FF7F50']
ax = sns.barplot(x="MONTH", y="TRAN_PER_CUST", hue = "TRAN_PER_CUST", data=monthly_sales_88, palette = colors)
plt.xticks(rotation = 90)
plt.title('TRANSACTION PER CUST DISTRIBUTION OF 88 VS 261 FEB-19 TO APR-19')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.savefig('bar_final_tpc_88.png', dpi = 100)



