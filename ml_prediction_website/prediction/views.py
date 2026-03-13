from django.shortcuts import render
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

def index(request):
    return render(request, 'index.html')

def result(request):
    math_score = None
    if request.method == "POST":
        # Get all input values from POST
        gender = request.POST.get("gender")
        race_ethnicity = request.POST.get("race_ethnicity")
        parental_level_of_education = request.POST.get("parental_level_of_education")
        lunch = request.POST.get("lunch")
        test_preparation_course = request.POST.get("test_preparation_course")
        reading_score = request.POST.get("reading_score")
        writing_score = request.POST.get("writing_score")

        # Convert numeric inputs
        try:
            reading_score = int(reading_score)
            writing_score = int(writing_score)
        except:
            reading_score = 0
            writing_score = 0

        data = CustomData(
            gender=gender,
            race_ethnicity=race_ethnicity,
            parental_level_of_education=parental_level_of_education,
            lunch=lunch,
            test_preparation_course=test_preparation_course,
            reading_score=reading_score,
            writing_score=writing_score
        )
        pred_df = data.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        math_score = predict_pipeline.predict(pred_df)[0]

    return render(request, 'result.html', {
        "math_score": math_score
    })