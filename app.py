
import streamlit as st
import pickle
import pandas as pd
import os

def recommend(query=None):
    recommended_books = []

    if query is not None:
        # Check if the query matches any book name
        book_match = book[book["Book Name"].str.contains(query, case=False, na=False)]
        if not book_match.empty:
            book_index = book_match.index[0]
            distances = similarity[book_index]

            book_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[:4]

            for i in book_list:
                recommended_books.append(book.iloc[i[0]]["Book Name"])

    return recommended_books

# Load data and similarity matrix
book_dict = pickle.load(open('book_dict.pkl1', 'rb'))
book = pd.DataFrame(book_dict)
similarity = pickle.load(open('similarity.pkl1', 'rb'))

st.title("Book Recommender System")

# Input field for the search query using st.form
with st.form("search_form"):
    # Add an empty option at the beginning of the book names
    book_names = [""] + list(book["Book Name"].values)
    search_query = st.selectbox("Select a book:", book_names)

    # Use only st.form_submit_button to check if the form is submitted
    search_button = st.form_submit_button("Search")

# Fetch recommendations
if search_button and search_query:
    with st.spinner("Fetching recommendations..."):
        recommendations = recommend(query=search_query)

        if recommendations:
            # Display recommendations in two columns
            col1, col2 = st.columns(2)
            
            for i in range(0, len(recommendations), 2):
                with col1:
                    if i < len(recommendations):
                        st.write(f"### {recommendations[i]}")
                        # Load and display poster from the "posters" folder
                        poster_path = os.path.join("posters", f"{recommendations[i]}.jpg")
                        if os.path.exists(poster_path):
                            # Set the image width directly
                            image_width_percent = 100  # Adjust this value to your preferred size
                            st.image(poster_path, width=image_width_percent)
                        else:
                            st.write("Poster not available")

                with col2:
                    if i + 1 < len(recommendations):
                        st.write(f"### {recommendations[i + 1]}")
                        # Load and display poster from the "posters" folder
                        poster_path = os.path.join("posters", f"{recommendations[i + 1]}.jpg")
                        if os.path.exists(poster_path):
                            # Set the image width directly
                            image_width_percent = 100  # Adjust this value to your preferred size
                            st.image(poster_path, width=image_width_percent)
                        else:
                            st.write("Poster not available")
        else:
            st.write("No recommendations found.")





