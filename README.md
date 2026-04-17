# Marine Propulsion Configurator

Streamlit app for configuring electric marine propulsion systems and generating a top-level Bill of Materials.

## Running locally
```
pip install -r requirements.txt
streamlit run app.py
```

## Updating options
Edit `data/configurator.csv` and commit to GitHub. The live app refreshes automatically within 60 seconds.

## Password
Set `APP_PASSWORD` in the Streamlit Cloud secrets dashboard.
Default password: marine2024
