# Social Security Baby Name Dataset
This is a dataset of the popularities of baby names among babies born in the United States between 1880 and 2021, which I scraped from the [U.S. Social Security Administration](https://www.ssa.gov/OACT/babynames/index.html). I'm using it to run longitudinal analyses to track names' popularity over time, some of which I'll be putting up here soon.

# Database Specifications
## babynames table
Each record provides information about a given name, assigned to a particular gender, in a particular year.
- name *string* A baby name.
- gender *string* The gender assigned to the babies accounted for by this record.
- year *integer* The year the record is from.
- rank *integer* The name's popularity. In case of a tie, both names receive the same rank.
- percent *real* Number of American babies born in that year.
- count *integer* Number of American babies born in that year.

# Contents
- ssa_baby_names.db *A one-table sqlite3 database*
- create_database.py *Used to create the database.*

# Limitations
This database only includes records for Americans who applied for Social Security cards, leaving out many, especially those who were born before the SSA began issuing cards at birth in 1938. It's also based exclusively on babies born in the United States, so the names of immigrants to the U.S. are not recorded here. Finally, the SSA records I scraped provided only the top 1000 names in a year for boys and girls - this means that any names outside the top 1000 are omitted from this dataset. In 2021, for example, any boy's name that was given fewer than 257 times was not counted, and the same is true for a girl's name given fewer than 217 times. For more information about the limitations of this dataset, please see the [SSA's notes.](https://www.ssa.gov/OACT/babynames/background.html)

