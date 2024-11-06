# File: cwx_aiml_app_template/templates/structure.py
DIRECTORY_STRUCTURE = {
    "api": {
        "__init__.py": "",
        "endpoints.py": "# Define your API endpoints here\n",
        "serializers.py": "# Define your serializers here\n"
    },
    "data": {
        "__init__.py": "",
        "external": {"__init__.py": ""},
        "interim": {"__init__.py": ""},
        "processed": {"__init__.py": ""},
        "raw": {"__init__.py": ""}
    },
    "evaluation": {
        "__init__.py": "",
        "metrics.py": "# Define your evaluation metrics here\n"
    },
    "examples": {
        "__init__.py": "",
        "sample_usage.py": "# Add example usage of your models here\n"
    },
    "notebooks": {
        "__init__.py": "",
        "exploratory.ipynb": "{\"cells\": [], \"metadata\": {}, \"nbformat\": 4, \"nbformat_minor\": 4}"
    },
    "src": {
        "__init__.py": "",
        "config": {
            "__init__.py": "",
            "settings.py": "# Define your configuration settings here\n"
        },
        "models": {
            "__init__.py": "",
            "base.py": "# Define your base model classes here\n"
        },
        "utils": {
            "__init__.py": "",
            "helpers.py": "# Define utility functions here\n"
        }
    },
    "tests": {
        "__init__.py": "",
        "conftest.py": "# Define your pytest fixtures here\n",
        "test_models.py": "# Add your model tests here\n"
    }
}