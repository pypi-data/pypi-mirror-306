# Switch Class

The `switch` class in Python mimics a `switch-case` statement found in other programming languages. This class allows you to define a set of case-output pairs and an optional `end` output for unmatched cases. Each case can map to either a static value or a callable function.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Initialization](#initialization)
  - [Example](#example)
- [License](#license)

## Installation

No additional packages are required. Simply copy the `Switch` class definition into your Python project.

## Usage

The `Switch` class is initialized with multiple case-output pairs, followed by an optional `end` output that acts as the default response when no cases match.

Cases can be dynaimically changed by setting the values with `__setitem__`, and also accessed with `__getitem__`

### Initialization

To create a `Switch` instance, pass cases and outputs in pairs, optionally followed by an `end` output:

```python
switch_instance = Switch(case1, output1, case2, output2, ..., end=default_output)

```
### Example

Below is a example of a useage of the switch object

```python
# Define functions to use as case outputs
def case_one_action():
    return "Action for Case 1"

def case_two_action():
    return "Action for Case 2"

# Initialize a Switch instance with cases and an end default
switch_example = Switch(
    "case1", case_one_action,    # Function to call for "case1"
    "case2", case_two_action,    # Function to call for "case2"
    end="Default action if no case matched"
)

# Call a case
print(switch_example("case1"))  # Output: "Action for Case 1"
print(switch_example("unknown_case"))  # Output: "Default action if no case matched"

# Access via getitem
print(switch_example["case1"])  # Output: <function case_one_action>
print(switch_example["unknown_case"]())  # Output: "Default action if no case matched"

# Modify a case
switch_example["case1"] = "New Output for Case 1"
print(switch_example("case1"))  # Output: "New Output for Case 1"

# Display all cases and outputs
print(switch_example)
```
## License
Veiw License Agreement Here: [License](LICENSE).
