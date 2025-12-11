# Sports Probabilistic Predictions
This repository contains a full pipeline for collecting, cleaning, processing, and analyzing sports betting data across the 4 major U.S. sports leagues (MLB, NBA, NFL, NHL). The primary objective is to evaluate and compare probabilistic prediction methods. The primary prediction method is the betting market prediction method (implied from moneyline scores). An alternative prediction method is the Bradley–Terry model. We examine their calibration, accuracy, teamwise, seasonal, and ROI performance.




## `processed_data/`
This folder contains all the cleaned and processed game data for each league.


## `raw_data/`
This folder contains all the raw data scraped from OddsPortal.


## `results/`
This folder contains all CSV results and PNG figures from the analysis of processed data. All results are derived only from games from the second half of each regular season. 


## `src/`
This folder contains all the Python scripts in the repository. 


## `utility/`
This folder contains all the utility and supportive files required for the repository.