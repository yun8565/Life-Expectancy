from asyncio.windows_events import NULL
import pandas as pd 
from matplotlib import pyplot as plt
import numpy as np
import math
import seaborn as sns
import sklearn
from sklearn import linear_model
from sklearn import preprocessing
import statsmodels.api as sm
import pylab 
import scipy.stats as stats
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn import ensemble
from sklearn.model_selection import cross_val_score
import missingno as msno


# Country- Country
# Year- Year
# Status- Developed or Developing status
# Life Expectancy- Age(years)
# Adult Mortality- Adult Mortality Rates of both sexes(probability of dying between 15&60 years per 1000 population)
# Infant Deaths- Number of Infant Deaths per 1000 population
# Alcohol- Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol)
# Percent Expenditure- Expenditure on health as a percentage of Gross Domestic Product per capita(%)
# Hep B- Hepatitis B (HepB) immunization coverage among 1-year-olds(%)
# Measles- number of reported measles cases per 1000 population
# BMI- Average Body Mass Index of entire population
# U-5 Deaths- Number of under-five deaths per 1000 population
# Polio- Polio(Pol3) immunization coverage among 1-year-olds(%)
# Total Expenditure- General government expenditure on health as a percentage of total government expenditure(%)
# Diphtheria- Diphtheria tetanus toxoid and pertussis (DTP3) immunization coverage among 1-year-olds(%)
# HIV/AIDS- Deaths per 1000 live births HIV/AIDS(0-4 years)
# GDP- Gross Domestic Product per capita(in USD)
# Population- Population Thinness 10-19- Prevalence of thinness among children and adolescents for Age 10 to 19(%)
# Thinness 5-9- Prevalence of thinness among children for Age 5 to 9(%)
# Income Composition- Human Development Index in terms of income composition of resources(0-1)
# Schooling- Number of years of Schooling


df=pd.read_csv('Life Expectancy.csv')
pd.set_option('display.max_columns', None) 
df.columns=['Country', 'Year', 'Status', 'Life Expectancy', 'Adult Mortality',
       'Infant Deaths', 'Alcohol', 'Percent Expenditure', 'Hep B',
       'Measles', 'BMI', 'U-5 Deaths', 'Polio', 'Total Expenditure',
       'Diphtheria', 'HIV/AIDS','GDP', 'Population', 'Thinness 10-19',
       'Thinness 5-9', 'Income Composition', 'Schooling']

# 전처리
#Countries Mislabeled as Developing
df[df['Country']=='Greece']['Status'].replace('Developing','Developed')
df[df['Country']=='France']['Status'].replace('Developing','Developed')
df[df['Country']=='Finland']['Status'].replace('Developing','Developed')
df[df['Country']=='Canada']['Status'].replace('Developing','Developed')
df[df['Country']=='Republic of Korea']['Status'].replace('Developing','Developed')
df.head(10)

print(msno.matrix(df))

#이상치를 결측치로 변환
numcol=['Adult Mortality', 'Alcohol', 'Percent Expenditure', 'Hep B',
        'Measles', 'BMI','Polio', 'Total Expenditure',
        'Diphtheria', 'HIV/AIDS','GDP', 'Population', 'Thinness 10-19',
        'Thinness 5-9', 'Income Composition', 'Schooling'] 

for column in numcol:
    for i in range(len(df)):
        country=df['Country'][i]
        q3 = df[df['Country']==country][column].quantile(0.75)
        q1 = df[df['Country']==country][column].quantile(0.25)
        iqr = q3-q1

        if df[column][i] > q3 + 1.5 * iqr or df[column][i] < q1 - 1.5 * iqr:
            df[column][i] = np.NaN
        else:
            pass

print(df)

#결측치 출력
print(msno.matrix(df))
df.describe()

#결측치를 나라별 평균으로 채우기
# TODO: MICE 적용해보고 평균으로 채운것과 비교

for column in df.columns:
    for i in range(len(df)): 
        country=df['Country'][i]
        status=df['Country'][i]

        if (df[column].isnull()[i]==True):
            df[column][i]=df[df['Country']==country][column].mean() 
        else:
             pass

print(df)

df1=df[(df['Status']=='Developed')].fillna(df[(df['Status']=='Developed')].mean())
df2=df[(df['Status']=='Developing')].fillna(df[(df['Status']=='Developing')].mean())
df=df2.append(df1)
print(df.shape)

#결측치 채운 뒤
print(msno.matrix(df))
df.describe()
