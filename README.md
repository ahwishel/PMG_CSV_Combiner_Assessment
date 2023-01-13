# PMG_CSV_Combiner_Assessment
This is my submission for the PMG technical assessment.

<h1>NOTE TO CODE TESTER</h1>
To run the unit tests on the code, please
<pre>cd tests</pre> then
<pre>python csv_combiner_tests.py</pre>
If you don't cd into the tests directory first before running csv_combiner_tests.py it will throw a ModuleNotFound error. <br/><br/>
The csv_combiner_tests.py does two things:
<ul>
  <li>Generate 3.5GB worth of randomized CSV files to stress test the csv_combiner (This takes at most 12 minutes)</li>
  <li>Run unit tests defined within the file</li>
</ul>
<br/>
The generation of randomized CSV files happens when the FLAG variable in csv_combiner_tests.py is True. Please keep it True when you run it for the first time.
If you need to re-run the unit tests but don't want to generate new csv files, set the FLAG variable to False.

<br/><br/>

To run the csv_combiner, in the repo root directory <pre>python csv_combiner.py csv_file1 csv_file2 csv_file3 ...</pre>
