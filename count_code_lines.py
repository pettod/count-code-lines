import os


PROJECT_ROOT = os.getcwd()


def filesInDirectory(directory_path=PROJECT_ROOT, check_sub_directories=True,
                     file_format=".py"):
    # Create a list of files and subdirectories in the directory
    # Names in the given directory
    file_names = os.listdir(directory_path)
    only_files = []

    # Iterate over all the entries
    for entry in file_names:

        # Don't add project root to file names
        if directory_path == PROJECT_ROOT:
            directory_path = ''
        full_path = os.path.join(directory_path, entry)

        # If entry is a directory then get the file list inside the it
        if os.path.isdir(full_path) and check_sub_directories:
            only_files += filesInDirectory(full_path)
        elif full_path.endswith(file_format):
            only_files.append(full_path)

    return only_files


def printCodeLines(file_names):
    # Count code lines in all files
    number_of_lines = []
    for f in file_names:
        number_of_lines.append(len(open(f).readlines()))

    # Print results
    print(
        "\n" +
        "Lines | File name\n" +
        "------|----------")
    for i in range(len(file_names)):
        print(
            number_of_lines[i], " "*(4 - len(str(number_of_lines[i]))), "|",
            file_names[i])
    print(
        "-----------------\n" + str(sum(number_of_lines)) + " altogether\n")


def main():
    py_files = filesInDirectory("src")
    py_files += filesInDirectory(check_sub_directories=False)
    printCodeLines(py_files)


main()
