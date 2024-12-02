#!/usr/bin/env python3
import requests
import pandas as pd
import numpy as np
BASE_URL = "https://api.squiggle.com.au/"
USER_AGENT = "Lucky's Tipping Bot - tom.lucken@gmail.com"

# Define initial Elo ratings for each team
teamnames = [
    'Sydney',
    'Melbourne',
    'Brisbane Lions',
    'Carlton',
    'Collingwood',
    'Essendon',
    'Fremantle',
    'Geelong',
    'Gold Coast',
    'Greater Western Sydney',
    'Hawthorn',
    'North Melbourne',
    'Port Adelaide',
    'Richmond',
    'St Kilda',
    'West Coast',
    'Western Bulldogs',
    'Adelaide',
    'Fitzroy']

initial_elo_ratings = {
    'Sydney': 1000,
    'Melbourne': 1000,
    'Brisbane Lions': 1000,
    'Carlton': 1000,
    'Collingwood': 1000,
    'Essendon': 1000,
    'Fremantle': 1000,
    'Geelong': 1000,
    'Gold Coast': 1000,
    'Greater Western Sydney': 1000,
    'Hawthorn': 1000,
    'North Melbourne': 1000,
    'Port Adelaide': 1000,
    'Richmond': 1000,
    'St Kilda': 1000,
    'West Coast': 1000,
    'Western Bulldogs': 1000,
    'Adelaide': 1000,
    'Fitzroy': 1000
}

# Define K-factor
#would like to implement a sliding K_FACTOR - something like:
# 
K_FACTOR = 32
# Function to calculate expected score
def expected_score(rating1, rating2):
    return 1 / (1 + 10 ** ((rating2 - rating1) / 480)) #value of 440 should offer additional accuracy in prediction


# Function to update Elo ratings based on match results including winning margin
def update_elo_ratings_with_margin(ratings, team1, team2, margin):
    expected_team1 = expected_score(ratings[team1], ratings[team2])
    expected_team2 = 1 - expected_team1
    # Determine the outcome based on the margin
    if margin > 0:
        outcome = 1  # Team 1 won
    elif margin < 0:
        outcome = 0  # Team 2 won
    else:
        outcome = 0.5  # Draw
    # Calculate the margin factor
    
    #how to work out winner
    #if outcome == 1:
    #    winner = ratings[team1]
    #    loser = ratings[team2]
    #if outcome == 0:
    #   winner = ratings[team2]
    #    loser = ratings[team1]
    #if outcome == 0.5:
    #    winner = 0
    #    loser = 0
    
    #if winner == ratings[team1]:
    #    HG = 50
    #if winner == ratings[team2]:
    #    HG = -50
    #if winner == 0:
    #    HG = 1
    #else:
    #    margin_factor = 0
    
     #margin factor /w Home ground adv built in. Tweak HG (100)
    #margin_factor = (1 + abs((margin) / 60)/abs((7.5+.006)*(winner - loser + HG)))
        #MFtest= ((margin+3)^(.8)/(7.5+0.006(winner-loser+HG)))
   # margin_factor = abs(((margin-3)**0.8) / (winner - loser + HG))   
    #original margin factor below   
    margin_factor = 1 + abs(margin) / 60
    #print (margin_factor)
    # Update Elo ratings
    new_rating1 = ratings[team1] + K_FACTOR * margin_factor * (outcome - expected_team1)
    new_rating2 = ratings[team2] + K_FACTOR * margin_factor * ((1 - outcome) - expected_team2)
    return new_rating1, new_rating2
# Define match results (team1, team2, margin)

def get_tips_for_round(season):
    url = f"{BASE_URL}?q=games;year={season}"#;round={round_number}"
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("games", [])
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return []

def display_tips(games):
    # Convert games to a DataFrame for easy handling
    pd.options.mode.copy_on_write = True #avoid copy errors from old pandas version
    df = pd.DataFrame(games)
    if df.empty:
        print("No games found for this round.")
        return None
    # Display a human-readable table of games
    #create a margin column to be used by my existing ELO calculation
    df['margin'] = np.where(df.hscore>df.ascore, df.hscore-df.ascore, df.hscore-df.ascore)
    #remove all games that aren't complete - this allows us to ingest data from 2025 games that are completed automatically. No more manual game entry
    df["complete"] = pd.to_numeric(df["complete"],errors="coerce") #convert complete field to number
    completed = df[df["complete"] == 100] #validate game is complete
    readable_df = completed[["date","hteam","hscore", "ateam", "ascore","venue","winner","margin","complete" ]]
    formatted = completed[["hteam","ateam","margin"]] #creates the useable tuple for the elo calculation
    
    newmatches = list(formatted.itertuples(index=False, name=None)) #writes tuple to newmatches variable as this function runs once per year
    global matches
    #if statement below fixes error for matches not defined for first year
    if season == seasonconstant: 
        matches = newmatches
    elif season > seasonconstant:
        matches = matches + newmatches #combines existing scraped matches with matches scraped from this current execution of this function. 
    
   
# Update Elo ratings based on match results including winning margin
def setratings():
    for match in matches:
        (team1, team2, margin) = match
        initial_elo_ratings[team1], initial_elo_ratings[team2] = update_elo_ratings_with_margin(
            initial_elo_ratings, team1, team2, margin
        )

def predictor(ratings, team1, team2, margin):
    expected_team1 = expected_score(ratings[team1], ratings[team2])
    expected_team2 = 1 - expected_team1
    # Calculate the predicted winning margin based on Elo ratings
    predicted_margin = round(20 * (ratings[team1] - ratings[team2]) / 60)
    # Determine the winner and winning margin
    if predicted_margin > 0:
        winner = team1
    elif predicted_margin < 0:
        winner = team2
    else:
        winner = "Draw"
    # Display the predicted winner and winning margin
    print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
    print("The predicted results are:\n")
    print("Predicted Winner:", winner)
    print("Predicted Winning Margin:", abs(predicted_margin), "points")
    print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")


def HistoricalData():
    global season
    global seasonconstant
    seasonconstant = input("what year should we start the ratings from?")
    seasonconstant = int(seasonconstant)
    season = int(seasonconstant)
    
    manyseasons = False
    while manyseasons is False:
    
        tips = get_tips_for_round(season)

        if tips:
            tips_df = display_tips(tips)
        if tips_df is not None:
            print("Matches grabbed")
            #calculate_most_tipped_teams(tips_df)
            #Bet_advisor(tips_df)
        else:
            print(f"Matches grabbed for {season}")
    
        #print (season)
        season = season + 1
        if season <= 2025:
            manyseasons is False
        elif season > 2025:
            manyseasons is True
            break
    #Need to pull 2025 data here but ignore non completed. 

def ratings():
    sorted_ratings = sorted(initial_elo_ratings.items(), key=lambda x: x[1], reverse=True)
    print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
    print("Updated Elo Ratings:\n")
    for team, rating in sorted_ratings:
        print(f"{team}: {rating}")
    print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n") 

def main():
    HistoricalData() 
    setratings()
    ratings()
main()