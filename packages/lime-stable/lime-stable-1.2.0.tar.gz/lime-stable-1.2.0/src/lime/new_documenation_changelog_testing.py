from pathlib import Path

def create_rst_from_changelog(input_file, output_file):

    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Start the rst file content
    rst_content = ["Changelog\n", "=========\n\n"]

    # Detect version lines (assuming LiMe start)
    for line in lines:
        if line.strip().startswith("LiMe") and "LiMe" in line:
            version_type, version_number, version_date = line.split('-')
            version_info = f'{version_number.strip()} {version_type.strip()} ({version_date.strip()})\n'
            rst_content.append(version_info)
            rst_content.append(f"{'-' * len(version_info)}\n\n")

        # Process bullet points with indentation
        elif line.strip().startswith("-"):
            rst_content.append(f"* {line.strip()[1:].strip()}\n")

        # Detect the date format and append it after the version
        elif line.strip():
            rst_content.append(f"**{line.strip()}**\n")

        # Empty lines or additional text
        else:
            rst_content.append(f"{line.strip()}\n")

    # Write the content to the output rst file
    with open(output_file, 'w') as file:
        file.writelines(rst_content)

# Usage
input_txt_file = 'changelog.txt'  # Path to the uploaded changelog file
output_rst_file = '/home/vital/PycharmProjects/lime/docs/source/introduction/changelog.rst'  # Output rst file

create_rst_from_changelog(input_txt_file, output_rst_file)