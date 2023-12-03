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
            
            df = df.iloc[2:]

            processed_data_id = generate_unique_id()
            if DataModel.objects.filter(processed_data_id=processed_data_id).exists():
                return redirect("success_page", processed_data_html=processed_data_id, data_name=data_name)

            column_mapping = {
                "experiment_name": None,
                "value": None,
            }

            for column in df.columns:
                values = df[column].astype(str).str.strip()

                if pd.to_numeric(values, errors="coerce").notna().all():
                    column_mapping["value"] = column

                if not pd.to_numeric(values, errors="coerce").notna().all():
                    column_mapping["experiment_name"] = column

            if (
                column_mapping["value"] is not None
                and column_mapping["experiment_name"] is not None
            ):
                data_instances = [
                    DataModel(
                        data_name=data_name,
                        experiment_name=row[column_mapping["experiment_name"]],
                        measurement_value=row[column_mapping["value"]],
                        timestamp=timezone.now(),
                        processed_data_id=processed_data_id,
                    )
                    for _, row in df.iterrows()
                ]
                DataModel.objects.bulk_create(data_instances)

                return redirect("success_page", processed_data_html=processed_data_id, data_name=data_name)
            else:
                pass
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
