#KULLANICI ve ZAMAN AGIRLIKLI KURS PUANI HESAPLAMA

#Average
#Time-Based Weighted Average
#User-Based Weighted Average
#Weighted Rating

#-----KÜTÜPHANE VE AYARLAR-------#
import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option("display.max_columns",None)
pd.set_option("display.max_rows",None)
pd.set_option("display.width",500)
pd.set_option("display.expand_frame_repr",False)
pd.set_option("display.float_format",lambda x:"%.5f"%x)


#-----TEMEL BİLGİLER-------#
#Python(A-Z):Veri Bilimi Kursu
#Puan: 4.8(4.764925)
#Toplam Puan: 4611
#Puan Yüzdeleri: 75,20,4,1,<1 (Puan Sıralaması: 5,4,3,2,1)
#Yaklaşıksal Sayısal Karşılıkları: 3458,922,184,46,6


#-----VERİ HAZIRLAMA-------#
df=pd.read_csv("course_reviews.csv")
df.head()
df.shape #toplam değerlendirme sayısı 4323

df["Rating"].value_counts()
df["Questions Asked"].value_counts()

df.groupby("Questions Asked").agg({"Questions Asked":"count",
                                   "Rating":"mean"}) #soru sayısına göre ortalama değerlendirme


#-----AVERAGE(Ortalama Puan Hesabı)-------#
df["Rating"].mean()


#-----TIME-BASED WEIGHTED AVERAGE(Puan Zamanlarına Göre Ağırlıklı Ortalama)-------#
df.info()
df["Timestamp"]=pd.to_datetime(df["Timestamp"]) #datetime yaptık

current_date = pd.to_datetime('2021-02-10 0:0:0')
df["days"] = (current_date - df["Timestamp"]).dt.days

df.loc[df["days"] <= 30, "Rating"].mean()
df.loc[(df["days"] > 30) & (df["days"] <= 90), "Rating"].mean()
df.loc[(df["days"] > 90) & (df["days"] <= 180), "Rating"].mean()
df.loc[(df["days"] > 180), "Rating"].mean()

#tarih aralıklarına ağırlık verdik
df.loc[df["days"] <= 30, "Rating"].mean() * 28/100 + \
df.loc[(df["days"] > 30) & (df["days"] <= 90), "Rating"].mean() * 26/100 + \
df.loc[(df["days"] > 90) & (df["days"] <= 180), "Rating"].mean() * 24/100 + \
df.loc[(df["days"] > 180), "Rating"].mean() * 22/100

#tarih aralıklarına ağırlık vermeyi fonksiyonlaştırdık(deneyler yapmak için)
def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[df["days"] <= 30, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["days"] > 30) & (dataframe["days"] <= 90), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["days"] > 90) & (dataframe["days"] <= 180), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["days"] > 180), "Rating"].mean() * w4 / 100

time_based_weighted_average(df)
time_based_weighted_average(df,w1=30,w2=28,w3=22,w4=20)


#-----USER-BASED WEIGHTED AVERAGE-------#
df.groupby("Progress").agg({"Rating": "mean"})

#kurs izlenme aralıklarına ağırlık verdik
df.loc[df["Progress"] <= 10, "Rating"].mean() * 22 / 100 + \
df.loc[(df["Progress"] > 10) & (df["Progress"] <= 45), "Rating"].mean() * 24 / 100 + \
df.loc[(df["Progress"] > 45) & (df["Progress"] <= 75), "Rating"].mean() * 26 / 100 + \
df.loc[(df["Progress"] > 75), "Rating"].mean() * 28 / 100

#kurs izlenme aralıklarına ağırlık vermeyi fonksiyonlaştırdık.
def user_based_weighted_average(dataframe, w1=22, w2=24, w3=26, w4=28):
    return dataframe.loc[dataframe["Progress"] <= 10, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 10) & (dataframe["Progress"] <= 45), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 45) & (dataframe["Progress"] <= 75), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 75), "Rating"].mean() * w4 / 100


user_based_weighted_average(df, 20, 24, 26, 30)


#-----WEIGHTED RATING-------#
#time weighted & user weighted
def course_weighted_rating(dataframe, time_w=50, user_w=50):
    return time_based_weighted_average(dataframe) * time_w/100 + user_based_weighted_average(dataframe)*user_w/100

course_weighted_rating(df)
course_weighted_rating(df, time_w=40, user_w=60)