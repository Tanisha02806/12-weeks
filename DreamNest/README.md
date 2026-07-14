# DreamNest – House Price Prediction Preprocessing Pipeline

## Project Overview

DreamNest is a Flask-based web application developed as a hands-on learning project to understand the complete **Machine Learning data preprocessing workflow** while simultaneously strengthening **Frontend Development** skills using modern CSS techniques.

The application allows users to upload a housing dataset and execute every preprocessing step individually through an interactive dashboard. Instead of focusing on achieving the highest prediction accuracy, this project emphasizes understanding **how raw datasets are transformed into machine-learning-ready data**.

The dashboard guides users through each preprocessing stage:

- Dataset Upload
- Data Cleaning
- Categorical Encoding
- Feature Scaling
- Train/Test Split
- Scikit-Learn Pipeline

Each stage updates the interface in real time, providing a visual representation of the preprocessing workflow.

---

# Project Objectives

The primary objective of DreamNest was to gain practical experience with:

- Building responsive web interfaces
- Creating structured Flask applications
- Working with real-world datasets
- Understanding the Machine Learning preprocessing pipeline
- Learning modern CSS layout techniques
- Implementing an interactive workflow using Python and Flask

---

# Features

- Upload CSV datasets
- Dataset preview
- Dataset statistics
- Missing value handling
- One-Hot Encoding
- Feature Scaling
- Train/Test Split
- Scikit-Learn Pipeline
- Progress Tracker
- Fully Responsive UI
- Cute pastel-themed interface

---

# Machine Learning Workflow

```
Dataset Upload
       │
       ▼
Data Cleaning
       │
       ▼
Categorical Encoding
       │
       ▼
Feature Scaling
       │
       ▼
Train/Test Split
       │
       ▼
Scikit-Learn Pipeline
```

Each preprocessing stage is executed independently, helping visualize how data moves through a typical Machine Learning pipeline.

---

# Learning Outcomes

This project was built as a demonstration of learning and implementing the following topics.

---

## Advanced CSS Layouts

During the development of DreamNest, the following CSS concepts were implemented:

### Flexbox

Used for:

- Navigation Bar
- Hero Section
- Upload Section
- Dashboard Alignment
- Pipeline Tracker
- Card Alignment
- Footer Layout

Skills demonstrated:

- `display: flex`
- `justify-content`
- `align-items`
- `flex-direction`
- `gap`
- Responsive alignment

---

### CSS Grid

Implemented for:

- Feature Cards
- Dataset Information Cards
- Dashboard Cards
- Analysis Section

Skills demonstrated:

- `display: grid`
- `grid-template-columns`
- `auto-fit`
- `minmax()`
- Responsive grids
- Card layouts

---

### Positioning

Implemented:

- Sticky Navigation Bar
- Fixed layout behavior
- Card positioning
- Progress tracker alignment

Skills demonstrated:

- `position: sticky`
- `top`
- `z-index`
- Relative spacing

---

### Responsive Design

Designed to work across:

- Desktop
- Tablet
- Mobile

Techniques used:

- Flexible widths
- Percentage-based layouts
- Responsive grids
- Flexible typography
- Fluid spacing

---

### Media Queries

Implemented multiple breakpoints to ensure proper responsiveness.

Concepts covered:

- Layout adjustments
- Grid restructuring
- Mobile navigation
- Responsive cards
- Responsive forms
- Responsive tables

---

### Mobile-First Responsive Components

The project includes responsive implementations of:

- Navigation Bar
- Upload Form
- Dashboard
- Feature Cards
- Information Cards
- Tables
- Pipeline Tracker
- Progress Bar
- Buttons

---

# Machine Learning Concepts Learned

This project demonstrates the complete preprocessing workflow required before training a Machine Learning model.

### Dataset Handling

- CSV Upload
- Pandas DataFrames
- Dataset Analysis
- Missing Value Detection

---

### Data Cleaning

Implemented:

- Numerical missing values → Median
- Categorical missing values → Mode

---

### Encoding

Implemented:

- One-Hot Encoding
- Categorical Feature Detection

---

### Scaling

Implemented:

- StandardScaler

---

### Train/Test Split

Implemented:

- 80/20 Split
- Random State
- Feature/Target Separation

---

### Scikit-Learn Pipeline

Implemented:

- Pipeline
- ColumnTransformer
- fit()
- transform()

---

# Tech Stack

## Frontend

- HTML5
- CSS3
- Jinja2 Templates

---

## Backend

- Python
- Flask

---

## Machine Learning

- Pandas
- NumPy
- Scikit-Learn

---

## Libraries Used

- Flask
- Pandas
- NumPy
- Scikit-Learn
- Joblib

---

# Project Structure

```
DreamNest/

│
├── app.py
│
├── ml/
│   ├── analyzer.py
│   ├── cleaning.py
│   ├── encoding.py
│   ├── scaling.py
│   ├── splitter.py
│   └── pipeline_builder.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   ├── upload.html
│   └── dashboard.html
│
├── static/
│   └── style.css
│
├── uploads/
│   ├── cleaned_dataset.csv
│   ├── encoded_dataset.csv
│   ├── scaled_dataset.csv
│   ├── X_train.csv
│   ├── X_test.csv
│   ├── y_train.csv
│   ├── y_test.csv
│   └── pipeline.pkl
│
└── requirements.txt
```

---

# Future Improvements

- Model Training
- House Price Prediction
- Data Visualization
- Feature Importance
- Download Processed Dataset
- User Authentication
- Database Integration
- Model Performance Metrics
- Deployment on Render

---

# Summary

DreamNest is a practical learning project that combines **Frontend Development** and **Machine Learning preprocessing** into a single interactive web application.

From a frontend perspective, the project demonstrates modern web development concepts including **Advanced CSS layouts, Flexbox, CSS Grid, responsive design, media queries, mobile-first development, sticky navigation, and responsive dashboards**.

From a machine learning perspective, it showcases the complete preprocessing pipeline using **Pandas** and **Scikit-Learn**, including data cleaning, encoding, scaling, train/test splitting, and pipeline creation.

Rather than focusing solely on prediction accuracy, DreamNest emphasizes understanding **how real-world datasets are prepared before machine learning models are trained**, making it a strong educational project that highlights both software engineering and frontend development skills.