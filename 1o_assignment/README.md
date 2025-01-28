# Vulnerabilities in Software Products

## Introduction
Online shop with DETI memorabilia

## Description
Development of 2 versions of a small online shop application that sells DETI memorabilia.
The shop has a variety of items and features, as well as 5 vulnerabilities and its solutions in the respective version (app for unsafe and app_sec for safe).   

## Features
- User Management - login/register, profiles and roles;
- Product Catalog - listings and search functionality;
- Shopping Cart - item management and total calculation;
- Checkout Process - shipping/billing info collection, payment processing and order confirmation with receipt generation;  
- Inventory Management - product quantities;
- Order History - view and track orders

## Vulnerabilities
**Mandatory:**

- [CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')](https://cwe.mitre.org/data/definitions/79.html)

- [CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')](https://cwe.mitre.org/data/definitions/89.html)

**Chosen:**

- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)

- [CWE-256: Plaintext Storage of a Password](https://cwe.mitre.org/data/definitions/256.html)

- [CWE-521: Weak Password Requirements](https://cwe.mitre.org/data/definitions/521.html)

## How to run

> :warning: ***Python version MUST be 3.10.11 due to greenlet compatibility issues***

1. Download files:
    ```bash
    git clone git@github.com:detiuaveiro/1st-project-group_30.git
    ```

2. Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment (this step needs to be repeated every time a new terminal is opened):

    ```bash
    source venv/bin/activate
    ```

4. Install the requeriments:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the server (**use these exact paths**):

    unsafe version (2 terminals):
    ```bash
    python3 cookies_server.py
            
    python3 app/app.py
    ```

    safe version:
    ```bash
    python3 app_sec/app.py
    ```

6. Access the website:

    <http://127.0.0.1:5000/>

7. Admin account credentials:
    ```
    email: administrador@email.com
    pass:  Abc.1234
    ```

8. Payment Processing (test credit card info):
    ```
    4242424242424242
    12/34        000
    ```

## Authors
- Gonçalo José Queirós da Silva Sousa | 98152

- Joaquim Cristóvão Paiva Rascão | 107484

- Diogo Santos da Silva Martins | 108548

## Template
https://github.com/diwash007/Flask-O-shop.git