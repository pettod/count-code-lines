import os


PROJECT_ROOT = os.getcwd()


def countLines(file_names):
    # Count code lines in all files
    number_of_lines = []
    code_lines = 0
    documentation_lines = 0
    comment_lines = 0
    empty_lines = 0
    for file_name in file_names:
        with open(file_name) as file:
            lines = file.readlines()
            inside_documentation = False
            for line in lines:
                line_without_spaces = line.strip()
                if inside_documentation:
                    documentation_lines += 1
                    if line_without_spaces.endswith('"""'):
                        inside_documentation = False
                else:
                    if line_without_spaces == "":
                        empty_lines += 1
                    elif line_without_spaces.startswith('#'):
                        comment_lines += 1
                    elif line_without_spaces.startswith('"""') and \
                            line_without_spaces.endswith('"""') and \
                            len(line_without_spaces) != 3:
                        documentation_lines += 1
                    elif line_without_spaces.startswith('"""'):
                        documentation_lines += 1
                        inside_documentation = True
                    else:
                        code_lines += 1
        number_of_lines.append(len(open(file_name).readlines()))

    return number_of_lines, {
        "code_lines": code_lines,
        "documentation_lines": documentation_lines,
        "comment_lines": comment_lines,
        "empty_lines": empty_lines
    }


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
    lines_per_file, class_separated_lines = countLines(file_names)

    # Print results
    print(
        "\n" +
        "Lines | File name\n" +
        "------|----------")
    for i in range(len(file_names)):
        print(
            lines_per_file[i], " "*(4 - len(str(lines_per_file[i]))), "|",
            file_names[i])
    print(
        "-----------------\n" + str(sum(lines_per_file)) + " altogether")
    print(
        "\nCode lines:         ", class_separated_lines["code_lines"],
        "\nDocumentation lines:", class_separated_lines["documentation_lines"],
        "\nComment lines:      ", class_separated_lines["comment_lines"],
        "\nEmpty lines:        ", class_separated_lines["empty_lines"])


def main():
    py_files = filesInDirectory("src")
    py_files += filesInDirectory(check_sub_directories=False)
    printCodeLines(py_files)


main()
