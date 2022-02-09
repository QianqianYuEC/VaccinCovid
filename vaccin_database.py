import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os
from vaccin_datahantering import Datahantering 


class Vaccin_database:

    def __init__(self, input_datavacc):
 
       self.data_vaccin = input_datavacc
       self.creat_database()
       self.seed_database()
       self.creat_tabel()
       self.copy_data_to_table()
       self.delete_useless_table()
       

    def creat_database(self):
       self.db = sqlite3.connect('vaccin_covid.db')
       self.cur = self.db.cursor()
       self.db_path =os.getcwd()+'\\vaccin_covid.db'
       print("Database has been created {0}.".format(self.db_path))
       
    def seed_database(self):
        "Import dataframe to SQL in database"
        self.data_vaccin.df_vacc_daily_number.to_sql('vacc_daily_number', self.db, if_exists='replace', index = False)
        self.data_vaccin.df_vacc_accum_number.to_sql('vacc_accum_number', self.db, if_exists='replace', index = False)
        self.data_vaccin.df_vacc_text_info.to_sql('vacc_text_info', self.db, if_exists='replace', index = False)

    def creat_tabel(self):
        "Create vacc_daily_table that include daily data info, 'iso_code and date' are composite Primary Key"
        self.cur.execute("""CREATE TABLE IF NOT EXISTS vacc_daily_table(
            iso_code text,
            date text, 
            daily_vaccinations real,
            daily_vaccinations_per_million real,
            PRIMARY KEY (iso_code, date))""")
        
        """Create vacc_accum_table that include accummulate data info, 
        'iso_code and date' are composite Primary Key, they are also Foreign Key which reference vacc_daily_table"""
        self.cur.execute("""CREATE TABLE IF NOT EXISTS vacc_accum_table(
            country text,
            iso_code text,
            date text, 
            total_vaccinations real,
            people_vaccinated real, 
            people_fully_vaccinated real,
            total_vaccinations_per_hundred real, 
            people_vaccinated_per_hundred real,
            people_fully_vaccinated_per_hundred real,
            PRIMARY KEY (iso_code, date)
            FOREIGN KEY (iso_code, date) REFERENCES vacc_daily_table (iso_code, date))
            """)
        
        """Create vacc_text_table that include all text info, 
        'country_ID' are Primary Key, which is also Foreign Key that reference vacc_daily_table"""
        self.cur.execute("""CREATE TABLE IF NOT EXISTS vacc_text_table(
            country_ID text PRIMARY KEY, 
            iso_code text, 
            a text, 
            b text, 
            c text,
            d text,
            e text,
            f text,
            g text,
            source_name text,
            source_website text,
            FOREIGN KEY (iso_code) REFERENCES vacc_daily_table (iso_code))
            """)

    def copy_data_to_table(self):
        "Insert relative data to three tables which have relation with each other"
        self.cur.execute("INSERT OR REPLACE INTO vacc_daily_table SELECT * FROM vacc_daily_number")
        self.cur.execute("INSERT OR REPLACE INTO vacc_accum_table SELECT * FROM vacc_accum_number")
        self.cur.execute("INSERT OR REPLACE INTO vacc_text_table SELECT * FROM vacc_text_info")
        
        print("There are three relational tables in database.")

    def delete_useless_table(self):
        "Delete the three useless tables"
        self.cur.execute("DROP TABLE IF EXISTS vacc_daily_number")
        self.cur.execute("DROP TABLE IF EXISTS vacc_accum_number")
        self.cur.execute("DROP TABLE IF EXISTS vacc_text_info")
        self.db.commit()


    def get_db_path(self):
       return self.db_path


