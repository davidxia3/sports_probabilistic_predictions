# TODO

## March 5
- **Tables:** Check that all tables reflect the most recent updates.
- **Descriptive statistics tables/figures (Section 5.3):**  Home winrates (full season), bookmmaker profits (second half season), two negative moneylines (full season), distribution of home win probabilities (second half season): **Recalculate the home winrates and two negative moneylines data based on second half season only.**
- **Home win probabilities for coin flip model:** These can vary from game to game, but they are based on at least half a season's worth of data.   **Are all of these strictly greater than 50%?** (See the footnote on page 10.)
  
## February 25
- **Calculation of ML averages:**  
  - Potential (minor) issue:   The mapping m -> pstar(m) is not always reversible. Need to assume (1) m> 100 or m < -100, and (2) pstar != 1/2.
    - Regarding (1): **Check if all moneylines satisfy this condition i.e., are >100 in absolute value.**   (No: values of 100 occur in the original data.)
    - Regarding (2): If |m|>100, pstar is always <1/2 or >1/2, so for individual moneylines p=1/2 cannot happen. However, if moneylines (or probabilities) are averaged, it is theoretically possible that the average is exactly 1/2.  **Check if this actually occurs in the data.** (Fix: Define the inverse mapping m(pstar) to be -100 if pstar = 1/2)
- **Bookmaker profits:** Maybe put this table back in. **Prepare an updated version, based on the revised ML average calculations, put it in the temporary.tex file.**

## February 19
- **Updated files at Overleaf:**
  - *results.tex:*   (today, 3:11 pm) Changes in table of excluded scores. (earlier today I uploaded new version of results.tex.)
    - Tables currently at Overleaf are up to date.
      - **AJH: Update local versions of these tables.**
      - **David: Leave this file alone. Add changed tables to temporary.tex file.**)
  - *data.tex:* No changes (as of today)? (**David: Leave this file alone. Add changed tables to temporary.tex file.**)
  - *Graphics:* updated graphics files, names unchanged?
- **Moneylines:** Recompute moneylines using averages instead of maxima/minima, and recreate graphics files.
- **Next meeting:** Wednesday, Feb. 25, 4:15 pm, English Building Computer Lab

## February 13
- **Binary accuracies for MLB in 2025:** All models are nearly tied. Worth looking into. In particular, the ML accuracy is by far the lowest among all years (53% versus >= 57% for other years). Some ways to check: (1) Calculate accuracy based on oddsportal averages. (2) Calculate accurcy based on a specific bookmaker's quotes (e.g., DraftKings, Bet365). 
- **Data summary table:** Remove column with home winrates (it fits better into the Descriptive Statistics subsection), and add a column showing the # of First Half Games. (Also, the # of second half games shown is **greater** than half the total number of games, which conflicts with what you said under "Potential new version".)
- **Computation of ML averages:** Check calculations, e.g., check if the averages you computed are contained in the intervals between highest and lowest ML offered by bookmakers.
- **Raw data:** Add files containing individual bookmaker moneylines that have been used to calculate averages.
- **Average ML computations:** Use ordinary averages (arithmetic means) of moneylines instead of averaging implied probabilities.

## February 5
- **Calculation of moneyline averages:** Try to figure out how the avg moneylines at OddsPortal were computed. 
  - **NFL, MLB, NBA:** 
  - **NHL:** 


## January 29
- **Ties in moneylines and BT probabilities:**  Check how many (if any) cases there are in which the two moneylines were equal or the BT probabilities were equal.  (In these cases the "winner" of the game is not defined, so one needs to decide on how to handle those cases in computing the binary accuracy rates. Suggest to ignore cases with ties in calculation of binary accuracies.)
- **Binary accuracy rate bar chart:**  Replace the horizontal line (at 50%) by an additional (4th) bar of height 50%, labeled "Coinflip"  (so that there are 4 groups of 4 bars), in analogy to the 4 line graphs shown in the seasonal accuracy figures.
- **Terminology:** Replace "binary accuracy" by "Accuracy rate (%)" throughout.
- **Table and Bar Chart for overall Brier scores:** Create a table and a bar chart,formatted in the same way as the binary accuracy table/chart, showing the  *overall* Brier score for each of the four leagues and the four models (ML, BT, Home Bias Coinflip, Coinflip).  In the table, put the models in the following order: Home Bias Coin Flip, Bradley-Terry, Moneyline (i.e., an order analogous to that in Stern's table).
  
## January 22
- Redo bar charts (forgot to commit the notes made during meeting)
  - Changed colors
  - Changed font size
  - Changed figure size
  - Changed font
  - Added baselines for binary accuracy and predicted home team winrate graph
  - Removed titles and X axis labels
  - Standardized y axis scale for matching graphs
  

## January 15
- **Coin flip model with home bias:** Is this defined as a probabilistic prediction with constant prediction probability equal to the home team win proportion for the league, i.e, with P(Home team wins)=p, P(Away team wins) = 1-p, where p is the home team win proportion? **YES**   Or as "home team ALWAYS wins", i.e., P(Home team wins) = 1, P(Away team wins) = 0? **NO**
- **New bar charts:** Color-code the bars, increase the spacing between the bars (or make the bars skinnier).
- **Binary accuracy chart:** Change y-axis range to full range 0 to 100 percent, and create similar chart grouped 3 by 4 (three sets of 4 bars, corresponding to the different models)

## January 12
- **Additional tables/charts:**
  - ("Description of Data" section) Table of bookmaker profits (average profit by league, accompanied with basic bar char (4 bars, one bar per league)  
  - ("Description of Data" section) Basic bar chart for home win percentage per league to accompany the home won percentage table (4 bars, one bar per league) make range 40%-60% or something
  - (Results section) Grouped bar chart to accompany binary accuracy table (either 3 groups of 4 bars, corresponding to the three methods (ML, BT, Coin Flip), or 4 groups of 3 bars, corresponding to the 4 leagues)
  - Bradley-Terry: Find appropriate reference (ideally scholarly paper, e.g., Bradley-Terry article), use Wikipedia to find sources/references

Cite both of the following. The first is the original paper about the statistical model. The second is the webpage that has the code for the model implementation.
  Bradley, Ralph Allan; Terry, Milton E. (1952). "Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons". Biometrika. 39 (3/4): 324–345.
  https://datascience.oneoffcoder.com/btl-model.html

## January 3
- **ML Data:** There might be a few cases where both moneylines are positive.   Compile statistics (raw numbers and percentages) for each league of such cases. (This is for a possible footnote, or addition,  to the explanations of moneyline scores.)

## December 13
- **Figures:** Create pdf versions of all figures
- **Data:** Create a summary table of processed/clean data used for the analysis. Columns: League, Seasons, total # of games, # of second half games, home win percentage.
  - Write a paragraph detailing any data points that were thrown out, with total numbers and percentages per league (combine the numbers thrown out for reasons other than oddsportal availability, only mention explicitly the percentages thrown out due to availability of Moneyline numbers.
  - Put the histograms of moneyline implied home win probabilities in the data section
- **Results:** Breakdown by subsection
  


## December 11
- **Meeting Schedule:** TBD 
- **Reformatting floating point numbers in csv files:**  As it stands, the number of digits after the decimal point that is displayed varies from file to file and is generally unnecessarily large.  For data that may be used in formatted tables, it would be good to have versions of this files where all floating point numbers have the same, fixed precision. I would suggest 3 digit precision, which is the most common format in the literature.  Thus, 0.25135 would be converted to 0.251, 0.25 to 0.250, etc.   To implement this in an efficient manner, I suggest the following:
  - Keep all csv files as is (i.e., with full precision floats) since the higher precision may be useful for future work.
  - Write a script that takes a csv file   (and possibly a list of columns that are to be converted) as input and outputs a file with the data in the (specified) columns converted to 3 digit accuracy, with a similar filename. For the naming scheme, I suggest changing ".csv" to "_fmt.csv" (so that the formatted version of ml_brier.csv would become ml_brier_fmt.csv).
  - Apply this script to the csv files in results (at least those accompanying the figures).

## December 9
- **Seasonal ROI plots**: For each bin, plot the ROI for this bin as a function of the season (not the other way around). This is the type of visualization that would indicate whether betting on a particular bin with a positive ROI overall might be a viable betting strategy.
- **Home win percentages histograms**: Put these histograms for the 4 leagues into separate figures (analogous to the other league-based visualizations).
- Continue work on Readme files/documentation.
- **Data files for figures:** Ideally, each figure should be associated with a csv file that contains the data used to generate the figure (inside the figures directory).  If possible, use the same or a similar naming scheme as for the figures, replacing the extension .png by .csv.
- **ROI plots:** Reduce y-axis to a smaller range (e.g., -30 to +30)
- **Next meeting:** Thursday 6 pm Central/4 pm Pacific

## December 8
- Add documentation files (as .md files), move the description of the data that is currently in LaTeX to these markdown files (the formatting in LaTeX can be done at a later stage).
- Check if home win pct changes a lot by season compared to overall.  Create line graph showing season-by-season home win percentages for all 4 leagues combined.
- General comment on line graphs with multiple lines (e.g., NFL, NBA,MLB, NHL): In addition to using colors to distinguish the lines, also use different shapes for the data points (e.g., disk, square, star, ...).
- ROI graphs: (1) Use the same y-scale for each League. (2) On the x-axis, put percentage labels (10%, 20%, etc), and put data points for the bins in the middle of the corresponding percentage interval (e.g., the 10-20 percent bin data point would be placed in the middle of the interval (10,20).
- ROI: Generate seasonal ROI plots for each bin. (i.e., for each bin plot the ROI as a function of the season). (This is just to get some idea of seasonal variations, especially in case the overall ROI for a particular bin is positive).
- Home win percentages:  Generate histograms for the home win percentages for each of the 4 leagues and for both ML and BT. Make sure to use the same y-scale and, ideally, the same number of bars. 
  
