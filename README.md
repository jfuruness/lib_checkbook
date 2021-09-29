
# lib\_checkbook
This package contains functionality to send checks from a CSV using checkbook.io. NOTE: This is an interview question, definitely do not use this for anything else.

* [lib\_checkbook](#lib_checkbook)
* [Description](#package-description)
* [Usage](#usage)
* [Installation](#installation)
* [Development/Contributing](#developmentcontributing)
* [History](#history)
* [Credits](#credits)
* [Licence](#license)
* [To do](#todo)


## Package Description
* [lib\_checkbook](#lib_checkbook)

This package contains functionality to send checks from a CSV. NOTE: This is an interview question, definitely do not use this for anything else.

## Usage
* [lib\_checkbook](#lib_checkbook)

The script will ingest a CSV with the format:

Name,Email,Amount,Check Number,Description

The script will validate and normalize the email. Then the check will be sent. Any errors that occur for any rows will be saved in the error csv path so that you can correct them, delete the errors column, and attempt to send again.

First, export your API keys. I used the default sandbox API keys because my sandbox API keys were not authenticating properly, and I don't have time to contact support.

```
export CHECKBOOK_API_KEY="d6aa2703655f4ba2af2a56202961ca86"
export CHECKBOOK_API_SECRET="dXbCgzYBMibj8ZwuQMd2NXr6rtvjZ8"
```

From the command line:

```lib_checkbook <csv_path> <err_csv_path>```

From python:

```python
from lib_checkbook import CheckSender
CheckSender().send_checks("<csv_path>", "err_csv_path")
```

## Installation
* [lib\_checkbook](#lib_checkbook)

I wrote this in Ubuntu, windows is not supported but might work regardless (assuming os.environ.get works on windows)

```bash
pip3 install "git+https://github.com/jfuruness/lib_checkbook"
```

To install for development:

```bash
git clone git@github.com:jfuruness/lib_checkbook.git
cd lib_checkbook
python3 setup.py develop
```
This will install the package and all of it's python dependencies.


## Development/Contributing
* [lib\_checkbook](#lib_checkbook)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
6. Email me at jfuruness@gmail.com

## History
* [lib\_checkbook](#lib_checkbook)
* 0.0.2 Changed input CSV to have address
* 0.0.1 First working version

## Credits
* [lib\_checkbook](#lib_checkbook)

Thank you to the checkbook.io team for considering me in this application process

## License
* [lib\_checkbook](#lib_checkbook)

BSD License (see license file)

## Todo
* [lib\_checkbook](#lib_checkbook)

* Add address parsing functionality
  * If there is a standardized format for this then the information can be parsed fairly easily, however it doesn't look like that is the case with these CSVs
  * If the address isn't standardized, you come across a situation where you basically need to guess the address
    * There are a few python libraries that can do this
      * USA address package
      * Google APIs (probably the best and most supported)
    * These tools are a risky approach, because you are trying to guess the address, and you could guess incorrectly and send money to the wrong location
    * Additionally, you must check if the address is deliverable.
      * This requires a USPS-Certified service that uses delivery point validation
      * There are APIs that can do this, but I don't have time today to go down this rabbit hole
* Catch all error codes
  * Each error code should be caught and either retried or fail nicely
    * https://docs.checkbook.io/reference/error-codes
* Use idempotent key so that if you retry on error you do not resend the same request
* Use the webhooks to verify the signature
* Make sure the return response comes from the correct IP addresses
* Ensure that this works at scale over large CSVs
* Sanitize the amount of money being sent, so that you must manually verify any transaction sent over a certain amount, or something like that so a user can't send infinite amounts of money
* Slow down for rate limiting
  * continuously query the server until you determine what this rate limit is
* You should have a way of verifying the transactions that you sent in case something happens to your program (you don't want to send it again). Potentially hash a bunch of columns for the idempotent key.
* Add lots of unit testing and system testing
* Move to logging
* General refactoring and other validation steps that I can't think of off the top of my head right now
