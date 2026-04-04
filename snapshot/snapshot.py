#section-start import stuff
import argparse
import filecmp
import os
import shutil
import subprocess
import importlib.util
import sys
#section-end
#section-start define constants
REFERENCE_FILE_SUFFIX = ".reference.txt"
CURRENT_FILE_SUFFIX = ".current.txt"
TEST_FILE_DIRECTORY = "./snapshot_tests/"
TEST_MODULE_FILEPATH = TEST_FILE_DIRECTORY + "/snapshot_tests.py"
#section-end
def snapshot_test(*, computed_value, test_name): #section-start
    """ #section-start
    tests the computed outputs against existing snapshots.
    """
    #section-end
    #section-start convert non string outputs to strings
    if not isinstance(computed_value, str):
        computed_value = repr(computed_value)
    #section-end
    #section-start construct filenames!
    reference_filename = TEST_FILE_DIRECTORY + test_name + REFERENCE_FILE_SUFFIX
    current_filename = TEST_FILE_DIRECTORY + test_name + CURRENT_FILE_SUFFIX
    #section-end
    #section-start write computed value to current
    with open(current_filename, "w") as file:
        file.write(computed_value)
    #section-end
    #section-start deal with no previous snapshots existing
    if not os.path.isfile(reference_filename):
        print("  FAIL[x]: "+test_name+"\nprevious test record not found. you need to make a reference test to compare against! to do this; run `snapshot -i "+test_name+"` to examine the current output. If you find the results satisfactory then use `snapshot -r "+test_name+"` to set the current output as the reference output for this test.")
        return(False)
    #section-end
    #section-start compare the reference to the current!
    #section-start if they match pass the test!
    if filecmp.cmp(reference_filename, current_filename):
        print("  PASS[ ]: "+test_name)
        return(True)
    #section-end
    #section-start if they don't fail the test!
    else:
        print("  FAIL[x]: "+test_name)
        return(False)
    #section-end
    #section-end
#section-end
def display_diff(filename1, filename2): #section-start
    subprocess.run(["nvim", "-d", filename1, filename2])
#section-end
def display_file(filename1): #section-start
    subprocess.run(["nvim", filename1])
#section-end
def snapshot():
    #section-start ensure the test directory exists.
    if not os.path.isdir(TEST_FILE_DIRECTORY):
        print("No tests directory found (are you calling this in the correct location?).")
        if input("Create template test directory (yes/no)")=="yes":
            #section-start create the directory
            print("no test directory not found. performing fist time setup!")
            print("creating test directory")
            os.mkdir(TEST_FILE_DIRECTORY)
            #section-end
            #section-start make the gitignore file
            print("creating test directory gitignore file")
            with open(TEST_FILE_DIRECTORY+".gitignore", "w") as gitignore:
                gitignore.write("*"+REFERENCE_FILE_SUFFIX+"\n__pycache")
            #section-end
            #section-start make the tests file
            print("creating test directory tests file")
            with open(TEST_FILE_DIRECTORY+"snapshot_tests.py", "w") as gitignore:
                gitignore.write("*"+REFERENCE_FILE_SUFFIX+"\n__pycache")
            #section-end
        else:
            print("Test dir not avaliable. Exiting.")
            return()
    #section-end
    #section-start load the tests
    spec = importlib.util.spec_from_file_location("snapshot_tests", TEST_MODULE_FILEPATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["snapshot_tests"] = module
    spec.loader.exec_module(module)
    tests = module.tests
    #section-end
    #section-start always run the tests
    print("\ntests:")
    for test_name in tests:
        snapshot_test(
            test_name=test_name,
            computed_value=tests[test_name](),
        )
    print()
    #section-end
def main(): #section-start
    #section-start read arguments
    parser = argparse.ArgumentParser(
        prog="snapshot",
        description="minimalist snapshot test program")
    parser.add_argument("-i", "--inspect", type=str, help="inspect test results to see the differences between the reference output and the current output. this takes the test name")
    parser.add_argument("-r", "--rereference", type=str, help="overwrite the reference output with the current output. this takes the test name. use this after performing an examination and finding that the current output is correct.")
    args = parser.parse_args()
    #section-end
    #section-start ensure the test directory exists.
    if not os.path.isdir(TEST_FILE_DIRECTORY):
        #section-start create the directory
        print("no test directory not found. performing fist time setup!")
        print("creating test directory")
        os.mkdir(TEST_FILE_DIRECTORY)
        #section-end
        #section-start make the gitignore file
        print("creating test directory gitignore file")
        with open(TEST_FILE_DIRECTORY+".gitignore", "w") as gitignore:
            gitignore.write("*"+REFERENCE_FILE_SUFFIX+"\n__pycache")
        #section-end
    #section-end
    #section-start load the tests
    spec = importlib.util.spec_from_file_location("snapshot_tests", TEST_MODULE_FILEPATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["snapshot_tests"] = module
    spec.loader.exec_module(module)
    tests = module.tests
    #section-end
    #section-start always run the tests
    print("\ntests:")
    for test_name in tests:
        snapshot_test(
            test_name=test_name,
            computed_value=tests[test_name](),
        )
    print()
    #section-end
    #section-start deal with inspection
    if args.inspect is not None:
        print("inspecting: "+ args.inspect)
        #section-start construct filenames!
        reference_filename = TEST_FILE_DIRECTORY + args.inspect + REFERENCE_FILE_SUFFIX
        current_filename = TEST_FILE_DIRECTORY + args.inspect + CURRENT_FILE_SUFFIX
        #section-end
        #section-start deal with no reference existing
        if not os.path.isfile(reference_filename):
            print("  no reference exists so only the current output will be displayed")
            display_file(current_filename)
        #section-end
        #section-start deal with passed test
        elif filecmp.cmp(reference_filename, current_filename):
            print("  the test is passed so only the reference will be displayed")
            display_file(reference_filename)
        #section-end
        #section-start deal with failed test
        else:
            print("  the test failed so both the reference output and the current output will be opened")
            display_diff(reference_filename, current_filename)
        #section-end
        print("  done\n")
    #section-end
    #section-start deal with rereference
    elif args.rereference is not None:
        print("rereferencing: "+ args.rereference)
        #section-start construct filenames!
        reference_filename = TEST_FILE_DIRECTORY + args.rereference + REFERENCE_FILE_SUFFIX
        current_filename = TEST_FILE_DIRECTORY + args.rereference + CURRENT_FILE_SUFFIX
        #section-end
        #section-start copy the file over!
        shutil.copy(current_filename, reference_filename)
        #section-end
        print("  done\n")
    #section-end
#section-end
if __name__=="__main__": #section-start
    main()
#section-end
