#Code written by Abdallah Hwishel for the PMG technical assessment.

import csv
import sys
from re import match

#Gather all input filenames from the command line
csv_filenames = sys.argv[1:]


def check_for_incompatible_csvs(filenames):
    """
    This function checks if there are incompatible csv files with mismatching columns. 
    If it finds any, it throws an error with the filename that has the issue.
        Arguments: a list of filenames for csv files
        Returns: None
    """
    csvs_with_matching_columns = []
    column_names = set()
    enumerated_filenames = enumerate(filenames)
    for i,csv_file in enumerated_filenames:
        skip = False
        with open(csv_file) as csvfile:
            columns = csvfile.readline().split(",")
            for column in columns:
                if i == 0:
                    column_names.add(column)
                else:
                    if column not in column_names:
                        raise ValueError(f"Input csv files don't have matching columns: {csv_file}")

def combine_csv(filenames):
    """
    This function is responsible for aggregating the data of all input csv files into one list.
    Returns a tuple containing the title_header as a list for the output and the aggregate csv rows as a list
        Arguments: a list of filenames for csv files
        Returns: Tuple[str, list[str]]
    """
    combined_csv_data = [] #This list is where the csv rows will be aggregated
    title_header = "" #This list will contain the names of all columns + the new filename column
    for csv_file in filenames: #given that the number of csv files is fixed, this will be some constant factor for runtime
        #Extract the filename without path to append to the rows
        filename_without_path = match(r".*(\\|\/)(\w*.csv)", csv_file).groups()[1]
        with open(csv_file) as csvfile:
            csv_as_list = csvfile.readlines()
            if title_header == "": #define a title_header only once
                if len(csv_as_list) > 0:
                    title_header = f"{csv_as_list[0].strip()},filename"
                else:
                    return None, None
            data_rows = csv_as_list[1:] #Get all rows except for the row with table headers
            for i in range(len(data_rows)):
                data_rows[i] = f"{data_rows[i].strip()},{filename_without_path}"
            combined_csv_data.extend(data_rows) #add all rows of each csv file with exception to titles
    return title_header, combined_csv_data



def output_csv(filenames, save_to_csv_in_test=False, output_csv_name=None):
    """
    This function is responsible for formatting and outputing the aggregate csv data to stdout
        Arguments: a list of filenames for csv files
        Returns: None
    Format and output the aggregate csv data in a csv-compatible format
    """
    title_header, combined_csv_data = combine_csv(filenames) #Get the title header and combined csv data for formatting
    if save_to_csv_in_test:
        if title_header != None and combined_csv_data != None:
            with open(output_csv_name, 'w') as csvfile:
                csvfile.write(f"{title_header}\n")
                for line in combined_csv_data:
                    csvfile.write(f"{line}\n")
        else:
            with open(output_csv_name, 'w') as csvfile:
                print("Created an empty csv file")
    else:
        print(title_header) #This ensures that the header is printed only once
        for row in combined_csv_data:
            print(row) #comma separate the column values to make it csv-compatible

if __name__ == "__main__":
    check_for_incompatible_csvs(csv_filenames)
    output_csv(csv_filenames)

                

