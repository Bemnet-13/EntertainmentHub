# EntertainmentHub
EntertainmentHub is an AI powered movie and book recommendation system. This project uses Natural Language Processing to implement content-based and popularity based recommendation systems by using the TMDB-movie dataset and GoodBooks-10k dataset. It also uses Streamlit for great Frontend experience streamlining the HTTP requests with the recommendation system.

To run the application, follow these steps.
1. Run movie_recommender.ipynb and book_recommendation_system.ipynb to generate the required pkl files
2. Replace the API token for movie recommender with your own TMDB account API token to access movie poster. This step is manadatory for running the application. Otherwise, the HTTP request will fail to go through.
3. Run the application by using the command streamlit run app.py
The datasets used are found here
https://www.kaggle.com/datasets/zygmunt/goodbooks-10k
https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
