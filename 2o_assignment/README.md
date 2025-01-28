# Vulnerabilities in Software Products

## Introduction
Online shop with DETI memorabilia

## Description
**2nd Project:**  
Evolve DETI memorabilia online shop to comply with level 1
Application Security Verification Standard (ASVS) requirements. 

For that purpose, a full Web application compliance audit was conducted, and security improvements resulting from the audit were implemented.  

6 level 1 ASVS key issues were explored and 2 software features implemented: Password strength evaluation and Multi-factor Authentication (MFA).  

The original code that was audited is in app_org (has it's own README.md). 

The resulting code of this 2nd project is present in app_sec.

## Features

- User Management - change password, delete account;
- Password Strength Evatuator (zxcvbn API);
- Password Breach Checker (haveibeenpwned API)

## Vulnerabilities

- [CWE-212: Improper Removal of Sensitive Information Before Storage or Transfer](https://cwe.mitre.org/data/definitions/212.html)

- [CWE-285: Improper Authorization](https://cwe.mitre.org/data/definitions/285.html)

- [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html)

- [CWE-521: Weak Password Requirements](https://cwe.mitre.org/data/definitions/521.html)

- [CWE-620: Unverified Password Change](https://cwe.mitre.org/data/definitions/620.html)

- [CWE-641: Improper Restriction of Names for Files and Other Resources](https://cwe.mitre.org/data/definitions/641.html)

**Key Issues Resolved:**

- 8.3.2 - Verify that users have a method to remove or export their data on demand.

- 8.3.3 - Verify that users are provided clear language regarding collection and use of supplied personal information and that users have provided opt-in consent for the use of that data before it is used in any way.

- 12.1.1 - Verify that the application will not accept large files that could fill up storage or cause a denial of service.

- 2.1.7 - Verify that passwords submitted during account registration, login, and password change are checked against a set of breached passwords either locally (such as the top 1,000 or 10,000 most common passwords which match the system's password policy) or using an external API. If using an API a zero knowledge proof or other mechanism should be used to ensure that the plain text password is not sent or used in verifying the breach status of the password. If the password is breached, the application must require the user to set a new non-breached password.

- 2.1.5 - Verify users can change their password.

- 12.3.4 - Verify that the application protects against Reflective File Download (RFD) by validating or ignoring user-submitted filenames in a JSON, JSONP, or URL parameter, the response Content-Type header should be set to text/plain, and the Content-Disposition header should have a fixed filename.

**Other Issues Resolved (Not examplified in analysis):**
- 2.1.1(*) - Verify that user set passwords are at least 12 characters in length (after multiple spaces are combined).

- 2.1.2 - Verify that passwords 64 characters or longer are permitted but may be no longer than 128 characters.

- 2.1.3(*) - Verify that password truncation is not performed. However, consecutive multiple spaces may be replaced by a single space.

- 2.1.4 - Verify that any printable Unicode character, including language neutral characters such as spaces and Emojis are permitted in passwords.

- 2.1.6 - Verify that password change functionality requires the user's current and new password.

- 2.1.8 - Verify that a password strength meter is provided to help users set a stronger password.

- 2.1.9 - Verify that there are no password composition rules limiting the type of characters permitted. There should be no requirement for upper or lower case or numbers or special characters.

- 2.1.11 - Verify that "paste" functionality, browser password helpers, and external password managers are permitted.

- 2.1.12 - Verify that the user can choose to either temporarily view the entire masked password, or temporarily view the last typed character of the password on platforms that do not have this as built-in functionality.

    (\*) -> multiple spaces are not combined   

## How to run
> :warning: ***Python version MUST be 3.10.11 due to greenlet compatibility issues***

1. Download files ():
    ```bash
    git clone git@github.com:detiuaveiro/2nd-project-group_30.git
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

    original version:
    ```bash
    python3 app_org/app_sec/app.py
    ```

    improved version:
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