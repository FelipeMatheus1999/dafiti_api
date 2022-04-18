import csv
import io
import tablib
import pandas as pd

from django.http import HttpResponse
from import_export import resources
from rest_framework import status
from rest_framework.response import Response
from tablib import Dataset

from apps.category.models import CategoryModel


class DBToFile:
    def __init__(self):
        pass

    supported_files_types = ("xlsx", "csv")
    resource = None

    @staticmethod
    def convert_file_to_excel(data_frame, file_name):
        bio = io.BytesIO()
        writer = pd.ExcelWriter(bio, engine="xlsxwriter")
        data_frame.to_excel(writer, f"{file_name}.xlsx", index=False)
        writer.save()
        bio.seek(0)

        excel_file = bio.read()

        return excel_file

    def create_excel_file(self, resources, file_name):
        resource = resources()
        dataset = resource.export()
        df = pd.read_excel(dataset.xlsx)

        excel_file = self.convert_file_to_excel(df, file_name)

        return excel_file

    def http_csv(self, _):
        dataset = self.resource().export()
        response = HttpResponse(dataset.csv, content_type="text/csv")
        response.headers["Content-Disposition"] = f'attachment; filename="Products.csv"'
        return response

    def http_excel(self, resources, file_name):
        excel_file = self.create_excel_file(resources, file_name)
        response = HttpResponse(excel_file, content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f'attachment; filename="{file_name}.xlsx"'

        return response

    def is_supported(self, file_type):
        return file_type in self.supported_files_types


class ExportCSVMixin(DBToFile):
    fields_to_csv = None
    queryset = None
    serializer_class = None
    model_import = None

    errors = []
    count_lines = 0

    @staticmethod
    def get_itertuples(request):
        dataframe = pd.read_csv(request.data["file"].file)

        return dataframe.itertuples()

    @staticmethod
    def get_field_or_none(field):
        return field if str(field) != "nan" else None

    def get_fields(self, row):
        try:
            received_fields = {
                "title": self.get_field_or_none(row.Title),
                "description": self.get_field_or_none(row.Description),
                "image": self.get_field_or_none(row.Image),
                "price": float(row.Price) if str(row.Price) != "nan" else None,
                "stock": int(float(row.Stock)) if str(row.Stock) != "nan" else None,
                "categories": self.get_field_or_none(row.Categories),
                "date_joined": self.get_field_or_none(row._8),
                "date_modified": self.get_field_or_none(row._9),
                "is_active": self.get_field_or_none(row._10),
            }

            fields = {
                k: v
                for k, v in received_fields.items()
                if received_fields[k] is not None
            }

            return fields
        except Exception as e:
            self.errors.append(str(e))
            return {}

    def create_instance(self, fields):
        try:
            categories = (
                fields["categories"].split(" | ") if "categories" in fields else []
            )
            categories = [
                CategoryModel.objects.get(id=int(category)) for category in categories
            ]

            if "categories" in fields:
                del fields["categories"]

            instance = self.model_import.objects.create(**fields)

            instance.categories.set(categories)
            instance.save()
        except Exception as e:
            self.errors.append(str(e))

    @staticmethod
    def get_id(row):
        return row._1

    def id_is_none(self, row):
        return str(self.get_id(row)) == "nan"

    def import_csv_file(self, request):
        itertuples = self.get_itertuples(request)

        for row in itertuples:
            if self.id_is_none(row):
                self.create_instance(self.get_fields(row))

            self.count_lines += 1

        import_status = (
            status.HTTP_200_OK if len(self.errors) == 0 else status.HTTP_400_BAD_REQUEST
        )

        return Response(
            {
                "count_lines": self.count_lines,
                "count_errors": len(self.errors),
                "errors": self.errors,
            },
            status=import_status,
        )

    def export_csv_file(self, _):
        dataset = self.resource().export()
        response = HttpResponse(dataset.csv, content_type="text/csv")
        response.headers[
            "Content-Disposition"
        ] = f'attachment; filename="{self.model_import.__name__}.csv"'
        return response
