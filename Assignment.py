# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 12:14:08 2019

@author: Sanjay-Sir
"""

import pymysql
import pandas as pd
import numpy as np
import pandas
import matplotlib.pyplot as plt
import seaborn as sns


conn=pymysql.connect(host='52.66.79.237',user='candidate',passwd='asdfgh123',db='servify_assignment')
cursor = conn.cursor()
query = 'select * from consumer'
query2 = 'select * from consumer_product'
query3 = 'select * from consumer_servicerequest'
query4 = 'select * from sold_plan'


Consumer = pandas.read_sql_query(query, conn)
Consumer.to_csv("C:/Users/Sanjay-Sir/Desktop/Servify Assignment/Consumer.csv", index=False)

Consumer_product = pandas.read_sql_query(query2, conn)
Consumer_product.to_csv("C:/Users/Sanjay-Sir/Desktop/Servify Assignment/Consumer_product.csv", index=False)

Consumer_servicerequest = pandas.read_sql_query(query3, conn)
Consumer_servicerequest.to_csv("C:/Users/Sanjay-Sir/Desktop/Servify Assignment/Consumer_servicerequest.csv", index=False)

Sold_plan = pandas.read_sql_query(query4, conn)
Sold_plan.to_csv("C:/Users/Sanjay-Sir/Desktop/Servify Assignment/Sold_plan.csv", index=False)


# Question one

Sold_plan['Year-Week'] = Sold_plan['DateOfPurchase'].dt.strftime('%Y-%U')

table =pd.pivot_table(Sold_plan, values='SoldPlanID', index=['Year-Week'], aggfunc='count') #making the pivot table

table.reset_index(level=0, inplace=True)

table_new=table.sort_values('SoldPlanID', ascending=False)# Sorting by highest

#Visualization
ax = table_new.plot(x="Year-Week",y="SoldPlanID",kind='bar',color="g")
sns.set(rc={'figure.figsize':(16.7,8.27)})

Average_number = table_new["SoldPlanID"].mean()
print(Average_number)

#Question 2

Sold_plan_abc=Sold_plan.join(Consumer_product.set_index('ConsumerID')['BrandID'], on='ConsumerID')

Sold_plan_abc=Sold_plan_abc.drop_duplicates(subset='SoldPlanID')
table2 =pd.pivot_table(Sold_plan_abc, values='SoldPlanID', index=['BrandID'], aggfunc='count') #making the pivot table

table2.reset_index(level=0, inplace=True)

table_new2=table2.sort_values('SoldPlanID', ascending=False)# Sorting by highest


#Visualization
bx = table_new2.plot(x="BrandID",y="SoldPlanID",kind='bar',color="g")

sns.set(rc={'figure.figsize':(16.7,12.27)})

Highest_brandID = table_new2.loc[table_new2['SoldPlanID'].idxmax()]
print(Highest_brandID)

#Question 3

Consumer_Servicerequest_abc=Consumer_servicerequest.join(Sold_plan.set_index('ConsumerID')['PlanID'], on='ConsumerID') #Vlookup

Consumer_Servicerequest_abc=Consumer_Servicerequest_abc.drop_duplicates(subset='ConsumerID')

Consumer_Servicerequest_final= Consumer_Servicerequest_abc[Consumer_Servicerequest_abc['PlanID'].notnull()]

table3 =pd.pivot_table(Consumer_Servicerequest_final, values='ConsumerServiceRequestID', index=['PlanID'], aggfunc='count') #making the pivot table

table3.reset_index(level=0, inplace=True)

table_new3=table3.sort_values('ConsumerServiceRequestID', ascending=False)# Sorting by highest

table_new3['perc']= table_new3['ConsumerServiceRequestID']/table_new3['ConsumerServiceRequestID'].sum() *100 #Calculating the Percentage


#Visualization
cx = table_new3.plot(x="PlanID",y="perc",kind='barh',color="b")

sns.set(rc={'figure.figsize':(6.7,9.2)})

#to check the percentage

print(table_new3)