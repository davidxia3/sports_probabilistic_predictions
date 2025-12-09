# TODO
## December 9
- **Seasonal ROI plots**: For each bin, plot the ROI for this bin as a function of the season (not the other way around). This is the type of visualization that would indicate whether betting on a particular bin with a positive ROI overall might be a viable betting strategy.
- **Home win percentages histograms**: Put these histograms for the 4 leagues into separate figures (analogous to the other league-based visualizations).
- Continue work on Readme files/documentation.
- Data files for figures: Ideally, each figure should be associated with a csv file that contains the data used to generate the figure (inside the figures directory).  If possible, use the same or a similar naming scheme as for the figures, replacing the extension .png by .csv.
- ROI plots: Reduce y-axis to a smaller range (e.g., -30 to +30)

## December 8
- Add documentation files (as .md files), move the description of the data that is currently in LaTeX to these markdown files (the formatting in LaTeX can be done at a later stage).
- Check if home win pct changes a lot by season compared to overall.  Create line graph showing season-by-season home win percentages for all 4 leagues combined.
- General comment on line graphs with multiple lines (e.g., NFL, NBA,MLB, NHL): In addition to using colors to distinguish the lines, also use different shapes for the data points (e.g., disk, square, star, ...).
- ROI graphs: (1) Use the same y-scale for each League. (2) On the x-axis, put percentage labels (10%, 20%, etc), and put data points for the bins in the middle of the corresponding percentage interval (e.g., the 10-20 percent bin data point would be placed in the middle of the interval (10,20).
- ROI: Generate seasonal ROI plots for each bin. (i.e., for each bin plot the ROI as a function of the season). (This is just to get some idea of seasonal variations, especially in case the overall ROI for a particular bin is positive).
- Home win percentages:  Generate histograms for the home win percentages for each of the 4 leagues and for both ML and BT. Make sure to use the same y-scale and, ideally, the same number of bars. 
  
