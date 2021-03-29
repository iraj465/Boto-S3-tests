# Boto S3 tests
This repository contains tests for boto S3 for both [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) and [Boto2](http://boto.cloudhackers.com/en/latest/) SDKs.


## Getting started

* Clone the repository:
```bash
git clone git@github.com:iraj465/Boto-S3-tests.git
cd Boto-S3-tests
```
* Install virtual environment and required dependencies:

```bash
# Create a virtual environment
$ python3 -m venv env
$ source ./env/bin/activate

# Install the dependencies:
$ pip install -r requirements.txt

```
* Copy `.env.example` to `.env` or create your own `.env` and fill in the credentials as given in `.env.example`

* Runs tests for Boto3 SDK by running:
```bash
coverage run --source boto3/ -m pytest boto3/tests_s3.py
```

* Runs tests for Boto2 SDK by running:
```bash
coverage run --source boto2/ -m pytest boto2/tests_s3.py
```

* Run the following command to generate coverage report:
```bash
coverage report
```

* Run the following command to generate coverage report in html(for website viewing):
```bash
coverage html
```
