# Yash Pathak
# pathaky@uci.edu
# 51317074

from pathlib import Path
import ui_helper
import Profile as Profile


MENU = 'Welcome! Do you want to-\n\n1. Create a Profile.\n2. Open an existing Profile.\n3. Edit an existing Profile.\n4. Print an existing Profile.\n5. Quit the program.\n'

def run(special_path: Path = '', profile_object: Profile = None):
    # Print menu and ask for input
    print(MENU)
    user_input = input()

    # Create a profile
    if user_input == '1':
        # For creating file or loading an existing file
        print('Please enter command in format below to create a profile :\n C [path_name to your profile] -n [File Name].')
        user_input = input()

        # create file or load an existing file
        input_lst = ""
        command, path_variable, options_lst, input_lst, edit_lst = ui_helper.ui_process(user_input)
        while (input_lst == ""):
            print('Please enter command in  CORRECT format below to create a profile :\n C [path_name to your profile] -n [File Name].')
            user_input = input()
            command, path_variable, options_lst, input_lst, edit_lst = ui_helper.ui_process(user_input)
        error_code, output_message, profile_object, special_path = ui_helper.create(path_variable, input_lst)
        print(output_message)

    # Open an existing profile
    elif user_input == '2':
        # For opening a file
        print('Please enter command in format below to open a profile: O [existing path]')
        user_input = input()
        path_variable = ""
        command, path_variable, options_lst, input_lst, edit_lst = ui_helper.ui_process(user_input)
        
        while (path_variable == ""):
            print('Please enter command in CORRECT format below to open a profile: O [existing path]')
            user_input = input()
            command, path_variable, options_lst, input_lst, edit_lst = ui_helper.ui_process(user_input)
        error_code, output_message, profile_object, special_path = ui_helper.open(path_variable)
        print(output_message)

    # Edit a profile
    elif user_input == '3':
        if profile_object == None:
            print("Nothing to edit. Please Create or Open profile before editing")
        else:
            print('Please enter command in format below to edit a profile: E [[-]OPTION] [INPUT]')
            print('where OPTION can be -usr [USERNAME], -pwd [PASSWORD], -bio [BIO], -addpost [NEW POST], -delpost [ID]')
            user_input = input()
            ui_helper.editProfile(user_input, profile_object, special_path)

    # Print a profile
    elif user_input == '4':
        if profile_object == None:
            print("Nothing to print. Please Create or Open profile before editing")
        else:
            print('Please enter command in format below to print a profile: P [[-]OPTION] [INPUT]')
            print('where OPTION can be -usr, -pwd, -bio, -posts, -post [ID], -all')
            user_input = input()
            ui_helper.printProfile(user_input, profile_object, special_path)

    # Recursively run if user did not input 5 to quit
    if user_input != "5":
        run(special_path, profile_object)
