# Storefront e-commerce web application
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Website](#accessing-the-website)
* [Running tests](#running-tests)
* [Troubleshooting](#troubleshooting)

## General Info
This e-commerce web application is designed to allow visitors to browse a list of products, add a quantity of them to their cart, and check out their items converting the cart into an order associated with their account. I created this project to learn and show my level of understanding of backend technologies like the Django framework, MVT design pattern and database management, and frontend technologies like Javascript, Ajax and Bootstrap.

## Technologies
* Python 3.10.7
* Django 4.2.1
* JavaScript
* jQuery 3.7.1
* Bootstrap v5
* SQLite 3.41.2

## Setup

### Prerequisites

* Python

This project requires Python3 which can be installed from their [website](https://www.python.org/). Install version ```3.10.7```, if installing another version be sure to check it is compatible.

* SQLite3

To install SQLite3 head to their website [here](https://www.sqlite.org/index.html) and follow the instructions to install version ```3.41.2```.

### Installation

1. Clone this repository
```powershell
git clone https://github.com/jchurcher/Storefront.git
```

2. Create and activate a new Python virtual environment. Fill in \<path\> with the path location you would like to store your environments files (usually just env, venv, etc.).
```powershell
# Enter project
cd Storefront/

# Install virtual environment package
pip install virtualenv

# Make new virtual environment
py -m venv <path>

# Activate the environment
<path>/Scripts/Activate
```

3. Install the required packages from the provided requirements.txt using pip
```powershell
pip install -r requirements.txt
```

4. Run the server
```powershell
# Run server
py manage.py runserver localhost:8000

# Server is now running on localhost:8000
```

## Accessing the website

To access the website got to ```localhost:8000``` in the browser, there are several URLs to access the app listed below:

#### Homepage: [http://localhost:8000/store/](http://localhost:8000/store/)

#### Products list: [http://localhost:8000/store/products/](http://localhost:8000/store/products/)

#### Collections list: [http://localhost:8000/store/collections/](http://localhost:8000/store/collections/)

#### Cart: [http://localhost:8000/store/cart/](http://localhost:8000/store/cart/)

#### Product detail page: [http://localhost:8000/store/products/?/](http://localhost:8000/store/products/1/)
The ```?``` refers to the product id that you are requesting the details for. This URL in particular, the id is set to 1 and will redirect you to that product.

## Running tests

## Troubleshooting
