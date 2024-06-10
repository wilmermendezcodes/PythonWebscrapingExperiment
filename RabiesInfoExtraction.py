import mysql.connector
import nltk
from nltk.tokenize import word_tokenize

# Connect to MySQL database
connection = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

# Download NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Function to process abstracts
def process_abstracts(abstracts):
    processed_abstracts = []
    for abstract in abstracts:
        # Tokenize the abstract into words
        words = word_tokenize(abstract)
        
        # Perform part-of-speech tagging
        tagged_words = nltk.pos_tag(words)
        
        # Perform named entity recognition
        entities = nltk.chunk.ne_chunk(tagged_words)
        
        processed_abstracts.append(entities)
    return processed_abstracts

# Retrieve abstracts from the database
cursor = connection.cursor()
query = "SELECT abstract FROM rabies_raw_data"
cursor.execute(query)
rows = cursor.fetchall()

# Extract abstracts from rows
abstracts = [row[0] for row in rows]

# Process abstracts
processed_abstracts = process_abstracts(abstracts)

# Print or process the processed abstracts as needed
for abstract in processed_abstracts:
    print(abstract)

# Close cursor and connection
cursor.close()
connection.close()