from flask import Flask, render_template, request
import joblib
import os

from predict import predict_price

# Flask App Initialization
app = Flask(__name__)

# Load Trained Model
MODEL_PATH = os.path.join("model", "house_price_model.pkl")
FEATURE_PATH = os.path.join("model", "feature_names.pkl")

model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURE_PATH)

# Routes
@app.route("/")
def home():
    return render_template(
        "index.html",
        prediction=None,
        category=None,
        user_input=None,
        error=None
    )

@app.route("/predict", methods=["POST"])
def predict():
    try:
    
        # Get form values
        user_input = {

            # Numerical Features
            "area": float(request.form["area"]),
            "bedrooms": int(request.form["bedrooms"]),
            "bathrooms": int(request.form["bathrooms"]),
            "stories": int(request.form["stories"]),
            "parking": int(request.form["parking"]),

            # Categorical Features
            "mainroad": request.form["mainroad"],
            "guestroom": request.form["guestroom"],
            "basement": request.form["basement"],
            "hotwaterheating": request.form["hotwaterheating"],
            "airconditioning": request.form["airconditioning"],
            "prefarea": request.form["prefarea"],
            "furnishingstatus": request.form["furnishingstatus"]

        }
        
        print("\nReceived User Input:")
        print(user_input)
        
        # Validation
        
        if user_input["area"] <= 0:
            raise ValueError("Area must be greater than 0.")
        
        if user_input["bedrooms"] < 0:
            raise ValueError("Bedrooms cannot be negative.")
                
        if user_input["bathrooms"] < 0:
            raise ValueError("Bathrooms cannot be negative.")
        
        if user_input["stories"] < 0:
            raise ValueError("Stories cannot be negative.")
        
        if user_input["parking"] < 0:
            raise ValueError("Parking cannot be negative.")
        
        predicted_price = predict_price(
            model,
            feature_names,
            user_input
        )
        
        return render_template(
            "index.html",
            prediction=predicted_price,
            category=category,
            user_input=user_input
        )
        
    except ValueError as e:
        
        return render_template(
            "index.html",
            prediction=None,
            category=None,
            user_input=None,
            error=str(e)
        )

    except Exception:
        
        if predicted_price < 3000000:
            category = "Affordable Home"
            
        elif predicted_price < 7000000:
            category = "Mid-Range Home"
        
        else:
            category = "Luxury Home"
            
        return render_template(
            "index.html",
            prediction=predicted_price,
            category=category,
            user_input=user_input,
            error=None
            
        )        
# Run Server
if __name__ == "__main__":
    app.run(debug=True)