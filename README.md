# ratio-calculation-module

## Table of Contents

1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Team](#team)
4. [Installation](#installation)
    - [Manual Installation](#manual-installation)
    - [Installation using Shell Script](#installation-using-shell-script)
5. [Run the Application](#run-the-application)
6. [Modules](#modules)
    - [Ratio Calculation](#ratio-calculation)
    - [Portfolio Manager](#portfolio-manager)
    - [Engine](#engine)

## Introduction

This is a simple application that has 3 modules that can be utilized. The modules are:

1. Ratio Calculation
2. Stock Portfolio Analysis
3. Engine to run the modules

## Requirements

To run the application, you need to have Python 3.7 installed on your machine. You can download Python from the [official website](https://www.python.org/downloads/).

## Team

- Aditya
- Anirudh
- Anmol

## Installation

### Manual Installation

To install the application manually, follow the steps below:

#### 1. Create a Virtual Environment

    python -m venv <venv-name>

#### 2. Activate the Virtual Environment

    source <venv-name>/bin/activate

#### 3. Install the requirements

    pip install -r requirements.txt

### Installation using Shell Script

If you want to install the application using the shell script, just run the following command:

    bash setup.sh

## Run the application

To run the application, run the following command:

    python base.py

Or to run the application with the shell script, run the following command:

    bash run.sh


## Modules

### Ratio Calculation

The ratio calculation module allows users to calculate the price-to-earnings ratio for a given stock. Users are prompted to input the ticker symbol, start date, and end date. The application then utilizes the provided information to calculate the price-to-earnings ratio.

### Portfolio Manager

The portfolio manager module enables users to manage their stock portfolios. Users can input details such as ticker symbol, buy date, buy price, and quantity bought for each stock in their portfolio. The application calculates the portfolio's performance and generates recommendations based on the analysis.

### Engine

The engine serves as the core component of the application, facilitating the interaction with the user and the execution of the modules. It provides a user-friendly interface for selecting and running the desired modules. Users can choose between the ratio calculation and portfolio manager modules, with the ability to exit the engine at any point.
