from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd
import mysql.connector


connection = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

# Define your SQL query
query = "SELECT * FROM rabies_raw_data"
# Execute the query and fetch the results into a pandas DataFrame
df = pd.read_sql(query, connection)
# Prepare the data for LDA
count_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
dtm = count_vectorizer.fit_transform(df['abstract'].dropna())


# Perform LDA
lda = LatentDirichletAllocation(n_components=5, random_state=0)
lda.fit(dtm)

feature_names = count_vectorizer.get_feature_names_out()
# Display the top words for each topic
topics_data = []
for index, topic in enumerate(lda.components_):
    top_words = [feature_names[i] for i in topic.argsort()[-10:]]
    topics_data.append({'Topic': index, 'Top Words': ', '.join(top_words)})

topics_df = pd.DataFrame(topics_data)

table_name = 'lda_rabies_topics'

# Create a cursor object
cursor = connection.cursor()

# Drop the table if it already exists
cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

# Create a new table
cursor.execute(f"CREATE TABLE {table_name} (Topic INT, Top_Words TEXT)")

# Insert data into the table
for index, row in topics_df.iterrows():
    cursor.execute(f"INSERT INTO {table_name} (Topic, Top_Words) VALUES (%s, %s)", (row['Topic'], row['Top Words']))

# Commit changes and close the connection
connection.commit()
connection.close()

print("Data saved to MySQL database.")