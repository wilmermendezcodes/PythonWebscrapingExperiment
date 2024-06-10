import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Establish a connection to your MySQL database
connection = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

# Define your SQL query
query = "SELECT pub_year FROM rabies_raw_data"

# Execute the query and fetch the results into a pandas DataFrame
df = pd.read_sql(query, connection)

# Close the database connection
connection.close()

# Plot number of publications per year
plt.figure(figsize=(10, 6))
sns.countplot(data=df, y='pub_year', order=df['pub_year'].value_counts().index)
plt.title('Number of Publications per Year')
plt.xlabel('Number of Publications')
plt.ylabel('Year')
plt.show()

# Check for missing values
print(df.isnull().sum())