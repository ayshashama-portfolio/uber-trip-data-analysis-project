## Uber Trip Data Analysis Project using Python

### Project Overview
This project performs an in-depth Exploratory Data Analysis on Uber trip data to understand ride patterns, peak hours, travel purposes, distances traveled, weekday trends, and monthly usage behavior. The analysis includes preprocessing, feature engineering, visualizations, and correlation analysis to uncover insights into user behavior and trip characteristics.

### Data Sources
The dataset used for this analysis is the "UberDataset.csv" file, containing Uber ride details such as start and end date with timestamps, trip categories, purpose of travel, distance traveled, and start and end stop name. It contains upto 1155 entries with 7 columns.

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
