# CWX AIML App Template

A standardized project template generator for AIML (Artificial Intelligence and Machine Learning) applications. This tool helps teams maintain consistency across projects by providing a well-structured template with best practices built in.


## Installation

```bash
pip install cwx-aiml-app-template
```
## Basic Usage
### Create a new AIML project:

```bash
aimlapp init <project_name>
```
### Project Structure

The generated project follows this structure:

```bash
my_project_name/
├── api/                    # API-related code
│   ├── __init__.py
│   ├── endpoints.py        # API endpoint definitions
│   └── serializers.py      # Data serialization logic
│
├── data/                   # Data storage and processing
│   ├── external/           # Data from third-party sources
│   ├── interim/           # Intermediate processed data
│   ├── processed/         # Final, processed data
│   └── raw/               # Original, immutable data
│
├── evaluation/            # Model evaluation scripts
│   ├── __init__.py
│   └── metrics.py         # Evaluation metrics
│
├── examples/              # Example scripts and notebooks
│   ├── __init__.py
│   └── sample_usage.py
│
├── notebooks/            # Jupyter notebooks
│   └── exploratory.ipynb
│
├── src/                  # Source code
│   ├── config/          # Configuration files
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── models/         # Model implementations
│   │   ├── __init__.py
│   │   └── base.py
│   └── utils/         # Utility functions
│       ├── __init__.py
│       └── helpers.py
│
├── tests/              # Test files
│   ├── __init__.py
│   ├── conftest.py    # pytest fixtures
│   └── test_models.py
│
├── Dockerfile         # Container definition
├── requirements.txt   # Project dependencies
├── README.md         # Project documentation
└── version.txt       # Version information
```

### Directory Details

/api

endpoints.py: Define your API endpoints here
serializers.py: Implement data serialization/deserialization

/data

/external: Data from third-party sources
/interim: Intermediate data that has been transformed
/processed: Final, canonical data sets for modeling
/raw: Original, immutable data dumps

/evaluation

Contains scripts for model evaluation:

metrics.py: Implementation of evaluation metrics
Custom evaluation scripts can be added here

/examples

Example implementations and usage:

sample_usage.py: Basic usage examples
Add more example scripts as needed

/notebooks

Jupyter notebooks for:

Data exploration
Model experimentation
Result visualization
Analysis presentation

/src

Main source code:

/config: Configuration management
/models: Model implementations
/utils: Utility functions and helpers

/tests

Test suite:

Unit tests

Integration tests
Test fixtures and configurations

###Advanced Usage
#### Custom Templates
You can customize the generated structure:

``` bash
from cwx_aiml_app_template.generator import create_project_structure
from cwx_aiml_app_template.templates.structure import DIRECTORY_STRUCTURE

# Customize the structure
custom_structure = DIRECTORY_STRUCTURE.copy()
custom_structure["custom_dir"] = {
    "__init__.py": "",
    "custom_module.py": "# Your custom code here\n"
}

# Create project with custom structure
create_project_structure("my_project", structure=custom_structure)
```

#### Docker Support
The generated project includes a Dockerfile:

Dockerfile: Container definition

```bash
# Build the Docker image
docker build -t my-aiml-project .

# Run the container
docker run -it my-aiml-project
```

#### Best Practices

##### Code Organization

Keep raw data immutable
Document data transformations
Use configuration files for parameters
Write tests for critical functionality
Keep notebooks organized and documented

##### Development Workflow

Start with exploratory notebooks
Move stable code to source files
Write tests for new functionality
Document API changes
Update requirements.txt as needed

##### Data Management

Use version control for code, not data
Document data sources and transformations
Keep sensitive data out of version control
Use data validation in pipelines
Maintain data processing scripts

#### Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write or update tests
5. Submit a pull request


#### Troubleshooting

##### Common Issues

1. Import Errors
```bash
# Wrong
from src.models import MyModel
# Correct
from my_project_name.src.models import MyModel
```

2. Path Issues
```bash
# Use pathlib for path handling
from pathlib import Path
data_dir = Path("data/raw")
```

3. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

##### FAQ

Q: Can I use this for non-ML projects?

A: Yes, though the structure is optimized for ML workflows.

Q: How do I update the template?

A: Run pip install --upgrade cwx-aiml-app-template

Q: Can I add custom directories?

A: Yes, see the Custom Templates section above.

###License
This project is licensed under the MIT License - see the LICENSE file for details.