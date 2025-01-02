from django.http import JsonResponse
from rest_framework.decorators import api_view
import pickle
import numpy as np
from django.views.decorators.csrf import csrf_exempt

# Load models from the saved .sav files
with open('Diagnos/trained_models/diabetes_model.sav', 'rb') as f:
    diabetes = pickle.load(f)

with open('Diagnos/trained_models/heart_disease_model.sav', 'rb') as f:
    heart_disease = pickle.load(f)

with open('Diagnos/trained_models/parkinsons_model.sav', 'rb') as f:
    parkinsons = pickle.load(f)

# Disable CSRF validation for testing (you can enable it later if needed)
@csrf_exempt
@api_view(['GET', 'POST'])  # Now allows both GET and POST
def predict_disease(request):
    # Handling GET request
    if request.method == 'GET':
        # Returning a list of available disease types
        disease_types = ['diabetes', 'heart', 'parkinsons']
        return JsonResponse({'available_diseases': disease_types}, status=200)

    # Handling POST request
    elif request.method == 'POST':
        try:
            data = request.data
            disease_type = data.get('disease_type')
            symptoms = data.get('symptoms')
            
            if not disease_type or not symptoms:
                return JsonResponse({'error': 'Missing disease_type or symptoms'}, status=400)

            # Handle predictions based on disease type
            if disease_type == 'diabetes':
                symptoms = np.array(symptoms).reshape(1, -1)
                prediction = diabetes.predict(symptoms)[0]
                diagnosis = 'Diabetic' if prediction == 1 else 'No Diabetes'
            
            elif disease_type == 'heart':
                symptoms = np.array(symptoms).reshape(1, -1)
                prediction = heart_disease.predict(symptoms)[0]
                diagnosis = 'Heart Disease' if prediction == 1 else 'No Heart Disease'
            
            elif disease_type == 'parkinsons':
                symptoms = np.array(symptoms).reshape(1, -1)
                prediction = parkinsons.predict(symptoms)[0]
                diagnosis = 'Parkinson\'s Disease' if prediction == 1 else 'No Parkinson\'s Disease'
            
            else:
                return JsonResponse({'error': 'Invalid disease type'}, status=400)

            return JsonResponse({'prediction': diagnosis}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
