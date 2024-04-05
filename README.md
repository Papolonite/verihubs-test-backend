# Track User Coin

This Backend service is an example on how to track coin based on [Coincap API](https://docs.coincap.io) and not intended to be use for production use.

## Prerequisites

- Python 3.10 or Up
- Pipenv 
	`pip install --user pipenv`

## How to Run

 1. Clone the git repo and open the repository
 2. In repository directory, install environment using pipenv in terminal
	 ```
	 python -m pipenv install
	 ```
3. Run the program using this command
	```
	uvicorn main:app --reload
	```
