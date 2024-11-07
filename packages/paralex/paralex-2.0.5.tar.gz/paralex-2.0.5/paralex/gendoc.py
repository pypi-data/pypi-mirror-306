#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module generates standard files & documentation.
"""
import frictionless as fl
import json
from .paths import docs_path, standard_path
from .markdown import to_markdown
from .meta import package_from_kwargs
import requests
import io
import zipfile
import pandas as pd

def _make_standard_package(*args, **kwargs):
    with (standard_path / "package_spec.json").open('r', encoding="utf-8") as flow:
        package_infos = json.load(flow)

    with (standard_path / "columns_spec.json").open('r', encoding="utf-8") as flow:
        columns = json.load(flow)

    with (standard_path / "tables_spec.json").open('r', encoding="utf-8") as flow:
        tables = json.load(flow)["tables"]

    resources = []
    for table in tables:
        # replace column names by their full definition
        table["schema"]["fields"] = [dict(columns[f]) for f in table["schema"]["fields"]]

        if table["name"] == "forms":
            for col in table["schema"]["fields"]:
                if col["name"] in ["lexeme", "cell"]:
                    col["constraints"] =  {"required": True }

        resources.append(fl.Resource(table))

    package = package_from_kwargs(resources=resources, **package_infos)

    package.to_json(str(standard_path / "paralex.package.json"))


def _gather_dataset_info():
    response = requests.get('https://zenodo.org/api/records',
                            params={'communities': 'paralex'})

    data = []
    for record in response.json()["hits"]["hits"]:
        doi = record["links"]["doi"]
        title = record["title"]
        for file in requests.get(record["links"]["files"]).json()["entries"]:
            file_link = file["links"]["content"]


            with zipfile.ZipFile(io.BytesIO(requests.get(file_link).content)) as zfile:
                for info in zfile.infolist():
                    if info.filename.endswith('.json'):
                        try:
                            json_data = json.loads(zfile.read(info.filename))
                            data.append({"doi": doi,
                                         "name": json_data.get("name", json_data.get("title", "Unknown")),
                                         "lang": json_data.get("languages_iso639", "Unknown")})
                        except Exception as e:
                            print(f"{e} occured at {doi}, {title}")

    ######### TEMPORARY HACK TO FAKE UPDATED DATASETS
    tmp_replacer = {"vlexique":"fra",
                    "eesthetic":"est",
        "PrinParLat":"lat",
        "LatInfLexi":"lat",
        "LeFFI":"ita",
        "paralex_std_modern_arabic":"ara",
        "portuguese_verbal_lexicon":"por",
                    }
    for line in data:
        if line["name"] in tmp_replacer:
            line["lang"] = tmp_replacer[line["name"]]

    ######### END TEMPORARY HACK TO FAKE UPDATED DATASETS

    data = pd.DataFrame(data)
    print(data)

def _write_doc(*args, **kwargs):
    to_markdown(fl.Package(standard_path / "paralex.package.json"),
                docs_path / "specs.md")
    _gather_dataset_info()

