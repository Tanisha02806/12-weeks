HireWise AI — Employee Attrition Prediction System
📌 Project Summary

HireWise AI is a machine-learning-powered web application designed to predict the likelihood of employee attrition based on employee and workplace characteristics.

The application provides an interactive interface where users can enter employee information such as age, job role, monthly income, job satisfaction, overtime, work-life balance, and other relevant factors. The trained machine-learning model then generates an attrition risk prediction and probability, along with supporting information such as feature importance and prediction history.

The project also demonstrates my practical understanding of advanced CSS layouts, responsive web design, Flexbox, CSS Grid, positioning, responsive navigation, cards, forms, and mobile-first design.

Rather than being only an ML project, HireWise AI demonstrates how a machine-learning system can be presented through a structured, responsive, and user-friendly web interface.

🎯 Project Objectives
Build a web-based employee attrition prediction system.
Integrate a trained machine-learning classification model with a Flask application.
Create an intuitive employee prediction form.
Display prediction probability and risk level clearly.
Maintain prediction history.
Provide analytics and model information.
Build a responsive interface that works across desktop, tablet, and mobile devices.
Demonstrate practical application of modern CSS layout and responsive-design concepts.
🧠 Key Features
Employee Attrition Prediction

Users can enter employee information including:

Age
Business Travel
Job Role
Job Satisfaction
Monthly Income
Number of Companies Worked
Over Time
Environment Satisfaction
Work-Life Balance

The model processes these inputs and provides:

Attrition prediction
Attrition probability
Risk level
Risk interpretation
📊 Analytics Dashboard

The application provides an analytics section containing information such as:

Dataset statistics
Prediction activity
Model information
Feature importance
Model performance/comparison information
Insights derived from the model
📋 Prediction History

Predictions are stored so users can review previous analyses.

The history section provides a structured view of previous predictions and allows users to start a new prediction or move to analytics.

🎨 Responsive User Interface

The UI was designed to work across:

Desktop
Laptop
Tablet
Mobile
Small-screen devices

The design uses responsive CSS rather than creating separate desktop and mobile pages.

💻 Frontend Skills Demonstrated

One of the major goals of this project was to demonstrate practical understanding of advanced CSS layouts and responsive design.

1. Advanced CSS Layouts

The project uses multiple CSS layout techniques to organize complex application interfaces.

Different sections such as dashboards, analytics cards, forms, result panels, and navigation elements are arranged using modern CSS layout approaches.

This demonstrates the ability to move beyond basic styling and create structured application layouts.

2. Flexbox

Flexbox is used for one-dimensional layouts where elements need to be aligned horizontally or vertically.

Examples include:

Navigation links
Button groups
Hero actions
Result-page actions
Prediction activity actions
Footer layouts
Responsive form sections

For example:

.hero-actions {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}

This allows buttons to automatically wrap when the available screen width decreases.

3. CSS Grid

CSS Grid is used for structured two-dimensional layouts.

It is particularly useful for:

Dashboard cards
Analytics sections
Statistics
Model comparison sections
Form layouts
Multi-column content

The layout can transition from multiple columns on desktop to a single column on mobile.

Example:

.analytics-grid {
    display: grid;
    grid-template-columns:
        repeat(3, minmax(0, 1fr));
    gap: 24px;
}

On smaller screens:

@media (max-width: 768px) {


    .analytics-grid {
        grid-template-columns: 1fr;
    }


}

This demonstrates practical use of CSS Grid together with responsive design.

📍 4. Positioning

The project demonstrates CSS positioning through UI elements such as:

Navigation elements
Active navigation indicators
Card accents
Loading indicators
Accessibility elements
Fixed/positioned interface components where appropriate

For example, the active navigation indicator uses positioning:

.nav-link {
    position: relative;
}


.nav-link.active::after {
    content: "";


    position: absolute;


    left: 50%;
    bottom: -7px;


    width: 5px;
    height: 5px;


    border-radius: 50%;
}

This demonstrates control over element positioning relative to its parent.

📌 5. Sticky / Fixed Layout Concepts

The project demonstrates understanding of positioning elements independently from normal document flow.

This is useful for application interfaces where navigation, accessibility controls, or important actions need to remain available while the user interacts with a page.

The project also uses positioning concepts for elements such as:

Navigation UI
Skip-to-content accessibility controls
UI indicators
Floating/positioned elements
📱 6. Responsive Design

Responsive design is one of the main focuses of HireWise AI.

Instead of designing only for a desktop screen, the application adapts its layout according to the available viewport.

The project uses CSS media queries such as:

@media (max-width: 768px) {
    ...
}

and:

@media (max-width: 480px) {
    ...
}

This allows layouts to change based on screen size.

📐 7. Media Queries

Media queries are used to modify:

Grid columns
Navigation layout
Button sizing
Form layouts
Card spacing
Typography
Tables
Chart containers
Mobile actions

For example:

@media (max-width: 768px) {


    .form-grid {
        grid-template-columns: 1fr;
    }


}

A multi-column form can therefore become a single-column form on smaller devices.

📱 8. Mobile-First / Responsive Thinking

The project emphasizes responsive thinking by ensuring that components remain usable when screen space becomes limited.

For example:

Desktop
┌────────────┬────────────┬────────────┐
│   Card     │   Card     │   Card     │
└────────────┴────────────┴────────────┘


Tablet
┌────────────┬────────────┐
│   Card     │   Card     │
├────────────┴────────────┤
│          Card           │
└─────────────────────────┘


Mobile
┌─────────────────────────┐
│          Card           │
├─────────────────────────┤
│          Card           │
├─────────────────────────┤
│          Card           │
└─────────────────────────┘

This demonstrates how the same content can be reorganized rather than simply shrunk.

🧭 9. Responsive Navbar

The navigation system is shared throughout the application.

It provides access to:

Home
Predict
Prediction History
Analytics

The navigation adapts to smaller screens using responsive layout rules.

The project also includes:

Active-page indication
Keyboard focus states
Responsive navigation spacing
Mobile navigation behavior
Consistent navigation across pages
🃏 10. Responsive Cards

Cards are extensively used throughout the application.

Examples include:

Analytics cards
Dataset statistics
Model information
Feature importance
Prediction results
Prediction history
Insights

Cards use:

Border radius
Borders
Shadows
Hover states
Responsive widths
Responsive spacing

Example:

.analytics-stat-card {
    border-radius: 14px;


    border: 1px solid
        rgba(0, 0, 0, 0.08);


    box-shadow:
        0 4px 18px
        rgba(0, 0, 0, 0.05);
}
📝 11. Responsive Forms

The prediction form demonstrates responsive form design.

On larger screens, fields can be arranged into multiple columns, while on smaller screens they transition into a single-column layout.

The form also demonstrates:

Input validation
Required fields
Error states
Loading states
Accessible focus states
Responsive controls
Mobile-friendly buttons
♿ 12. Accessibility

The project also incorporates accessibility-focused UI improvements.

Examples include:

Keyboard focus indicators
aria-invalid
aria-busy
role="alert"
Skip-to-content navigation
Screen-reader-only content
Reduced-motion support
Visible validation feedback

Example:

<input
    aria-invalid="true"
>

This allows assistive technologies to understand that a field currently contains invalid input.

🛠️ Tech Stack
Frontend
HTML5
CSS3
JavaScript
Flexbox
CSS Grid
Media Queries
Responsive Design
Backend
Python
Flask
Machine Learning
scikit-learn
Pandas
NumPy
Joblib
Random Forest-based classification
Data
HR Employee Attrition dataset
CSV-based dataset processing
Development Tools
Visual Studio Code / code editor
Python virtual environment
Git / GitHub
🏗️ Project Structure
HireWise-AI/
│
├── app.py
├── train_model.py
├── eda.py
├── requirements.txt
├── README.md
│
├── dataset/
│   └── hr.csv
│
├── data/
│   └── ...
│
├── model/
│   ├── trained model
│   ├── preprocessor
│   ├── feature importance
│   └── model information
│
├── templates/
│   ├── index.html
│   ├── predict.html
│   ├── result.html
│   ├── history.html
│   └── analytics.html
│
└── static/
    ├── css/
    │   ├── style.css
    │   ├── predict.css
    │   └── ...
    │
    └── js/
        ├── predict.js
        └── ...
🔄 Application Workflow
             User
               │
               ↓
        HireWise AI UI
               │
               ↓
       Employee Input Form
               │
               ↓
        Client Validation
               │
               ↓
          Flask Backend
               │
               ↓
         Data Preprocessor
               │
               ↓
       ML Classification Model
               │
               ↓
       Prediction + Probability
               │
        ┌──────┴───────┐
        ↓              ↓
     Result          History
        │              │
        └──────┬───────┘
               ↓
            Analytics
🎓 Learning Outcomes

This project demonstrates that I have learned and implemented:

CSS & Frontend
✅ Advanced CSS layouts
✅ Flexbox
✅ CSS Grid
✅ Positioning
✅ Sticky/fixed layout concepts
✅ Responsive design
✅ Media queries
✅ Mobile-first/responsive thinking
✅ Responsive navigation
✅ Responsive cards
✅ Responsive forms
✅ Interactive UI states
✅ Accessibility-focused styling
Web Development
✅ HTML5
✅ CSS3
✅ JavaScript
✅ Flask
✅ Form handling
✅ Client-side validation
✅ Server-side validation
✅ Error handling
✅ Dynamic templates
✅ Backend/frontend integration
Machine Learning
✅ Dataset preprocessing
✅ Feature engineering/preprocessing
✅ Classification
✅ Random Forest-based prediction
✅ Probability-based prediction
✅ Feature importance
✅ Model integration into a web application
🚀 Why This Project Demonstrates My Learning

HireWise AI is not just a machine-learning model.

The project demonstrates how I can take a machine-learning concept and turn it into a complete interactive web application.

The frontend specifically demonstrates my understanding of advanced CSS layout techniques, including Flexbox and Grid, while the responsive system demonstrates how the same application can adapt to different screen sizes.

The prediction form demonstrates responsive form design and validation, while the dashboard and analytics pages demonstrate how cards, grids, navigation, charts, and information panels can be combined into a structured application interface.

Overall, the project serves as a practical demonstration of my ability to combine frontend development, responsive CSS, JavaScript, Flask, and machine learning into one complete project.

🔮 Future Improvements

Possible future improvements include:

User authentication
Database-backed prediction history
Admin dashboard
More advanced model comparison
Explainable AI visualizations
SHAP-based explanations
Cloud deployment
REST API
Automated model retraining
More comprehensive accessibility testing
Dark/light theme support
⚠️ Responsible Use

HireWise AI is intended as a decision-support and educational machine-learning application.

Predictions should not be treated as definitive judgments about individual employees. Model outputs should be interpreted alongside appropriate human judgment, organizational context, and other relevant information.

⭐ Project Summary

HireWise AI combines machine learning + Flask + responsive frontend development into a complete employee attrition prediction application.

The project demonstrates practical knowledge of advanced CSS layouts, Flexbox, Grid, positioning, responsive design, media queries, responsive navigation, cards, forms, accessibility, JavaScript validation, Flask backend integration, and machine-learning model deployment.