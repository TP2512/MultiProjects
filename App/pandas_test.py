import pandas as pd
d1={
    "a":[1,2,3,4],
    "b":[5,6,7,8],
    "c":[9,10,11,12]
}
df1=pd.DataFrame(d1)

print("dataframe from dictionary of lists:\n",df1)

l1=[[1,2,3,4],[5,6,7,8],[9,10,11,12]]
df2=pd.DataFrame(l1,index=[1,2,3],columns=['a','b','c','d'])
print("\ndataframe from list of lists:\n",df2)

print("concatenated dataframe append one df below other:\n",pd.concat([df1,df2]))
print("concatenated dataframe append one df besides other:\n",pd.concat([df1,df2],axis=1))

d2={
    'a':[4,5,6],
    'b':[7,8,9],
    'c':[10,11,12]
}

index=pd.MultiIndex.from_tuples([('d',1),('d',2),('e',2)],names=['n','v'])
df3=pd.DataFrame(d2,index=index)
print("multiindex dataframe from dict of listss:\n",df3)

print("melting of dataframe ")# melting is col into rows
d3={
    "Name" : ["Sangram", "Mangesh", "Tarkesh"],
    "Std" : [6,7,8],
    "History" : [90, 80, 70],
    "Maths" : [100,80,70],
    "Geo" : [50,60,70]
}
df1=pd.DataFrame(d3)
d4={
    "Name":["Sangram","Mangesh","Tarkesh"],
    "Address":["Ahamdanagr","Borovali","Solapur"],
    "Std":[6,7,8]
}
print("original df:\n",df1)
print("melted df:\n",(pd.melt(df1,id_vars=['Name','Std'],var_name="Subject",value_name="Score")))
df4=(pd.melt(df1,id_vars=['Name','Std'],var_name="Subject",value_name="Score")).query('Score>=70 and Std==6')
print("melted df with query more than 70 and class 6:\n",df4)
df4=(pd.melt(df1,id_vars=['Name','Std'],var_name="Subject",value_name="Score"))
print("melted df:\n",df4)
print("pivot rows into column:\n",df1.pivot(columns='Name',values='History'))
print("sorted values by column values(low to high):\n",df4.sort_values('Score'))
print("sorted values by column values(high to low):\n",df4.sort_values('Score',ascending=False))
df4.rename(columns={'Score':'Marks'},inplace=True)
print("df after changing column name:\n",df4)
print(df4.sort_index())
print("df after reseting index:\n",df4.reset_index())
print("df after deleting col Std:\n",df4.drop(columns=['Std']))
print(df4[df4.Marks>90])
print("Randomly select n rows:\n",df4.sample(n=3).reset_index())
print("n largest:\n",df4.nlargest(2,'Marks'))
print("n smallest:\n",df4.nsmallest(2,'Marks'))
print("first 4 rows:\n",df4.head(4))    #df4[:4]
print("last 4 rows:\n",df4.tail(4))    #df4[-4:]
print("df with specific colunms:\n",df4[["Name"]][:4])
print(df4[-4:])
print("df with specific column:\n",df4.Marks[:3])
print("filter using regex on column name:\n",df4.filter(regex="^N.*.e$")[:2])
print("querying df:\n",df4.query('Marks>70'))
print("querying df:\n",df4.query('Marks>70 and Name=="Sangram"'))
print("querying df:\n",df4.query('Name.str.startswith("M")',engine="python"))
print("select specific rows using iloc:\n",df4.iloc[2:4])
print("select specific rows:\n",df4[2:4])
print("select specific columns by position:\n",df4.iloc[:,2:4])
print("select specific columns by position:\n",df4.iloc[:,[1,3]])
print("select specific columns by name:\n",df4.loc[:,["Name","Std"]])
print("select specific data with query and specific columns:\n",df4.loc[df4.Marks>70,["Name"]])
print("select specific cell by index:\n",df4.iat[2,3])
print("select specific cell of perticular col name:\n",df4.at[4,"Std"])
print("count number of rows in one column with unique value of col:\n",df4.Name.value_counts())
print("no of rows in df:\n",len(df4))
print("shape of df row x col:\n",df4.shape)
print("describe all rows and column of df:\n",df4.describe())
print("sum of specific column:\n",df4.Marks.sum())
print("min of specific column:\n",df4.Marks.min())
print("max of specific column:\n",df4.Marks.max())
print("mean of specific column:\n",df4.Marks.mean())
print("count of specific column:\n",df4.Marks.count())
print("mean of specific column:\n",max(df4.Marks))
print("mean of specific column:\n",df4.Marks.mean())
print("original df:\n")
print("using apply:\n",df4.Subject.apply(lambda x:x[:4]))
print("group by std and avg of marks:\n",df4.groupby(by='Std')['Marks'].mean())
# print("groupby level index:\n",df4.groupby(level="ind"))
print(df4.rename(columns={'Markes':'M'}))
# print("group by std and avg of marks:\n",df4.groupby(level=0)['Marks'].mean())
print("use of agg function with groupby:\n",df4.groupby('Std')['Marks'].agg(['sum','mean','min','max','count']))
print("use of shift function with groupby:\n",df4.groupby('Std')['Marks'].shift(1))
print("use of shift function with groupby:\n",df4.groupby('Std')['Marks'].shift(-1))
# df4['Rank'] = df4['Marks'].rank()
# print("use of rank function :\n",df4)
# df4['Dense_Rank'] = df4['Marks'].rank(method='dense')
# print("use of dense rank function :\n",df4)
print("original df:\n",df4)
print("use of shift function with groupby:\n",df4.groupby('Std')['Marks'].rank(method='dense'))
print("adding new column into df using assign:\n",df4.assign(stdmarks=lambda df4: df4.Std+df4.Marks))


d3={
    "Name" : ["Sangram", "Mangesh", "Tarkesh","Wahid"],
    "Std" : [6,7,8,9],
    "History" : [90, 80, 70,90],
    "Maths" : [100,80,70,87],
    "Geo" : [50,60,70,66]
}
df1=pd.DataFrame(d3)
d4={
    "Name":["Sangram","Mangesh","Tarkesh"],
    "Address":["Ahamdanagr","Borovali","Solapur"],
    "Std":[6,7,8]
}
df2=pd.DataFrame(d4)

print("df1,df2:\n",df1,"\n",df2)

print("left join:\n ",pd.merge(df1,df2,how="left",on="Name"))
print("right join:\n ",pd.merge(df1,df2,how="right",on="Name"))
print("inner join:\n ",pd.merge(df1,df2,how="inner",on="Name"))
print("outer join:\n ",pd.merge(df1,df2,how="outer",on="Name"))

print("all match in 2nd df:\n",df1[df1.Name.isin(df2.Name)])
print("all not match in 2nd df:\n",df1[~df1.Name.isin(df2.Name)])
df1.plot.hist()
