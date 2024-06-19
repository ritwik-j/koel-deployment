from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import torch
import os
from opensoundscape.metrics import predict_multi_target_labels
from django.http import FileResponse
from .apps import MlConfig
import pandas as pd
import os.path

# Create your views here
class PredictAudioView(APIView): 
    permission_classes = [AllowAny]  # Allow this endpoint even withut logged in user
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        data = {'message': 'Hello, get world!'} # test
        return Response(data)
    
    def post(self,request): 
        '''to be abstracted away'''
        if 'audio' not in request.FILES:
            return Response({'error': 'No audio uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        audio_file = request.FILES['audio']  # This is an instance of MIME (in-memory object)

<<<<<<< Updated upstream
        try: 
=======
        audio_file = request.FILES.getlist('audio')  # This is an instance of MIME (in-memory object)
        response_data = {
            "HEADER" : {
                    "fileName": "Summary",
                    "Lat": None,
                    "Long": None,
                    "NumFiles": None,
                    "TotalMins": None,
                    "animal": {},
                },
            "audioFiles" : {}
            }

        try:
>>>>>>> Stashed changes
            # Save audio file temporarily
            temp_file_path = os.path.join(os.getcwd(), '\\tmp', audio_file.name)
            os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
            with open(temp_file_path, 'wb') as f:
                f.write(audio_file.read())

            # print(temp_file_path)

            # Load from MLconfig and make predictions
            predictions = MlConfig.model.predict([temp_file_path])
            
            # Clean up temp folder
            os.remove(temp_file_path)

<<<<<<< Updated upstream
            scores = predict_multi_target_labels(predictions, threshold=0.5) # filter predictions above thresh value
            scores = scores.loc[:, (scores != 0).any(axis=0)] # discard scores which are 0

            # print("nfnrifnri , ", type(scores), scores.columns, scores)

            # csv code
            # csv_file = BytesIO()
            scores_df = pd.DataFrame(scores)
            scores_df.to_csv('csv_outputs.csv', sep=',')

            data = {'scores': scores}

=======
            # scores_df = pd.DataFrame(scores)
            # scores_df.to_csv('csv_outputs.csv', sep=',')
            count = 0
            for file in os.listdir(output_path):
                model_output = pd.read_csv(output_path + file)   # read model output csv into pd dataframe for processing
                model_output = model_output.sort_values(by='Confidence', ascending=False).drop_duplicates(subset=['Scientific name', 'Common name', 'Start (s)'])
                os.remove(output_path + file) # delete old csv
                updated_csv = model_output.to_csv(output_path + file)

                max_end_time = model_output["End (s)"].max()    # creates interval windows for each file read
                intervals = range(0, int(max_end_time) + 3, 3)

                # response_data["audioFiles"][str(count)] = {"fileName": str(file), "animal": {}}

                print("01")

                for _, row in model_output.iterrows():
                    common_name = row["Common name"]
                    scientific_name = row["Scientific name"]
                    animal_key = f"{common_name}_{scientific_name}"
                    print("01a")
                    # loop through results of each file
                    print(str(animal_key))
                    print(str(count))
                    print(response_data)
                    if str(animal_key) not in response_data["audioFiles"][count]["animal"]:
                        print("01b")
                        response_data["audioFiles"][count]["animal"][animal_key] = {str(i // 3): 0 for i in intervals} # initialize animal detection confidence scores to 0
                    print("01c")
                    if animal_key not in response_data["0"]["animal"]:
                        print("01d")
                        response_data["0"]["animal"][animal_key] = {"file": set(), "occurrences": [0]}

                print("02")

                for _, row in model_output.iterrows():
                    start, end = row["Start (s)"], row["End (s)"]
                    common_name = row["Common name"]
                    scientific_name = row["Scientific name"]
                    confidence = row["Confidence"]
                    animal_key = f"{common_name}_{scientific_name}"

                    for i in range(len(intervals)):
                        interval_start = intervals[i]
                        interval_end = intervals[i + 1] if i + 1 < len(intervals) else interval_start + 3

                        if start < interval_end and end > interval_start:
                            response_data["audioFiles"][count]["animal"][animal_key][str(i)] = confidence
                            print("02x")
                            response_data["0"]["animal"][animal_key]["occurrences"][0] += 1

                            print("02a")

                            if count not in response_data["0"]["animal"][animal_key]["file"]:
                                response_data["0"]["animal"][animal_key]["file"].add(count)         # add file number to "file" : {}

                            print("02b")

                print("03")

                count += 1

            print("04")

            # For front-end to receive
            data = {'result': response_data}

>>>>>>> Stashed changes
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # return Response(data)
        return Response(data)

class PredictWithCsvView(APIView): 
    permission_classes = [AllowAny]  # Allow this endpoint even withut logged in user
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        data = {'message': 'Hello, get world!'} # test
        return Response(data)
    
    def post(self,request): 
        
        try: 
            # Save audio file temporarily
           os.path.isfile('csv_outputs.csv')


        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # return Response(data)
        return FileResponse(open('csv_outputs.csv', 'rb'), as_attachment=True)