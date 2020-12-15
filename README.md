# USElectionVisual
US federal election results visualized using python and plotly dash

## :floppy_disk: Data
The election data is sourced from the MIT Election Data + Science Lab and can be found [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ).

Results are at a US county level for the 2000 to 2016 presidential elections with results split by candidate and party. FIPS identifiers were used to map the data at a county level. 

## :mag: Methodology
Used the python library pandas to clean up and prepare the data for visualization doing initial testing in Jupyter notebooks. Initial results were visualized using plotly chloropleth maps and any outliers or discrepancies were cleaned up. 

In order to make the content interactive, plotly's dash framework was used. By changing the year, users can visualize the election results at a county and state level with the winner clearly displayed at the top of the live dashboard. 

## :pencil2: Formatting
As plotly's dash supports HTML/CSS formatting, a custom header and simple page structure was built using HTML and CSS to display the election results. The live dashboard is responsive, although it is not yet mobile optimized. 

## :computer: Final Visualization
[The final visualization can be found here](https://alexk-dash-app.herokuapp.com/)

## :wave: Author
Alex Kruczkowski
