#!/usr/bin/env python3


# Define initial Elo ratings for each team
teamnames = [
    'Sydney Swans',
    'Melbourne Demons',
    'Brisbane Lions',
    'Carlton Blues',
    'Collingwood Magpies',
    'Essendon Bombers',
    'Fremantle Dockers',
    'Geelong Cats',
    'Gold Coast Suns',
    'GWS Giants',
    'Hawthorn Hawks',
    'North Melbourne Kangaroos',
    'Port Adelaide Power',
    'Richmond Tigers',
    'St Kilda Saints',
    'West Coast Eagles',
    'Western Bulldogs',
    'Adelaide Crows']

initial_elo_ratings = {
    'Sydney Swans': 105,
    'Melbourne Demons': 110,
    'Brisbane Lions': 135,
    'Carlton Blues': 105,
    'Collingwood Magpies': 160,
    'Essendon Bombers': 100,
    'Fremantle Dockers': 100,
    'Geelong Cats': 100,
    'Gold Coast Suns': 100,
    'GWS Giants': 105,
    'Hawthorn Hawks': 100,
    'North Melbourne Kangaroos': 100,
    'Port Adelaide Power': 110,
    'Richmond Tigers': 100,
    'St Kilda Saints': 105,
    'West Coast Eagles': 100,
    'Western Bulldogs': 100,
    'Adelaide Crows': 100
}
# Define K-factor
K_FACTOR = 25
# Function to calculate expected score
def expected_score(rating1, rating2):
    return 1 / (1 + 10 ** ((rating2 - rating1) / 400))

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
def openfile():
    with open(r'Matches', 'r') as fp:
        data = fp.read()
        global matches
        matches = (list(eval(data)))
openfile()
# Update Elo ratings based on match results including winning margin

for match in matches:
    (team1, team2, margin) = match
    initial_elo_ratings[team1], initial_elo_ratings[team2] = update_elo_ratings_with_margin(
        initial_elo_ratings, team1, team2, margin
    )

# Display updated Elo ratings sorted from highest to lowest
def ratings():
    sorted_ratings = sorted(initial_elo_ratings.items(), key=lambda x: x[1], reverse=True)
    print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
    print("Updated Elo Ratings:\n")
    for team, rating in sorted_ratings:
        print(f"{team}: {rating}")
    print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")    

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

 #Define function to predict match outcome
def predict_match():
    input1 = False
    while input1 is False:
        team1 = input("Enter the name of the first team: ")
        if team1 in teamnames:
            input1 is True
            break
        else:
            print("Invalid team name - do it like this: Geelong Cats")
            continue

    input2 = False
    while input2 is False:
        team2 = input("Enter the name of the second team: ")
        if team2 in teamnames:
            input2 is True
            break
        else:
            print("Invalid team name - do it like this: Geelong Cats")
            continue
    
    
    # Update Elo ratings based on user input
    margin = 0  # We don't need the user to enter the margin
    predictor(initial_elo_ratings, team1, team2, margin)

def count():
    number = int(input("How many matches do you want to input?:"))
    for _ in range(number):
        matchinput()
    


def matchinput():
    input1 = False
    while input1 is False:
        hometeamraw = input("Enter the Home team:")
        if hometeamraw in teamnames:
            input1 is True
            break
        else:
            print("Invalid team name - do it like this: Geelong Cats")
            continue

    global hometeam
    hometeam = f"('{hometeamraw}',"
    input2 = False
    while input2 is False:
        awayteamraw = input("Enter the Away team:")
        if awayteamraw in teamnames:
            input2 is True
            break
        else:
            print("Invalid team name - do it like this: Geelong Cats")
            continue

    global awayteam
    awayteam = f"'{awayteamraw}',"
    
    input3 = False
    while input3 is False:
        marginraw = input("Enter the margin:")
        try:
            int(marginraw)
            break
        except ValueError:
            try:
                float(marginraw)
                break
            except ValueError:
                print("Margins are numbers man!")
                continue
    marginint = int(marginraw)
        

    global margin
    margin = f"{marginraw}),"
    matches.append((hometeamraw ,awayteamraw ,marginint))


def savefile():
    f = open('Matches', 'w')
    for t in matches:
        f.write(repr(t)+",")
    f.close()
savefile()

def menu():
    print("\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\nWelcome to LuckyTom's AFL ratings and Predictor Tool! - YMMV\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n")
    print("1. Print ELO Rating")
    print("2. Predict a single match")
    print("3. Predict a whole round")
    print("4. Input match results")
    print("5. Exit\n")

    choice = input("Enter your choice (1-5):")

    if choice == '2':
        print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
        print("You have chosen to predict one match. Enter Teams below:\n")
        print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
        predict_match()
        menu()
    elif choice == '3':
        print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
        print("You have chosen to predict a full round.\n")
        for _ in range(9):
            predict_match()
        menu()
    elif choice == '1':
        print("\n\n")
        ratings()
        menu()
    elif choice == '4':
        print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
        print("You have chosen to input matches. Remember to exit and reload script to update ratings")
        print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
        count()
        savefile()
        openfile()
        menu()
    
    elif choice == '5':
        print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
        print("Seeya Legend - Happy Bets :)")
        print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
        exit
    else:
        print("Please choose a valid option")
        menu()

    
menu()
savefile()
