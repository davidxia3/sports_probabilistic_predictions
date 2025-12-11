# src/analysis/
This folder contains all the Python scripts for extracting CSV results from the processed data. All results are derived only from games from the second half of each regular season. 

### src/analysis/binary_accuracy.py
This Python script computes the binary accuracy of various model based prediction methods for each league and saves the results to `results/binary_accuracy.csv`. Probabilistic predictions are converted to binary predictions using a 0.5 threshold. The models used are below.
- ml: Predictions derived from moneyline scores.
- bt: Predictions derived from Bradley-Terry rating algorithm.
- hom_win_base: Predictions that home team wins with first half of season home win probability. 