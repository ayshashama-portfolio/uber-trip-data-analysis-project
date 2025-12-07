## Uber Trip Data Analysis Project using Python

### Project Overview
This project performs an in-depth Exploratory Data Analysis on Uber trip data to understand ride patterns, peak hours, travel purposes, distances traveled, weekday trends, and monthly usage behavior. The analysis includes preprocessing, feature engineering, visualizations, and correlation analysis to uncover insights into user behavior and trip characteristics. [PythonCode](https://github.com/ayshashama-portfolio/uber-trip-data-analysis-project/blob/main/main.py)

### Data Sources
The dataset used for this analysis is the ["UberDataset.csv"](https://github.com/ayshashama-portfolio/uber-trip-data-analysis-project/blob/main/UberDataset.csv) file, containing Uber ride details such as start and end date with timestamps, trip categories, purpose of travel, distance traveled, and start and end stop name. It contains upto 1155 entries with 7 columns.

### Tools Used
* Python - Main programming language 
* Excel - Initial data viewing & basic checks
* Pandas - Data cleaning & manipulation
* NumPy - Numerical operations
* Matplotlib & Seaborn - Data visualization
* Scikit-Learn - OneHotEncoding for categorical variables

### Data Preprocessing
Before creating visualization for data insights, we performed the following pre-processing tasks:
1. Converted START_DATE and END_DATE to datetime format
2. Created additional features: date, time, day-night category (Morning/Afternoon/Evening/Night), month and day.
3. Removed rows with missing values
4. Dropped duplicate entries
5. Applied OneHotEncoding on categorical variables CATEGORY and PURPOSE
6. Extracted numerical columns and generated a correlation heatmap

### Exploratory Data Analysis
Key questions explored:
* How many rides occur per category and purpose?
* Which time-of-day category has the highest ride count?
* What is the relationship between trip purpose and category?
* What are the longest trips recorded each month?
* Which weekday has the most Uber rides?
* How is the distance distributed? Are there outliers?
* How do monthly ride counts vary through the year?

### Data Analysis
Some interesting features worked during this project are:
* day-night segmentation based on ride start and end time
* Monthly ride pattern detection using START_DATE
* Maximum miles per month to detect long-trip surges
* One-Hot Encoding to analyze categorical influence numerically
* Correlation matrix to study relationship between miles, time, and encoded purpose/category.

### Results
The Analysis results are summarized as follows:
1. Business trips dominate over personal rides.
2. Most common purposes: Meeting, Meal, Errand-running.
3. Ride activity peaks during Evening.
4. Wednesday and Friday show highest weekday ride counts.
5. November has the highest number of rides, while September has the lowest.
6. A notable distance spike occurs in April and October, showing exceptionally long rides.
7. Distances mostly fall under 40 miles, with a few high outliers.
8. No strong correlation between ride count and maximum miles—long trips are rare exceptions.

### Recommendations
Based on the analysis made, the following actions are recommended:
1. Uber service teams can focus more resources on evening rides (high demand).
2. September dip suggests a seasonal low-ideal for driver onboarding or maintenance schedules.
3. Long-distance trips in April & October could indicate events or travel patterns worth investigating.
4. Business customers drive most demand → introduce business loyalty programs.
5. Use purpose data to offer targeted discounts (e.g., frequent “Meal” riders).
   
