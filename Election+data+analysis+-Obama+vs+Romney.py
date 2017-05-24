
# coding: utf-8

# question to answer by this data analysis
# 1.) Who was being polled and what was their party affiliation?
# 2.) Did the poll results favor Romney or Obama?
# 3.) How do undecided voters effect the poll?
# 4.) Can we account for the undecided voters?
# 5.) How did voter sentiment change over time?
# 6.) Can we see an effect in the polls from the debates?

# In[1]:

import pandas as pd
from pandas import DataFrame,Series
import numpy as np


# In[2]:

import matplotlib.pyplot as plt
import seaborn as sb


# In[3]:

sb.set_style('whitegrid')


# In[4]:

get_ipython().magic('matplotlib inline')


# In[5]:

from __future__ import division
import requests


# In[6]:

from io import StringIO


# In[7]:

url = "http://elections.huffingtonpost.com/pollster/2012-general-election-romney-vs-obama.csv"

source = requests.get(url).text


pollData = StringIO(source)


# In[8]:

pollDf = pd.read_csv(pollData)

pollDf.info()


# In[9]:

pollDf.head()


# In[10]:

sb.factorplot('Affiliation',kind='count',data=pollDf)


# In[11]:

sb.factorplot('Affiliation',kind='count',data=pollDf,hue='Population')


# In[12]:

avg = pd.DataFrame(pollDf.mean()) 


# In[13]:

avg


# In[14]:

pollDf.mean()


# In[15]:

avg.drop('Number of Observations',axis=0,inplace=True)


# In[16]:

avg


# In[17]:

std = pd.DataFrame(pollDf.std())
std.drop('Number of Observations',axis=0,inplace=True)


# In[18]:

std.head()


# In[19]:

std.drop('Question Text',axis=0,inplace=True)


# In[20]:

std.drop('Question Iteration',axis=0,inplace=True)


# In[21]:

std


# In[22]:

avg.plot(yerr=std,kind='bar',legend=False)


# In[23]:

poll_avg = pd.concat([avg,std],axis=1) 
poll_avg.columns = ['Average','STD']


# In[24]:

poll_avg


# In[26]:

pollDf.plot(x='End Date',y=['Obama','Romney','Undecided'],marker='o',linestyle='')


# In[27]:

from datetime import datetime


# In[30]:

pollDf['Difference'] = (pollDf.Obama - pollDf.Romney)/100
pollDf.head()


# In[31]:

pollDf = pollDf.groupby(['Start Date'],as_index=False).mean()
pollDf.head()


# In[32]:

fig = pollDf.plot('Start Date','Difference',figsize=(12,4),marker='o',linestyle='-',color='red')


# In[36]:

row_in = 0
xlimit = []

for date in pollDf['Start Date']:
    if date[0:7] == '2012-10':
        xlimit.append(row_in)
        row_in +=1
    else:
        row_in += 1
        


# In[38]:

print(min(xlimit)) 
print(max(xlimit)) 


# In[41]:

#we printed the index of 2012-10


# In[44]:

fig = pollDf.plot('Start Date','Difference',figsize=(12,4),marker='o',linestyle='-',color='purple',xlim=(325,352))

#debates
plt.axvline(x=329+2, linewidth=4, color='grey')
plt.axvline(x=329+10, linewidth=4, color='grey')
plt.axvline(x=329+21, linewidth=4, color='grey')


# In[46]:

#Donors data
#The questions we will be trying to answer while looking at this Data Set is:

#1.) How much was donated and what was the average donation?
#2.) How did the donations differ between candidates?
#3.) How did the donations differ between Democrats and Republicans?
#4.) What were the demographics of the donors?
#5.) Is there a pattern to donation amounts?


# In[47]:

donor_df = pd.read_csv('Election_Donor_Data.csv')


# In[48]:

donor_df.info()


# In[49]:

donor_df.head()


# In[50]:

donor_df['contb_receipt_amt'].value_counts()


# In[53]:

don_mean = donor_df['contb_receipt_amt'].mean()

don_std = donor_df['contb_receipt_amt'].std()
#ecat type
print ('The average donation was %.2f with a std of %.2f' %(don_mean,don_std))


# In[54]:

top_donor = donor_df['contb_receipt_amt'].copy()

top_donor.sort()
top_donor


# In[55]:

# no negative values
top_donor = top_donor[top_donor >0]

top_donor.sort()

top_donor.value_counts().head(10)


# In[56]:

com_don = top_donor[top_donor < 2500]
com_don.hist(bins=100)


# In[57]:

candidates = donor_df.cand_nm.unique()

candidates


# In[58]:

party_map = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Huntsman, Jon': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}


donor_df['Party'] = donor_df.cand_nm.map(party_map)


# In[59]:

# Clear refunds
donor_df = donor_df[donor_df.contb_receipt_amt >0]

# Preview DataFrame
donor_df.head()


# In[60]:

donor_df.groupby('cand_nm')['contb_receipt_amt'].count()


# In[61]:

# Groupby candidate and then displayt the total amount donated
donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()


# In[63]:

# Start by setting the groupby as an object
cand_amount = donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()

# index 
i = 0

for don in cand_amount:
    print(" The candidate %s raised %.0f dollars " %(cand_amount.index[i],don))
    print('\n')
    i += 1


# In[64]:

# PLot out total donation amounts
cand_amount.plot(kind='bar')


# In[67]:

# Groupby party and then count donations
donor_df.groupby('Party')['contb_receipt_amt'].sum().plot(kind='bar')


# In[68]:

occupation_df = donor_df.pivot_table('contb_receipt_amt',
                                index='contbr_occupation',
                                columns='Party', aggfunc='sum')


# In[69]:

occupation_df.head(10)


# In[70]:

occupation_df.shape


# In[71]:

occupation_df = occupation_df[occupation_df.sum(1) > 1000000]
occupation_df.shape

occupation_df.plot(kind='bar')


# In[72]:


occupation_df.plot(kind='barh',figsize=(10,12),cmap='seismic')


# In[73]:


occupation_df.drop(['INFORMATION REQUESTED PER BEST EFFORTS','INFORMATION REQUESTED'],axis=0,inplace=True)


# In[74]:

# Set new ceo row as sum of the current two
occupation_df.loc['CEO'] = occupation_df.loc['CEO'] + occupation_df.loc['C.E.O.']
# Drop CEO
occupation_df.drop('C.E.O.',inplace=True)


# In[75]:

occupation_df.plot(kind='barh',figsize=(10,12),cmap='seismic')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



