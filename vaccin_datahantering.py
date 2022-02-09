import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

class Datahantering:

    def __init__(self,pathName):
        
    #self.path = 'C:/Users/QianqianYu/OneDrive/ECstudy/Python/python_programmering/Assignment/vaccin_covid.csv'
        
        self.vaccin_covid_df = pd.read_csv(pathName)
        self._preprocess()
        self._text_info()
        self._daily_data()
        self._accum_data()


    def _preprocess(self):
        "Remove unmeccessary column"
        self.vaccin_covid_df = self.vaccin_covid_df.drop(columns='daily_vaccinations_raw')
        
        "split colomn 'vaccines'"
        self.df_vc_split = self.vaccin_covid_df.vaccines.str.split(",",expand=True)
        self.df_vc_split = self.df_vc_split.rename(columns= {0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g"})
    
    def _text_info(self):
        
        "Purpose: extract all text info to a seperate table 'vacc_text_info'"
        "Creat new coloums that include all text information, delete duplicate information"
        iso_code=self.vaccin_covid_df["iso_code"].tolist()
        source_name=self.vaccin_covid_df["source_name"].tolist()
        source_website=self.vaccin_covid_df["source_website"].tolist()
        self.df_vc_split["iso_code"],self.df_vc_split["source_name"],self.df_vc_split["source_website"] = [iso_code,source_name,source_website]
        self.df_vacc_text_info = self.df_vc_split.drop_duplicates(keep='last')
        
        "Creat index 'country_ID, change the order of coloums"
        country_ID= [*range(1, 1+len(self.df_vacc_text_info), 1)]
        self.df_vacc_text_info.loc[:,'country_ID'] = country_ID
        self.df_vacc_text_info.set_index("country_ID")
        self.df_vacc_text_info = self.df_vacc_text_info[["country_ID","iso_code","a","b","c","d","e","f","g","source_name","source_website"]]
        
        #print(self.df_vacc_text_info.head())


    def _daily_data(self):
        
        "Purpose: extract daily data info to a seperate tabel 'vacc_daily_number'"
        self.df_vacc_daily_number = self.vaccin_covid_df[['iso_code','date','daily_vaccinations','daily_vaccinations_per_million']]
        
        "Replace all 'NaN' with '0'"
        "TODO: there is warning 'SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame', why?"
        self.df_vacc_daily_number.loc[:,'daily_vaccinations'].fillna(0,inplace=True)
        self.df_vacc_daily_number.loc[:,'daily_vaccinations_per_million'].fillna(0,inplace=True)

        #print(self.df_vacc_daily_number.head())
      

    def _accum_data(self):
        "Purpose: extract accumulate data info to a seperate tabel 'vacc_accum_number'"
        "Create new dataframe with all accumulate date and drop 'NaN'"
        self.df_vacc_accum_number = self.vaccin_covid_df.iloc[:,0:11].drop(columns=['daily_vaccinations','daily_vaccinations_per_million'])
        self.df_vacc_accum_number = self.df_vacc_accum_number.dropna()

        #print(self.df_vacc_accum_number.head())

