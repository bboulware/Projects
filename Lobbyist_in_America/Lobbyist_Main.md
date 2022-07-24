## Goal:
This task was to create a dashboard that displayed more in-depth information on how the top lobbyist groups spent their money in 2020. By clicking on each state, the viewer will be able to view who recieved funds and which years recieved the most amount of funds. According to Statista.com, these were the top lobbyist groups for 2020.

<a href="https://www.statista.com/statistics/257344/top-lobbying-spenders-in-the-us/" rel="nofollow"><img src="https://www.statista.com/graphic/1/257344/top-lobbying-spenders-in-the-us.jpg" alt="Statistic: Top lobbying spenders in the United States in 2020 (in million U.S. dollars) | Statista" style="width: 100%; height: auto !important; max-width:1000px;-ms-interpolation-mode: bicubic;"/></a><br />Find more statistics at  <a href="https://www.statista.com" rel="nofollow">Statista</a>

## To gather more information I decided to use the API from FEC.gov.

**'The Federal Election Commission (FEC) is the independent regulatory agency charged with administering and enforcing the federal campaign finance law. The FEC has jurisdiction over the financing of campaigns for the U.S. House, Senate, Presidency and the Vice Presidency.'  -FEC.gov website**

**Downloaded from fec.gov after using search by committee.**
[Committees](committee.csv)

## Code

**Python script to read the committee file, and create an api request for each committee then saving the data as its own csv.**<br>
[Python API Request](Disbursements.py)

**Jupyter Notebook to clean the data. Removing columns that were completely empty as well as rename and consolidate information.**<br>
[Jupyter Notebook Cleaning](Disbursements_Notebook.ipynb)


## Dashboard

**Tableau Dashboard displaying the data in a user friendly way.**<br> 
[Tableau Dashboard](https://public.tableau.com/views/TopLobbyist/Dashboard1?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link)

<br>

#### [Back to Main](https://github.com/bboulware7/Projects)