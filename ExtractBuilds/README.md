# Extract Firefox Build Reports

Following describes each of the files in this folder:
## Unzip build-reports (firefox_build_steps_load_db.py)
The build reports we collected from Firefox came as the zipped bundles. This made us write a script to unzip each of the build reports before we extract data from them. 
The file firefox_build_steps_load_db.py unzips the files.

## Load the basic information about a build from the build reports (firefox_build_steps_load_db.py)
The top portion of the log file contains the basic build summary including information about the builder, slave process, start time, pass or fail verdict, build id, and source code revision number (commit hash). 
We load these basic information using the script "firefox_build_steps_load_db.py".

## Load the tests from the build reports into database (firefox_build_tests_load_db.pl and test_steps.py)
The test information is contained at the end of the build log file and includes the test status, test path, and a short description of the test. 
We load the tests using both the perl script "firefox_build_tests_load_db.pl" and the python script "test_steps.py".

