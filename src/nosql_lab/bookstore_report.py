#!/usr/bin/env python3
import os
import sys
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# Module-level variables for MongoDB connection credentials
MONGODB_ATLAS_URL = os.environ.get("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.environ.get("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.environ.get("MONGODB_ATLAS_PWD")

# Configure logging to report connection status and errors
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    """
    Main function that connects to MongoDB, selects the database and collections,
    retrieves specific authors and their linked books, and prints the report.
    """
    if not MONGODB_ATLAS_URL or not MONGODB_ATLAS_USER or not MONGODB_ATLAS_PWD:
        logging.error("Missing one or more MongoDB environment variables.")
        sys.exit(1)

    client = None
    try:
        logging.info("Attempting to connect to MongoDB Atlas...")
        # Open the MongoDB client
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            serverSelectionTimeoutMS=5000
        )
        # Ping the server to verify the connection is active
        client.admin.command('ping')
        logging.info("Successfully connected to MongoDB Atlas.")
        
        # Select the 'bookstore' database
        db = client["bookstore"]
        
        # Select the 'authors' and 'books' collections
        authors_collection = db["authors"]
        books_collection = db["books"]
        
        # Define a list of author _ids. 
        # 'author_001' and 'author_003 are from the loaded files.
        # 'author_004' is what was added. 
        author_ids_to_query = ["author_001", "author_003", "author_004"]
        
        # Print the total number of authors in the list
        print(f"Total number of authors in the list: {len(author_ids_to_query)}")
        print(f"      ")
        
        # Iterate over each author _id in the list
        for author_id in author_ids_to_query:
            # Query the authors collection for the current author _id
            author = authors_collection.find_one({"_id": author_id})
            
            if author:
                author_name = author.get("name", "Unknown Name")
                # Print the author's name
                print(f"Author: {author_name}")
                
                # Query the books collection for books linked to this author
                # The author_ids can be a single string or an array of strings in the document
                books = books_collection.find({"author_ids": author_id})
                
                books_list = list(books)
                if books_list:
                    # Print each linked book's title and published year
                    for book in books_list:
                        title = book.get("title", "Unknown Title")
                        year = book.get("published_year", "Unknown Year")
                        print(f"   {title} ({year})")
                else:
                    print("   No books found for this author.")
            else:
                # If author not found in the DB, print a placeholder
                print(f"Author ID '{author_id}' not found in the database.")
            
            print(f"        ")

    except (ConnectionFailure, OperationFailure) as e:
        # Catch and log connection or authentication errors
        logging.error(f"MongoDB Connection/Authentication Error: {e}")
    except Exception as e:
        # Catch and log any other unexpected errors
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        # Close the client connection in the finally block to ensure it always runs
        if client:
            client.close()
            logging.info("MongoDB connection closed.")

if __name__ == "__main__":
    main()
