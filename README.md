# QR Code Generator

This Python application generates QR codes based on user input strings. It offers options to add common prefixes and postfixes to the input string or generate the QR code directly from the input. The generated QR code is displayed in a graphical user interface using Tkinter.

## Description

The QR Code Generator application allows users to create QR codes for any string input. It provides two options for generating QR codes:
- With assumptions of common prefixes and postfixes (e.g., http://, www., .com).
- Without any assumptions, allowing custom input handling.

The application uses the `pyqrcode` library to generate QR codes and `tkinter` for the graphical user interface. It includes error handling to ensure valid input and displays the generated QR code with a message confirming its creation.

## Features

- Two modes of generating QR codes: with and without assumptions.
- User-friendly interface using Tkinter with input validation.
- Displays the generated QR code and status messages.

## Usage

1. Enter any string into the input field.
2. Click on "Generate QR Code (with Prefix & Postfix)" to create a QR code with assumptions.
3. Alternatively, click on "Generate QR Code" for a QR code without assumptions.
4. The generated QR code and a success message will be displayed.

## Requirements

- Python 3.x
- tkinter
- pyqrcode

## Installation

Clone the repository and install dependencies using pip:

```bash
git clone https://github.com/yourusername/qr-code-generator.git
cd qr-code-generator
pip install -r requirements.txt
