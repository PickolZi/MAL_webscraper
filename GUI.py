from customtkinter import CTk, CTkFrame, CTkLabel, CTkRadioButton, StringVar, CTkButton, CTkImage, CTkEntry
from PIL import Image
from main import *
from urllib.request import urlopen


class GUI(CTk):
    def __init__(self):
        super().__init__()

        # Settings
        self.title("MyAnimeList Webscraper")
        # self.geometry("500x500")

        # Left Column - Anime Categories Frame
        self.anime_categories = ["All Anime", "Top Airing", "Top Upcoming", "Top TV Series", "Top Movies", "Top OVAs",
                                 "Top ONAs", "Most Popular", "Most Favorited"]
        self.anime_categories_radio_buttons = RadioButtonFrame(self, header_name="Sort by: ",
                                                               values=self.anime_categories)
        self.anime_categories_radio_buttons.set_value("All Anime")
        self.anime_categories_radio_buttons.grid(row=0, column=0, padx=10, pady=10)

        # Middle Image
        self.anime_image = CTkImage(Image.open("MAL.png"), size=(425, 425))
        self.anime_image_label = CTkLabel(self, image=self.anime_image, text="")
        self.anime_image_label.grid(row=0, column=1, padx=10, pady=10)
        # TODO: Grab #1 anime image

        # Middle Filename Entry Bar
        self.filename_entry = CTkEntry(self, placeholder_text="filename here...")
        self.filename_entry.grid(row=1, column=1, padx=10, pady=10, sticky="EW")

        # Right Column - Sort data by:
        self.sorting_categories = ["rank", "title", "anime type", "episodes", "release date", "members", "score"]
        self.sorting_categories_radio_buttons = RadioButtonFrame(self, header_name="Sort data by:",
                                                                 values=self.sorting_categories)
        self.sorting_categories_radio_buttons.set_value("rank")
        self.sorting_categories_radio_buttons.grid(row=0, column=2, padx=10, pady=10)

        # Right Column - Generate xlsx file button
        self.generate_xlsx_button = CTkButton(self, text="Generate!", command=self.generate_xlsx_button)
        self.generate_xlsx_button.grid(row=1, column=2, padx=10, pady=10)

    def generate_xlsx_button(self):
        """
        Gathers information from the 2 radio buttons and entry form to create an xlsx file.
        """
        # Grabs the filename from the entry and uses it for the xlsx file.
        filename = self.filename_entry.get() + ".xlsx"
        if filename == ".xlsx":
            filename = "results.xlsx"

        # Uses the anime category radio button to grab the correct link path.
        link_categories = ["", "airing", "upcoming", "tv", "movie", "ova", "ona", "bypopularity", "favorite"]
        index = self.anime_categories.index(self.anime_categories_radio_buttons.get_value())
        link = LINK
        if index != 0:
            link += "?type=" + link_categories[index]

        # Grabs #1 image
        image_link = grab_image_from_google(link)
        image = urlopen(image_link)
        self.anime_image_label.configure(image=CTkImage(Image.open(image), size=(425, 425)))

        # Decides how to sort the data.
        pass

        # Downloads anime data and saves as xlsx file.
        animes = retrieve_data(link)
        save_to_excel(animes)


class RadioButtonFrame(CTkFrame):
    """
    Class is used to create a frame filled with radio buttons given header_name as the label, and values as a list of
    options to be used for the radio buttons.
    """

    def __init__(self, *args, header_name, values, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_name = header_name
        self.values = values

        self.header = CTkLabel(self, text=self.header_name)
        self.header.grid(row=0, column=0, padx=10, pady=10)

        self.radio_button_var = StringVar()

        # Creating radio buttons
        for index, value in enumerate(values):
            self.radio_button = CTkRadioButton(self, text=value, value=value, variable=self.radio_button_var)
            self.radio_button.grid(row=index + 1, column=0, padx=10, pady=10, sticky="W")

    def get_value(self):
        """
        :return: radio button value.
        """
        return self.radio_button_var.get()

    def set_value(self, value):
        """
        :param value: Sets the radio button value
        """
        self.radio_button_var.set(value)


if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()
