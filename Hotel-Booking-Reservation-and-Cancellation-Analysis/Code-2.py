#!/usr/bin/env python
# coding: utf-8

# # Importing necessary libraries 

# In[1]:


import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


# In[2]:


df=pd.read_csv('Desktop\Datasets\hotel_bookings 2.csv')


# # EDA and Cleaning

# In[3]:


df.head() #First 5 rows


# In[4]:


df.tail() #Last 5 Rows


# In[5]:


df.shape #Total no. of rows and colums


# In[6]:


df.columns 


# In[7]:


df.info()


# In[8]:


from datetime import datetime


# In[9]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'],format="mixed")


# In[10]:


df.info()


# In[11]:


df.describe(include='object')


# In[12]:


for col in df.describe(include='object').columns:
    print(col)
    print(df[col].unique())
    print('-'*50)


# In[13]:


df.isnull().sum()


# In[14]:


df.drop(['company','agent'],axis=1 , inplace=True)
df.dropna(inplace=True)


# In[15]:


df.isnull().sum()


# In[16]:


df.describe()


# In[17]:


df = df[df['adr']<5000]


# # Data Analysis and Visualization

# In[18]:


canceled_perc = df['is_canceled'].value_counts(normalize=True) 
print(canceled_perc)
plt.figure(figsize = (5,4))
plt.title('Reservation_status_count')
plt.bar(['Not_Canceled','Canceled'],df['is_canceled'].value_counts(), edgecolor = 'k' , width = 0.75)
plt.show()


# In[19]:


plt.figure(figsize = (5,4))
ax1 = sns.countplot(x='hotel' , hue = 'is_canceled' , data = df , palette = 'Blues')
legend_labels,_= ax1. get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('Reservation status in different hotels' , size = 20)
plt.xlabel('hotels')
plt.ylabel('reservation status')


# In[20]:


# Above bar graph clearly shows that the number of reservations as well as cancellations of city hotels are high
resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize = True)


# In[21]:


city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize = True)


# In[22]:


# By now we have also seen in numbers that there is higher rate of cancellation at city hotels , so now we check the reasons , possibly beginning with the adr 
resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[23]:


plt.figure(figsize = (20,8))
plt.title('Average daily rate in both the Hotels' , fontsize = 20)
plt.plot(resort_hotel.index , resort_hotel['adr'], label = 'Resort Hotel')
plt.plot(city_hotel.index , city_hotel['adr'], label = 'City Hotel')
plt.legend(fontsize = 20)
plt.show


# In[25]:


df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize = (16,8))
ax1 = sns.countplot(x='month',hue='is_canceled',data=df,palette = 'bright')
legend_labels,_=ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('Reservation per month',size=20)
plt.xlabel('month')
plt.ylabel('number of reservations')
plt.legend('not canceled','canceled')
plt.show


# In[32]:


#From above graph we can understand that maximum cancellations are in January and maximum reservations are in August. So now we testing a hypothesis which is checking the correlation between Hotel pricing in the months and their reservations or cancellations.
plt.figure(figsize=(15,8))
plt.title('ADR per month', fontsize = 30)
sns.barplot(x='month',y='adr',data=df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index())
plt.legend(fontsize = 20)
plt.show()


# In[33]:


#After seeing the above graph it is visually appearing that the pricing and the cancellations are closely associated.Now we look onto the country wise cancellation rates.
cancelled_data = df[df['is_canceled'] == 1]
top_10_country=cancelled_data['country'].value_counts()[:10]
plt.figure(figsize = (8,8))
plt.title('Country-wise-Reservation-Cancellations')
plt.pie(top_10_country, autopct='%.2f' , labels = top_10_country.index)
plt.show()


# From above Pie Chart we can infer that the highest amount of cancellations are from Portuguese (70.7%)

# In[35]:


df['market_segment'].value_counts()


# Above data show that Online Travel Agencies have higher number of reservations.

# In[36]:


df['market_segment'].value_counts(normalize = True)


# In[37]:


cancelled_data['market_segment'].value_counts(normalize = True)


# The above values show us that corresponding to high reservations on online travel agencies, there is a significant percentage of cancellations on these.

# In[42]:


cancelled_df_adr=cancelled_data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace = True)
cancelled_df_adr.sort_values('reservation_status_date', inplace = True)

not_cancelled_data=df[df['is_canceled'] == 0]
not_cancelled_df_adr=not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_df_adr.reset_index('reservation_status_date', inplace = True)
not_cancelled_df_adr.sort_values

plt.figure(figsize = (20,6))
plt.title('Average Daily Rate')
plt.plot(not_cancelled_df_adr['reservation_status_date'],not_cancelled_df_adr['adr'],label='not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'],cancelled_df_adr['adr'], label= 'cancelled')
plt.legend()
plt.show()


# In[46]:


#As you can see data before 2016 in uneven so filter it out
cancelled_df_adr = cancelled_df_adr[(cancelled_df_adr['reservation_status_date'] > '2016') & (cancelled_df_adr['reservation_status_date'] < '2017-09')]
not_cancelled_df_adr = not_cancelled_df_adr[(not_cancelled_df_adr['reservation_status_date'] > '2016') & (not_cancelled_df_adr['reservation_status_date'] < '2017-09')]


# In[49]:


plt.figure(figsize = (20,6))
plt.title('Average Daily Rate' , fontsize=25)
plt.plot(not_cancelled_df_adr['reservation_status_date'],not_cancelled_df_adr['adr'],label='not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'],cancelled_df_adr['adr'], label= 'cancelled')
plt.legend()
plt.show()


# In[ ]:




