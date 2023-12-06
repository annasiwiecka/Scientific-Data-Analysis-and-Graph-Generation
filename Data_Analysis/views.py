from django.shortcuts import render, redirect
from .models import *
from .forms import *
from urllib.parse import quote, unquote
from django.shortcuts import get_object_or_404


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
            data_name_str = form.cleaned_data['data_name']

            data_name, created = DataName.objects.get_or_create(name=data_name_str)

            if file.name.endswith(".csv"):
                df = pd.read_csv(file, skiprows=2, header=None)
            elif file.name.endswith(".xlsx"):
                df = pd.read_excel(file, skiprows=2, header=None)
            
            first_column_with_data = df.apply(lambda col: col.first_valid_index(), axis=1).min()

            df = df.iloc[:, int(first_column_with_data):] if pd.notna(first_column_with_data) else df
            
            timestamp_info = TimestampInfo(data_name=data_name, timestamp=timezone.now())
            timestamp_infos = []
            
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
                measurement_value = float(measurement_value) if measurement_value is not None else 0.0

                data_instance = DataModel(
                    data_name=data_name,
                    experiment_name=experiment_name, 
                    measurement_value=measurement_value, 
                    timestamp_info=timestamp_info,
                    processed_data_id=processed_data_id,
                )
                data_instances.append(data_instance)
            
            timestamp_infos.append(timestamp_info)
            TimestampInfo.objects.bulk_create(timestamp_infos)

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
    unique_data_names = DataName.objects.values_list('name', flat=True).distinct()

    data_with_timestamp = []

    for data_name in unique_data_names:
        timestamp_info = TimestampInfo.objects.filter(data_name__name=data_name).order_by('-timestamp').first()
        timestamp = timestamp_info.timestamp if timestamp_info else None
        data_with_timestamp.append({
            'data_name': data_name,
            'timestamp': timestamp
        })

    return render(request, 'Data_Analysis/my_data.html', {
        'data_with_timestamp': data_with_timestamp
    })

def data_analysis(request, data_name):
    data_name_instance = get_object_or_404(DataName, name=data_name)
    preprocessed_data = DataModel.objects.filter(data_name=data_name_instance)
    
    return render(request,"Data_Analysis/data_analysis.html",{
        'data_name': data_name_instance,
        'preprocessed_data': preprocessed_data
        })
