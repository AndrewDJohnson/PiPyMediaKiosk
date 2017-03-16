#=======================================================
# PiPy Media Player V1.0 - for Raspberry Pi
# A.D. Johnson - 14 Mar 2017
#
# This Python Program is designed to be a simple front end menu for a "kiosk" type media player.
# The media player has a simple 3-button keyboard which is connected to 4 GPIO pins to make the cheapest
# possible keyboard.
#
# Files are copied to the SD card from a USB stick and can be played in sequence.
# Works in conjunction with:
#   LibreOffice Impress - to show PowerPoint files (a separate script runs this`)
#   qiv - Quick image viewer
#   mpv video player for playing videos using Pi's hardware acceleration
#
# Menu includes simple file management and configuration features - could be customised to do anything.
#=======================================================

#Import Modules/Libraries which are needed by the Menu Program....
from Tkinter import *
import time
import tkMessageBox
import tkFont
import os
import platform
import subprocess
import shutil
from ConfigParser import SafeConfigParser
from time import sleep

#Main window dimensions. Fits on a 640 x 480 screen!
win_width = 590 
win_height = 400 
#We could have more or less buttons per menu...
MENU_SIZE=5

#Create a window using the Tkinter library
win = Tk()


#These are the GPIO Numbers used for the buttons, along with 3.3V pin for common/high.
GPIO_RIGHT_NEXT_BUTTON=17
GPIO_LEFT_PREV_BUTTON=22
GPIO_OK_BUTTON=27
#We will have Several Different Menus.....
MAIN_MENU_STATE=0
SETTINGS_MENU_STATE=5
FILES_MENU_STATE=10
PLAY_MODE_MENU_STATE=15
QUIT_MENU_STATE=20


#Create an object that we will use to save/load configuration options later
config = SafeConfigParser()
#This will be the filename for the config file which is created.
config_file_name="pi-ppt-play.ini"

#A few global variables which will help us remember a few things...
waiting_for_yes_no=False
show_running=False
menu_timeout=30


#Move mouse pointer out of the way using xvkbd command
os.system('xvkbd -text "\x2000 \y2000"')


#-----------------------------------------#
#This will be a Timer Object used for 
#displaying messages and for starting our 
#show after a timeout 
#-----------------------------------------#
class TimeOut():

    #Initialise/Constructor function
    def __init__(self):
        #Configure our own variables/class members...
        
        #Link this object to the main window
        self.root = win
        #We will be changing text in a label control....
        self.label = timeout_label
        #Set the timeout count to be the same as that configured.
        self.timeout=int(menu_timeout)
        #We will use this to check when a show just stopped.
        self.last_show_running_check = 0
        #Kick off the updating...
        self.update_clock()
        
    def update_clock(self):
        #We will refer to this global variable to check if a show is running.
        global show_running
        
        #Decrement the timer value in the object
        self.timeout=self.timeout-1
        
        #We will start our show when the timeout reaches zero...
        if (self.timeout==0):
                start_show()
        else:
            #Update the timer message..
            if (self.timeout > 0):
                self.label.configure(text="Starting in " + str (self.timeout) +" ...")
            else:
                self.label.configure(text="")

        #Check if we have gone from a state or "show running" to "not running anymore"
        if self.last_show_running_check and not show_running:
            #Reset the timeout to the configured value.
            self.timeout=int(menu_timeout)
            #Make the Python menu window re-appear
            win.deiconify()

        #Update the "show_running" flag check
        self.last_show_running_check = show_running
        
        #Set timeout for a "Clock update" so this function gets called again after 1 second
        self.root.after(1000, self.update_clock)
#-----------------------------------------#
# End of Timeout Object Definition
#-----------------------------------------#

#Check if we're on a Raspberry Pi/Linux and do do appropriate initialisation/setup.
#This allows some testing of the menu operation to be done without having a Pi
if sys.platform == "linux2":
        #Import Ras Pi specific libraries for the hardware.
        import RPi.GPIO as GPIO
        import uinput
        #Set up "Device" object from the Uinput library so we can generate keypresses - with the type listed below.
        device = uinput.Device([
            #These are the keypresses we want to generate to operate the menu using switches attached
            #to the GPIO pins, rather than using a real keyboard etc.
            uinput.KEY_UP,
            uinput.KEY_DOWN,
            uinput.KEY_LEFT,
            uinput.KEY_RIGHT,
            uinput.KEY_SPACE,
            uinput.KEY_TAB,
            uinput.KEY_ENTER,
            uinput.KEY_LEFTSHIFT
            ])
#=======================================================
# Key Scan Object
# Sets up and scans GPIO pins to generate keypresses
#=======================================================
        #This object will be instantiated to scan the GPIO pins for state changes.
        class KeyScanObj():

            #Initialise  
            def __init__(self):
                #Initialise GPIO
                GPIO.setmode(GPIO.BCM)
                #Set the  pins to be "Pull Down" Inputs
                GPIO.setup(GPIO_RIGHT_NEXT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(GPIO_LEFT_PREV_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(GPIO_OK_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                #Associate this object with the TKinter window we created.
                self.root = win
                #Kick off the key scanning (see below)
                self.scan_switches()

            #We are using 3 different viewers/players and this function sends a quite/abort sequence...
            def send_quit(self):
                #We might need to send a "Space" keypress...
                device.emit_click(uinput.KEY_SPACE)
                #We use the "echo" command to send another command to a socket which the mpv video player listens on...
                cmd_line = 'echo \'{ "command": ["quit", "0"] }\'  | socat - /tmp/mpvsocket'
                #Invoke through command line.
                os.system (cmd_line)
                #Now we will use xvkkbd to send key pressess to "qiv" image viewer and LibreOffice Impress - to quit out.
                cmd_line = 'xvkbd -window "qiv*" -text "\e" && xvkbd -window "LibreOffice 4.3" -text "\e"'
                os.system (cmd_line)
                #Delay for 1 tenth of a second.
                sleep (.1)
                
            #This method scans the switches and sends different key sequences etc depending on current state.
            def scan_switches (self):
                #We need to look at these globals from the main program...
                global show_running, waiting_for_yes_no, menu_timeout
  
                if GPIO.input(GPIO_RIGHT_NEXT_BUTTON) == GPIO.IN:
                    if GPIO.input(GPIO_LEFT_PREV_BUTTON) == GPIO.IN:
                        self.send_quit()
                    else:
                        #Special state in menu handling.
                        if (waiting_for_yes_no==True):
                                device.emit_click(uinput.KEY_TAB)
                                print "Sent TAB button"
                        else:
                                if (show_running):
                                    if (config.get("Settings","Interactive") == "Yes"):
                                        #Execute commands to control mpv video player and image qiv viewer to go to next image etc
                                        cmd_line = 'xvkbd -window "qiv*" -text " " && echo \'{ "command": ["seek", "+30"] }\'  | socat - /tmp/mpvsocket'
                                        os.system (cmd_line)
                                else:
                                    #Else - we just send the "down" key to move the menu selection down.
                                    device.emit_click(uinput.KEY_DOWN)

                if GPIO.input(GPIO_LEFT_PREV_BUTTON) == GPIO.IN:
                    if GPIO.input(GPIO_RIGHT_NEXT_BUTTON) == GPIO.IN:
                            self.send_quit()
                    else:
                            #Special state in menu handling.
                            if (waiting_for_yes_no==True):
                                #Allow us to select Yes/No options (needs different key code)
                                device.emit_combo([uinput.KEY_LEFTSHIFT,uinput.KEY_TAB])
                            else:
                                if (show_running): 
                                    if (config.get("Settings","Interactive") == "Yes"):
                                        #Execute commands to control mpv video player and image qiv viewer to go to previous image etc
                                        cmd_line = 'xvkbd -window "qiv*" -text "\\b" && echo \'{ "command": ["seek", "-20"] }\'  | socat - /tmp/mpvsocket'
                                        os.system (cmd_line)
                                else:
                                    #Allow us to select Yes/No options (needs different key code)
                                    device.emit_click(uinput.KEY_UP)

                #Has the "OK" button been pressed?
                if GPIO.input(GPIO_OK_BUTTON) == GPIO.IN:
                    #Simulate a keypress of ENTER
                    device.emit_click(uinput.KEY_ENTER)
                    #Debounce so that we don't detect more than 1 keypress.
                    sleep (.05)
                    
                #Set flag based on whether stuff is still running...
                show_running=os.path.isfile("show_running.temp")
                sleep(.09)
                #Call this same function again after a delay of 50ms
                self.root.after(50, self.scan_switches)

        #Instantiate the keyscan object to kick off key scanning...
        key_scan = KeyScanObj()


#=======================================================
# Now some data we need... Self explanatory, I hope!
#=======================================================
menu_names = (
    "Main",
    "Settings",
    "Delete Files",
    "Set Play Mode",
    "Reboot/Shutdown",
    )

play_modes = (
    "All",
    "One",
    "List"
    )

video_file_extensions_list=['avi','mpg','mpg','mpeg','mp4','mov','wmv','mts','mkv']
ppt_file_extensions_list=['ppt','pptx','pps','odp']
image_file_extensions_list=["jpg","jpeg","png","gif"]

#=======================================================    
#The following section defines functions which are typically called
#when a menu option is selected. The mapping between function names and 
#menu options is set in a list/table/array below the function definitions.
#=======================================================

#This function is called when we start a show running.
def start_show():
    #Global vars we need to access in this function.
    global file_listbox,show_running,timeout_obj
    
    #Check if we're already running - if we are, drop out.
    if (show_running):
        return
    
    #Get the delay we set in the config
    slide_delay = config.get("Settings","SlideDelay")

    #Minimise the window.
    win.iconify()
    
    #We will build up a command line to invoke the PPT/Image viewers and video player...
    cmd_line=""
    
    #Are we going to play PPT files?
    if (config.get("Settings","PlayPPT") == "Yes"):
        show_running=True
        #Go and recurse down the PPT folder to find all the powerpoints to play
        for root, dirs, files in os.walk("./media/PPT",followlinks=True):
            #Check each folder...
            for file in files:
                #Get a file name...
                filename=os.path.join(root, file)
                #Check it's not a leftover....
                if not file.lower().startswith(".~lock") and os.path.isfile(filename):
                    #Check if we are doing an interactive show (user presses buttons to advance)
                    if (config.get("Settings","Interactive") == "Yes"):
                        show_running=True
                        #Set up the command line to run Office Impress (from a separate script)
                        cmd_line = cmd_line + "bash ./runppt.sh " + "0" + ' "' + filename + '" && '
                    else:
                        #Non-interactive run - so add the delay value.
                        cmd_line = "bash ./runppt.sh " + str(int(slide_delay)*1000) + ' "' + filename  + '" && '

    #Are we going to play images?
    if (config.get("Settings","PlayImages") == "Yes"):
        show_running=True
        #Set up an appropriate command line for an interactive or non-interactive run
        if (config.get("Settings","Interactive") == "No"):
            cmd_line ="qiv -f -m -P -s -i -C -d " + slide_delay 
        else:
            cmd_line = cmd_line + " qiv -f -m -P -s -i -C -d 3600"
        #Scan through any sub-folders of images.
        for root, dirs, files in os.walk("./media/Images",followlinks=True):
            cmd_line = cmd_line + " " + root 
        
        #Get ready to add on next command...                
        cmd_line = cmd_line + " && "

    #Are we going to play videos?                                
    if (config.get("Settings","PlayVideos") == "Yes"):
          show_running=True
          #Command line for mpv video player - it will scan subdirectories by itself
          #Additionally, it can listen on a socket for commands - as the process *won't* be attached to a console
          #that we can send keypresses to...
          cmd_line = cmd_line + "mpv --really-quiet --input-ipc-server=/tmp/mpvsocket ./media/Video/* &&"
          
    #Now we run everything - creating a file before we run and deleting it when we finish, so that
    #we know when the show has finished....
    cmd_line = "echo temp>show_running.temp && " + cmd_line + " sudo rm show_running.temp &"
    os.system (cmd_line)
    print "Commands: " + cmd_line
        
        
#This will display the Settings Menu buttons (and modify the appropriate button text based on our current settings)
def settings_menu ():
    #Set up the menu buttons.
    populate_menu(SETTINGS_MENU_STATE)
    #Set up the button labels based on whatever is in the settings we saved.
    menu_label="Autostart Delay="+config.get("Settings","StartDelay")+" secs"
    main_menu_object[0].core.config(text=menu_label)
    menu_label="Slide Delay="+config.get("Settings","SlideDelay")+" secs"
    main_menu_object[1].core.config(text=menu_label)

    menu_label="Interactive Show="+config.get("Settings","Interactive")
    main_menu_object[2].core.config(text=menu_label)

#Set the start delay - between runs of the show.         
def set_auto_start_delay():
    global config_value_to_set
    #This value is set so that when we press the menu button, the handler knows which value to 
    #write to in the config settings.
    config_value_to_set="AutoStart"
    #Set up the spin control to allow us to set the value using up/down buttons.
    spin_label.config(text="Auto Start Delay-OK to Set")
    #Make the label visible
    spin_label.pack()
    #Make the spin control visible
    spin_box_val.pack()
    var = StringVar(win)
    #Set the contents of the spin control to be the value in our config.
    var.set(config.get('Settings', 'StartDelay'))
    spin_box_val.config(textvariable=var)
    #Set the focus on the control.
    spin_box_val.focus_set()
    #Disable the normal up/down key association so we can work the spin control.
    unbind_nav_keys()

#Set the slide delay - this is essentially the same as the previous function, but we set a different config item.
def set_slide_delay():
    global config_value_to_set
    config_value_to_set="SlideDelay"
    spin_label.config(text="Slide Delay - OK to Set")
    spin_label.pack()
    spin_box_val.pack()
    var = StringVar(win)

    var.set(config.get('Settings', 'SlideDelay'))
    spin_box_val.config(textvariable=var)
    spin_box_val.focus_set()
    unbind_nav_keys()
        
#This function will copy files off an attached USB stick
#it assumes the stick will be mounted under the "/media directory - this is the default in Raspbian Jessie
#from what I could work out, it seems to something associated with PCManFM which does this.
def copy_files_from_folder(source_path,delete_source):
    global timeout_label, waiting_for_yes_no
    #Some initial setup
    file_count=0
    abort_copying=False
    timeout_label.pack()
    abort_copying=""
    #Look in the "media" folder for any devices.
    for root, dirs, files in os.walk(source_path,followlinks=True):
        #Get the folder we are in.
        folders = []
        path=root
        while 1:
            #Set the path and folder we are in 
            path, folder = os.path.split(path)
            #Build up the correct path etc
            if folder != "":
                folders.append(folder)
            else:
                if path != "":
                    folders.append(path)
                break

        if (abort_copying==True):
            break
        
        #Go through files
        for file in files:
            if (abort_copying==True):
                break
            #Get the filename found and convert to lowercase.
            fn = file.lower()
            #Get the full filename
            filename=os.path.join(root, file)
            
            #Check if we have found a splash screen...
            if (fn=="pipymediakiosk.png"):
                shutil.copy(filename,"/usr/share/plymouth/themes/pix/splash.png")
                continue
            #Check we have enough free space  for the file
            file_size = os.path.getsize(filename)
            statvfs = os.statvfs('.')
            free_space = statvfs.f_frsize * statvfs.f_bavail
            
            #Get ready to set up where we copy it to...
            dest_dir=""
            #Check for PPT file
            if fn[-3:] in ppt_file_extensions_list:
                dest_dir = "./media/PPT"
            #Check for Image file
            elif fn[-3:] in image_file_extensions_list or fn[-4:] in image_file_extensions_list:
                dest_dir = "./media/Images/"+folders[1]

            #Check for video file
            elif fn[-3:] in video_file_extensions_list:
                dest_dir = "./media/Video"
                
            #Check we have enough space to copy etc
            if dest_dir != "":
                if (file_size < free_space):
                    timeout_label.config(text="Copying... "+ file)
                    file_count = file_count + 1
                    try:
                       #print "Trying to make " + dest_dir
                       os.makedirs(dest_dir)
                    except OSError:
                       pass
                    #Allow labels on menu window to be updated.
                    win.update_idletasks()
                    #Do the copying!
                    shutil.copy (filename,dest_dir)
                    if (delete_source==True):
                        os.remove(filename)
                else:
                    #Not enough space so go into a special state...
                    waiting_for_yes_no=True
                    #Display a warning message
                    abort_copying = tkMessageBox.askyesno("Abort Copying?", "Not enough Space for " + file+ "\n - Abort Copying?")
                    #Reset the state.
                    waiting_for_yes_no=False
                    
                #Allow labels on menu window to be updated.                        
                win.update_idletasks()

    #Display a message that we have now finished copying...
    tkMessageBox.showinfo("Finished Copying",str(file_count) + " files copied. ")
    timeout_label.forget()


def copy_files_from_usb():
    copy_files_from_folder("/media",False)
    waiting_for_yes_no=True
    #Display a warning message
    if (tkMessageBox.askyesno("Move Files from Boot?", "Move Media files from Boot Partition?")==True):
        waiting_for_yes_no=False
        copy_files_from_folder("/boot/media",True)
    
    

#Setup the "Play Mode" menu.
def set_play_mode():
    #Draw the menu
    populate_menu(PLAY_MODE_MENU_STATE)
    #Now set the buttons up based on the state of config items.
    menu_label="Play PPT="+config.get("Settings","PlayPPT")
    main_menu_object[0].core.config(text=menu_label)
    menu_label="Play Images="+config.get("Settings","PlayImages")
    main_menu_object[1].core.config(text=menu_label)
    menu_label="Play Videos="+config.get("Settings","PlayVideos")
    main_menu_object[2].core.config(text=menu_label)
    menu_label="Audio Ouput ="+config.get("Settings","Audio")
    main_menu_object[3].core.config(text=menu_label)


#Set the "Interactive Show" config item in the menu
def set_interactive_show():
    if config.get("Settings","Interactive")=="Yes":
        config.set("Settings","Interactive","No")
    else:
        config.set("Settings","Interactive","Yes")
    write_config_file()
    settings_menu()

#Delete all the files in the "media" sub folder.
def delete_all_files():
    global waiting_for_yes_no
    waiting_for_yes_no=True
    if tkMessageBox.askyesno("Delete Files", "Are you sure you want to delete ALL files?"):
        shutil.rmtree("./media",ignore_errors=True)
    waiting_for_yes_no=False

#Selectively delete files using a listbox.    
def select_files_to_delete():
        global file_listbox
        
        #Call another function to build a list of all the files to delete!
        file_listbox=build_file_list("./media")
        #If any files were found, display help and then the listbox itself.
        if (file_listbox.size()>0):
            msg="Press Both Directional Buttons to Select A File, Enter to Delete"
            tkMessageBox.showinfo("Now Select Files",msg)
            playmode_label.config(text=msg,foreground="red")
            #We now use different navigation keys.
            unbind_nav_keys()
            #Set the size / width of the listbox
            file_listbox.config(width=80,height=6)
            #Display the listbox and set the focus
            file_listbox.pack(side=BOTTOM)
            file_listbox.focus_set()
        else:
            #We didn't find any files to delete!
            tkMessageBox.showinfo("No Files","No files to delete!")

#Set a menu item            
def set_play_mode_item(play_type):
    if config.get("Settings",play_type)=="Yes":
        config.set("Settings",play_type,"No")
    else:
        config.set("Settings",play_type,"Yes")
    write_config_file()
    set_play_mode()

#Set the flag to play powerpoint files or not!
def set_play_ppt():
    set_play_mode_item("PlayPPT")
    
#Set the flag to play image files or not!
def set_play_images():
    set_play_mode_item("PlayImages")

#Set the flag to play video files or not!
def set_play_videos():
    set_play_mode_item("PlayVideos")

#Set the audio output
def set_audio_output():
    if config.get("Settings","Audio")=="HDMI":
        config.set("Settings","Audio","Analogue")
        output_value="1"
    else:
        config.set("Settings","Audio","HDMI")
        output_value="2"
    os.system("amixer cset numid=3 " + output_value)
    write_config_file()
    set_play_mode()
    
def quit_shutdown():
        os.system("sudo halt")

def reboot():
        os.system("sudo reboot")

def exit_prog():
    if sys.platform == "linux2":
        win.destroy()
#=======================================================
# Now we define a menu structure with states and functions to be called.
# The format is:
#   <button text> , <next state>, <action function to be called>
#=======================================================

#This is the array that maps the menu buttons to functions called, and resulting state.        

menu_buttons = [

    #Index 0 - Main Menu
    ["Start",0,start_show],
    ["Settings",SETTINGS_MENU_STATE,settings_menu],
    ["Copy Files From USB/Boot",-1,copy_files_from_usb],
    ["Delete Files",FILES_MENU_STATE,0],
    ["Quit/Shutdown",QUIT_MENU_STATE,0],
    
    #Any lines showing ["",0,0] are padding out the menu to "menu size" items.

    #Index 5 - Settings menu
    ["Autostart Delay",-1,set_auto_start_delay],
    ["Slide Delay",-1,set_slide_delay],
    ["Interactive Show",-1,set_interactive_show],
    ["Set Play Mode",15,set_play_mode],
    ["Back",0,0],

    #Index 10 - File delete menu
    ["Delete All Files",-1,delete_all_files],
    ["Select Files to Delete ",-1,select_files_to_delete],
    ["Back",0,0],
    ["",0,0],
    ["",0,0],
    
    #Index 15 - Play mode menu
    ["Play PPT=",-1,set_play_ppt],
    ["Play Images=",-1,set_play_images],
    ["Play Videos=",-1,set_play_videos],
    ["Audio Output",-1,set_audio_output],
    ["Back",5,0],
    
    #Index 20 - Quit/Exit menu
    ["Shut Down",-1,quit_shutdown],
    ["Reboot",-1,reboot],
    ["Back",0,0],
    ["",0,0],
    ["",0,0],    
]

#=======================================================
#  Now we define a menu button object for making our menu work!
#=======================================================
class MenuButton(object):

    #This variable holds the next menu state.
    next_state=0
    current_state=0
    #Passed in : win=window ref, y is button position
    
    #Initialise a button...
    def __init__(self, win, y):
        #Initialise next state
        self.next_state=0
        self.state=0
        self.function_to_call=0
        #Create a button with the specified parameters.
        self.core = Button(win, height=2, width=22, command=self.button_pressed)
        self.core.pack(pady=3)

    #This function is called when each button is pressed
    def button_pressed(self):
        timeout_obj.timeout=-1

        #Is a handler function defined?
        if self.function_to_call:
            #Call the handler function...
            self.function_to_call()
            #The change state...
            self.current_state=self.next_state
        else:
            if (self.next_state>=0):
                #Populate the new menu...
                populate_menu (self.next_state)

#=======================================================
# Config file handling functions are next.
#
#=======================================================
#Write/save the config file
def write_config_file():
    with open(config_file_name, 'w') as f:
        config.write(f)

#Check/create config file.
def check_config_file():
    
    #Check for a config file and create a default config if none is found.
    if not os.path.isfile(config_file_name):
        config.add_section('Settings')
        config.set('Settings', 'Interactive', 'No')
        config.set('Settings', 'SlideDelay', '6')
        config.set('Settings', 'PlayPPT', 'Yes')
        config.set('Settings', 'PlayVideos', 'Yes')
        config.set('Settings', 'PlayImages', 'Yes')
        config.set('Settings', 'StartDelay', '30')
        config.set('Settings', 'Audio', 'HDMI')

        write_config_file()
    else:
        #Read the file that is found.
        config.read(config_file_name)

#Bind keys to allow easier navigation.
def bind_keys():
    win.bind("<Return>", focus_select)
    win.bind("<Down>", focus_next_window)
    win.bind("<Up>", focus_prev_window)

#Unbind keys when we are not doing menu navigation.
def unbind_nav_keys():
    win.unbind("<Down>")
    win.unbind("<Up>")


#Move button focus and select to the next menu btton and reset the timeout.
def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    timeout_obj.timeout=-1
    return("break")

def focus_prev_window(event):
    event.widget.tk_focusPrev().focus()
    timeout_obj.timeout=-1
    return("break")

#Action whatever was object had focus set
#This function actions whatever button or control was set.
#To do this, it needs to work out what control was pressed (this is a bit of a kludge, as you'll see`)
def focus_select(event):
    global file_listbox
    global waiting_for_yes_no
    timeout_obj.timeout=-1

    #Check if listbox control generated the event
    if (len (event.widget.config())<30):
        #Hide the listbox.
        file_listbox.forget()
        #Set us back to "normal" menu navigation
        bind_keys()
        #Get the items selected
        selection = file_listbox.curselection()
        reslist=list()

        #Go into "wait state"
        waiting_for_yes_no=True
        #Display a message to confirm file deletion. 
        if tkMessageBox.askyesno("Delete Files", "Are you sure you want to delete these files?"):
            #Go through the selection.
            for i in selection:
                item = file_listbox.get(i)
                #Does the file exist?
                if os.path.isfile (item):
                    os.remove(item)
                elif os.path.isdir(item):
                    shutil.rmtree(item)

            waiting_for_yes_no=False

    #Was it one of the menu buttons created the event?
    elif event.widget.config("text")[0] != "textvariable":
        event.widget.invoke();
    else:
        #It must've been the spin box that created the event.
        bind_keys()
        #Spinbox created the event.
        #Get the value from the spinbox
        val_to_set = spin_box_val.get()
        #Hide the spinbox
        spin_box_val.forget()
        spin_label.forget()

        #Write the value to the appropriate config file entry.
        if config_value_to_set=="AutoStart":
            config.set('Settings', 'StartDelay',val_to_set)
        elif config_value_to_set=="SlideDelay":
            config.set('Settings', 'SlideDelay',val_to_set)
        #Save the config file and re-display the menu
        
        write_config_file ()
        settings_menu()
    return("break")


#=======================================================
# This function builds the menu button list and sets all the required object fields in the buttons etc.
#
#=======================================================
def populate_menu(state_num):
    global playmode_label

    #Set the menu title text.
    menu_title = str(menu_names[state_num/MENU_SIZE])
    win.title(menu_title + " - " + str(get_free_space()))
    
    #Set up a message to show what the play mode will be set to.
    msg = "Play PPT: " + config.get('Settings','PlayPPT')+  " - Play Images: " + config.get('Settings','PlayImages')+  " - Play Video: " + config.get('Settings','PlayVideos')
    playmode_label.config(text=msg,foreground="blue")
    playmode_label.pack(side = BOTTOM)

    #Hide objects only used on 1 menu
    file_listbox.forget()
    spin_box_val.forget()
    spin_label.forget()

    #Loop through a portion of the menu table...
    for y in range(MENU_SIZE):
        #Set up the menu button items
        menu_item_index=(state_num) + y
        menu_label = menu_buttons[menu_item_index][0]
        next_state = menu_buttons[menu_item_index][1]
        func_to_call = menu_buttons[menu_item_index][2]

        #Do we need to make the button visible or invisible?
        if menu_label <> "":
            #Set up the various menu button members!
            main_menu_object[y].core.config(text=menu_label)
            main_menu_object[y].next_state=next_state
            main_menu_object[y].function_to_call = func_to_call
            main_menu_object[y].core.pack(pady=3)
        else:
            main_menu_object[y].core.pack_forget()
           
    #Set the focus to be on the first button in the list
    main_menu_object[0].core.focus_set()
    #Set up the navigation keys.
    bind_keys()

#Get the amount of free disk space.
def get_free_space():
    #Get free disk space
    if sys.platform == "linux2":
        #Set up the File System Object
        statvfs = os.statvfs('.')
        #Get the number of KB free in the partition.
        free_space = statvfs.f_frsize * statvfs.f_bavail/1024.0
        mill_count=0
        
        #This is a simply a list to show either Kilobytes, Megabytes or Gigabytes///
        size_desc=[" KB"," MB"," GB"]
        while free_space >= (1024.0):
            mill_count = mill_count + 1
            free_space=free_space/1024

        return "Free space = " + str(int(free_space*10)/10.0) + size_desc[mill_count]
    else:
        return ""


#=======================================================
# This function builds a list of files and puts them in a list box - this is used
# to then select files for deletion.
#=======================================================
def build_file_list (start_dir):

    global file_listbox
    file_listbox.delete(0,END)
    path_list=["PPT","Video","Images"]
    
    for path in path_list:
        for root, dirs, files in os.walk("./media/" + path,followlinks=True):
            for file in files:
                filename=os.path.join(root, file)
                file_listbox.insert(END,filename)
    return file_listbox

#=======================================================   
# Set up main window and kick everything off!
#=======================================================

show_running=False

#Check for any "show_running" temp file and delete it!
if os.path.isfile("show_running.temp"):
    os.remove("show_running.temp")

#Get screen width and height
ws = win.winfo_screenwidth() # width of the screen
hs = win.winfo_screenheight() # height of the screen

#Calculate x and y coordinates for the Tk root window
x = (ws/2) - (win_width/2)
y = (hs/2) - (win_height/2)

#Set the dimensions of the Window and where it is placed
win.geometry('%dx%d+%d+%d' % (win_width, win_height, x, y))


config_value_to_set=""
#Set up navigation buttons
bind_keys()

#Check for and create config file if necessary
check_config_file()
menu_timeout=config.get('Settings', 'StartDelay')

#Create empty array/list to store menu buttons!
main_menu_object = []

#Create Column of buttons - i.e. the menu!.
for y in range(MENU_SIZE):
    main_menu_object.append(MenuButton(win, y) )

#Create label for messages
timeout_label = Label(win, text="Starting in " + str (menu_timeout) +" ...")
timeout_label.pack(side = BOTTOM)

#Create a listbox for later 
file_listbox = Listbox(win,selectmode=MULTIPLE)

#Create a label to show play mode
playmode_label = Label(win)

#Create a spinbox which will be used to set delay values so limit to 60 )
spin_box_val = Spinbox(win, from_=1, to=60)
spin_label = Label(win)


#Call the "set audio output" twice - it's "toggle" so it will set it back.
set_audio_output()
set_audio_output()


#Populate initial menu
populate_menu (MAIN_MENU_STATE)

#Kick off the timer/timeout now...
timeout_obj=TimeOut()



#Set focus on 1st button
main_menu_object[0].core.focus_set()



#Carry on running...
mainloop()
#When we get to here, it means the menu was exited...

#Do GPIO cleanup as required.
if sys.platform == "linux2":
        GPIO.cleanup()
        
#Finish
win.quit()
