## Data Science Research

# Overview
This repository is a part of `Data Science Research` at `Seattle University`.

- The repository contains Flask applicaion code to generate synthetic data for the minority class for a `csv` file input.
- The website also provides option to choose a particular balancing algorithm and also visualize the results.

# Features 
- Upload an unbalanced CSV file.
- Choose from various balancing algorithms.
- Generate a balanced CSV file.
- Download the balanced CSV file.

### Getting Started 
Setting up
- Clone the repository
- Run `pip install -r requirements.txt`

Usage
- Run `python app.py`
- Open a web browser and navigate to `http://localhost:5000` to access the application.

Default Setup
- Use the home page to balance your dataset if your dataset has values `between 0 and 1`.
- Else, to select a custom `activation` function or to modify the balancing algorithm, click on `Algorithms`.
 
## Screenshot
<div>
<img src="https://github.com/SartajBhuvaji/Flask-app-Data-Augmentation/blob/main/github_readme/image_1.jpg" alt="Alt Text">
</div>


## Balancing Algorithms
- AutoEncoders
    - Balanced
    - Single Encoder
    - Heavy Decoder

# For Team
- To add your code, update `index.html`
- Call your function from `main.py`
- Validate in `validate.py`
- Add your code to `scripts` folder , you can follow the `algorithm_template.py`

# Do not change app.py