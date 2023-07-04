# Trading Bot with Fan Tokens

This repository contains a trading bot that utilizes fan tokens and integrates data from API-FOOTBALL for match information and python-binance library for OHLC (Open-High-Low-Close) values. The bot follows specific rules for buying and selling fan tokens based on match events and outcomes.

## Overview
The trading bot is designed to automate the buying and selling of fan tokens based on two rules:

1. If a team scores a goal that puts them ahead, the bot will buy the corresponding fan token and sell it after 5 minutes.

2. If a team wins a match, the bot will buy the fan token at the end of the game and sell it 15 minutes after the game ends.

The bot relies on the API-FOOTBALL service to fetch match information such as goal minutes, result scores, and other relevant data. It also utilizes the python-binance library to retrieve OHLC values, which are used for trading decisions.

## Prerequisites
Before using the trading bot, ensure that you have the following:

* Python 3.x installed on your system
* Pandas
* API-FOOTBALL account with access to match data

## Installation
To set up the trading bot, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running the following command:
    ```bash
    pip install -r requirements.txt
    ```
3. Configure your API-FOOTBALL credentials in the **.env** file 
4. Run the trading bot by executing the following command:
    ```bash
    python main.py
    ```

## Configuration
The trading bot can be customized based on your specific trading strategies and preferences. Some possible modifications include:

* Adjusting the time thresholds for buying and selling after a goal or match outcome.
* Implementing additional trading rules based on different match events.
* Integrating other data sources or APIs to enhance trading decisions.
* Adding risk management features, such as stop-loss or take-profit mechanisms.

## Disclaimer
Please note that trading involves financial risks, and the trading bot provided in this repository is for educational and experimental purposes only. It is essential to understand the risks involved and perform thorough testing before using any trading strategies with real funds. The creators of this repository are not responsible for any financial losses incurred while using the trading bot.

## Acknowledgments
The trading bot utilizes the following libraries:

* API-FOOTBALL - API for fetching match data.
* python-binance - Python library for interacting with the Binance API.

## Conclusion
The trading bot with fan tokens provides a starting point for developing automated trading strategies based on match events and outcomes. Feel free to explore and customize the bot according to your trading preferences and requirements. If you have any questions or suggestions, please contact us at tunaeem@gmail.com