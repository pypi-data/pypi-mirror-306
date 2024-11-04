# data_generation_tool

## Description
This tool aims to play a crucial role in facilitating the explainability of AI models. By enabling
to create synthetic datasets from specific contexts and defined attribute types ,
the tool offers a unique opportunity to explore and understand the behaviour
of AI models.

## Setup
```bash
git clone https://github.com/friare/data_generation_tool
cd data_generation_tool
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\Scripts\activate.bat  # Windows
pip install -r requirements.txt
```

### Building the documentation (Using [sphinx](https://www.sphinx-doc.org/en/master/))
```bash
pip install sphinx sphinx-rtd-theme
cd docs
sphinx-apidoc -f -o . ../data_generation_tool
make html
```