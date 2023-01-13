#Code written by Abdallah Hwishel for the PMG technical assessment.

"""
Write all Auxiliary functions that supplements the test methods in csv_combiner_tests here.
Here, I will include the code that is responsible for generating various sizes of csv files
"""
from os import system, getcwd, listdir, remove
from os.path import join, getsize, isfile
from random import randint, choice #I will use randint to generate random data for each row and choice to generate random strings
from string import ascii_lowercase
import csv

def convert_bytes_to_megabytes(size_in_bytes):
    """
    This is a simple function that converts the number of bytes to MB for ease of programming
        Arguments: an int that is the size in bytes
        Returns: the size converted to megabytes
    """
    size = size_in_bytes / (1024**2)
    return size


def generate_random_string():
    """
    This function generates a random string
        Arguments: None
        Returns: None
    NOTE: This will be used to generate random filenames for the randomly created csv
    """
    return ''.join(choice(ascii_lowercase) for i in range(10))

def generate_fieldnames(n):
    """
    This function generates n fieldnames as such: field1, field2, field3, ...fieldn
        Arguments: The number of fields desired as an integer
        Returns: list[str]
    """
    return [f"field{i}" for i in range(n)]

def generate_csvs_of_approx_size(fieldnames, size_in_mb, path=None, repeat_rows=100):
    """
    This function generates a set of randomized csv files that is approximately the desired size passed in
        Arguments: a list containing the desired header names
                   an integer size representing the total size in MB desired
                   an optional str -> path to new file that will be generated
                   an optional int -> how much you want a randomized row to be repeated (larger val = faster runtime)
        Returns: None

    NOTE: This is primarily used to stress test the csv_combiner by giving it very large files to work with
    """
    number_of_files = randint(2, 10)
    size_in_mb_per_file = size_in_mb / number_of_files
    for i in range(number_of_files):
        rows = [fieldnames]
        pathname = None
        if path != None:
            pathname = join(path, f"{generate_random_string()}.csv")
        else:
            pathname = f"{generate_random_string()}.csv"
        currsize = 0
        while currsize < size_in_mb_per_file:
            with open(pathname, 'a', newline='') as csvfile:
                row_val = generate_random_string()
                row = [row_val for i in range(len(fieldnames))]
                #To reduce runtime, I'll add the same row 100 times by default before a new row is generated
                #NOTE: If repeat_rows is a much lower number (at worst 1) then generating 100% random csv will take significantly longer
                for i in range(repeat_rows):
                    rows.append(row)
                writer = csv.writer(csvfile)
                writer.writerows(rows)
                rows = []
            currsize = convert_bytes_to_megabytes(getsize(pathname))
            # print(f"size: {currsize}/{size_in_mb_per_file}")

def add_filename_column_to_csvs(dirname):
    """
    This function takes all the csv files in the given directory and adds the filename column along with their
    file's name as values.
        Arguments: The directory containing the test csv files as a string path
        Returns: Tuple[str, list[str]]
    """
    title = None
    filenames = listdir(dirname)
    for filename in filenames:
        pathname = join(dirname, filename)
        lines = []
        if(isfile(pathname)):
            with open(pathname, 'r') as file:
                enumerated_filelines = enumerate(file.readlines())
                for i,line in enumerated_filelines:
                    if i == 0:
                        title = f"{line.strip()},filename\n"
                        lines.append(title)
                    else:
                        lines.append(f"{line.strip()},{filename}\n")
            updated_pathname = join(dirname, 'with_new_column_and_data', filename)
            with open(updated_pathname, 'w') as file:
                file.writelines(lines)
    return title,filenames

def concat_csvs(dirname, filenames, title):
    """
    This function takes all the csv files in the given directory and adds the filename column along with their
    file's name as values.
        Arguments: The directory containing the test csv files as a string path
                   a list of file names
                   a string title
        Returns: None
    NOTE: This is meant to be called with the return values of add_filename_column_to_csvs as its arguments
    """
    lines = [title]
    for filename in filenames:
        pathname = join(dirname,'with_new_column_and_data',filename)
        if(isfile(pathname)):
            with open(pathname, 'r') as file:
                filelines = file.readlines()[1:] #Exclude titles
                lines.extend(filelines)
            #Remove file when done
            remove(pathname)
    updated_pathname = join(dirname, 'with_new_column_and_data', 'aggregate_comparison.csv')
    with open(updated_pathname, 'w') as file:
        file.writelines(lines)


def create_output_comparison_csv(dirname):
    """
    This function generates an aggregate csv to compare with the actual output of csv_combiner.
    It does so by simply calling add_filename_column_to_csvs and concat_csvs
        Arguments: The directory containing the test csv files as a string path
        Returns: None
    """
    print(f"Adding columns and data to csv files in {dirname}")
    title, filenames = add_filename_column_to_csvs(dirname)
    print(f"Creating aggregated comparison csv file")
    concat_csvs(dirname, filenames, title)

def no_diff(actual, expected):
    """
    This function compares the lines of two csv files. It returns true if they're the same, false otherwise.
        Arguments: csv file path for csv_combiner output as a string
                   csv file path for aggregate csv to compare it with
        Returns: bool
    """
    actual_text = []
    expected_text = []

    with open(actual, 'r') as file:
        actual_text = file.readlines()
    
    with open(expected, 'r') as file:
        expected_text = file.readlines()

    return actual_text == expected_text

def main(num_fields=3):
    """
    This is the main function that does everything from generating all the test cases to creating aggregate csvs
    for those various sizes. The size estimate for the test cases are as follows:
        Small = ~ 512 MB
        Medium = ~ 1 GB
        Large = ~ 2 GB
        Arguments: the number of columns desired for the test cases
        Returns: None
    """
    #SMALL CSV GENERATION
    DESIRED_SIZE_IN_MB = 512
    ALT_PATH = join(getcwd(),'randomly_generated_csvs','small_tests')
    print("GENERATING RANDOM CSVS OF TOTAL SIZE ~512MB")
    generate_csvs_of_approx_size(generate_fieldnames(num_fields), DESIRED_SIZE_IN_MB, path=ALT_PATH)

    #MEDIUM CSV GENERATION
    DESIRED_SIZE_IN_MB = 1024
    ALT_PATH = join(getcwd(),'randomly_generated_csvs','medium_tests')
    print("GENERATING RANDOM CSVS OF TOTAL SIZE ~1GB")
    generate_csvs_of_approx_size(generate_fieldnames(num_fields), DESIRED_SIZE_IN_MB, path=ALT_PATH)

    #Large CSV GENERATION
    DESIRED_SIZE_IN_MB = 2048
    ALT_PATH = join(getcwd(),'randomly_generated_csvs','large_tests')
    print("GENERATING RANDOM CSVS OF TOTAL SIZE ~2GB")
    generate_csvs_of_approx_size(generate_fieldnames(num_fields), DESIRED_SIZE_IN_MB, path=ALT_PATH)
    
    #Generate small test case comparison file
    PATH = join(getcwd(),'randomly_generated_csvs','small_tests')
    print("GENERATING SMALL COMPARISON CSV FILE")
    create_output_comparison_csv(PATH)

    #Generate medium test case comparison file
    PATH = join(getcwd(),'randomly_generated_csvs','medium_tests')
    print("GENERATING MEDIUM COMPARISON CSV FILE")
    create_output_comparison_csv(PATH)

    #Generate large test case comparison file
    PATH = join(getcwd(),'randomly_generated_csvs','large_tests')
    print("GENERATING LARGE COMPARISON CSV FILE")
    create_output_comparison_csv(PATH)

if __name__ == "__main__":
    main()