# Import the library
from electron_configuration import ElectronConfiguration

# Create an instance of the ElectronConfiguration class
element = ElectronConfiguration()

# Take atomic number as input from the user
n = int(input("Enter the atomic number of the element: "))

# Get the electron configuration and element name for the given atomic number
config = element.get_configuration(n)
name=element.pretty_print(n)
print(name)
# Print the result
print(config)
