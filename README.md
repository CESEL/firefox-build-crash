# Replication package for the paper: "The Impact of Failing, Flaky, and High Failure Tests on the number of Crash Reports associated with Firefox Builds"

The following folders contain the code for extracting the build and crash reports:

## Extract Builds
We collect the historical build logs and crash reports of Mozilla Firefox spanning from December 2010 to December 2012. Each build report file contains the log lines for one complete build process that includes basic information, test environment detail, overall build result and the test steps. The "ExtractBuilds" folder contains the scripts that process the build reports and store the data into the database.

## Extract Crash Reports
The crash reports we collect in csv format and the initial raw data for build logs as the text files. Each crash report CSV file contains browser-crash information for a day. The "ExtractCrashReports" folder contains the scripts that process the crash reports and store the data into the database.


The following folders contain the code for extracting the HighFailure and the Flaky tests:

## Extract HighFailure Tests
In software system problems cluster around defective code and tests that have failed frequently in the past are likely to fail in the future. To investigate these tests, we classify test that fail in 10% or more of their total runs as historically HighFailureTests. The "ExtractHighFailureTests" folder contains the script that finds out the historically high-failing tests from the database.

## Extract Flaky Tests
We use the existing Firefox classification in the build reports to identify flaky tests. In the test logs inside the build reports, the tests that are marked as "RANDOM", we include them in the "Flaky" category. This means, tests that are labelled with the statuses "PASS(EXPECTED RANDOM)" and "KNOWN-FAIL(EXPECTED RANDOM)" are considered to be the flaky tests. These tests are already extracted into the database when we extract the tests using the scripts "[firefox_build_tests_load_db.pl](https://github.com/tajmilur-rahman/firefox-build-crash/blob/master/ExtractBuilds/firefox_build_tests_load_db.pl)" and "[test_steps.py](https://github.com/tajmilur-rahman/firefox-build-crash/blob/master/ExtractBuilds/test_steps.py)" in "ExtractBuilds" folder.
