#section-start setup
#section-start import stuff
import argparse
import filecmp
import os
import shutil
import subprocess
import importlib.util
import sys
import prompt_toolkit.completion
import prompt_toolkit
#section-end
#section-start define constants
REFERENCE_FILE_SUFFIX = ".reference.txt"
CURRENT_FILE_SUFFIX = ".current.txt"
TEST_FILE_DIRECTORY = "./snapshot_tests/"
TEST_MODULE_FILEPATH = TEST_FILE_DIRECTORY + "snapshot_tests.py"
FAIL_STRING = "FAIL[X]: "
PASS_STRING = "PASS[ ]: "
#section-end
#section-start define enums
NO_REFERENCE="NO_REFERENCE"
#section-end
#section-end
#section-start make supporting functions
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
        print(FAIL_STRING+test_name+"    NO_REFERENCE")
        return(NO_REFERENCE)
    #section-end
    #section-start compare the reference to the current!
    #section-start if they match pass the test!
    if filecmp.cmp(reference_filename, current_filename):
        print(PASS_STRING+test_name)
        return(True)
    #section-end
    #section-start if they don't fail the test!
    else:
        print(FAIL_STRING+test_name)
        return(False)
    #section-end
    #section-end
#section-end
def display_diff(filename1, filename2): #section-start
    subprocess.run(["git", "diff", "--no-index", filename1, filename2])
#section-end
def display_file(filename1): #section-start
    print("Contents of file: "+filename1+"\n\n```", end="")
    subprocess.run(["cat", filename1])
    print("```\n\nEnd of file "+filename1)
#section-end
def load_tests(): #section-start
    #section-start load the tests
    try:
        spec = importlib.util.spec_from_file_location("snapshot_tests", TEST_MODULE_FILEPATH)
        module = importlib.util.module_from_spec(spec)
        sys.modules["snapshot_tests"] = module
        spec.loader.exec_module(module)
        tests = module.tests
        return(tests)
    except Exception as e:
        raise RuntimeError("Failure while trying to load test module: " + TEST_MODULE_FILEPATH) from e
    #section-end
#section-end
def make_selection(prompt, items): #section-start
    user_input = prompt_toolkit.prompt(
        prompt,
        completer=prompt_toolkit.completion.WordCompleter(items)
    )
    return(user_input)
#section-end
#section-end
#section-start make commands!
def snapshot(): #section-start
    #section-start ensure the test directory exists.
    if not os.path.isdir(TEST_FILE_DIRECTORY):
        print("No tests directory found (are you calling this in the correct location?).")
        if make_selection("Create template test directory?\n(y/n): ", ["y","n"])=="y":
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
                gitignore.write("def helloworld():\n\treturn(\"helloworld\")\ntests={\"helloworld\":helloworld}")
            #section-end
        else:
            print("Test dir not avaliable. Exiting.")
            return()
    #section-end
    #section-start load tests
    tests=load_tests()
    #section-end
    #section-start run the tests
    print("\ntests:")
    all_tests_good = True
    no_reference_flag = False
    for test_name in tests:
        test_success = snapshot_test(
            test_name=test_name,
            computed_value=tests[test_name](),
        )
        if not test_success:
            all_tests_good = False
        if test_success==NO_REFERENCE:
            all_tests_good = False
            no_reference_flag = True
    print()
    if no_reference_flag:
        print("At least one test reference output was not found. you need to make a reference test to compare against! to do this; run `si` and then enter a test name to examine the current output. If you find the current output satisfactory then use `sr` then enter the test name to set the current output as the reference output for this test!\n")
    if not all_tests_good:
        sys.exit(1)
    #section-end
#section-end
def snapshot_rereference(): #section-start
    #section-start have user select the test to rereference
    tests=load_tests()
    selected_test = make_selection("Enter the test which you would like to overwrite the reference for: ", tests.keys())
    #section-end
    #section-start deal with rereference
    print("rereferencing: "+ selected_test)
    #section-start construct filenames!
    reference_filename = TEST_FILE_DIRECTORY + selected_test + REFERENCE_FILE_SUFFIX
    current_filename = TEST_FILE_DIRECTORY + selected_test + CURRENT_FILE_SUFFIX
    #section-end
    #section-start copy the file over!
    shutil.copy(current_filename, reference_filename)
    #section-end
    print("Done rereferencing\n")
    #section-end
#section-end
def snapshot_inspect(): #section-start
    #section-start have user select the test to inspect
    tests=load_tests()
    selected_test = make_selection("Enter the test to inspect: ", tests.keys())
    #section-end
    print("inspecting: "+ selected_test)
    #section-start construct filenames!
    reference_filename = TEST_FILE_DIRECTORY + selected_test + REFERENCE_FILE_SUFFIX
    current_filename = TEST_FILE_DIRECTORY + selected_test + CURRENT_FILE_SUFFIX
    #section-end
    #section-start deal with no reference existing
    if not os.path.isfile(reference_filename):
        print("no reference exists so only the current output will be displayed")
        display_file(current_filename)
    #section-end
    #section-start deal with passed test
    elif filecmp.cmp(reference_filename, current_filename):
        print("the test is passed so only the reference will be displayed")
        display_file(reference_filename)
    #section-end
    #section-start deal with failed test
    else:
        print("the test failed so both the reference output and the current output will be opened")
        display_diff(reference_filename, current_filename)
    #section-end
    print("inspection complete!")
#section-end
#section-end
