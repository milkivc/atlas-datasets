import os
import requests
import hashlib
from datetime import datetime

TOKEN = os.getenv("ZENODO_TOKEN")
TAG = os.getenv("TAG_NAME", "v1.0.0")
API = "https://zenodo.org/api"

def main():
    r = requests.post(f"{API}/deposit/depositions", json={
        "metadata": {
            "title": f"Atlas Vivo Dataset - {TAG}",
            "upload_type": "dataset",
            "description": "Dataset geospacial do Atlas Vivo - Associação MILK",
            "creators": [
                {"name": "Nuno Filipe Fernandes Vieira Cabral e Araújo", "orcid": "0009-0004-9132-2925", "affiliation": "Associação MILK"},
                {"name": "Eduardo Maurício Vieira Cabral e Araújo", "orcid": "0009-0007-6892-6570", "affiliation": "Associação MILK"}
            ],
            "resource_type": {"type": "dataset", "subtype": "geospatial"},
            "license": "CC-BY-4.0",
            "version": TAG,
            "keywords": ["Atlas Vivo", "MILK", "Portugal", "geospatial", "cultural heritage"],
            "related_identifiers": [
                {"identifier": "https://codeberg.org/milkivc/atlas-datasets", "scheme": "url", "relation": "isSupplementTo"},
                {"identifier": "0009-0004-9132-2925", "scheme": "orcid", "relation": "isAuthoredBy"},
                {"identifier": "0009-0007-6892-6570", "scheme": "orcid", "relation": "isAuthoredBy"}
            ],
            "subjects": [
                {"subject": "geospatial data", "subject_scheme": "GEMET"},
                {"subject": "cultural heritage", "subject_scheme": "INSPIRE"}
            ]
        }
    }, headers={"Authorization": f"Bearer {TOKEN}"})
    deposition_id = r.json()["id"]
    print(f"Deposition criado: {deposition_id}")
