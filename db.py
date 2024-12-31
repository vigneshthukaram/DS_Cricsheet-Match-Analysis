import pandas as pd
from sqlalchemy import JSON, create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Setup SQLAlchemy and SQLite
Base = declarative_base()
engine = create_engine('sqlite:///cricket_matches.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Define the tables using SQLAlchemy ORM

class TestMatch(Base):
    __tablename__ = 'test_matches'
    id = Column(Integer, primary_key=True)
    match_date = Column(Date)
    match_type = Column(String)
    teams = Column(String)
    match_result = Column(String)
    outcome = Column(JSON)
    player_of_match = Column(String)
    runs_batter = Column(Integer)
    wickets_bowler = Column(Integer)
    extras_noballs = Column(Integer)
    runs_total = Column(Integer)
    over = Column(Float)
    team = Column(String)
    
class ODIMatch(Base):
    __tablename__ = 'odi_matches'
    id = Column(Integer, primary_key=True)
    match_date = Column(Date)
    match_type = Column(String)
    teams = Column(String)
    match_result = Column(String)
    outcome = Column(JSON)
    player_of_match = Column(String)
    runs_batter = Column(Integer)
    wickets_bowler = Column(Integer)
    extras_noballs = Column(Integer)
    runs_total = Column(Integer)
    over = Column(Float)
    team = Column(String)

class T20Match(Base):
    __tablename__ = 't20_matches'
    id = Column(Integer, primary_key=True)
    match_date = Column(Date)
    match_type = Column(String)
    teams = Column(String)
    match_result = Column(String)
    outcome = Column(JSON)
    player_of_match = Column(String)
    runs_batter = Column(Integer)
    wickets_bowler = Column(Integer)
    extras_noballs = Column(Integer)
    runs_total = Column(Integer)
    over = Column(Float)
    team = Column(String)

class IT20Match(Base):
    __tablename__ = 'it20_matches'
    id = Column(Integer, primary_key=True)
    match_date = Column(Date)
    match_type = Column(String)
    teams = Column(String)
    match_result = Column(String)
    outcome = Column(JSON)
    player_of_match = Column(String)
    runs_batter = Column(Integer)
    wickets_bowler = Column(Integer)
    extras_noballs = Column(Integer)
    runs_total = Column(Integer)
    over = Column(Float)
    team = Column(String)

# Create all tables in the SQLite database
Base.metadata.create_all(engine)

# Helper function to insert data from CSV into the database
def insert_data_from_csv(file_path, table_class):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Loop through the rows of the dataframe and add them to the table
    for index, row in df.iterrows():
        # Convert the match_date to a Python datetime.date JSON
        try:
            match_date = datetime.strptime(row['match_date'], '%Y-%m-%d').date()
        except ValueError:
            print(f"Skipping row due to invalid date format: {row['match_date']}")
            continue  # Skip rows with invalid date formats
        
        record = table_class(
            match_date=match_date,
            match_type=row['match_type'],
            teams=row['teams'],
            match_result=row['match_result'],
            player_of_match=row['player_of_match'],
            runs_batter=row['runs_batter'],
            wickets_bowler=row['wickets_bowler'],
            extras_noballs=row['extras_noballs'],
            runs_total=row['runs_total'],
            over=row['over'],
            team=row['team']
        )
        session.add(record)
    
    # Commit the session to save the changes
    session.commit()

# Example usage: insert data from CSVs into the respective tables
insert_data_from_csv('t20_matches.csv', T20Match)
insert_data_from_csv('test_matches.csv', TestMatch)
insert_data_from_csv('odi_matches.csv', ODIMatch)
insert_data_from_csv('it20_matches.csv', IT20Match)

print("Data inserted successfully into the database.")

# Close the session
session.close()
