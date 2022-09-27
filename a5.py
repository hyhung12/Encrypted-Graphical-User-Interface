# NAME Hung Nguyen
# EMAIL hunghn4@uci.edu
# STUDENT ID 26441523
#
# a5.py
# 
# ICS 32 
#
# v0.4
# 
# The following module provides a graphical user interface shell for the DSP journaling program.


import tkinter as tk
from tkinter import ttk, filedialog
from Profile import Post
from NaClProfile import NaClProfile
from copy import deepcopy
import ds_client
import ds_protocol
USERNAME = 'a5ok'
PASSWORD = '12'
PORT = 3021
HOST = "168.235.86.101"

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback

        # a list of the Post objects available in the active DSU file
        self._posts = [Post]
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    
    """
    Update the entry_editor with the full post entry when the corresponding node in the posts_tree
    is selected.
    """
    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._posts[index].entry
        self.set_text_entry(entry)
    
    """
    Returns the text that is currently displayed in the entry_editor widget.
    """
    def get_text_entry(self) -> str:
        return self.entry_editor.get('1.0', 'end').rstrip()

    """
    Sets the text to be displayed in the entry_editor widget.
    NOTE: This method is useful for clearing the widget, just pass an empty string.
    """
    def set_text_entry(self, text:str):
        self.entry_editor.delete(0.0, 'end')
        self.entry_editor.insert('0.0', text)
        
    """
    Populates the self._posts attribute with posts from the active DSU file.
    """
    def set_posts(self, posts:list):
        # populate self._posts with the post data passed
        # in the posts parameter and repopulate the UI with the new post entries.
        self._posts = posts
        for idx, post in enumerate(self._posts):
            self._insert_post_tree(idx, post)
            
    """
    Inserts a single post to the post_tree widget.
    """
    def insert_post(self, post: Post):
        self._posts.append(post)
        id = len(self._posts) - 1 #adjust id for 0-base of treeview widget
        self._insert_post_tree(id, post)

    """
    Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
    as when a new DSU file is loaded, for example.
    """
    def reset_ui(self):
        self.set_text_entry("")
        self.entry_editor.configure(state=tk.NORMAL)
        self._posts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    """
    Inserts a post entry into the posts_tree widget.
    """
    def _insert_post_tree(self, idx, post: Post):
        entry = post.entry
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widget.
        if len(entry) > 25:
            entry = entry[:24] + "..."
        
        self.posts_tree.insert('', idx, idx, text=entry)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        
        self.entry_editor = tk.Text(editor_frame, width=0)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""
class Footer(tk.Frame):
    def __init__(self, root, save_callback=None, online_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._online_callback = online_callback
        # IntVar is a variable class that provides access to special variables
        # for Tkinter widgets. is_online is used to hold the state of the chk_button widget.
        # The value assigned to is_online when the chk_button widget is changed by the user
        # can be retrieved using the get() function:
        # chk_value = self.is_online.get()
        self.is_online = tk.IntVar()
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()
    
    """
    Calls the callback function specified in the online_callback class attribute, if
    available, when the chk_button widget has been clicked.
    """
    def online_click(self):
        if self.is_online is not None:
            self._online_callback(self.is_online.get())

    """
    Calls the callback function specified in the save_callback class attribute, if
    available, when the save_button has been clicked.
    """
    def save_click(self):
        if self._save_callback is not None:
            self._save_callback()

    """
    Updates the text that is displayed in the footer_label widget
    """
    def set_status(self, message):
        self.footer_label.configure(text=message)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        save_button = tk.Button(master=self, text="Save Post", width=20)
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.chk_button = tk.Checkbutton(master=self, text="Online", variable=self.is_online)
        self.chk_button.configure(command=self.online_click) 
        self.chk_button.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the main portion of the root frame. Also manages all method calls for
the NaClProfile class.
"""
class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._profile_filename = None

        # Initialize a new NaClProfile and assign it to a class attribute.
        self._current_profile = NaClProfile()
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    """
    Creates a new DSU file when the 'New' menu item is clicked.
    """
    def new_profile(self):
        self.body.reset_ui()
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        if filename is not None:
            self._profile_filename = filename.name
            # Generate a keypair
            self._current_profile.generate_keypair()
            # Remove all existing posts before creating a new profile
            while len(self._current_profile._posts) > 0:
                self._current_profile._posts.pop()
            
    """
    Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
    data into the UI.
    """
    def open_profile(self):
        self.body.reset_ui()
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        if filename is not None:
        
            # load a profile, import encryption keys and update the UI with posts.
            self._profile_filename = filename.name
            self._current_profile.load_profile(self._profile_filename)
            self._current_profile.import_keypair(self._current_profile.keypair)
            try:
                self.body.set_posts(self._current_profile.get_posts())
            except:
                print('ERROR!!Something went wrong. Unable to retrieve the posts in this dsu file')
        
    """
    Closes the program when the 'Close' menu item is clicked.
    """
    def close(self):
        self.root.destroy()
        
    """
    Join the server with ds_client.sent() to get the server's public key
    Then encrypt the post with encrypt_entry() and send it to the DS server
    """
    def publish(self, post:Post):
        msg = post.entry
        server = self._current_profile.dsuserver 
        port = 3021
        username = self._current_profile.username
        password = self._current_profile.password
        p_key = self._current_profile.public_key
        
        token, conn_obj = ds_client.send(server, port, username, password, p_key)
        # Remove the comment to send post to the server with hardcored username,password
        #token, conn_obj = ds_client.send(HOST, PORT, USERNAME, PASSWORD, self._current_profile.public_key)
        if token is not None:
            encrypted_msg = self._current_profile.encrypt_entry(msg, token)
            resp_msg = ds_protocol.post(conn_obj, self._current_profile.public_key, encrypted_msg)
            if not (ds_protocol.ok(resp_msg) and (not ds_protocol.error(resp_msg))):
                print('ERROR!! Cannot send this post to the DS Server')
                return False
            return True
        else:
            print('ERROR!! One of the user input is not correct. Unable to connect to the DS Server')
            return False
            
          
    """
    Saves the text currently in the entry_editor widget to the active DSU file.
    """
    def save_profile(self):     
        post = Post(self.body.get_text_entry())
        
        if self.footer.is_online.get() == 1:
                publish_ok = self.publish(post)
                if publish_ok:
                    self.save_all(post)
        else:
            self.save_all(post)
                    
    """
    Saves the post the profile and insert it to the post tree
    """  
    def save_all(self, post):
        copy_of_post = deepcopy(post)                                  
        try:
            self._current_profile.add_post(post)
            self._current_profile.save_profile(self._profile_filename)
        except:
            print('ERROR!! Cannot save this post')
        else:
            self.body.insert_post(copy_of_post)
           
        self.body.set_text_entry("")    

    """
    A callback function for responding to changes to the online chk_button.
    """
    def online_changed(self, value):        
        if value == 1:
            self.footer.set_status("Online")
            
        else:
            self.footer.set_status("Offline")
            
    """
    A callback function for responding to save the input bio and display it
    when "Update bio" is clicked again
    """            
    def update_bio(self):
        self._current_profile.bio = self.bio_window.get_bio()
        if self._profile_filename is not None:
            self._current_profile.save_profile(self._profile_filename)
        self.bio_window.destroy()
        
    """
    A callback function for responding to save the user inputs(server address, username, password)
    and display them when "Configure DS Server" is clicked again
    """ 
    def save_info(self):
        self._current_profile.dsuserver  = self.config_account_window.get_server_address()
        self._current_profile.username = self.config_account_window.get_user_name()
        self._current_profile.password = self.config_account_window.get_pass_word() 
        if self._profile_filename is not None:
            self._current_profile.save_profile(self._profile_filename) 
        self.config_account_window.destroy()    
            
    """
    Create a window to display the previously saved bio
    in the profile and update the new input bio.
    """             
    def prompt_bio(self):
        self.bio_window = Window(self.root, ui_option=1, bio_callback=self.update_bio)
        self._current_profile.bio = self._current_profile.bio or ""
        self.bio_window.input_bio.insert('0.0', self._current_profile.bio)

    """
    Create a window to display the previously saved information(dsuserver, usn, pwd) in
    the profile and update the new user inputs
    """       
    def configure_account(self):
        self.config_account_window = Window(self.root, ui_option=2, save_info_callback=self.save_info)
        # Check if the profile's attributes are None, 
        # if true then set them to empty string to avoid error
        self._current_profile.dsuserver = self._current_profile.dsuserver or ""
        self._current_profile.username = self._current_profile.username or ""
        self._current_profile.password = self._current_profile.password or ""
        # Update the value
        self.config_account_window.server_entry.insert('0.0', self._current_profile.dsuserver)
        self.config_account_window.usn_entry.insert('0.0', self._current_profile.username)
        self.config_account_window.pwd_entry.insert('0.0', self._current_profile.password)
             
    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)

        menu_settings = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_settings, label='Settings')
        menu_settings.add_command(label='Update Bio', command=self.prompt_bio)
        menu_settings.add_command(label='Configure DS Server', command=self.configure_account)

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        self.footer = Footer(self.root, save_callback=self.save_profile, online_callback=self.online_changed)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)
        
"""
A subclass of tk.Toplevel that is responsible for drawing all of the widgets
in the menu portion of the root frame.
"""        
class Window(tk.Toplevel):
    def __init__(self, root, ui_option=None, bio_callback=None, save_info_callback=None):
        tk.Toplevel.__init__(self, root)
        self.root = root
        # Profile attributes (bio, dsuserver, username, password)
        self._bio = None       
        self._server_address = ""
        self._usn = ""
        self._pwd = ""
        self._bio_callback = bio_callback
        self._save_info_callback = save_info_callback
        
        if ui_option == 1:
            self._draw_biowindow()
        elif ui_option == 2:
            self._draw_configwindow()
            
    """
    Collect the bio, dsuserver, username and password from the input entries
    """    
    def get_bio(self):
        self._bio = self.input_bio.get('1.0', 'end').rstrip()  
        return self._bio
     
    def get_server_address(self):
        self._server_address = self.server_entry.get('1.0', 'end').rstrip()
        return self._server_address 
    
    def get_user_name(self):
        self._usn = self.usn_entry.get('1.0', 'end').rstrip()
        return self._usn
        
    def get_pass_word(self):
        self._pwd = self.pwd_entry.get('1.0', 'end').rstrip()
        return self._pwd
    
    """
    Call the callback function specified in the save_info_callback class attribute, if
    available, when the input_update_button widget has been clicked.
    """    
    def save_info_click(self):
        if self._save_info_callback is not None:
            self._save_info_callback()
            
    """
    Call the callback function specified in the save_info_callback class attribute, if
    available, when the config_account_connect_button widget has been clicked.
    """             
    def update_click(self):
        if self._bio_callback is not None:
            self._bio_callback()
                      
    """
    Call only once upon initialization to add widgets to the menu
    """    
    def _draw_biowindow(self):
        self.geometry('400x100')
        self.title('Input Bio')
        
        self.input_label = tk.Label(master = self, text = 'How would you like to update your bio?')
        self.input_label.pack()  
        self.input_bio = tk.Text(master = self, width=15, height=1)
        self.input_bio.pack()
        
        self.input_update_button = tk.Button(master = self, text = 'OK', width=8)
        self.input_update_button.configure(command=self.update_click)
        self.input_update_button.pack(side='left', anchor='ne', padx=8, pady=10, expand=True)
        
        self.input_cancel_button = tk.Button(master = self, text = 'Cancel',width=8)
        self.input_cancel_button.configure(command=self.destroy)
        self.input_cancel_button.pack(side='right', anchor='nw', padx=8, pady=10, expand=True)

    def _draw_configwindow(self):
        self.geometry('400x180')
        self.title('Configure Account')
        
        self.server_label = tk.Label(master = self, text = 'DS Server Address')
        self.server_label.pack()
        self.server_entry = tk.Text(master = self, width=15, height=1)
        self.server_entry.pack()
        
        self.usn_label = tk.Label(master = self, text = 'Username')
        self.usn_label.pack()
        self.usn_entry = tk.Text(master = self, width=15, height=1)
        self.usn_entry.pack()
            
        self.pwd_label = tk.Label(master = self, text = 'Password')
        self.pwd_label.pack()
        self.pwd_entry = tk.Text(master = self, width=15, height=1)
        self.pwd_entry.pack()

        self.config_account_save_button = tk.Button(master = self, text = 'Save', width=8)
        self.config_account_save_button.configure(command=self.save_info_click)
        self.config_account_save_button.pack(side='left', anchor='ne', padx=8, pady=10, expand=True)
        
        self.config_account_cancel_button = tk.Button(master = self, text = 'Cancel',width=8)
        self.config_account_cancel_button.configure(command=self.destroy)
        self.config_account_cancel_button.pack(side='right', anchor='nw', padx=8, pady=10, expand=True)    


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Demo")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()