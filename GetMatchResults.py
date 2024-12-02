import requests
import pandas as pd
import numpy as np
BASE_URL = "https://api.squiggle.com.au/"
USER_AGENT = "Lucky's Tipping Bot - tom.lucken@gmail.com"
def get_tips_for_round(season, round_number):
    url = f"{BASE_URL}?q=games;year={season};round={round_number}"
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("games", [])
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return []

def display_tips(games):
    # Convert tips to a DataFrame for easy handling
    pd.options.mode.copy_on_write = True
    df = pd.DataFrame(games)
    if df.empty:
        print("No tips found for this round.")
        return None
    # Display a human-readable table of tips
    df['margin'] = np.where(df.hscore>df.ascore, df.hscore-df.ascore, df.hscore-df.ascore)
    readable_df = df[["date","hteam","hscore", "ateam", "ascore","venue","winner","margin" ]]
    formatted = df[["hteam","ateam","margin"]]
    #print(formatted.to_string(index=False,header=False))
    print(list(formatted.itertuples(index=False, name=None)))
    matches = list(formatted.itertuples(index=False, name=None))
    for match in matches:
        (hteam, ateam, margin) = match
        if margin > 0:
            print(f"The Winner is {hteam} by {margin}")
        elif margin < 0:
            print(f"The winner is {ateam} by {margin}")# Team 2 won
        else:
            print(f"The Match was a draw") # Draw

        #print(f"the margin is {margin}")

    print(readable_df.to_string(index=False))
    
    

   
    
    



    return df




def main():
    print("\nLuckyTom's AFL Tip and Bet tool")
    print("Have fun - don't bet the house, I'm probably wrong")
    print("Bet risk aversion can be set in the code - currently only taking bets for >75 confidence rating - you might be playing $1.05 odds all season")
    print("Run Multi's to get decent odds")
    print("Remember if the season has an opening round - its a zero")


    global season
    season = 2024

    global round_number
    round_number = input("Which round do you want tips for?:")

    # Fetch tips
    tips = get_tips_for_round(season, round_number)
    if tips:
        tips_df = display_tips(tips)
        if tips_df is not None:
            print("Matches grabbed")
            #calculate_most_tipped_teams(tips_df)
            #Bet_advisor(tips_df)
    else:
        print("No data available for this round.")

    
if __name__ == "__main__":
    main()