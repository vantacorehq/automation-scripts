Automation Scripts
A growing collection of small Python scripts built to eliminate repetitive manual work.
What's inside
- File sorting and organization
- Automated report generation
- API data pulls and processing
Tech stack
Python · Requests · OS/file handling libraries
Status
New scripts added regularly. Custom automation built for client workflows.
Get in touch
Open for freelance work — DM on Twitter for custom automation projects.
## Usage

```bash
pip install -r requirements.txt

# Sort files in a folder by type
python file_sorter.py "C:/Users/Me/Downloads" --dry-run
python file_sorter.py "C:/Users/Me/Downloads"

# Fetch live exchange rates and save to JSON
python fetch_api_data.py
python fetch_api_data.py --base EUR --output eur_rates.json
```

## Sample output

See [`sample_output.json`](sample_output.json) for an example of the fetched data.
