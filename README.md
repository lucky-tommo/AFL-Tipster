#AFL-Tipster

Python script to predict outcomes of upcoming AFL Matches based on ELO Rating of teams. 
ELO rating began at the beginning of season 2024. Teams did not start even. 

Future enhancements: 
1) Take ranking back to beginning of current "era"
2) Add adjustments/allowances for Home ground advantag
3) Add the ability to de-rate a team due to big outs.


YMMV - Have fun!


How to use
-----------
Run the script.

To see the current rating - select 1. 
To predict a single match - select 2
To Predict a whole round - select 3
To Input match results and update the Matches file - select 4. 

When entering teams - team names need to look like: North Melbourne Kangaroos. - note the capitalisation. 
When entering the margin - if the home team won, margin is like 23. If the away team won, the margin is like -23.
After inputting matches, exit the script and rerun it to update the elo ratings. (the file saves on exit **change this**) 
