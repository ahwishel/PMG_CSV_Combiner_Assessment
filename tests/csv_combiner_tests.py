#Code written by Abdallah Hwishel for the PMG technical assessment.

"""
Some general tests must be implemented that answers the following questions:
1) What happens when the files have no content within them?
2) What happens when the files only contain the header rows without data?
3) What happens when one file contains headers only while the others have headers and data?
4) What happens when the files are small? Takes roughly < 1 minute to generate and create an aggregate csv file
5) What happens when the files are medium? Takes roughly < 2 minutes to generate and create an aggregate csv file
6) What happens when the files are large? Takes roughly 1.5 minutes to generate and create an aggregate csv file

I will use both the randomly generated csv files as well as the fixture files within those tests
"""

import unittest
from os import system, listdir, remove
from os.path import exists, isfile, join
from tests_auxiliary_funcs import no_diff, main
import sys
sys.path.insert(1, '../')
from csv_combiner import output_csv

class TestCSVCombiner(unittest.TestCase):

   def test1(self):
      output_csv(['./fixtures/empty1.csv', './fixtures/empty2.csv'], True, "./test_aggregate_output/test1_aggregate.csv")
      self.assertTrue(no_diff('./test_aggregate_output/test1_aggregate.csv', './fixtures/empty_aggregate.csv'))
      print(".Test 1 Passed!")

   def test2(self):
      output_csv(['./fixtures/headers_only1.csv', './fixtures/headers_only2.csv'], True, "./test_aggregate_output/test2_aggregate.csv")
      self.assertTrue(no_diff('./test_aggregate_output/test2_aggregate.csv', './fixtures/headers_only_aggregate.csv'))
      print("Test 2 Passed!")
   
   def test3(self):
      output_csv(['./fixtures/headers_only1.csv', './fixtures/headers_with_small_data.csv'], True, "./test_aggregate_output/test3_aggregate.csv")
      self.assertTrue(no_diff('./test_aggregate_output/test3_aggregate.csv', './fixtures/headers_with_no_headers_aggregate.csv'))
      print("Test 3 Passed!")

   def test4(self):
      #Get list of files in a given directory
      small_csvs = listdir("./randomly_generated_csvs/small_tests")
      input_files = []
      for filename in small_csvs:
         if isfile(f"./randomly_generated_csvs/small_tests/{filename}"):
            input_files.append(f"./randomly_generated_csvs/small_tests/{filename}")
      output_csv(input_files, True, "./test_aggregate_output/test4_aggregate.csv")
      self.assertTrue(no_diff('./test_aggregate_output/test4_aggregate.csv', './randomly_generated_csvs/small_tests/with_new_column_and_data/aggregate_comparison.csv'))
      print("Test 4 Passed!")

   def test5(self):
      #Get list of files in a given directory
      medium_csvs = listdir("./randomly_generated_csvs/medium_tests")
      input_files = []
      for filename in medium_csvs:
         if isfile(f"./randomly_generated_csvs/medium_tests/{filename}"):
            input_files.append(f"./randomly_generated_csvs/medium_tests/{filename}")
      output_csv(input_files, True, "./test_aggregate_output/test5_aggregate.csv")
      self.assertTrue(no_diff('./test_aggregate_output/test5_aggregate.csv', './randomly_generated_csvs/medium_tests/with_new_column_and_data/aggregate_comparison.csv'))
      print("Test 5 Passed!")

   def test6(self):
      #Get list of files in a given directory
      large_csvs = listdir("./randomly_generated_csvs/large_tests")
      input_files = []
      for filename in large_csvs:
         if isfile(f"./randomly_generated_csvs/large_tests/{filename}"):
            input_files.append(f"./randomly_generated_csvs/large_tests/{filename}")
      output_csv(input_files, True, "./test_aggregate_output/test6_aggregate.csv")
      self.assertTrue(no_diff('./test_aggregate_output/test6_aggregate.csv', './randomly_generated_csvs/large_tests/with_new_column_and_data/aggregate_comparison.csv'))
      print("Test 6 Passed!")

if __name__ == '__main__':
   # Set this FLAG to true if you want to create new datasets. If you download it, it will be set to True by default
   # because i'll delete the csv files before uploading to github to reduce the upload size.
   FLAG = True
   if FLAG:
      print("REGENERATING NEW CSV TEST FILES... This may take several minutes")
      test_dirs = ["./test_aggregate_output",
      "./randomly_generated_csvs/small_tests",
      "./randomly_generated_csvs/small_tests/with_new_column_and_data",
      "./randomly_generated_csvs/medium_tests",
      "./randomly_generated_csvs/medium_tests/with_new_column_and_data",
      "./randomly_generated_csvs/large_tests",
      "./randomly_generated_csvs/large_tests/with_new_column_and_data"
      ]
      for dirpath in test_dirs:
         for filename in listdir(dirpath):
            pathname = join(dirpath,filename)
            if isfile(pathname):
               remove(pathname)
      # main()
      
   # unittest.main()