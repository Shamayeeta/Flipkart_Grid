# Flipkart Grid 5.0

## Problem Statement: Conversational Fashion Output Generator using GenAI

This repository contains the code for a GenAI-based Fashion Recommender Chatbot, **FashionKart**. The GitHub link is here - https://github.com/Shamayeeta/Flipkart_Grid
The application is live at - fashionkart.streamlit.app
## Run using Python environment
1. It is suggested to create a new conda environment with Python 3.11
2. Install the required libraries using
   >pip -r requirements.txt
3. Run the chatbot using the command
   >streamlit run langchain_togetherai.py

## Run using Docker
1. Build the image using the command in the project directory
 > docker build -t "fashionkart" . 
2. Run the container using the command
 > docker run -it -d --rm -p 5000:5000 fashionkart

## Team 
1. Aadarsh Shaw
2. Ananya Mehrotra
3. Shamayeeta Dass
