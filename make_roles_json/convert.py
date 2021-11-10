
# Run using: cls && python3 convert.py

### Heading
print("####### Raw Lines to Roles.JSON Converter #######")


### SETUP
# Set name of raw file (adjust as needed)
raw_file_name = "AFRICAN_COUNTRIES_RAW.txt"

# Open existing raw lines file for reading
raw_file = open(raw_file_name, "r")
# - Get lines as list
raw_file_line_content = raw_file.readlines()
# - Get number of lines
raw_file_line_count = len(raw_file_line_content)

# Create new "roles.json" file for writing
# - If "roles.json" does not exist = Will be created
# - If "roles.json" does exist = Will be overwritten 
new_file = open("roles.json","w+")



### WRITE LINES
# Write starting bracket 
new_file.write("{\n")

# For each line in raw file
for line_no in range(0, raw_file_line_count):

    # Get curline
    curline = raw_file_line_content[line_no]

    # # Clean input
    curline = curline.rstrip()

    # # Create new string
    new_curline = " " + " " + "\"" + curline + "\"" 
    new_curline += ": \"99aab5\""

    # # If not on last, add comma
    if(line_no is not (raw_file_line_count-1)):
        new_curline += ","

    # Write it
    new_file.write(new_curline + "\n")


# Write ending bracket 
new_file.write("}\n")

### Finish
print("\nFinished!\n")
