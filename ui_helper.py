# Yash Pathak
# pathaky@uci.edu
# 51317074

import os
from pathlib import Path
from Profile import Profile, Post, DsuFileError, DsuProfileError
from enum import Enum
import ds_client
from OpenWeather import OpenWeather
from LastFM import LastFM
from ExtraCreditAPI import ExtraCreditAPI

PORT = 3021

def last_index_maker(usr_input: str) -> str:
    """
    Checks the options provided by user and returns the last index of the actual 'path' part of the user_input.
    
    """
    # Check for index based on the various functions that could follow after the path
    if ' -r' in usr_input:
        last_index = usr_input.index(' -r')
    elif ' -e ' in usr_input:
        last_index = usr_input.index(' -e ')
    elif ' -f' in usr_input:
        last_index = usr_input.index(' -f')
    elif ' -s ' in usr_input:
        last_index = usr_input.index(' -s ')
    elif ' -n ' in usr_input:
        last_index = usr_input.index(' -n ')

    # If there is no function after, then set the last index to the whole length
    else:
        last_index = len(usr_input)
    
    return last_index


def options_input_lst_maker(user_input: str, last_index: str, tracker: int, options_lst: list, input_lst: list) -> list:
    """
    Format input if it is a 'C' or 'L' command. Returns options_lst and input_lst.
    """
    # Takes the part of the user input after the path
    options_and_text_lst = user_input[last_index:].split(' ')

    for item in options_and_text_lst:
        # Separates the [input] from the options and appends to a new input_lst
        if '.' in item or (len(item) >= 2 and '-' not in item):
            input_lst.append(item)
            tracker += 1
    
    # Checks if the part after the path has more than one option and input as well
    if len(options_and_text_lst) > 2:

        # If input list has already been created then puts everything from options_and_text_lst to options_lst except the input
        if tracker == 1:
            for item in options_and_text_lst[1:-1]:
                options_lst.append(item)

        # If input list has not been created then it appends everything in options_and_text_lst to options_lst
        else:
            for item in options_and_text_lst[1:]:
                options_lst.append(item)

    # checks for if there are only 2 options in the options_and_text_lst
    elif len(options_and_text_lst) != 1:
        options_lst.append(options_and_text_lst[1])
    
    return options_lst, input_lst


def ui_process(user_input):
    """
    According to admin input, the function creates and distributes the function accordingly.
    Returns the Command, the path_variable, The options_lst, the input_lst, and the edit_lst.
    """
    # Initialize variables
    command = user_input[:1]
    last_index = last_index_maker(user_input)
    options_lst = ""
    input_lst = ""
    path_variable = ""
    edit_lst = ""

    # Format based on if it is a 'C' or 'L' command
    if command == 'C' or command == 'L':
        options_lst, input_lst = options_input_lst_maker(user_input, last_index, tracker = 0, options_lst = [], input_lst = [])

    # Format based on if it is 'O' or 'D' or 'R'
    if command not in ['E', 'P']:
            path_variable = user_input[2:last_index]
            edit_lst = None

    # Format based on if it is 'E' or 'P'
    else:
        edit_lst = user_input.split(' ')
        path = None

    # Return information
    return command, path_variable, options_lst, input_lst, edit_lst


def create(path_variable: str, input_lst: list, special_path = ''):
    """
    Return error code, output message, profile object, special path.
    """
    # Stop if the path is not provided (length is 0)
    if len(path_variable) == 0:
        return 0, 'Re-enter path variable (Current length: 0)', None, ''
    
    # Stop if empty
    elif input_lst == None or input_lst == "":
        return 0, 'Invalid input name', None, ''
        
    else:
        path_join = str(input_lst[0]) + '.dsu'
        special_path = Path(path_variable) / path_join
        profile = Profile()
        
        # If path does not exist then create a new path
        if not special_path.exists():
            # Gather user input to populate the profile object

            # Get the IP address
            print('Please specify the user IP address')
            dsu_server = input()
            while ' ' in dsu_server or dsu_server.isspace() or dsu_server == '':
                print('Can not have whitespaces in IP address. Please re-enter IP Address.')
                dsu_server = input()

            # Get the username
            print('Please enter a username: ')
            user_name = input()
            while ' ' in user_name or user_name.isspace() or user_name == '':
                print('Can not have whitespaces in username. Please re-enter username: ')
                user_name = input()

            # Get the password
            print('Please enter a password: ')
            password = input()
            while ' ' in password or password.isspace() or password == '':
                print('Can not have whitespaces in password. Please re-enter password: ')
                password = input()

            # Get the bio
            print('Enter your user bio: ')
            bio = input()
            while bio == '' or bio.isspace():
                print('Can not have empty bio. Please re-enter bio: ')
                bio = input()
            
            # Ask if bio should be posted online
            print('Would you like to upload this bio online? [Y/N]')
            bio_online = input()
            while bio_online not in ['Y', 'N']:
                print('Please enter \'Y\' or \'N\'')
                bio_online = input()
            if bio_online == 'Y':
                ds_client.send(dsu_server, PORT, user_name, password, "don't print this awawawawawwa", bio)
            
            # Stop if any field is empty
            if (user_name.isspace() or user_name == '' or user_name == None
                    or password.isspace() or password == '' or password == None
                    or bio.isspace() or bio == '' or bio == None):
                return 0, 'User input not completed.', None, ''

            # Create the profile locally
            special_path.touch()
            profile.dsuserver =  dsu_server
            profile.username = user_name
            profile.password = password
            profile.bio = bio
            profile.save_profile(special_path)
            return 1, 'Profile has been created.', profile, special_path
            
        # If path exists load into profile and return profile 
        else:
            try:
                profile.load_profile(special_path)
                return 1, 'Existing profile has been loaded.', profile, special_path
            
            # Error if file DNE or is not dsu format
            except DsuFileError:
                return 0, 'Not a DsuFile or File doesnt exist.', None, special_path

            # Error if dsu file is not formatted correctly to load into a profile
            except DsuProfileError:
                return 0, 'Error loading profile', None, special_path


def open(path_variable: str):
    """
    Return error code, output message, open file, special path.
    """
    # Return immediately if there is no path (length is 0)
    if len(path_variable) == 0:
        return 0, 'Re-enter path variable (Current length: 0)', None, ''
    
    else:
        special_path = Path(path_variable)
        profile = Profile()
        
        # Stop if the file is not in dsu format
        if special_path.suffix != '.dsu':
            return 0, 'Your file is not in dsu format', None, ''

        # Try to load the dsu file
        try:
            profile.load_profile(special_path)
            return  1, 'Your dsu file has been loaded and opened.',  profile, special_path

        # Error if file doesn't exist
        except DsuFileError:
            return 0, 'Your dsu file doesnt exist', None, ''

        # Error if profile could not be loaded
        except DsuProfileError:
            return 0, 'Error loading dsu profile. Maybe file is not in proper dsu format', None, ''


def editProfile(user_input, profile, special_path) -> None:
    """
    When user uses the E (Edit) Function. Edits fields as per the user input.
    """
    edit_dict = {}
    edit_lst = user_input.split(' ')
    edits_options_lst = ['-usr', '-pwd', '-bio', '-addpost', '-delpost']
    posts = profile.get_posts()

    # Iterates over edit_lst which is the user input split by whitespace.
    for index in range(len(edit_lst)):
        temp = index

        # Enters if item in both edit_lst and edit_options_lst.
        if edit_lst[index] in edits_options_lst:
            # Tracks current common item/command
            sub_command = edit_lst[index]
            
            # Intializes edit_str and puts all chars in the edit_str, which could be an ID, a post, a bio, a usr, a pwd, etc.
            edit_str = ''
            while index < (len(edit_lst) - 1) and edit_lst[index + 1] not in edits_options_lst:
                if edit_str == '':
                    edit_str = edit_lst[index + 1]
                else:
                    edit_str += f' {edit_lst[index + 1]}'
                index += 1
            edit_str = edit_str.strip("\"").strip("\'")
            
            # Error handling empty edit option.
            if len(edit_str) == 0:
                print("Wrong input. Edit fields cant be empty. Stopping further processing")
                break
            
            # Error handling for deleting post ID out of bounds
            if sub_command == '-delpost' and int(edit_str) > len(posts):
                print("Wrong input. Cant delete out of bounds. Stopping further processing")
                break
            
            # Adds the common option to the edit_dict as key, and the key corresponds to the edit_str.
            if edit_lst[temp] not in edit_dict:
                edit_dict[edit_lst[temp]] = edit_str
            
            # Considers special cases for 'addpost' and 'delpost'.
            else:
                # If the keys are 'addpost' or 'delpost' and their corresponding value is not a list.
                if type(edit_dict[edit_lst[temp]]) != list and (edit_lst[temp] == '-addpost' or edit_lst[temp] == '-delpost'):
                    temp_str = edit_dict[edit_lst[temp]]
                    edit_dict[edit_lst[temp]] = [temp_str]
                    edit_dict[edit_lst[temp]].append(edit_str)

                # If multiple 'addpost' or 'delpost' options.
                else:
                    if (edit_lst[temp] == '-addpost' or edit_lst[temp] == '-delpost'):
                        edit_dict[edit_lst[temp]].append(edit_str)
                    else:
                        edit_dict[edit_lst[temp]] = edit_str


    # Change the username
    if '-usr' in edit_dict:
        profile.username = edit_dict['-usr']

    # Change the password
    if '-pwd' in edit_dict:
        profile.password = edit_dict['-pwd']

    # Change the bio
    if '-bio' in edit_dict:
        profile.bio = edit_dict['-bio']

        # Prompt if changes should be published online
        print('Would you like to upload this bio online? [Y/N]')
        bio_online = input()
        
        # Re-ask for input if not 'Y' or 'N'
        while bio_online not in ['Y', 'N']:
            print('Please enter \'Y\' or \'N\'')
            bio_online = input()
            
        if bio_online == 'Y':
            ds_client.send(profile.dsuserver, PORT, profile.username, profile.password, "don't print this awawawawawwa", profile.bio)
        
    # Add a post
    if '-addpost' in edit_dict:
        # Initialize OpenWeather Object, set apikey, load data.
        open_weather = OpenWeather(zipcode = "92697", ccode = "US")
        open_weather.set_apikey(apikey = 'acb9858a37fbea9ff876d852b50bb85e')
        open_weather.load_data()

        # Initialize LastFM Object, set apikey, load data.
        last_fm = LastFM()
        last_fm.set_apikey(apikey = '080bc3102eb83b87ddeb7f80699c145d')
        last_fm.load_data()

        # Initialize Extracredit Object, set apikey, load data.
        extra_credit = ExtraCreditAPI()
        extra_credit.set_apikey(apikey = '6f3cf60b6699477db0f8d939c4305ffb')
        extra_credit.load_data()

        # If there are multiple '-addpost' iterate through all of them
        if type(edit_dict['-addpost']) == list:
            index = 0
            for post in edit_dict['-addpost']:
                index += 1
                transclude_post = post
                if '@weather' in post:
                    transclude_post = open_weather.transclude(transclude_post)
                if '@lastfm' in post:
                    transclude_post = last_fm.transclude(transclude_post)
                if '@extracredit' in post:
                    transclude_post = extra_credit.transclude(transclude_post)

                profile.add_post(Post(transclude_post))

                # Prompt if changes should be published online
                print(f'Would you like to upload post {index} online? [Y/N]')
                post_online = input()

                # Re-ask for input if not 'Y' or 'N'
                while post_online not in ['Y', 'N']:
                    print('Please enter \'Y\' or \'N\'')
                    post_online = input()
                    
                if post_online == 'Y':
                    ds_client.send(profile.dsuserver, PORT, profile.username, profile.password, transclude_post)

        # If only one '-addpost' then make the change
        else:
            transclude_post = edit_dict['-addpost']

            if '@weather' in transclude_post:
                transclude_post = open_weather.transclude(transclude_post)
            if '@lastfm' in transclude_post:
                transclude_post = last_fm.transclude(transclude_post)
            if '@extracredit' in transclude_post:
                transclude_post = extra_credit.transclude(transclude_post)

            profile._posts.append(Post(transclude_post))

            # Prompt if changes should be published online
            print('Would you like to upload this post online? [Y/N]')
            post_online = input()
            while post_online not in ['Y', 'N']:
                print('Please enter \'Y\' or \'N\'')
                post_online = input()
            if post_online == 'Y':
                ds_client.send(profile.dsuserver, PORT, profile.username, profile.password, transclude_post)

    # Delete a post
    if '-delpost' in edit_dict:

        # If multiple 'delpost' then iterate through the list of changes
        if type(edit_dict['-delpost']) == list:
            edit_dict['-delpost'].sort(reverse=True)
            for i in edit_dict['-delpost']:
                deleted = profile.del_post(int(i))
                if deleted == False:
                    print("index ", i, " is out of bounds.")

        # Only one 'delpost' so make the changes
        else:
            deleted = profile.del_post(int(edit_dict['-delpost']))
            if deleted == False:
                print("index ", edit_dict['-delpost'], " is out of bounds.")

    # Save the profile
    profile.save_profile(special_path)
    if edit_dict != {}:
        print("The edits have been made, and your profile has been saved.")


def printProfile(user_input, profile, special_path):
    """
    Iterate through and format user input to know what to print.
    """
    # Initialize variables
    edit_dict = {}
    edit_lst = user_input.split(' ')
    edits_options_lst = ['-usr', '-pwd', '-bio', '-all', '-posts', '-post']
    
    # Format input into a dict to know what to print
    for index in range(len(edit_lst)):
        temp = index
        if edit_lst[index] in edits_options_lst:
            edit_str = ''
            while index < (len(edit_lst) - 1) and edit_lst[index + 1] not in edits_options_lst:
                if edit_str == '':
                    edit_str = edit_lst[index + 1]
                else:
                    edit_str += f' {edit_lst[index + 1]}'
                index += 1
            if edit_lst[temp] not in edit_dict:
                edit_dict[edit_lst[temp]] = edit_str

    # Print username
    if '-usr' in edit_dict:
        print('Profile username:', profile.username)

    # Print password
    if '-pwd' in edit_dict:
        print('Profile password:', profile.password)

    # Print bio
    if '-bio' in edit_dict:
        print('Profile bio:', profile.bio)

    # Print all posts
    if '-posts' in edit_dict:
        for index, post in enumerate(profile._posts):
            print(f'Post ID: {index}, Post entry:', post['entry'])

    # Print single post by ID
    if '-post' in edit_dict:
        try:
            id_out_of_bounds = False
            for index, post in enumerate(profile._posts):
                if int(edit_dict['-post']) == index:
                    print(post['entry'])
                elif int(edit_dict['-post']) >= len(profile._posts):
                    id_out_of_bounds = True
            if id_out_of_bounds:
                print('ID out of bounds, re-enter statement.')
        except:
            print('Invalid Input. Please try again.')

    # Print everything
    if '-all' in edit_dict:
        print('Profile server:', profile.dsuserver)
        print('Profile username:', profile.username)
        print('Profile password:', profile.password)
        print('Profile bio:', profile.bio)
        for index, post in enumerate(profile._posts):
            print(f'Post ID: {index}, Post entry:', post['entry'])
