# VITA Validation Software

## Description

The **VITA Validation Software** is a Python-based application designed for dentists and dental professionals to validate their accuracy in predicting the color of a tooth sample. Users are shown a random sample from the 16 shapes in the VITA Classical shade guide and must determine the correct matching shade based on the reference chart. After making a decision, users can submit their predicted shade along with their confidence level (0-1).

### Features
- Randomized selection of tooth samples from the VITA Classical shade guide.
- Input interface for selecting the predicted shade and confidence level.

### Installation

1. Download the library as a .zip file from the "Clone or Download" option or from the releases section.
2. Unzip the file into a local folder.
3. In the main directory, install the external libraries using the following command: 
```
pip install -r VITA_VS\requirements.txt
```
4. Now it's possible to use one of the different test programs located in the test directory. Here's an example of usage, _color_percentage_ is just an example of the test programs; it can be run with all the files present in that test directory:
```
python VITA_VS\vs_app.py
```
