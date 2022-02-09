import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from vaccin_datahantering import Datahantering
from vaccin_database import Vaccin_database

class Visual_extract:

    def __init__(self, input_db_vacc):
        
        self.db_vacc = input_db_vacc
        self.db = sqlite3.connect(self.db_vacc)
        self.cur = self.db.cursor()
        #self.plot_daily_vaccination()

    def _extract_country_data(self):
        
        "Extract relative info when you input country iso_code and date"
        "TODO: return empty list if you input one date that not exists in vacc_accum_table, which because I droped all NaN in the table"

        self.input_iso_code = input("Enter country iso_code:")
        self.input_date = input("Enter the date:")
        
        self.cur.execute("""SELECT d.iso_code, d.date, d.daily_vaccinations,
        a.total_vaccinations, t.source_name
        FROM vacc_daily_table d
        JOIN vacc_accum_table a
        ON (a.iso_code = d.iso_code AND a.date = d.date)
        JOIN vacc_text_table t
        ON (d.iso_code = t.iso_code) 
        WHERE (d.iso_code = ? AND d.date = ?)""", 
        (self.input_iso_code, self.input_date))

        self.country_info = self.cur.fetchall()
        print(self.country_info)


    def plot_daily_vaccination(self):
        "Visuelize daily vaccine info when you input a country iso_code"
        "TODO: set condition and excption when input iso_code and date"

        self.input_iso_code = input("Enter country iso_code:")
        self.df_plot = pd.read_sql("""SELECT iso_code, date, daily_vaccinations 
        FROM vacc_daily_table WHERE iso_code = '%s'"""
        %self.input_iso_code, self.db)
        self.df_plot.plot(x='date', y ='daily_vaccinations', kind ='line', rot=45)
        plt.title(self.input_iso_code)
        plt.show()
        
