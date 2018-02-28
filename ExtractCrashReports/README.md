# Following describes the files in this folder:

## Unzip the crash reports (firefox_crash_unzip.py)
Like the build reports, we collected the crash reports as the zippzed bundles and before extracting the crash reports we unzip them as the CSV files using the script "firefox_crash_unzip.py".

## Extract crashes and load into the database (firefox_crash_load_db.py) 
We parse and extract all the crash reports into the database. Each crash report contains a crash signature, URL with an unique id, build id, operating system and other information that may be useful to the developers.
The script "firefox_crash_load_db.py" extracts all the crash reports from each of the CSV files.
