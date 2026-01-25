# TODO
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
  
