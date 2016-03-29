# Evaluation of Inflation Predictions by the Norwegian Central Bank.

The objective of this project is to calculate and present the predicition
error in the CPI and CPI_JAE estimates.

## Repository structure

- *data*: The source dataset, and converted csv files.
- *tests*: Tests of functions, run with nosetest.
- *inflastudy*: A package with helper functions and objects to work with the 
predictions and datasets.
- *[inflastudy.ipynb](inflastudy.ipynb)*: The front-end of the repository. The iPython notebook 
will present the data and plots.

## Convert to csv

- File --> Options
	- change language to English (U.S)
	- Advanced: Use system separators; set decimal separator to dot
- Delete text and notes
- Delete unnecessary data, with æ,ø,å
- Save as csv (MS - DOS)