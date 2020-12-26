import ctypes
import tkinter as tk

from Controller import *
from PIL import ImageTk, Image
from ScrollableFrame import ScrollableFrame

TITLE_FONT_STYLE = ("David", 20, "bold")
SUBTITLE_FONT_STYLE = ("David", 16, "bold")
TITLE_FONT_COLOR = 'DarkBlue'
BACKGROUND_COLOR = "darkseagreen1"
BUTTON_BACKGROUND_COLOR = "darkseagreen2"
BUTTON_FONT_STYLE = ("David", 12, "bold")

# Popups list
opened_popups = []

controller = Controller()
# Open a custom popup
def popup(title, content, justify="left"):
    for w in opened_popups:
        if w is None:
            opened_popups.remove(w)
        else:
            w.destroy()
            w = None

    win = tk.Toplevel()
    win.wm_title(title)
    win.configure(bg=BACKGROUND_COLOR)

    # Screen size
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Popup size
    popup_width = 700
    popup_height = 400

    # Center the popup
    x_coordinate = int((screen_width / 2) - (popup_width / 2))
    y_coordinate = int((screen_height / 2) - (popup_height / 2))
    win.geometry("{}x{}+{}+{}".format(popup_width, popup_height, x_coordinate, y_coordinate))

    # Title
    new_title(win, title)

    # Content
    tk.Label(win, text=content, bg=BACKGROUND_COLOR, justify=justify).pack()

    opened_popups.append(win)


# Show full screen single picture
def show_full_picture(image_path):
    win = tk.Toplevel()
    win.configure(bg=BACKGROUND_COLOR)
    win.attributes("-fullscreen", True)

    # Menu bar
    menu_bar = tk.Menu(win)
    menu_bar.add_command(label="Close", command=win.destroy)
    win.configure(menu=menu_bar)

    # Screen size
    screen_height = win.winfo_screenheight()
    screen_width = win.winfo_screenwidth()

    inner_frame = tk.Canvas(win, bg=BACKGROUND_COLOR)

    # Image
    img = Image.open(image_path)
    img = img.resize((screen_width, screen_height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    image = tk.Label(inner_frame, image=img)
    image.image = img
    image.grid(row=0, column=0)

    inner_frame.pack(side="top")

# Show multiple pictures
def show_pictures(images_paths, title):
    win = tk.Toplevel()
    win.wm_title("Pictures")
    win.configure(bg=BACKGROUND_COLOR)
    win.attributes("-fullscreen", True)
    frame = tk.Frame(win, bg=BACKGROUND_COLOR)
    new_title(frame, title)
    frame.pack()
    # Menu bar
    menu_bar = tk.Menu(win)
    menu_bar.add_command(label="Close", command=win.destroy)
    win.configure(menu=menu_bar)
    scale = 0.8
    scrollable_frame = ScrollableFrame(win, win.winfo_screenheight()*scale, IMAGE_MAX_SIZE, 3, 30, 30, BACKGROUND_COLOR)
    scrollable_frame.fill_data(images_paths, command_bind_on_click=show_full_picture)



# Initiations
def init_directories():
    if not os.path.isdir(DATA_PATH):
        os.mkdir(DATA_PATH)
    if not os.path.isdir(FACES_PATH):
        os.mkdir(FACES_PATH)
    if not os.path.isdir(CLUSTERS_PATH):
        os.mkdir(CLUSTERS_PATH)
    if not os.path.isdir(CONNECTIONS_PATH):
        os.mkdir(CONNECTIONS_PATH)

# Check if connections file generated
def are_connections_generated():
    if not os.path.isfile(os.path.join(CONNECTIONS_PATH, 'total_connections.json')):
        return False
    return os.path.getsize(os.path.join(CONNECTIONS_PATH, 'total_connections.json')) > 0

# New custom title
def new_title(frame, title):
    tk.Label(frame, text=title, fg=TITLE_FONT_COLOR, font=TITLE_FONT_STYLE, bg=BACKGROUND_COLOR).pack(side="top", fill="x", pady=10)

# New custom sub title
def new_subtitle(frame, subtitle):
    return tk.Label(frame, text=subtitle, fg=TITLE_FONT_COLOR, font=SUBTITLE_FONT_STYLE, bg=BACKGROUND_COLOR)

# New custom button
def new_button(frame, text, command):
    return tk.Button(frame, text=text, command=command, bg=BUTTON_BACKGROUND_COLOR, fg=TITLE_FONT_COLOR, font=BUTTON_FONT_STYLE, activebackground="darkseagreen3")


# Main App
class SocialConnectionsApp(tk.Tk):

    def __init__(self):
        self.tk = tk.Tk()
        self.tk.attributes("-fullscreen", True)
        self.tk.wm_title(APP_NAME)
        self.tk.configure(bg=BACKGROUND_COLOR)

        # Menu bar
        menu_bar = tk.Menu(self)
        menu_bar.add_command(label="Main", command=lambda: self.switch_frame(MainFrame))
        menu_bar.add_command(label="Instructions", command=lambda: self.popup_instructions())
        menu_bar.add_command(label="Contact", command=lambda: self.popup_contact())
        menu_bar.add_command(label="About", command=lambda: self.popup_about())
        menu_bar.add_command(label="Exit", command=self.tk.destroy)
        self.tk.configure(menu=menu_bar)

        self.current_frame = None
        self.switch_frame(MainFrame)

    # Switching frames
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()

    # Popup instructions
    def popup_instructions(self):
        instructions_string = "Follow the next 3 steps:\n\n" \
                              "1.\tPlace pictures in Data directory\n\n" \
                              "2.\tClick 'Generate Connections' and wait until completion\n\n" \
                              "3.\tView the results\n\n" \


        popup("Instructions", instructions_string)

    # Popup contact
    def popup_contact(self):
        contact_string = "Project Members:\n\n" \
                         "\tLiat Cohen\t\tliatico@post.bgu.ac.il\n\n" \
                         "\tAdir Biran\t\tadir.biran@gmail.com\n\n\n\n" \


        popup("Contact", contact_string)

    # Popup about
    def popup_about(self):
        about_string = "This project is made for connections analysis based on pictures dataset.\n\n" \
                       "The project contains 5 main steps:\n\n" \
                       "\t1. Cropping - Cut the faces of the pictures\n\n" \
                       "\t2. Extractor - Extract 128 numeric features for each face\n\n" \
                       "\t3. Classifier - Cluster the faces based on Cosine Similarity\n\n" \
                       "\t4. Connections - Create the connections between the clusters\n\n" \
                       "\t5. Visualization - Draw the graphs and connections\n\n" \
                       "\t6. Controller - Control the request of the UI to the lower layers\n\n" \
                       "\t7. UserInterface - GUI for different user operations\n\n\n\n" \
                       "Programming Languages Principles\n\n" \
                       "December 2020\n\n"

        popup("About", about_string)


# Main frame
class MainFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        # Titles
        new_title(self, APP_NAME)
        new_subtitle(self, "Social analysis based on pictures").pack(side="top")

        inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)

        # Sub titles
        new_subtitle(inner_frame, "Generate Connections").grid(row=0, column=0, padx=100, pady=(100, 0))
        new_subtitle(inner_frame, "View Results").grid(row=0, column=1, padx=100, pady=(100, 0))

        # Explanations
        tk.Label(inner_frame, text="Cut the faces, cluster the faces and generate the social connections", bg=BACKGROUND_COLOR).grid(row=1, column=0, padx=100, pady=50)
        tk.Label(inner_frame, text="View the results of the generated connections", bg=BACKGROUND_COLOR).grid(row=1, column=1, padx=100, pady=50)

        # Buttons
        generate_connections_btn = new_button(inner_frame, "Generate Connections", lambda: master.switch_frame(GenerateConnections))
        generate_connections_btn.grid(row=2, column=0, padx=100)
        results_btn = new_button(inner_frame, "View Results", self.check_generated_connections)
        results_btn.grid(row=2, column=1, padx=100)

        inner_frame.pack(side="top")

    def check_generated_connections(self):
        if are_connections_generated():
            self.master.switch_frame(Results)
        else:
            ctypes.windll.user32.MessageBoxW(0, "No generated connections found", "Error!", 0)


# Generate connections frame
class GenerateConnections(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        # Title
        new_title(self, "Generate Connections")

        inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)

        # Instructions
        new_subtitle(inner_frame, "Instructions").grid(row=0, column=0, sticky="w", pady=(50, 20))
        tk.Label(inner_frame, text="1. Place pictures in project's Data directory", bg=BACKGROUND_COLOR, justify="left").grid(row=1, column=0, sticky="w")
        new_button(inner_frame, "Data Directory", self.open_data_directory).grid(row=2, column=0, pady=(0, 30))
        tk.Label(inner_frame, text="2. Click Generate Connections", bg=BACKGROUND_COLOR, justify="left").grid(row=3, column=0, sticky="w")
        new_button(inner_frame, "Generate Connections", self.generate_connections).grid(row=4, column=0, pady=(0, 30))
        tk.Label(inner_frame, text="3. After generating the connections the results will be shown", bg=BACKGROUND_COLOR, justify="left").grid(row=5, column=0, sticky="w")

        inner_frame.pack(side="top")

    # Open data directory
    def open_data_directory(self):
        os.startfile(DATA_PATH)

    # Generate the connections
    def generate_connections(self):
        if are_connections_generated():
            res = ctypes.windll.user32.MessageBoxW(0, "Connections are already generated.\nDo you want to recluster the data?", "Alert!", 4)

            # 6 for "yes"
            if res == 6:
                controller.clean_data()
                controller.generate_connections()
                self.master.switch_frame(Results)

        else:
            controller.generate_connections()
            self.master.switch_frame(Results)


# Results frame
class Results(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        # Title
        new_title(self, "Results")

        inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)

        # If connections were generated
        if are_connections_generated():
            # Sub titles
            new_subtitle(inner_frame, "Personal Connections Graph").grid(row=0, column=0, padx=50, pady=(100, 0))
            new_subtitle(inner_frame, "Personal Pictures").grid(row=0, column=1, padx=50, pady=(100, 0))
            new_subtitle(inner_frame, "Connection's Pictures").grid(row=0, column=2, padx=50, pady=(100, 0))

            # Explanations
            tk.Label(inner_frame, text="All people with common pictures", bg=BACKGROUND_COLOR).grid(row=1, column=0, padx=50, pady=50)
            tk.Label(inner_frame, text="All pictures of someone", bg=BACKGROUND_COLOR).grid(row=1, column=1, padx=50, pady=50)
            tk.Label(inner_frame, text="All pictures of a connection (between 2 people)", bg=BACKGROUND_COLOR).grid(row=1, column=2, padx=50, pady=50)

            # Buttons
            new_button(inner_frame, "View", self.switch_frame_personal_connections).grid(row=2, column=0, padx=50)
            new_button(inner_frame, "View", self.switch_frame_personal_pictures).grid(row=2, column=1, padx=50)
            new_button(inner_frame, "View", self.switch_frame_connections_pictures).grid(row=2, column=2, padx=50)

        # Connections weren't generated
        else:
            tk.Label(inner_frame, text="Connections haven't generated yet", bg=BACKGROUND_COLOR).pack(side="top", fill="x", pady=10)

        inner_frame.pack(side="top")


    def switch_frame_personal_connections(self):
        self.master.switch_frame(PersonalConnectionsChooseScreen)

    def switch_frame_personal_pictures(self):
        self.master.switch_frame(PersonalPicturesChooseScreen)

    def switch_frame_connections_pictures(self):
        self.master.switch_frame(ConnectionsPictureChooseScreen)


# Personal connections choosing screen
class PersonalConnectionsChooseScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        # Title
        new_title(self, "Personal Connections Graph")





        new_subtitle(self, "Please choose 1 cluster").pack(side="top", fill="x", pady=10)

        controller.load_connections_from_disk()

        # Connections' results
        results = controller.get_results()

        i = 1
        j = 1
        inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        new_button(inner_frame, "Back", lambda: self.master.switch_frame(Results)).grid(row=0, column=1, pady=(0,50))

        # Looping each cluster (face) in the results
        for res in results:
            img_path = os.path.join(FACES_PATH, results[res])
            img = Image.open(img_path)
            img = img.resize((FACE_SIZE, FACE_SIZE), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            face_button = tk.Button(inner_frame, image=img, command=lambda r=res: self.draw_personal_graph(r))
            face_button.image = img
            face_button.grid(row=j, column=i, padx=10, pady=5)

            # 10 clusters per row
            if i % 15 == 0:
                j += 1
                i = 0
            i += 1

        inner_frame.pack(side="top")


    def draw_personal_graph(self, choice):
        controller.draw_personal_graph(choice)

# Personal pictures choosing screen
class PersonalPicturesChooseScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)

        # Title
        new_title(self, "Personal Pictures")



        new_subtitle(self, "Please choose 1 cluster").pack(side="top", fill="x", pady=10)
        controller.load_connections_from_disk()

        # Connections' results
        results = controller.get_results()

        i = 1
        j = 1
        inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        new_button(inner_frame, "Back", lambda: self.master.switch_frame(Results)).grid(row=0, column=1, pady=(0,50))

        # Looping each cluster (face) in the results
        for res in results:
            img_path = os.path.join(FACES_PATH, results[res])
            img = Image.open(img_path)
            img = img.resize((FACE_SIZE, FACE_SIZE), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            face_button = tk.Button(inner_frame, image=img, command=lambda r=res: self.personal_pictures(r))
            face_button.image = img
            face_button.grid(row=j, column=i, padx=10, pady=5)

            # 10 clusters per row
            if i % 15 == 0:
                j += 1
                i = 0
            i += 1

        inner_frame.pack(side="top")


    def personal_pictures(self, choice):
        images_paths = controller.get_all_personal_pictures(choice)

        show_pictures(images_paths, "Personal Pictures")

class ConnectionsPictureChooseScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bg=BACKGROUND_COLOR)
        new_title(self, "Connection's Pictures")

        self.face_buttons = []


        new_subtitle(self, "Please choose 2 cluster").pack(side="top", fill="x", pady=10)
        controller.load_connections_from_disk()

        # Connections' results
        self.results = controller.get_results()

        i = 1
        j = 1
        self.inner_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        new_button(self.inner_frame, "Back", lambda: self.master.switch_frame(Results)).grid(row=0, column=1, pady=(0,50))

        # Looping each cluster (face) in the results
        for res in self.results:
            img_path = os.path.join(FACES_PATH, self.results[res])
            img = Image.open(img_path)
            img = img.resize((FACE_SIZE, FACE_SIZE), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            face_button = tk.Button(self.inner_frame, text=res, image=img, command=lambda r=res: self.first_choice(r))
            face_button.image = img
            face_button.grid(row=j, column=i, padx=10, pady=5)
            self.face_buttons.append(face_button)

            # 10 clusters per row
            if i % 15 == 0:
                j += 1
                i = 0
            i += 1

        self.inner_frame.pack(side="top")

    # First cluster choice
    def first_choice(self, first_choice):
        # Configuring another command after first selection
        for btn in self.face_buttons:
            btn.configure(command=lambda r=btn['text']: self.second_choice(first_choice, r))

    # Second cluster choice
    def second_choice(self, first_choice, second_choice):
        # Getting the connection's pictures
        images_paths = controller.get_pictures_of_connection(first_choice, second_choice)

        # Configuring another command after second selection
        for btn in self.face_buttons:
            btn.configure(command=lambda r=btn['text']: self.first_choice(r))

        if images_paths is None:
            ctypes.windll.user32.MessageBoxW(0, "No common pictures found :(", "Error!", 0)
        else:
            # Showing pictures
            show_pictures(images_paths, "Connection's Pictures")




if __name__ == "__main__":
    init_directories()
    app = SocialConnectionsApp()
    app.mainloop()
