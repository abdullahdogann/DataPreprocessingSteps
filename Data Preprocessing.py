## Data preprocessing steps

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#maindata = pd.read_excel(r"")

#maindata.to_csv(r"") # reading much more faster

maindata2 = pd.read_csv(r"")
data=maindata2.copy() # keeping main data
data.drop(data.columns[[0]],axis=1, inplace=True) # data.columns[[0]] there is no columns name, axis=1 {0 rows, 1 columns} , inplace=True keeping changes

data.rename(columns={"Invoice":"Fatura No", "StockCode":"Stok Kodu", "Description":"Ürün Adı", "Quantity":"Adet", "InvoiceDate":"Fatura Tarihi", "Price":"Birim Fiyat",
                     "Customer ID":"Müşteri ID", "Country":"Ülke"},inplace=True) # renaming Turkish name

data["Toplam Tutar"]=data["Birim Fiyat"]*data["Adet"] # total price

#convert data types
data["Fatura Tarihi"]=pd.to_datetime(data["Fatura Tarihi"])

#deleting columns
data.drop("Müşteri ID", axis=1, inplace=True)

## Missing Value Analysis
data.isnull().sum() # total missing value

#data["Ürün Adı"].fillna(data["Ürün Adı"].mode()[0], inplace=True)

#rate=(data["Ürün Adı"].isnull().sum())/len(data)
#print(rate*100) # 0.26 delete null values cause the rate is low

data.dropna(axis=0, inplace=True) # deleting null values
data.reset_index(drop=True, inplace=True)

cancel=data[data["Fatura No"].str.startswith("C",na=False)] # finding start with 'C'
cancalindex=[]

for i in cancel.index:
    cancalindex.append(i)


data.drop(data.index[cancalindex], inplace=True)
data.reset_index(drop=True, inplace=True)


error=data[(data["Fatura No"].str.len()!=6) | (~data["Fatura No"].str.isdigit())] # found those that are not 6 digits and containing all of them not integer for invoice number

errorindex=[]

for j in error.index:
    errorindex.append(j)

data.drop(data.index[errorindex], inplace=True)
data.reset_index(drop=True, inplace=True)


stok_error = data[(data["Stok Kodu"].str.len()!=5) | (~data["Stok Kodu"].str.isdigit())] # found those that are not 5 digits and containing all of them not integer for stock code


stok_error2 = data[~data["Stok Kodu"].str.isdigit()]

stok_error_index = []

for k in stok_error2.index:
    stok_error_index.append(k)

data.drop(data.index[stok_error_index], inplace=True)
data.reset_index(drop=True, inplace=True)


error4 = data[data["Adet"] <= 0]


error4_index = []

for k in error4.index:
    error4_index.append(k)

data.drop(data.index[error4_index], inplace=True)
data.reset_index(drop=True, inplace=True)



error5 = data[data["Birim Fiyat"] <= 0]


error5_index = []

for k in error5.index:
    error5_index.append(k)

data.drop(data.index[error5_index], inplace=True)
data.reset_index(drop=True, inplace=True)

#Outliers

for j in ["Adet", "Birim Fiyat", "Toplam Tutar"]:
    Q1=data[j].quantile(0.25)
    Q3=data[j].quantile(0.75)
    IQR=Q3-Q1

    ustsınır= Q3+1.5*IQR
    altsınır=Q1-1.5*IQR

    aykiri=data[(data[j]>ustsınır) | (data[j]<altsınır)]

error6_index = []

for i in aykiri.index:
    error5_index.append(i)

data.drop(data.index[error6_index], inplace=True)
data.reset_index(drop=True, inplace=True)



# one hot encoder

# print(len(set(data["Ülke"]))) # distinct country count

data=pd.get_dummies(data=data,columns=["Ülke"],drop_first=True)

print(data.info())















