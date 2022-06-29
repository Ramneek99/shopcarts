# NYU DevOps Project Shopcarts

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/DevopsShopcarts/shopcarts/actions/workflows/ci.yml/badge.svg)](https://github.com/DevopsShopcarts/shopcarts/actions)
[![codecov](https://codecov.io/gh/DevopsShopcarts/shopcarts/branch/master/graph/badge.svg?token=I5TPOTMR9A)](https://codecov.io/gh/DevopsShopcarts/shopcarts)

## Overview

This project template contains starter code for your class project. The `/service` folder contains your `models.py` file for your model and a `routes.py` file for your service. The `/tests` folder has test case starter code for testing the model and the service separately. All you need to do is add your functionality. You can use the [lab-flask-tdd](https://github.com/nyu-devops/lab-flask-tdd) for code examples to copy from.

## Automatic Setup

The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository.

## Manual Setup

You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own `README.md` file so be selective in what you copy.

There are 4 hidden files that you will need to copy manually if you use the Mac Finder or Windows Explorer to copy files from this folder into your repo folder.

These should be copied using a bash shell as follows:

```bash
    cp .gitignore  ../<your_repo_folder>/
    cp .flaskenv ../<your_repo_folder>/
    cp .gitattributes ../<your_repo_folder>/
```

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── utils                  - utility package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## API Routes Documentation for Shopcarts

| HTTP Method | URL | Description | Return
| :--- | :--- | :--- | :--- |
| `GET` | `/shopcarts/{shopcart_id}` | Get shopcart based on its id | Shopcart Object
| `POST` | `/shopcarts/{shopcart_id}` | Create a shopcart based on the data | Shopcart Object
| `GET` | `/shopcarts/{customer_id}/products` | Returns a list of all the shopcarts | List of Shopcart Objects
| `GET` | `/shopcarts/{customer_id}/products/{product_id}` | Get the product based on its product_id | Product Object
| `POST` | `/shopcarts/{customer_id}/products` | Create a Product on a Shopcart | Product Object
| `DELETE` | `/shopcarts/{customer_id}/products/{product_id}` | Delete the Product based on the product_id | 204 Status Code
| `PUT` | `/shopcarts/{customer_id}/products/{product_id}/{quantity}` | Update a Product based on the given quantity | Product Object
| `GET` | `/shopcarts` | Get all of the shopcarts | List of Shopcart Objects

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
