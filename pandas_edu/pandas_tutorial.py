# File: pandas_tutorial.py 
# Description: A simple tutorial to demonstrate basic operations in pandas.

# Importing the pandas library
import pandas as pd
import numpy as np

# Import data from a CSV file
movies = pd.read_csv("movies.csv")

# Display the first few rows of the DataFrame
movies.head()

# We can use a column as an index and this column must be the one that uniquely identifies each row
movies = pd.read_csv("movies.csv", index_col="Title")

# Display the first few rows of the DataFrame with the new index
movies.head()


# Manipulating the DataFrame
    # - extracting few rows
movies.head(4)
movies.tail(4)
    # -check the length of the DataFrame
len(movies)
    # - check the total number of cells
movies.size
    # - check the data types of each column
movies.dtypes
    # - check the shape of the DataFrame
movies.shape
    # pull specific row from the dataset by its numeric order using its index position.
movies.iloc[499]  
    # - pull specific row from the dataset by its index label 
movies.loc["The Godfather"]
movies.loc["Forrest Gump"]
movies.loc["101 Dalmatians"] # try to keep index label unique if possible
    # Sorting of the data by a specific column
movies.sort_values(by = "Year", ascending=False).head()
    # Sorting by multiple columns
movies.sort_values(by = ["Studio", "Year"]).head()
    # Sorting by index
movies.sort_index().head()


# Counting values in a series
# - we get a series from a dataframe by extracting a column
movies["Studio"] # - we can count the number of occurrences of each value in the series
movies["Studio"].value_counts().head(10)


# Filtering a column by one or more criteria
# - we can filter the DataFrame by a specific cell value
movies[movies["Studio"] == "Universal"].sort_values(by = "Year", ascending = False)
# - this can be stored to provide context for readers
universal_movies = movies[movies["Studio"] == "Universal"].sort_values(by = "Year", ascending = False)
# - we can filter the DataFrame by multiple criteria -- This is done by using the & operator
universal_movies = movies["Studio"] == "Universal"
release_in_2015 = movies["Year"] == 2015
movies[universal_movies & release_in_2015]
# - we can filter the DataFrame by multiple criteria using the | operator
universal_movies = movies["Studio"] == "Universal"
release_in_2015 = movies["Year"] == 2015
movies[universal_movies | release_in_2015]
# Filtering by > or < operators
before_1975 = movies[movies["Year"] < 1975]
before_1975
# Filtering using a range between which all values must fall. 
mid_80s = movies[movies["Year"].between(1983, 1986)]
mid_80s

# Filtering the string index values
# - we can filter the DataFrame by a specific string value in the index
has_dark_in_title = movies[movies.index.str.lower().str.contains("dark")]
has_dark_in_title
# - we can filter the DataFrame by a specific string value in the index using regex
has_dark_in_title = movies[movies.index.str.contains("dark", case=False, regex=True)]
has_dark_in_title
# - we can filter the DataFrame by a specific string value in the index using regex and a specific pattern
has_dark_in_title = movies[movies.index.str.contains(r"dark", case=False, regex=True)]
has_dark_in_title

# Grouping data
# - we can group the data by a specific column and get the aggregate values
# - we want to group the data by "Studio" and get the aggregate "Gross" values per studio
# - replace the $ sign and convert the comma to empty string
movies["Gross"].str.replace("$", "", regex=False).str.replace(",", "", regex=False).astype(float)

# to make this permanent in the DataFrame we need to impose it on the DataFrame
movies["Gross"] = movies["Gross"].str.replace("$", "", regex=False).str.replace(",", "", regex=False).astype(float)
movies.head()
# Now the change is permanent and further numerical operations can be performed on the data.
movies["Gross"].mean()

studios = movies.groupby("Studio")

studios["Gross"].count().sort_values(ascending=False)

# - we can get the sum of Gross values per studio
studios["Gross"].sum().sort_values(ascending=False)


## The DataFrame object - a collection of Series objects
pd.read_csv("nba.csv")

# it could be observed that pandas imports Birthday column as a string 
#  rather than a datetime object, we can use parse_dates parameter to convert it
nba = pd.read_csv("nba.csv", parse_dates=["Birthday"])

# Display the first few rows of the DataFrame
nba.head()
# Display the data types of each column
nba.dtypes

# Counting the number of columns of each data type
nba.dtypes.value_counts()

# knowing the index of the DataFrame
nba.index
# knowing the column index of the DataFrame
nba.columns
# knowing the dimensions of the DataFrame
nba.ndim
nba.shape
# knowing the size of the DataFrame - this includes all cells with NaN values
nba.size
# exclusing NaN values from the size
nba.count()
# getting the number of rows and columns in the DataFrame
nba.shape[0], nba.shape[1]
# we can add all the series values in the DataFrame together after excluding NaN values
nba.count().sum()

# Extract few sample rows from the DataFrame - This extracts a random sample of 10 rows from the DataFrame
nba.sample(10)

# To know the unique in the DataFrame
nba.nunique()

# Getting the max and min values in the DataFrame
nba.max()
nba.min()

# Identifying multiple max values or Top N values in the DataFrame
nba.nlargest(n=4, columns = "Salary")
# Identifying multiple min values or Bottom N values in the DataFrame
nba.nsmallest(n=4, columns = "Birthday")

# Summing all NBA salaries
nba.sum(numeric_only=True)
# Mean salary of all NBA players
nba.mean(numeric_only=True)
# Median salary of all NBA players
nba.median(numeric_only=True)
# Mode salary of all NBA players
nba.mode(numeric_only=True)
# Standard deviation of all NBA salaries
nba.std(numeric_only=True)
# Variance of all NBA salaries
nba.var(numeric_only=True, skipna=True)

## Sorting a DataFrame
# Sorting the DataFrame by a specific column
nba.sort_values(by = "Name", ascending=False).head()
# Sorting the DataFrame by multiple columns
nba.sort_values(by = ["Team", "Name"], ascending=[True, False]).head()
# Since the DataFrame looks better when sorted by Team and Salary, we can sort it by these two columns and 
# store it back in the same variable
nba = nba.sort_values(by = ["Team", "Salary"], ascending=[True, False])

# Sorting by row index
nba.sort_index().head() # or 
nba.sort_index(ascending=True).head()

# Storing the row index sorted data in a nba takes us back to the original DataFrame
nba = nba.sort_index(ascending=True)

# Sorting by column index
nba.sort_index(axis = "columns").head() # or
nba.sort_index(axis = 1).head() # this sorts the columns in ascending order by column names
nba.sort_index(axis = 1, ascending=False).head() # this sorts the columns in descending order by column names

# Setting a new index for the DataFrame
# - we can set a new index for the DataFrame using the set_index() method
nba.set_index(keys="Name") # this is better so lets overwrite the original DataFrame
nba = nba.set_index(keys="Name")

# We can set index right from the start when reading the CSV file
""" nba = pd.read_csv(
    "nba.csv", 
    index_col="Name", 
    parse_dates=["Birthday"]
    )
 """

# Selecting columns and rows from a DataFrame
  # Selecting columns
# - we can select a specific column from the DataFrame using the column name
nba["Position"] # this returns a Series object
# - we can select multiple columns from the DataFrame using a list of column names
nba[["Salary", "Birthday"]] # this returns a DataFrame object
# - we use the select_dtypes() method to select columns by their data type
nba.select_dtypes(include = "object") # this returns a DataFrame object with only object data type columns
nba.select_dtypes(include = "int") # this returns a DataFrame object with only integer data type columns
nba.select_dtypes(include = "datetime") # this returns a DataFrame object with only datetime data type columns
# - we can select all columns except the specified data type
nba.select_dtypes(exclude=["object", "int"])
# - we can select columns by their data type using a list of data types
nba.select_dtypes(include=["object", "datetime"])

  # Selecting rows
# - Selecting rows by index label
nba.loc["LeBron James"] # this returns a Series object
nba.loc[["Kawhi Leonard", "Paul George"]] # this returns a DataFrame object
# pandas always organises the rows in the order in which their index labels appears in the list. 
# it is recommended to sort the index labels before selecting rows
nba.sort_index().loc["Otto Porter":"Patrick Beverley"] # this returns a DataFrame object with rows from Otto Porter to Patrick Beverley
# loc can also be used to pull rows from the middle of the DataFrame to its end.
nba.sort_index().loc["Otto Porter":] # this returns a DataFrame object with rows from Otto Porter to the end
nba.sort_index().loc[:"Al Horford"] # this returns a DataFrame object with rows from the start to Al Horford

# Extracting rows by index position
nba.iloc[0] # this returns a Series object with the first row
nba.iloc[0:5] # this returns a DataFrame object with the first 5 rows
nba.iloc[0:5, 0:3] # this returns a DataFrame object with the first 5 rows and the first 3 columns
nba.iloc[:2] # this returns a DataFrame object with the first 2 rows
# we can also extract rows by steps
nba.iloc[0:5:2] # this returns a DataFrame object with every 2nd row from the first 5 rows

# Renaming columns and rows
# - we can rename columns using the rename() method
nba.columns
# rename the column "Salary" to "Pay"
nba.columns = ["Team", "Position", "Birthday", "Pay"]
nba.head(1)
# we can also rename columns using the rename() method
nba.rename(columns={"Date of Birth": "Birthday"})
# let's make this change permanent in the DataFrame
nba = nba.rename(columns={"Date of Birth": "Birthday"})
# - we can rename rows using the rename() method
nba.index
# rename the row "LeBron James" to "King James"
nba = nba.rename(
    index={"Giannis Antetokounmpo": "Greek Freak"}
    )
nba.loc["Greek Freak"] # this returns a Series object with the row "Greek Freak"

# Resetting an index
nba.set_index("Team").head()
# - we can reset the index of the DataFrame using the reset_index() method
nba.reset_index().head() # this returns a DataFrame object with the index reset to the default integer index
# - we can use the set_index() method to move the Team column back to the index
nba.reset_index().set_index("Team").head() # this returns a DataFrame object with the Team column as the index
nba = nba.reset_index().set_index("Team") # this makes the change permanent in the DataFrame

# Coding Challenge
# 1. Load the nfl.csv file into a DataFrame and perform the following operations:
nfl = pd.read_csv("nfl.csv", parse_dates=["Birthday"])
nfl.head()
# 2. Use the two ways to set Name as the index of the DataFrame
nfl = nfl.set_index(keys="Name") # method 1
nfl = pd.read_csv("nfl.csv", parse_dates=["Birthday"], index_col="Name") # method 2

nfl.count().sum() # this returns the number of non-null values in each column
nfl["Team"].value_counts() # this returns the number of occurrences of each value in the Team column

nfl.sort_values(by="Salary", ascending=False).head(5) # this returns the top 5 rows sorted by Salary in descending order

nfl.sort_values(by = ["Team", "Salary"], ascending=[True, False]).head() # this returns the top 5 rows sorted by Team in ascending order and Salary in descending order

nfl.reset_index().set_index(
    "Team").loc["New York Jets"
                ].head().sort_values(
                    by = "Birthday", 
                    ascending=True
                    ).head(1) # this returns the rows for the New York Jets sorted by Team

######################################################################
#                           Filtering a DataFrame                   #
######################################################################

pd.read_csv("employees.csv")

## Reducing a DataFrame's memory use
employees = pd.read_csv("employees.csv", parse_dates=["Start Date"])
employees.info()  # Check memory usage before optimization

# - Converting data types with the astype() method
employees["Mgmt"] = employees["Mgmt"].astype(bool)  # Convert Mgmt column to boolean
employees.tail()
employees.info()  # Check memory usage after optimization. There is a reduction in memory usage
# - converting "Salary" column from float to int
employees["Salary"].fillna(0).astype(int).tail()  # Convert Salary column to int, filling NaN with 0
employees["Salary"] = employees["Salary"].fillna(0).astype(int)
# check the unique values in the DataFrame
employees.nunique()
# we can make Gender column more memory efficient by converting it to a categorical data type
employees["Gender"]=employees["Gender"].astype("category")
employees.info()  # Check memory usage after optimization
employees.head()
# we can do the same for Team column
employees["Team"] = employees["Team"].astype("category")
employees.info()  # Check memory usage after optimization


# Extracting a DataFrame rows by one or more conditions
# - filtering by a single condition
employees[employees["First Name"] == "Maria"] # Returns rows where First Name is Maria

employees[employees["Team"] != "Finance"] # Returns rows where Team is not Finance

employees[employees["Mgmt"] == True]  # Returns rows where Mgmt is True

high_earners = employees["Salary"] > 100000  # Returns rows where Salary is greater than 100000
high_earners.head()
employees[high_earners].head()  # Returns rows where Salary is greater than 100000
# or 
employees[employees["Salary"] > 100000].head()  # Returns rows where Salary is greater than 100000

# - filtering by multiple conditions
is_female = employees["Gender"] == "Female" # condition one 

is_biz_dev = employees["Team"] == "Business Dev" # condition two

employees[is_female & is_biz_dev].head() # calculating the intersection of the two conditions

# now let's add a third condition to this 
is_manager = employees["Mgmt"] == True  # condition three

employees[is_female & is_biz_dev & is_manager]

# - Using the OR condition
earning_below_40k = employees["Salary"] < 40000  # condition one
started_after_2015 = employees["Start Date"] > "2015-01-01"  # condition two

employees[earning_below_40k | started_after_2015].tail()  # Returns rows where Salary is below 40k or Start Date is after 2015

# -- Inversion with "~" operator
employees[employees["Salary"] < 100000].head()  # Returns rows where Salary is less than 100000
employees[~(employees["Salary"] >= 100000)].head()  # Returns rows where Salary is less than 100000 using the inversion operator

# - Filtering by condition
# - Filtering by multiple conditions using the "isin()" method
all_star_teams = ["Sales", "Legal", "Marketing"]
employee_in_star_teams = employees[employees["Team"].isin(all_star_teams)]
employee_in_star_teams.head()  # Returns rows where Team is in the list of all star teams

# - The between() method -- Selecting columns values that fall between a range

between_80k_and_90k = employees["Salary"].between(80000, 90000) 
employees[between_80k_and_90k].head()  # Returns rows where Salary is between 80k and 90k

eighties_folk = employees["Start Date"].between(
    left="1980-01-01",
    right="1990-01-01"
)
employees[eighties_folk].head()  # Returns rows where Start Date is between 1980 and 1990

# we can also use between() for string columns
name_starts_with_r = employees["First Name"].between("R", "S")  # Returns rows where First Name starts with R or S
employees[name_starts_with_r].head()  # Returns rows where First Name starts with R
employees[name_starts_with_r].tail()  # Returns rows where First Name starts with S


# Filtering a DataFrame for rows that include or exclude null values
  # - Filtering for null values - isnull() and notnull() methods
employees.head()
  # isnull() method
employees["Team"].isnull().head()
employees["Start Date"].isnull().head()

  # notnull() method
employees["Team"].notnull().head() # preferred for opposite of isnull() method
(~employees["Team"].isnull()).head()  # This is the same as notnull() method

# - now lets extract all employees with a missing Team value
no_team = employees["Team"].isnull()  # condition to check for null values in Team column
employees[no_team].head()  # Returns rows where Team is null

# - you can pull data with no null values in a specific column
has_name = employees["First Name"].notnull()  # condition to check for non-null values in First Name column
employees[has_name].tail()  # Returns rows where First Name is not null

### Removing duplicate and null values from a DataFrame
# bring back the original dataset
employees = pd.read_csv("employees.csv", parse_dates=["Start Date"])

employees.dropna()  # This will drop all rows with any null values
employees.dropna(how="all").tail()  # This will drop rows where all values are null
employees.dropna(how="any")  # This will drop rows where any value is null

# - we can drop rows with null values in a specific column
employees.dropna(subset = ["Gender"]).tail()
# - we can drop rows with null values in multiple columns
employees.dropna(subset = ["Start Date", "Salary"]).head()

# - droping na with threshold
employees.dropna(thresh = 4).head()

# Dealing with duplicates
employees["Team"].head()  # Check the Team column for duplicates
employees["Team"].duplicated().head()  # Returns a boolean Series indicating duplicate values in Team column

# drop_duplicates() method
employees.drop_duplicates()
# - drop duplicates in a specific column
employees.drop_duplicates(subset = ["Team"])  # Returns rows with unique values in

# argument "keep" in drop_duplicates()
employees.drop_duplicates(subset = ["First Name"], keep=False)  # Returns rows with unique values in First Name column, dropping all duplicates

# droping duplicates using a list of columns
employees.drop_duplicates(subset = ["Gender", "Team"]).head()  # Returns rows with unique values in Gender and Team columns

