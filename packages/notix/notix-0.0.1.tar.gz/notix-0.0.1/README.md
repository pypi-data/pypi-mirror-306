# Notix

Notix is a simple library for showing notifications on Windows using native message boxes. It provides an easy way to display info, warning, and error messages, as well as to ask yes/no questions.

## Features

- Display informational messages
- Display warning messages
- Display error messages
- Ask yes/no questions

## Installation

You can install Notix locally using pip:

pip install -e .

This will install Notix in editable mode, which means that changes made to the source code will be reflected immediately without needing to reinstall the package.

## Usage

Here is an example of how to use Notix:

from notix import mbox

message_box = mbox()

# Show an informational message
message_box.show_info("Hello", "This is an informational message!")

# Show a yes/no question
if message_box.show_question("Confirmation", "Do you want to proceed?"):
    message_box.show_warning("Warning", "You chose to proceed.")
else:
    message_box.show_error("Error", "Operation canceled.")


## User Guide

1. Import the Library: Start by importing the mbox class from the notix module.
2. Create an Instance: Create an instance of the mbox class. This will be used to show messages.
3. Show Messages:
- Use show_info(title, message) to display an informational message.
- Use show_warning(title, message) to show a warning message.
- Use show_error(title, message) to display an error message.
- Use show_question(title, question) to ask a yes/no question. This method returns True for "Yes" and False for "No".

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

Sergey Uvarov
Your Email: pop1avplov@example.com
GitHub: [Pop1avok](https://github.com/Pop1avok)
