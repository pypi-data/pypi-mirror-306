# File: cwx_aiml_app_template/generator.py
import os
import shutil
from pathlib import Path
from .templates.structure import DIRECTORY_STRUCTURE

def create_file(path, content=""):
    """Create a file with the given content"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def create_directory(path):
    """Create a directory if it doesn't exist"""
    os.makedirs(path, exist_ok=True)

def create_project_structure(project_name):
    """Create the complete project structure"""
    base_path = Path(project_name)
    
    # Create the project root directory
    create_directory(base_path)
    
    # Create directories and files based on the structure
    for dir_name, contents in DIRECTORY_STRUCTURE.items():
        dir_path = base_path / dir_name
        create_directory(dir_path)
        
        if isinstance(contents, dict):
            for filename, content in contents.items():
                file_path = dir_path / filename
                if isinstance(content, dict):
                    create_directory(file_path)
                    for subfile, subcontent in content.items():
                        create_file(file_path / subfile, subcontent)
                else:
                    create_file(file_path, content)
    
    # Create root level files
    create_file(base_path / "requirements.txt", "# Add your requirements here\n")
    create_file(base_path / "version.txt", "0.1.0\n")
    
    # Create template files
    template_dir = Path(__file__).parent / "templates"
    create_file(base_path / "Dockerfile", (template_dir / "dockerfile_template").read_text())
    create_file(base_path / ".gitignore", (template_dir / "gitignore_template").read_text())
    create_file(base_path / "README.md", 
               (template_dir / "readme_template.md").read_text().format(project_name=project_name))
