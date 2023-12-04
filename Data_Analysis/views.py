from django.shortcuts import render, redirect
from .models import *
from .forms import *
from urllib.parse import quote, unquote

import pandas as pd
import uuid


# Create your views here.


def generate_unique_id():
    return str(uuid.uuid4())


def import_and_preprocess_data(request):
    if request.method == "POST":
        form = DataUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            data_name = form.cleaned_data['data_name']
            if file.name.endswith(".csv"):
                df = pd.read_csv(file, skiprows=2, header=None)
            elif file.name.endswith(".xlsx"):
                df = pd.read_excel(file, skiprows=2, header=None)
            
            first_column_with_data = df.apply(lambda col: col.first_valid_index(), axis=1).min()

            df = df.iloc[:, int(first_column_with_data):] if pd.notna(first_column_with_data) else df
            
            data_instances = []
            for index, row in df.iterrows():
                processed_data_id = generate_unique_id()
                experiment_name = None
                measurement_value = None

                for col_index, value in enumerate(row):
                    if pd.notna(value):
                        if experiment_name is None:
                            experiment_name = value
                        elif measurement_value is None:
                            measurement_value = value
                            break

                experiment_name = str(experiment_name) if experiment_name is not None else '0'
                measurement_value = str(measurement_value) if measurement_value is not None else '0'

                data_instance = DataModel(
                    data_name=data_name,
                    experiment_name=experiment_name, 
                    measurement_value=measurement_value, 
                    timestamp=timezone.now(),
                    processed_data_id=processed_data_id,
                )
                data_instances.append(data_instance)
                
            DataModel.objects.bulk_create(data_instances)

        return redirect("success_page", processed_data_html=processed_data_id, data_name=data_name)

    else:
        form = DataUploadForm()

    return render(request, "Data_Analysis/import_data.html", {
        "form": form
        })


def success_page(request, processed_data_html, data_name):
    decoded_html = unquote(processed_data_html)
    return render(request,"Data_Analysis/success_page.html",{
            "processed_data_html": decoded_html,
            "data_name": data_name
            })


def my_data(request):
    preprocessed_data = DataModel.objects.order_by('-timestamp')

    return render(request, 'Data_Analysis/my_data.html', {
        'preprocessed_data': preprocessed_data
    })

def data_analysis(request, processed_data_id):
    data_instances = DataModel.objects.filter(processed_data_id=processed_data_id)
    
    return render(request,"Data_Analysis/data_analysis.html",{
            "data_instances": data_instances,
            })
