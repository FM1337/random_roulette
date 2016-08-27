# Random game roulette v3.0
# By FMCore
# This will choose a random game for you to playing
# It also gives you the option to tweet what game you are playing and for what system (e.g Gameboy Advance, Gameboy Color, etc etc)

import os, random
import subprocess
from twython import Twython
import time
import ConfigParser
import Tkinter as tk
import tkFileDialog
import tkMessageBox
import tkSimpleDialog
import os.path

systems_list = []

def options(option):
    if option == 1:
        title = 'Confirmation'
        choice = 'Just to be sure, you chose option 1, which means your roms are all mixed together in 1 folder.'
        icon = 'question'
        structure = 'mixed'
        return title, choice, icon, structure
    elif option == 2:
        title = 'Confirmation'
        choice = 'Just to be sure, you chose option 2, which means your roms are in different folders and not in the same parent folder (Same parent would be c:\\roms different folders is c:\\gba c:\\gbc)'
        icon = 'question'
        structure = 'different_folders'
        return title, choice, icon, structure
    elif option == 3:
        title = 'Confirmation'
        choice = 'Just to be sure, you chose option 3, other folder format setups'
        icon = 'question'
        structure = 'other'
        return title, choice, icon, structure
    elif option == 0:
        title = 'Confirmation'
        choice = 'Just to be sure, you wish to exit this app?'
        icon = 'question'
        structure = 'n/a'
        return title, choice, icon, structure
    elif option == None:
        title = 'Error'
        choice = 'You must input something!'
        type = 'error'
        structure = 'n/a'
        return title, choice, icon, structure
    else:
        title = 'Error'
        choice = 'This is not an option! Please try again!'
        icon = 'error'
        structure = 'n/a'
        return title, choice, icon, structure

def format():
    roms = tkMessageBox.askquestion('ROMs directory', 'Do you keep your ROMs in subfolders? (E.g C:\\ROMs\\GBA)', icon='question')
    if roms == 'yes':
        tkMessageBox.showinfo('Wonderful!', 'Alrighty! This makes setup a lot easier! :) When you click OK please select your ROMs subfolder holding directory (Using the case before, it would be C:\\ROMs)')
        structure = 'default'
        confirm = 'yes'
        rom_folder = folders(structure)
        return confirm, structure, rom_folder
    else:
        tkMessageBox.showinfo('I see', 'Alright, this is gonna be a bit more difficult to setup. Please Press OK to continue')
        tkMessageBox.showinfo('Ok', 'On the next screen, I\'m going to ask you how you have your ROMs folder set up, and I need you to answer EXACTLY as it says to answer or it will not work! when you\'re ready click OK')
        format = tkSimpleDialog.askinteger('Folder format', 'Please type 1 if your ROMs are all together (e.g C:\ROMs contains all your roms mixed together and not sorted by subfolder)\nPlease type 2 if your roms are in different folders (e.g C:\GBA C:\GB etc etc)\n Please type 3 for other.\n Please type 0 to cancel!', maxvalue=3, minvalue=0)
        title, choice, icon, structure = options(format)
        confirm = tkMessageBox.askquestion(title, choice, icon=icon)
        if confirm == 'yes' and format == 0:
            exit(0)
        else:
            rom_folder = folders(structure)
            return confirm, structure, rom_folder

def folders(structure):
    if structure == 'default':
        rom_folder = tkFileDialog.askdirectory(title='Please pick your ROMs folder')
        return rom_folder
    elif structure == 'mixed':
        rom_folder = tkFileDialog.askdirectory(title='Please pick your ROMs folder')
        return rom_folder
    elif structure == 'different_folders':
        rom_folder = 'Placehold'
        return rom_folder
    elif structure == 'other':
        tkMessageBox.showinfo('Sorry', 'I\'m afraid your sorting type isn\'t support :( Hopefully in the future it will be added!')
        exit(0)

def config(existing):
    if existing == 'no':
        config = ConfigParser.RawConfigParser()
        config.add_section('ROMs')
        config.add_section('Emulators')
        config.add_section('General')
        config.add_section('Twitter')
        config.add_section('Status')
        config.set('Status', 'status', 'first_run')
        root = tk.Tk()
        root.withdraw()
        confirm, structure, rom_folder = format()
        if confirm == 'no':
            while confirm == 'no':
                tkMessageBox.showinfo('I see', 'Alright, let\'s try this again')
                confirm = format()
        else:
            pass
        config.set('General', 'roms_directory', '%s' % rom_folder)
        config.set('General', 'folder_structure', '%s' % structure)
        twitter_enable = tkMessageBox.askquestion('Twitter', 'Do you want tweets enabled? This will tweet what game you are playing and will remove it when you are finished playing', icon='question')
        config.set('Twitter', 'enable', '%s' % twitter_enable)
        if twitter_enable == 'yes':
            app_key = tkSimpleDialog.askstring('Twitter App Key', 'Please enter your app key')
            app_secret = tkSimpleDialog.askstring('Twitter App Key Secret', 'Please enter your app secret key')
            oauth_token = tkSimpleDialog.askstring('Twitter OAuth Token', 'Please enter your oauth token')
            oauth_token_secret = tkSimpleDialog.askstring('Twitter OAuth Token Secret', 'Please enter your oauth secret token')
            screen_name = tkSimpleDialog.askstring('Twitter Screen name', 'Please enter your twitter screen name')
            config.set('Twitter', 'app', '%s' % app_key)
            config.set('Twitter', 'app_secret', '%s' % app_secret)
            config.set('Twitter', 'oauth', '%s' % oauth_token)
            config.set('Twitter', 'oauth_secret', '%s' % oauth_token_secret)
            config.set('Twitter', 'screen_name', '%s' % screen_name)
        else:
            config.set('Twitter', 'app', 'disabled')
            config.set('Twitter', 'app_secret', 'disabled')
            config.set('Twitter', 'oauth', 'disabled')
            config.set('Twitter', 'oauth_secret', 'disabled')
        fs = config.get('General', 'folder_structure')
        gb = tkMessageBox.askquestion('GB', 'Do you have any Gameboy roms?', icon='question')
        if gb == 'yes':
            fs = config.get('General', 'folder_structure')
            config.set('ROMs', 'gb', '%s' % gb)
            gb_emulator = tkFileDialog.askopenfilename(filetypes=[('Applications','*.exe')], title='Please pick a gameboy emulator')
            config.set('Emulators', 'gb', '%s' % gb_emulator)
            if fs == 'different_folders':
                systems_list.append('gb')
                rom_folder = tkFileDialog.askdirectory(title='Please pick your GB ROMs folder')
                config.set('ROMs', 'gb_location', '%s' % rom_folder)
        else:
            config.set('ROMs', 'gb', '%s' % gb)
        gbc = tkMessageBox.askquestion('GBC', 'Do you have any Gameboy color roms?', icon='question')
        if gbc == 'yes':
            config.set('ROMs', 'gbc', '%s' % gbc)
            gbc_emulator = tkFileDialog.askopenfilename(filetypes=[('Applications','*.exe')], title='Please pick a gameboy color emulator')
            config.set('Emulators', 'gbc', '%s' % gbc_emulator)
            if fs == 'different_folders':
                systems_list.append('gbc')
                rom_folder = tkFileDialog.askdirectory(title='Please pick your GBC ROMs folder')
                config.set('ROMs', 'gbc_location', '%s' % rom_folder)
        else:
            config.set('ROMs', 'gbc', '%s' % gbc)
        gba = tkMessageBox.askquestion('GBA', 'Do you have any Gameboy advance roms?', icon='question')
        if gba == 'yes':
            config.set('ROMs', 'gba', '%s' % gba)
            gba_emulator = tkFileDialog.askopenfilename(filetypes=[('Applications','*.exe')], title='Please pick a gameboy advance emulator')
            config.set('Emulators', 'gba', '%s' % gba_emulator)
            if fs == 'different_folders':
                systems_list.append('gba')
                rom_folder = tkFileDialog.askdirectory(title='Please pick your GBA ROMs folder')
                config.set('ROMs', 'gba_location', '%s' % rom_folder)
        else:
            config.set('ROMs', 'gba', '%s' % gba)
        nes = tkMessageBox.askquestion('NES', 'Do you have any Nintendo Entertainment System roms?', icon='question')
        if nes == 'yes':
            config.set('ROMs', 'nes', '%s' % nes)
            nes_emulator = tkFileDialog.askopenfilename(filetypes=[('Applications','*.exe')], title='Please pick a nes emulator')
            config.set('Emulators', 'nes', '%s' % nes_emulator)
            if fs == 'different_folders':
                systems_list.append('nes')
                rom_folder = tkFileDialog.askdirectory(title='Please pick your NES ROMs folder')
                config.set('ROMs', 'nes_location', '%s' % rom_folder)
        else:
            config.set('ROMs', 'nes', '%s' % nes)
        snes = tkMessageBox.askquestion('SNES', 'Do you have any Super Nintendo Entertainment System roms?', icon='question')
        if snes == 'yes':
            config.set('ROMs', 'snes', '%s' % snes)
            snes_emulator = tkFileDialog.askopenfilename(filetypes=[('Applications','*.exe')], title='Please pick a snes emulator')
            config.set('Emulators', 'snes', '%s' % snes_emulator)
            if fs == 'different_folders':
                systems_list.append('snes')
                rom_folder = tkFileDialog.askdirectory(title='Please pick your SNES ROMs folder')
                config.set('ROMs', 'snes_location', '%s' % rom_folder)
        else:
            config.set('ROMs', 'snes', '%s' % snes)
        with open('config.cfg', 'wb') as configfile:
            config.write(configfile)
    else:
        pass

def game_system(game):
    if game.lower().endswith('.gb') and config.get('ROMs', 'gb') == 'yes':
        system_type = 'gameboy'
        system_name = 'Gameboy'
        game_name = game[:-3]
        emulator_path = config.get('Emulators', 'gb')
        return system_type, system_name, game_name, emulator_path

    elif game.lower().endswith('.gbc') and config.get('ROMs', 'gbc') == 'yes':
        system_type = 'gameboy_color'
        system_name = 'Gameboy Color'
        game_name = game[:-4]
        emulator_path = config.get('Emulators', 'gbc')
        return system_type, system_name, game_name, emulator_path

    elif game.lower().endswith('.nes') and config.get('ROMs', 'nes') == 'yes':
        system_type = 'Nintendo_Entertainment_System'
        system_name = 'NES'
        game_name = game[:-4]
        emulator_path = config.get('Emulators', 'nes')
        return system_type, system_name, game_name, emulator_path

    elif game.lower().endswith('.smc') and config.get('ROMs', 'snes') == 'yes':
        system_type = 'Super_Nintendo'
        system_name = 'SNES'
        game_name = game[:-4]
        emulator_path = config.get('Emulators', 'snes')
        return system_type, system_name, game_name, emulator_path

    elif game.lower().endswith('.gba') and config.get('ROMs', 'gba') == 'yes':
        system_type = 'Gameboy_Advance'
        system_name = 'Gameboy Advance'
        game_name = game[:-4]
        emulator_path = config.get('Emulators', 'gba')
        return system_type, system_name, game_name, emulator_path
    else:
        system_type = 'Unknown'
        exit(1)

def delete_tweet(check_twitter):
    screen_name = config.get('Twitter', 'screen_name')
    status = config.get('Status', 'status')
    if check_twitter == 1:
        check = twitter.get_user_timeline(screen_name=screen_name,count=3)
        if status == 'opened':
            for tweet in check:
                text = tweet['text']
                if 'NES' in text or 'Gameboy Advance' in text or 'Gameboy' in text or 'SNES' in text:
                    id = tweet['id_str']
                    twitter.destroy_status(id=id)
        else:
            config.set('Status', 'status', 'opened')
            with open('config.cfg', 'wb') as configfile:
                config.write(configfile)
    elif check_twitter == 2:
        timeline = twitter.get_user_timeline(screen_name=screen_name,count=1)
        for tweet in timeline:
            text = tweet['text']
            if 'NES' in text or 'Gameboy Advance' in text or 'Gameboy' in text or 'SNES' in text or game_name in text: #
                id = tweet['id_str']
                twitter.destroy_status(id=id)
                config.set('Status', 'status', 'exited')
                with open('config.cfg', 'wb') as configfile:
                    config.write(configfile)
            else:
                exit(1)

def folder_structures(type):
    if type == '1':
        roms_directory = config.get('General', 'roms_directory')
        system = random.choice(os.listdir(roms_directory))
        game = random.choice(os.listdir('%s/%s' % (roms_directory, system)))
        system_type, system_name, game_name, emulator_path = game_system(game)
        path_to_rom = ('%s/%s/%s' % (roms_directory, system, game))
        return roms_directory, system, game, path_to_rom
    elif type == '2':
        roms_directory = config.get('General', 'roms_directory')
        game = random.choice(os.listdir('%s' % roms_directory))
        system_type, system_name, game_name, emulator_path = game_system(game)
        path_to_rom = ('%s/%s' % (roms_directory, game))
        return roms_directory, game, path_to_rom
    elif type == '3':
        system = random.choice(systems_list)
        roms_directory = config.get('ROMs', '%s_location' % system)
        game = random.choice(os.listdir('%s' % roms_directory))
        system_type, system_name, game_name, emulator_path = game_system(game)
        path_to_rom = ('%s/%s' % (roms_directory, game))
        return roms_directory, game, path_to_rom
    else:
        exit(1)

exists = os.path.isfile('./config.cfg')
if exists == False:
    existing = 'no'
    config(existing)
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')
else:
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')

tweeting = config.get('Twitter', 'enable')
if tweeting == 'yes':
    app = config.get('Twitter', 'app')
    app_secret = config.get('Twitter', 'app_secret')
    oauth = config.get('Twitter', 'oauth')
    oauth_secret = config.get('Twitter', 'oauth_secret')
    twitter = Twython(app, app_secret, oauth, oauth_secret)
    check_twitter = 1
    delete_tweet(check_twitter)
else:
    pass

def arrays():
    if config.get('ROMs', 'gb') == 'yes':
        systems_list.append('gb')
    if config.get('ROMs', 'gbc') == 'yes':
        systems_list.append('gbc')
    if config.get('ROMs', 'gba') == 'yes':
        systems_list.append('gba')
    if config.get('ROMs', 'nes') == 'yes':
        systems_list.append('nes')
    if config.get('ROMs', 'snes') == 'yes':
        systems_list.append('snes')
    else:
        pass
path = config.get('General', 'folder_structure')
if path == 'default':
    type = '1'
    roms_directory, system, game, path_to_rom = folder_structures(type)
    system_type, system_name, game_name, emulator_path = game_system(game)
    print('%s/%s/%s is a %s game' % (roms_directory, system, game, system_type))
    if tweeting == 'yes':
        twitter.update_status(status='I am playing %s for the %s' %(game_name, system_name))
    else:
        pass
elif path == 'mixed':
    type = '2'
    roms_directory, game, path_to_rom = folder_structures(type)
    system_type, system_name, game_name, emulator_path = game_system(game)
    print('%s/%s is a %s game' % (roms_directory, game, system_type))
    if tweeting == 'yes':
        twitter.update_status(status='I am playing %s for the %s' %(game_name, system_name))
    else:
        pass
elif path == 'different_folders':
    type = '3'
    arrays()
    roms_directory, game, path_to_rom = folder_structures(type)
    system_type, system_name, game_name, emulator_path = game_system(game)
    print('%s/%s is a %s game' % (roms_directory, game, system_type))
    if tweeting == 'yes':
        twitter.update_status(status='I am playing %s for the %s' %(game_name, system_name))
    else:
        pass
else:
    exit(1)

subprocess.call([emulator_path, path_to_rom])

if tweeting == 'yes':
    time.sleep(3)
    check_twitter = 2
    delete_tweet(check_twitter)
else:
    exit(0)
