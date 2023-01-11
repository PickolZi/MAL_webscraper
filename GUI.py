from customtkinter import CTk, CTkFrame, CTkLabel, CTkRadioButton, StringVar, CTkButton, CTkImage, CTkEntry
from PIL import Image

class GUI(CTk):
    def __init__(self):
        super().__init__()

        # Settings
        self.title("MyAnimeList Webscraper")
        # self.geometry("500x500")

        # Left Column - Anime Categories Frame
        self.anime_categories = ["All Anime", "Top Airing", "Top Upcoming", "Top TV Series", "Top Movies", "Top OVAs", "Top ONAs", "Most Popular", "Most Favorited"]
        self.anime_categories_radio_buttons = RadioButtonFrame(self, header_name="Sort by: ", values=self.anime_categories)
        self.anime_categories_radio_buttons.set_value("All Anime")
        self.anime_categories_radio_buttons.grid(row=0, column=0, padx=10, pady=10)

        # Middle Image
        self.anime_image = CTkImage(Image.open("tikki.png"), size=(425, 425))
        self.anime_image_label = CTkLabel(self, image=self.anime_image, text="")
        self.anime_image_label.grid(row=0, column=1, padx=10, pady=10)
        # TODO: Grab #1 anime image

        # Middle Filename Entry Bar
        self.filename_entry = CTkEntry(self, placeholder_text="filename here...")
        self.filename_entry.grid(row=1, column=1, padx=10, pady=10, sticky="EW")
        # TODO: Get string from entry field and use it to save as xlsx filename.

        # Right Column - Sort data by:
        self.sorting_categories = ["rank", "title", "anime type", "episodes", "release date", "members", "score"]
        self.sorting_categories_radio_buttons = RadioButtonFrame(self, header_name="Sort data by:", values=self.sorting_categories)
        self.sorting_categories_radio_buttons.set_value("rank")
        self.sorting_categories_radio_buttons.grid(row=0, column=2, padx=10, pady=10)

        # Right Column - Generate xlsx file button
        self.generate_xlsx_button = CTkButton(self, text="Generate!")
        self.generate_xlsx_button.grid(row=1, column=2, padx=10, pady=10)
        # TODO: When clicked, grab the information from self.anime_categories_radio_buttons and self.sorting_categories_radio_button
        # TODO: TO generate xlsx file.


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
            self.radio_button.grid(row=index+1, column=0, padx=10, pady=10, sticky="W")

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