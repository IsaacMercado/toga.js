# Toga.js

Compile [Toga](https://toga.readthedocs.io/) toga applications in javascript using Transcrypt and Bootstrap 4.

## Requeriments

- Python 3.6 or later
- Transcrypt 3.7.16 or later

It is recommended to use a virtual environment and install python packages. As follows:

**In linux**

´´´
python -m venv venv_toga
source venv_toga/bin/activate
pip install -r requeriments.txt
´´´

## Run samples

You write on the console.

´python -m transcrypt -b -m -n -ec -xp ./ path/to/app.py´

### Examples

Run single sample

´python -m transcrypt -b -m -n -ec -xp ./ samples/s1_togajs/app.py´

Run React Demo

´python -m transcrypt -b -m -n -ec -xp ./ samples/react_demo/react_demo.py´