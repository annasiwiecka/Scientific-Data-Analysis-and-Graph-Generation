from django import forms


class DataUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "accept": ".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }
        )
    )

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file:
            file_name = file.name
            if not file_name.endswith((".csv", ".xlsx")):
                raise forms.ValidationError(
                    "Unsupported file format. Please upload a CSV or Excel file."
                )
        return file
