# pyDivar

![pyDivar Icon](pics/icon.jpg)

**pyDivar** - The best divar crawler ever.

## Table of Contents

- [pyDivar](#pydivar)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

Welcome to **pyDivar**, a Python-based crawler designed to extract data from Divar, the largest classified ads website in Iran. This tool is aimed at providing efficient and robust data scraping capabilities to help you gather information from Divar seamlessly.

## Features

- Efficient data extraction from Divar.
- Easy-to-use interface.
- Customizable crawling settings.

## Installation

To install **pyDivar**, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/hadif1999/pyDivar.git
    ```

2. Navigate to the project directory:
    ```sh
    cd pyDivar
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To use **pyDivar**, follow these steps:

1. Change the config as per your need:
    1.1. Login to Divar in your browser.
    <br>
    1.2. Open the inspect tool and navigate to the network section.
    <br>
    1.3. Copy the content of the "Authorization" header from the response header of one of the pages that contains this header.
    <br>
    1.4. Add this to `config.json` as the `general.AUTH_TOKEN` field.
    <br>
    1.5. Change `general.category` to your desired category (find this category by copying from the URL of Divar when selecting a category).
    <br>
2. Run the following command:
    ```sh
    python3 main.py
    ```

3. The result will be saved as an XLSX file to the path specified in `general.output_path` of the config.

> **Note:** If crawling stops due to an error, check Divar and select a post, then pass the CAPTCHA by clicking on "اطلاعات تماس" then try again.
> <br>
> **Note 2:** If you are not in Iran, your IP will be banned after retrieving approximately 1 page (around 24 phone numbers).
> If you are in Iran, you can retrieve around 8 pages before your IP gets banned. After that, you will need to change your IP. The ban duration on Divar is approximately 24 hours.

## Contributing

We welcome contributions to **pyDivar**! If you have any suggestions, bug fixes, or new features, please feel free to submit a pull request. Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to customize this template to better fit your project's needs.
