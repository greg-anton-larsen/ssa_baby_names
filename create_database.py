import requests
from time import sleep
import sqlite3
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

# (Re-)initialize SQlite3 database
# I've got columns for a given name, its gender, the year the data are from, plus...
# Where it ranked that year (there are frequently ties)... 
# And the percentage and count of babies assigned that gender with that name in that year
# Note that running this function resets and blanks out the database
def reset_db():
	con = sqlite3.connect("ssa_baby_names.db")
	cur = con.cursor()
	cur.execute('DROP TABLE if exists babynames')
	cur.execute('''CREATE TABLE babynames (name text, gender text, year integer, rank integer, percent real, count integer)''')
	con.commit()
	cur.close()

def name_acquire(year):
	# I'm pulling the information about baby names from web pages accessible at ssa.gov
	# Each page has a table of the top 1000 names for each gender (plus a couple sometimes in the event of a tie)
	# This function takes both
	# Unfortunately, the pages I'm drawing from don't give both percentages and counts at once
	
	# Get a table of each name and its percentages
	r_pct = requests.post('https://www.ssa.gov/cgi-bin/popularnames.cgi', 
					  data = {"year":str(year), "top":"1000", "number":"p"})
	soup_pct = BeautifulSoup(r_pct.text, 'html.parser')
	nametable_pct = soup_pct.find_all("table")[1].find_all("tr")
	
	 # Get a table of each name and its counts
	r_cnt = requests.post('https://www.ssa.gov/cgi-bin/popularnames.cgi', 
					  data = {"year":str(year), "top":"1000", "number":"n"})
	soup_cnt = BeautifulSoup(r_cnt.text, 'html.parser')
	nametable_cnt = soup_cnt.find_all("table")[1].find_all("tr")
	
	# Create an empty list, to be filled with the top 1000 male and female names in that year
	entries = []
	
	# The tables I'm pulling from have headers and an explanation row at the end
	# The table has the same info for one male name and one female name next to each other in a row
	for row_pct, row_cnt in zip(nametable_pct[2:-1], nametable_cnt[2:-1]):
		pct_entries = row_pct.find_all("td")
		cnt_entries = row_cnt.find_all("td")
		
		# How high the name was ranked for a given gender in a given year
		rank = pct_entries[0].text
		
		# The name itself
		male_name = pct_entries[1].text.replace('\xa0', '')
		female_name = pct_entries[3].text.replace('\xa0', '')
		
		# What percentage of babies assigned that gender were given that name
		male_percent = float(pct_entries[2].text[:-1])
		female_percent = float(pct_entries[4].text[:-1])
		
		# How many babies assigned that gender were given that name
		male_count = int(cnt_entries[2].text.replace(',',''))
		female_count = int(cnt_entries[4].text.replace(',',''))
		
		# Also include the gender of the name and the year in records for each of the two names
		entries.append([male_name, "male", year, rank, male_percent, male_count])
		entries.append([female_name, "female", year, rank, female_percent, female_count])
	return entries

# function to grab information from the years 1880-2021 and insert it all into the database
def db_pack():
	for year in range(1880, 2022):
		print("Fetching data for {}.".format(year))
		
		# Get the top 2000 names from a given year, along with key info about each name in that year
		namelist = name_acquire(year)
		
		# Connect to the database and put them all in
		con = sqlite3.connect("ssa_baby_names.db")
		cur = con.cursor()
		cur.executemany("insert into babynames values (?, ?, ?, ?, ?, ?)", namelist)
		con.commit()
		cur.close()
		
		# Slight pause between steps to avoid getting rate limited
		sleep(1)
	
if __name__ == "__main__":
	# When running the script, re-initialize the database
	reset_db()
	db_pack()