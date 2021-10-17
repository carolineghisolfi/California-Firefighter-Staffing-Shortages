# California Firefighters Staffing Shortages

Staffing shortages are forcing many local fire departments in rural areas of Northern California to turn down service requests for larger fires and overwork their staff. In this repository, I retrieve data from the California State Controller's Office [Government Compensation in California](https://publicpay.ca.gov/) database and analyze staffing and overtime trends for firefighters in the state. 

Interactive charts produced with this data are available at https://observablehq.com/@carolineghisolfi/california-firefighters. 


*Created by Caroline Ghisolfi (<ceg1998@stanford.edu>)*

## Project notes

## Technical

* ETL: To download and clean data for 2009 through 2020, run `download_and_clean_payroll_data.py` in the ETL directory. The script retrieves and unzips data from the California State Controller's Office [Government Compensation in California](https://publicpay.ca.gov/) database, concatenates data for all years and returns a filtered database (`ff_payroll.csv` in data/processed) which only includes payroll data for firefighters employed by California state and local agencies. 
* Analysis: The `ff_payroll_analysis` notebook reshapes the data into two csv files located in data/processed:
    * `ff_1920_counts.csv`: Total number of firefighters employed by California state and local agencies in 2020. Includes columns with calculated difference, description of the difference (increase or decrease) and percent change from 2019 to 2020.
    * `ff_overtime_byyear.csv`: Overtime pay for firefighters employed by California state and local agencies between 2011 and 2020. Prices are adjusted for inflation through the U.S. Bureau of Labor Statistics API. Includes columns with calculated percent change for each agency type (City, County, Special District and State Department) by year. 
* Visualizations: Interactive charts produced with the data analyzed above can be found at https://observablehq.com/@carolineghisolfi/california-firefighters. 

### Project setup instructions

After cloning the git repo:

`datakit data pull` to retrieve the data files.


## Data notes

* Position/profession names provided in the State Controller's Office database are not standardized. For this analysis, I filter positions by name, searching for the key words "Firefighter" or "Fire Fighter". Some firefighters employed by state or local agencies in California may not be included in the analysis. 
* Although the data is available for the years 2009 through 2020, historical comparisons of overtime pay are limited to years 2011 through 2020 due to missing or incomplete data. 
