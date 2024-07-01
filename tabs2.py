import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from CTkToolTip import *
from customtkinter import *
from PIL import Image
import threading
import time
import datetime
import json
import pygame
import re
import pyttsx3


class BellSystemApp:
    def __init__(self, master):
        self.master = master
        self.master.minsize(600, 600)
        self.master.geometry("1000x600+400+200")
        self.master.wm_attributes("-fullscreen")

        # Load other data from JSON file
        self.other_data = self.load_other_data()
        self.set_window_size()

        self.master.title("Bell System")
        self.master.attributes("-transparentcolor", "magenta")
        self.master.attributes("-alpha", 1)
        ctk.set_default_color_theme("Assets/Themes/blue.json")

        self.get_images()

        # set the initial column length to 0
        self.column_length = 3

        self.col = 0
        self.row = 0

        # set the all breakpoint variables to false
        self.first_breakpoint = self.second_breakpoint = self.third_breakpoint = False

        # Load button names from JSON file
        self.button_names = self.load_button_names()

        # set theme
        self.set_theme_mode()

        # Taking all files names to a variable
        self.data1 = "Assets/json/data1.json"
        self.data2 = "Assets/json/data2.json"
        self.data3 = "Assets/json/data3.json"
        self.data4 = "Assets/json/data4.json"
        self.data5 = "Assets/json/data5.json"
        self.data6 = "Assets/json/data6.json"

        # Flag to signal the thread to stop
        self.stop_thread = False

        # Start background thread
        self.start_threading()

        # Load all alarm data to its List
        self.alarms1 = self.load_alarms(self.data1)
        self.alarms2 = self.load_alarms(self.data2)
        self.alarms3 = self.load_alarms(self.data3)
        self.alarms4 = self.load_alarms(self.data4)
        self.alarms5 = self.load_alarms(self.data5)
        self.alarms6 = self.load_alarms(self.data6)

        # create all widgets
        self.create_widgets()

    def get_images(self):
        # get all images
        self.dark_bell_image = Image.open("Assets/Images/dark_mode_bell2.png")
        self.light_bell_image = Image.open("Assets/Images/light_mode_bell2.png")
        self.dark_announce_image = Image.open(
            "Assets/Images/dark_mode_announcement.png"
        )
        self.light_announce_image = Image.open(
            "Assets/Images/light_mode_announcement.png"
        )
        self.dark_setting_image = Image.open("Assets/Images/dark_mode_setting.png")
        self.light_setting_image = Image.open("Assets/Images/light_mode_setting.png")
        self.light_mode_edit = Image.open("Assets/Images/light_mode_edit.png")
        self.dark_mode_edit = Image.open("Assets/Images/dark_mode_edit.png")
        self.light_mode_delete = Image.open("Assets/Images/light_mode_delete.png")
        self.dark_mode_delete = Image.open("Assets/Images/dark_mode_delete.png")
        self.dark_mode_cross = Image.open("Assets/Images/dark_mode_cross.png")
        self.light_mode_cross = Image.open("Assets/Images/light_mode_cross.png")
        self.dark_mode_label = Image.open("Assets/Images/dark_mode_label.png")
        self.light_mode_label = Image.open("Assets/Images/light_mode_label.png")
        self.save_icon = Image.open("Assets/Images/save_icon.png")

        self.play_icon = Image.open("Assets/Images/play_icon_1.png")

        self.dark_mode_arrow_up = Image.open("Assets/Images/dark_mode_arrow_up.png")
        self.light_mode_arrow_up = Image.open("Assets/Images/light_mode_arrow_up.png")
        self.dark_mode_arrow_down = Image.open("Assets/Images/dark_mode_arrow_down.png")
        self.light_mode_arrow_down = Image.open(
            "Assets/Images/light_mode_arrow_down.png"
        )

        self.dark_mode_music_icon = Image.open("Assets/Images/dark_mode_music_icon.png")
        self.light_mode_music_icon = Image.open(
            "Assets/Images/light_mode_music_icon.png"
        )

    def frame_resize(self, event, scrol_frame, alarm, data):
        # get the current width of the frame
        current_width = event.width

        # check the width of the frame
        # if 0 <= current_width < 500 and not self.first_breakpoint:
        #     self.first_breakpoint = True
        #     self.second_breakpoint = self.third_breakpoint = False
        #     self.column_length = 1
        #     self.arrange_elements(scrol_frame)
        #     self.button1.configure(width=200)

        # elif 500 <= current_width < 1000 and not self.second_breakpoint:
        #     self.second_breakpoint = True
        #     self.first_breakpoint = self.third_breakpoint = False
        #     self.column_length = 2
        #     self.arrange_elements(scrol_frame)
        #     # self.button1.configure(width=200)

        # elif 1000 <= current_width < 1500 and not self.third_breakpoint:
        #     self.third_breakpoint = True
        #     self.first_breakpoint = self.second_breakpoint = False
        #     self.column_length = 3
        #     self.arrange_elements(scrol_frame)
        #     self.button1.configure(width=300)

        # elif 1500 <= current_width < 2000 and not self.third_breakpoint:
        #     self.third_breakpoint = True
        #     self.first_breakpoint = self.second_breakpoint = False
        #     self.column_length = 4
        #     self.arrange_elements(scrol_frame)
        # self.button1.configure(width=300)

        # print(self.master.wm_attributes("-fullscreen"))
        # elif not self.master.wm_attributes("-fullscreen"):
        #     pass
        # else:
        #     self.button1.configure(width=300)
        #     print("hi")

    def arrange_elements(self, scrol_frame):
        row = col = 0
        for widget in scrol_frame.winfo_children():
            if col == self.column_length:
                col = 0
                row += 1
                self.col = 0
                self.row += 1

            widget.grid(row=row, column=col)

            col += 1
            self.col += 1

        for c in range(self.column_length):
            scrol_frame.columnconfigure(c, weight=1)

    def set_window_size(self):
        try:
            self.width = self.other_data["width"]
        except KeyError:
            self.width = 800

        try:
            self.height = self.other_data["height"]
        except KeyError:
            self.height = 600

        try:
            self.x = self.other_data["x"]
        except KeyError:
            self.height = 400

        try:
            self.y = self.other_data["y"]
        except KeyError:
            self.height = 250

        self.master.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")

    def set_theme_mode(self):
        try:
            if self.other_data["theme"] == 0:
                ctk.set_appearance_mode("light")
            elif self.other_data["theme"] == 1:
                ctk.set_appearance_mode("dark")
            elif self.other_data["theme"] == 2:
                ctk.set_appearance_mode("system")
        except KeyError:
            self.other_data["theme"] = 2

        self.save_other_data()

    def create_widgets(self):
        # Main Frame
        self.main_frame = ctk.CTkFrame(self.master, fg_color="transparent")

        # Left Frame
        self.left_frame = ctk.CTkFrame(
            self.main_frame, fg_color="transparent", width=600
        )
        self.create_buttons_for_left_frame(self.left_frame)
        self.left_frame.pack(side="left", fill="y")

        # Right Frame
        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.create_frames_for_right_frame(self.right_frame)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.main_frame.pack(fill="both", expand=True)

    def create_frames_for_right_frame(self, right_frame):
        self.frame1 = ctk.CTkFrame(right_frame, fg_color="transparent")
        self.scrol_frame1 = ctk.CTkScrollableFrame(
            self.frame1, corner_radius=0, fg_color="transparent"
        )
        # giving frame a frame_resize function
        # self.frame1.bind(
        #     "<Configure>",
        #     lambda event: self.frame_resize(
        #         event, self.scrol_frame1, self.alarms1, self.data1
        #     ),
        # )
        self.frame1.update_idletasks()

        self.frame2 = ctk.CTkFrame(right_frame, fg_color="transparent")
        self.scrol_frame2 = ctk.CTkScrollableFrame(
            self.frame2, corner_radius=0, fg_color="transparent"
        )  # giving frame a frame_resize function
        # self.frame2.bind(
        #     "<Configure>",
        #     lambda event: self.frame_resize(
        #         event, self.scrol_frame2, self.alarms2, self.data2
        #     ),
        # )
        self.frame2.update_idletasks()

        self.frame3 = ctk.CTkFrame(right_frame, fg_color="transparent")
        self.scrol_frame3 = ctk.CTkScrollableFrame(
            self.frame3, corner_radius=0, fg_color="transparent"
        )  # giving frame a frame_resize function
        # self.frame3.bind(
        #     "<Configure>",
        #     lambda event: self.frame_resize(
        #         event, self.scrol_frame3, self.alarms3, self.data3
        #     ),
        # )
        self.frame3.update_idletasks()

        self.frame4 = ctk.CTkFrame(right_frame, fg_color="transparent")
        self.scrol_frame4 = ctk.CTkScrollableFrame(
            self.frame4, corner_radius=0, fg_color="transparent"
        )  # giving frame a frame_resize function
        # self.frame4.bind(
        #     "<Configure>",
        #     lambda event: self.frame_resize(
        #         event, self.scrol_frame4, self.alarms4, self.data4
        #     ),
        # )
        self.frame4.update_idletasks()

        self.frame5 = ctk.CTkFrame(right_frame, fg_color="transparent")
        self.scrol_frame5 = ctk.CTkScrollableFrame(
            self.frame5, corner_radius=0, fg_color="transparent"
        )  # giving frame a frame_resize function
        # self.frame5.bind(
        #     "<Configure>",
        #     lambda event: self.frame_resize(
        #         event, self.scrol_frame5, self.alarms5, self.data5
        #     ),
        # )
        self.frame5.update_idletasks()

        self.frame6 = ctk.CTkFrame(right_frame, fg_color="transparent")
        self.scrol_frame6 = ctk.CTkScrollableFrame(
            self.frame6, corner_radius=0, fg_color="transparent"
        )  # giving frame a frame_resize function
        # self.frame6.bind(
        #     "<Configure>",
        #     lambda event: self.frame_resize(
        #         event, self.scrol_frame6, self.alarms6, self.data6
        #     ),
        # )
        self.frame6.update_idletasks()

        self.create_setting_page_widgets()
        self.create_Announcement_page_widgets()

        self.display_alarms(self.scrol_frame1, self.alarms1, self.data1)
        self.display_alarms(self.scrol_frame2, self.alarms2, self.data2)
        self.display_alarms(self.scrol_frame3, self.alarms3, self.data3)
        self.display_alarms(self.scrol_frame4, self.alarms4, self.data4)
        self.display_alarms(self.scrol_frame5, self.alarms5, self.data5)
        self.display_alarms(self.scrol_frame6, self.alarms6, self.data6)

        def pack():
            self.scrol_frame1.pack(expand=True, fill="both")
            self.scrol_frame2.pack(expand=True, fill="both")
            self.scrol_frame3.pack(expand=True, fill="both")
            self.scrol_frame4.pack(expand=True, fill="both")
            self.scrol_frame5.pack(expand=True, fill="both")
            self.scrol_frame6.pack(expand=True, fill="both")
            self.frame1.pack(expand=True, fill="both")

        pack()
        self.create_buttons_for_right_frame_frames()

    def open_frame(self, button, frame):
        self.button1.configure(fg_color="transparent")
        self.button2.configure(fg_color="transparent")
        self.button3.configure(fg_color="transparent")
        self.button4.configure(fg_color="transparent")
        self.button5.configure(fg_color="transparent")
        self.button6.configure(fg_color="transparent")

        self.settings_button.configure(fg_color="transparent")

        self.announcement_button1.configure(fg_color="transparent")

        self.frame1.forget()
        self.frame2.forget()
        self.frame3.forget()
        self.frame4.forget()
        self.frame5.forget()
        self.frame6.forget()

        self.settings_frame.forget()

        self.announcement_frame.forget()

        frame.pack(expand=True, fill="both")
        button.configure(fg_color="royalblue")

    def create_buttons_for_right_frame_frames(self):
        buttonframe = ctk.CTkFrame(self.frame1, corner_radius=0)
        buttonframe.place(relx=0.94, rely=0.94, anchor="se")
        btn = ctk.CTkButton(
            buttonframe,
            text="+",
            width=50,
            height=50,
            font=("arial", 40),
            command=lambda: self.open_add_alarm_window(
                self.scrol_frame1, self.alarms1, self.data1
            ),
        )
        btn.pack(ipadx=5, ipady=5)

        buttonframe = ctk.CTkFrame(self.frame2, corner_radius=0)
        buttonframe.place(relx=0.94, rely=0.94, anchor="se")
        btn = ctk.CTkButton(
            buttonframe,
            text="+",
            width=50,
            height=50,
            font=("arial", 40),
            command=lambda: self.open_add_alarm_window(
                self.scrol_frame2, self.alarms2, self.data2
            ),
        )
        btn.pack(ipadx=5, ipady=5)

        buttonframe = ctk.CTkFrame(self.frame3, corner_radius=0)
        buttonframe.place(relx=0.94, rely=0.94, anchor="se")
        btn = ctk.CTkButton(
            buttonframe,
            text="+",
            width=50,
            height=50,
            font=("arial", 40),
            command=lambda: self.open_add_alarm_window(
                self.scrol_frame3, self.alarms3, self.data3
            ),
        )
        btn.pack(ipadx=5, ipady=5)

        buttonframe = ctk.CTkFrame(self.frame4, corner_radius=0)
        buttonframe.place(relx=0.94, rely=0.94, anchor="se")
        btn = ctk.CTkButton(
            buttonframe,
            text="+",
            width=50,
            height=50,
            font=("arial", 40),
            command=lambda: self.open_add_alarm_window(
                self.scrol_frame4, self.alarms4, self.data4
            ),
        )
        btn.pack(ipadx=5, ipady=5)

        buttonframe = ctk.CTkFrame(self.frame5, corner_radius=0)
        buttonframe.place(relx=0.94, rely=0.94, anchor="se")
        btn = ctk.CTkButton(
            buttonframe,
            text="+",
            width=50,
            height=50,
            font=("arial", 40),
            command=lambda: self.open_add_alarm_window(
                self.scrol_frame5, self.alarms5, self.data5
            ),
        )
        btn.pack(ipadx=5, ipady=5)

        buttonframe = ctk.CTkFrame(self.frame6, corner_radius=0)
        buttonframe.place(relx=0.94, rely=0.94, anchor="se")
        btn = ctk.CTkButton(
            buttonframe,
            text="+",
            width=50,
            height=50,
            font=("arial", 40),
            command=lambda: self.open_add_alarm_window(
                self.scrol_frame6, self.alarms6, self.data6
            ),
        )
        btn.pack(ipadx=5, ipady=5)

    def create_buttons_for_left_frame(self, left_frame):
        # ==========================Bell Buttons===============================
        self.button1 = ctk.CTkButton(
            self.left_frame,
            text=self.button_names["1"],
            text_color=("black", "white"),
            fg_color="royalblue",
            font=("Arial", 17),
            width=300,
            anchor="w",
            image=CTkImage(
                dark_image=self.dark_bell_image, light_image=self.light_bell_image
            ),
            command=lambda: self.open_frame(self.button1, self.frame1),
        )
        self.button1.pack(fill="x", padx=10, ipady=5, pady=1)
        self.button1.bind(
            "<Double-Button-1>",
            lambda event, btn=self.button1, idx=1: self.rename_button(
                btn,
                idx,
            ),
        ),

        self.button2 = ctk.CTkButton(
            self.left_frame,
            text=self.button_names["2"],
            text_color=("black", "white"),
            fg_color="transparent",
            font=("Arial", 17),
            anchor="w",
            image=CTkImage(
                dark_image=self.dark_bell_image, light_image=self.light_bell_image
            ),
            command=lambda: self.open_frame(self.button2, self.frame2),
        )
        self.button2.pack(fill="x", padx=10, ipady=5, pady=1)
        self.button2.bind(
            "<Double-Button-1>",
            lambda event, btn=self.button2, idx=2: self.rename_button(
                btn,
                idx,
            ),
        ),
        self.button3 = ctk.CTkButton(
            self.left_frame,
            text=self.button_names["3"],
            text_color=("black", "white"),
            fg_color="transparent",
            anchor="w",
            font=("Arial", 17),
            image=CTkImage(
                dark_image=self.dark_bell_image, light_image=self.light_bell_image
            ),
            command=lambda: self.open_frame(self.button3, self.frame3),
        )
        self.button3.pack(fill="x", padx=10, ipady=5, pady=1)
        self.button3.bind(
            "<Double-Button-1>",
            lambda event, btn=self.button3, idx=3: self.rename_button(
                btn,
                idx,
            ),
        ),
        self.button4 = ctk.CTkButton(
            self.left_frame,
            text=self.button_names["4"],
            text_color=("black", "white"),
            fg_color="transparent",
            anchor="w",
            font=("Arial", 17),
            image=CTkImage(
                dark_image=self.dark_bell_image, light_image=self.light_bell_image
            ),
            command=lambda: self.open_frame(self.button4, self.frame4),
        )
        self.button4.pack(fill="x", padx=10, ipady=5, pady=1)
        self.button4.bind(
            "<Double-Button-1>",
            lambda event, btn=self.button4, idx=4: self.rename_button(
                btn,
                idx,
            ),
        ),
        self.button5 = ctk.CTkButton(
            self.left_frame,
            text=self.button_names["5"],
            text_color=("black", "white"),
            fg_color="transparent",
            anchor="w",
            font=("Arial", 17),
            image=CTkImage(
                dark_image=self.dark_bell_image, light_image=self.light_bell_image
            ),
            command=lambda: self.open_frame(self.button5, self.frame5),
        )
        self.button5.pack(fill="x", padx=10, ipady=5, pady=1)
        self.button5.bind(
            "<Double-Button-1>",
            lambda event, btn=self.button5, idx=5: self.rename_button(
                btn,
                idx,
            ),
        ),
        self.button6 = ctk.CTkButton(
            self.left_frame,
            text=self.button_names["6"],
            text_color=("black", "white"),
            fg_color="transparent",
            anchor="w",
            font=("Arial", 17),
            image=CTkImage(
                dark_image=self.dark_bell_image, light_image=self.light_bell_image
            ),
            command=lambda: self.open_frame(self.button6, self.frame6),
        )
        self.button6.pack(fill="x", padx=10, ipady=5, pady=1)
        self.button6.bind(
            "<Double-Button-1>",
            lambda event, btn=self.button6, idx=6: self.rename_button(
                btn,
                idx,
            ),
        ),
        # ==========================Bell Buttons===============================
        # ==========================Announcement Buttons===============================
        self.announcement_button1 = ctk.CTkButton(
            self.left_frame,
            text="Announcement",
            text_color=("black", "white"),
            font=("Arial", 17),
            anchor="w",
            # hover_color="#8B8B8B",
            fg_color="transparent",
            image=CTkImage(
                dark_image=self.dark_announce_image,
                light_image=self.light_announce_image,
            ),
            command=lambda: self.open_frame(
                self.announcement_button1, self.announcement_frame
            ),
        )
        self.announcement_button1.pack(fill="x", padx=10, ipady=5, pady=1)
        # ==========================Announcement Buttons===============================
        # ==========================Settings Buttons===============================
        self.settings_button = ctk.CTkButton(
            self.left_frame,
            text="Settings",
            font=("Arial", 17),
            anchor="w",
            fg_color="transparent",
            text_color=("black", "white"),
            # hover_color="#8B8B8B",
            image=CTkImage(
                dark_image=self.dark_setting_image, light_image=self.light_setting_image
            ),
            command=lambda: self.open_frame(self.settings_button, self.settings_frame),
        )
        self.settings_button.pack(side="bottom", fill="x", padx=10, ipady=5, pady=1)
        # ==========================Settings Buttons===============================

    def create_Announcement_page_widgets(self):
        engine = pyttsx3.init("sapi5")

        self.announcement_frame = ctk.CTkFrame(self.right_frame)
        self.scrol_announcement_frame = ctk.CTkScrollableFrame(
            self.announcement_frame, corner_radius=0
        )
        self.announcement_frame.update_idletasks()
        # label
        self.announcement_label = ctk.CTkLabel(
            self.scrol_announcement_frame,
            text="Announcement",
            font=("arial", 40, "bold"),
        )
        self.announcement_label.pack(anchor="w", padx=20, pady=20)
        # -----------------------------------------------------------------

        # btn and textbox frame
        btn_and_textbox_frame = ctk.CTkFrame(
            self.scrol_announcement_frame, fg_color="transparent"
        )
        btn_and_textbox_frame.pack(expand=True, fill="both")

        btn_frame = ctk.CTkFrame(btn_and_textbox_frame, fg_color="transparent")
        btn_frame.pack(fill="y", side="right")

        playbtn = ctk.CTkButton(
            btn_frame,
            text="",
            fg_color="transparent",
            corner_radius=60,
            width=50,
            font=("arial", 20),
            border_width=2,
            border_color="#1F6AA5",
            image=CTkImage(light_image=self.play_icon, dark_image=self.play_icon),
            command=lambda: self.start_Play(engine, textbox, playbtn),
        )
        playbtn.pack(ipadx=5, ipady=5)

        def openTools():
            pass

        editbtn = ctk.CTkButton(
            btn_frame,
            text="",
            width=50,
            corner_radius=60,
            image=CTkImage(dark_image=self.dark_mode_edit),
            command=openTools,
        )
        editbtn.pack()

        # automatic bg color change for play btn
        def printer(textbox, play_btn):
            text_content = textbox.get("0.0", "end")
            if any(c.isalpha() for c in text_content):
                play_btn.configure(fg_color="royalblue")
            else:
                play_btn.configure(fg_color="transparent")

        textbox = ctk.CTkTextbox(
            btn_and_textbox_frame, font=("arial", 20), height=500, undo=True
        )
        textbox.pack(expand=True, fill="both", padx=20, pady=20, side="left")
        textbox.bind("<KeyRelease>", lambda event: printer(textbox, playbtn))

        # -----------------------------------------------------------------
        self.scrol_announcement_frame.pack(expand=True, fill="both")

    def start_Play(self, engine, textbox, play_btn):
        play_btn.configure(state="disabled")

        def speak():
            voices = engine.getProperty("voices")

            text_content = textbox.get("0.0", "end")

            engine.setProperty(
                "voice",
                voices[1].id,
            )
            engine.setProperty("rate", 120)
            engine.say(text_content)
            try:
                engine.runAndWait()
            except RuntimeError:
                CTkMessagebox(
                    message="Don't Announce when one is already playing", icon="cancel"
                )
            engine.stop()

        play = threading.Thread(target=speak).start()
        play_btn.configure(state="normal")

    def create_setting_page_widgets(self):
        self.settings_frame = ctk.CTkFrame(self.right_frame)
        self.settings_scrl_frame = ctk.CTkScrollableFrame(self.settings_frame)

        self.setting_label = ctk.CTkLabel(
            self.settings_scrl_frame, text="Settings", font=("arial", 40, "bold")
        )
        self.setting_label.pack(anchor="w", padx=20, pady=20)
        self.settings_scrl_frame.pack(expand=True, fill="both")

        # ===========================dark mode===========================
        def on_enter(event):
            # inner_mode_frame1.configure(cursor="hand2")
            inner_mode_frame1.configure(fg_color=("#B6B6B6", "#3f3f4e"))

        def on_leave(event):
            inner_mode_frame1.configure(fg_color=("#C8C8C8", "#333333"))

        def on_click(event):
            inner_mode_frame1.configure(fg_color="#333333")

            if self.inner_mode_frame2_open:
                self.inner_mode_frame2_open = False
                icon2.configure(
                    image=CTkImage(
                        light_image=self.light_mode_arrow_down,
                        dark_image=self.dark_mode_arrow_down,
                    )
                )
                inner_mode_frame2.forget()
            else:
                self.inner_mode_frame2_open = True
                icon2.configure(
                    image=CTkImage(
                        light_image=self.light_mode_arrow_up,
                        dark_image=self.dark_mode_arrow_up,
                    )
                )
                inner_mode_frame2.pack(expand=True, fill="both", ipadx=20, ipady=10)

        mode_frame = ctk.CTkFrame(self.settings_scrl_frame, fg_color="transparent")
        mode_frame.pack(expand=True, fill="both", padx=20, pady=20, ipadx=5, ipady=5)

        # ============================================frame 1
        self.inner_mode_frame2_open = False
        inner_mode_frame1 = ctk.CTkFrame(
            mode_frame, fg_color=("#C8C8C8", "#333333"), cursor="hand2"
        )
        inner_mode_frame1.pack(fill="x", ipadx=10, ipady=10, pady=10)
        inner_mode_frame1.bind("<Enter>", on_enter)
        inner_mode_frame1.bind("<Leave>", on_leave)
        inner_mode_frame1.bind("<Button-1>", lambda event: on_click(event))

        # icon
        icon1 = ctk.CTkLabel(
            inner_mode_frame1,
            text="",
            font=("Arial", 17),
            image=CTkImage(
                light_image=self.light_setting_image, dark_image=self.dark_setting_image
            ),
        )
        icon1.pack(
            anchor="w",
            side="left",
            padx=10,
        )
        icon1.bind("<Enter>", on_enter)
        icon1.bind("<Leave>", on_leave)
        icon1.bind("<Button-1>", lambda event: on_click(event))

        # text
        text = ctk.CTkLabel(
            inner_mode_frame1,
            font=("Arial", 17),
            text="Choose your mode",
        )
        text.pack(
            anchor="w",
            side="left",
            padx=10,
        )
        text.bind("<Enter>", on_enter)
        text.bind("<Leave>", on_leave)
        text.bind("<Button-1>", lambda event: on_click(event))

        # icon
        icon2 = ctk.CTkLabel(
            inner_mode_frame1,
            text="",
            image=CTkImage(
                light_image=self.light_mode_arrow_down,
                dark_image=self.dark_mode_arrow_down,
            ),
        )
        icon2.pack(
            anchor="e",
            side="right",
            padx=10,
        )
        icon2.bind("<Enter>", on_enter)
        icon2.bind("<Leave>", on_leave)
        icon2.bind("<Button-1>", lambda event: on_click(event))

        # ============================================frame 2
        inner_mode_frame2 = ctk.CTkFrame(mode_frame)
        # inner_mode_frame2.pack(expand=True, fill="both")

        def radiobutton_event():
            if self.radio_var.get() == 0:
                self.other_data["theme"] = 0

            elif self.radio_var.get() == 1:
                self.other_data["theme"] = 1

            elif self.radio_var.get() == 2:
                self.other_data["theme"] = 2

            self.save_other_data()
            self.set_theme_mode()

        self.radio_var = ctk.IntVar(value=self.other_data["theme"])
        for i in range(3):
            theme_name = ["Light", "Dark", "Use System Setting"]
            CTkRadioButton(
                inner_mode_frame2,
                text=theme_name[i],
                command=radiobutton_event,
                font=("Arial", 17),
                border_width_unchecked=2,
                border_width_checked=5,
                variable=self.radio_var,
                value=i,
            ).pack(anchor="w", padx=5, pady=5)

        # ===========================dark mode===========================

    def get_entry_value(self, alarm):
        # Extracting numerical part from the "text" values using re for the "period()" format
        extracted_numbers = [
            int(match.group(1))
            for item in alarm
            if (match := re.match(r"Period\((\d+)\)", item["text"]))
        ]
        if extracted_numbers:
            # Find missing values in the sequence
            n = max(extracted_numbers)
            missing_values = [
                str(i) for i in range(1, n + 1) if i not in extracted_numbers
            ]

            # Displaying the result
            if missing_values:
                number = f"{', '.join(missing_values)}"
                return number[0]
            else:
                return n + 1
        else:
            return 1

    def open_add_alarm_window(self, scrol_frame, alarm, data):
        add_alarm_window = ctk.CTkFrame(root, fg_color=("#c4c4c4", "#303030"))
        card = ctk.CTkFrame(add_alarm_window, fg_color=("#EDEDED", "#272727"))

        # Widgets in the sub-window
        ctk.CTkLabel(
            card,
            text="Add New Bell",
            font=("helvitica", 30, "bold"),
        ).pack(pady=20)
        # ctk.CTkLabel(card, text="Add Alarm").grid(row=0, column=0, columnspan=2)

        # =============================time===============================
        main_time_frame = ctk.CTkFrame(card, fg_color="transparent")

        arrowupframe = ctk.CTkFrame(main_time_frame, fg_color="transparent")
        hr_Arrow_Up = ctk.CTkButton(
            arrowupframe,
            width=20,
            text="",
            fg_color="transparent",
            command=lambda: self.increment(self.hrbtn, "hour"),
            image=ctk.CTkImage(
                light_image=self.light_mode_arrow_up, dark_image=self.dark_mode_arrow_up
            ),
        )
        hr_Arrow_Up.pack(side="left", padx=(0, 40))
        hr_Arrow_Up.bind("<MouseWheel>", lambda event: self.scroll_event(event, "hour"))
        hr_Arrow_Up.bind("<Down>", lambda event: self.increment(self.hrbtn, "hour"))

        min_Arrow_Up = ctk.CTkButton(
            arrowupframe,
            text="",
            fg_color="transparent",
            width=20,
            command=lambda: self.increment(self.minbtn, "minute"),
            image=ctk.CTkImage(
                self.light_mode_arrow_up, dark_image=self.dark_mode_arrow_up
            ),
        )
        min_Arrow_Up.pack(side="left", padx=(45, 0))
        min_Arrow_Up.bind(
            "<MouseWheel>", lambda event: self.scroll_event(event, "minute")
        )
        min_Arrow_Up.bind("<Down>", lambda event: self.increment(self.hrbtn, "min"))

        ampm_Arrow_Up = ctk.CTkButton(
            arrowupframe,
            text="",
            fg_color="transparent",
            width=20,
            command=lambda: self.increment(self.minbtn, "minute"),
            image=ctk.CTkImage(
                self.light_mode_arrow_up, dark_image=self.dark_mode_arrow_up
            ),
        )
        ampm_Arrow_Up.pack(side="right", padx=(0, 10))
        ampm_Arrow_Up.bind(
            "<MouseWheel>", lambda event: self.scroll_event(event, "ampm")
        )
        ampm_Arrow_Up.bind("<Down>", lambda event: self.increment(self.hrbtn, "ampm"))

        arrowupframe.pack(fill="x", padx=28)

        # =============================hours===============================
        timeframe = ctk.CTkFrame(
            main_time_frame, fg_color="transparent", border_width=2
        )

        self.hrbtn = ctk.CTkButton(
            timeframe,
            text=time.strftime("%I"),
            width=55,
            text_color=("black", "white"),
            fg_color="transparent",
            height=60,
            font=("arial", 40, "bold"),
        )
        self.hrbtn.pack(ipadx=10, ipady=10, padx=10, side="left")
        self.hrbtn.bind("<MouseWheel>", lambda event: self.scroll_event(event, "hour"))

        # =============================hours===============================
        ctk.CTkLabel(timeframe, text=":", font=("arial", 40, "bold")).pack(
            ipadx=5, ipady=10, side="left"
        )

        # =============================minute===============================

        self.minbtn = ctk.CTkButton(
            timeframe,
            text=time.strftime("%M"),
            width=55,
            text_color=("black", "white"),
            fg_color="transparent",
            height=60,
            font=("arial", 40, "bold"),
        )
        self.minbtn.pack(ipadx=10, ipady=10, padx=10, side="left")
        self.minbtn.bind(
            "<MouseWheel>", lambda event: self.scroll_event(event, "minute")
        )

        # =============================minute===============================
        # =============================ampm===============================

        self.ampmbtn = ctk.CTkButton(
            timeframe,
            text=time.strftime("%p"),
            width=75,
            text_color=("black", "white"),
            fg_color="transparent",
            height=60,
            font=("arial", 40, "bold"),
        )
        self.ampmbtn.pack(ipadx=10, ipady=10, padx=10, side="left")
        self.ampmbtn.bind(
            "<MouseWheel>", lambda event: self.scroll_event(event, "ampm")
        )

        timeframe.pack(ipadx=0, ipady=5)
        # =============================ampm===============================

        arrowdownframe = ctk.CTkFrame(
            main_time_frame,
            fg_color="transparent",
        )
        hr_Arrow_down = ctk.CTkButton(
            arrowdownframe,
            width=20,
            fg_color="transparent",
            text="",
            command=lambda: self.decrement(self.hrbtn, "hour"),
            image=ctk.CTkImage(
                self.light_mode_arrow_down, dark_image=self.dark_mode_arrow_down
            ),
        )
        hr_Arrow_down.pack(side="left", padx=(0, 40))
        hr_Arrow_down.bind(
            "<MouseWheel>", lambda event: self.scroll_event(event, "hour")
        )

        min_Arrow_down = ctk.CTkButton(
            arrowdownframe,
            width=20,
            fg_color="transparent",
            text="",
            command=lambda: self.decrement(self.minbtn, "minute"),
            image=ctk.CTkImage(
                self.light_mode_arrow_down, dark_image=self.dark_mode_arrow_down
            ),
        )
        min_Arrow_down.pack(side="left", padx=(45, 0))
        min_Arrow_down.bind(
            "<MouseWheel>", lambda event: self.scroll_event(event, "minute")
        )

        ampm_Arrow_down = ctk.CTkButton(
            arrowdownframe,
            width=20,
            fg_color="transparent",
            text="",
            command=lambda: self.decrement(self.minbtn, "minute"),
            image=ctk.CTkImage(
                self.light_mode_arrow_down, dark_image=self.dark_mode_arrow_down
            ),
        )
        ampm_Arrow_down.pack(side="right", padx=(0, 10))
        ampm_Arrow_down.bind(
            "<MouseWheel>", lambda event: self.scroll_event(event, "ampm")
        )

        arrowdownframe.pack(fill="x", padx=28)
        main_time_frame.pack(padx=20, pady=20)
        # =============================time====================================
        # =============================Name field===============================
        name_frame = ctk.CTkFrame(card, fg_color="transparent")
        text_label = ctk.CTkLabel(
            name_frame,
            text="    ",
            font=("arial", 25),
            image=CTkImage(
                dark_image=self.dark_mode_label,
                light_image=self.light_mode_label,
                size=(25, 25),
            ),
        )
        text_label.grid(row=0, column=0, pady=5)

        value = self.get_entry_value(alarm)
        name = ctk.StringVar(value=f"Period({value})")

        text_entry = ctk.CTkEntry(
            name_frame,
            font=("arial", 20),
            width=280,
            textvariable=name,
            fg_color="transparent",
        )
        text_entry.grid(row=0, column=1, pady=5, ipadx=5, ipady=5)
        name_frame.pack(pady=(0, 30))
        # =============================Name field===============================
        # =============================days field===============================
        weekd_days_frame = ctk.CTkFrame(card, fg_color="transparent")
        weekd_days_frame.pack(pady=(0, 30))

        days_var = {}
        for i, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
            days_var[day] = ctk.BooleanVar(weekd_days_frame, value=True)
            ctk.CTkCheckBox(
                weekd_days_frame,
                text=day,
                border_width=2,
                corner_radius=50,
                width=20,
                checkbox_height=30,
                checkbox_width=30,
                variable=days_var[day],
            ).grid(row=0, column=i + 1, pady=10, sticky="w", padx=5)

        # =============================days field===============================
        # =============================music field===============================
        def get_music_files(folder_path):
            music_files = []
            for file in os.listdir(folder_path):
                if (
                    file.endswith(".mp3")
                    or file.endswith(".wav")
                    or file.endswith(".ogg")
                    or file.endswith(".aiff")
                    or file.endswith(".flac")
                    or file.endswith(".acc")
                    or file.endswith(".wma")
                ):
                    music_files.append(file)
            return music_files

        music_frame = ctk.CTkFrame(card, fg_color="transparent")
        music_frame.pack(pady=(0, 30))
        music_label = ctk.CTkLabel(
            music_frame,
            text="",
            font=("helvitica", 23),
            image=CTkImage(
                dark_image=self.dark_mode_music_icon,
                light_image=self.light_mode_music_icon,
                size=(25, 25),
            ),
        )
        music_label.pack(side="left", padx=5)
        music_files = get_music_files("Assets/music")
        curr_music = ctk.StringVar()
        curr_music.set(music_files[0])
        select_bell = ctk.CTkOptionMenu(
            music_frame,
            values=music_files,
            variable=curr_music,
            font=("helvitica", 16),
            width=280,
            text_color=("black", "white"),
            fg_color=("white", "#383838"),
        )
        select_bell.pack(side="left")
        # =============================music field===============================
        # =============================cancel button===============================
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(pady=(0, 30))

        cancel_button = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            fg_color=("white", "#383838"),
            text_color=("black", "white"),
            hover_color=("#DADADA", "#252525"),
            image=CTkImage(
                dark_image=self.dark_mode_cross, light_image=self.light_mode_cross
            ),
            command=add_alarm_window.destroy,
        )
        cancel_button.grid(row=0, column=0, pady=10, padx=10)
        # =============================cancel button===============================
        # =============================save button===============================

        save_button = ctk.CTkButton(
            btn_frame,
            text="Save",
            # fg_color="#4cc2ff",
            image=CTkImage(dark_image=self.save_icon),
            command=lambda: self.save_alarm(
                self.hrbtn.cget("text"),
                self.minbtn.cget("text"),
                self.ampmbtn.cget("text"),
                text_entry.get(),
                days_var,
                curr_music.get(),
                add_alarm_window,
                scrol_frame,
                alarm,
                data,
            ),
        )
        save_button.grid(row=0, column=1, pady=10, padx=10)
        # =============================save button===============================

        card.pack(padx=1005, pady=1005, ipadx=30)
        add_alarm_window.place(relx=0.5, rely=0.5, anchor="center")

    def scroll_event(self, event, time):
        if time == "hour":
            if event.delta > 0:
                self.increment(self.hrbtn, "hour")
            else:
                self.decrement(self.hrbtn, "hour")
        elif time == "minute":
            if event.delta > 0:
                self.increment(self.minbtn, "minute")
            else:
                self.decrement(self.minbtn, "minute")
        else:
            if event.delta > 0:
                self.ampmbtn.configure(text="am")
            else:
                self.ampmbtn.configure(text="pm")

    def increment(self, btn, time):
        value = btn.cget("text")
        if time == "hour":
            if int(value) == 12:
                btn.configure(text="01")
            else:
                btn.configure(text=f"{int(value)+1 :02}")
        elif time == "minute":
            if int(value) == 59:
                btn.configure(text="00")
            else:
                btn.configure(text=f"{int(value)+1:02}")

    def decrement(self, btn, time):
        value = btn.cget("text")
        if time == "hour":
            if int(value) == 1:
                btn.configure(text="12")
            else:
                btn.configure(text=f"{int(value)-1 :02}")
        elif time == "minute":
            if int(value) == 0:
                btn.configure(text="59")
            else:
                btn.configure(text=f"{int(value)-1 :02}")

    def edit_alarm(self, alar, scrol_frame, alarm, data, alarm_frame):
        edit_alarm_window = ctk.CTkFrame(root, fg_color=("#c4c4c4", "#303030"))
        card = ctk.CTkFrame(edit_alarm_window, fg_color=("White", "#252525"))

        # Widgets in the sub-window
        ctk.CTkLabel(
            card,
            text="Edit Bell",
            font=("helvitica", 30, "bold"),
        ).pack(pady=20)

        # =============================time===============================
        main_time_frame = ctk.CTkFrame(card, fg_color="transparent")

        arrowupframe = ctk.CTkFrame(main_time_frame, fg_color="transparent")
        hr_Arrow_Up = ctk.CTkButton(
            arrowupframe,
            width=20,
            text="",
            fg_color="transparent",
            command=lambda: self.increment(self.hrbtn, "hour"),
            image=ctk.CTkImage(
                light_image=self.light_mode_arrow_up, dark_image=self.dark_mode_arrow_up
            ),
        )
        hr_Arrow_Up.pack(side="left", padx=(0, 40))
        hr_Arrow_Up.bind("<MouseWheel>", lambda event: self.scroll_event(event, "hour"))
        hr_Arrow_Up.bind("<Down>", lambda event: self.increment(self.hrbtn, "hour"))

        min_Arrow_Up = ctk.CTkButton(
            arrowupframe,
            text="",
            fg_color="transparent",
            width=20,
            command=lambda: self.increment(self.minbtn, "minute"),
            image=ctk.CTkImage(
                self.light_mode_arrow_up, dark_image=self.dark_mode_arrow_up
            ),
        )
        min_Arrow_Up.pack(side="left", padx=(45, 0))
        min_Arrow_Up.bind(
            "<MouseWheel>", lambda event: self.scroll_event(event, "minute")
        )
        min_Arrow_Up.bind("<Down>", lambda event: self.increment(self.hrbtn, "min"))

        ampm_Arrow_Up = ctk.CTkButton(
            arrowupframe,
            text="",
            fg_color="transparent",
            width=20,
            command=lambda: self.increment(self.minbtn, "minute"),
            image=ctk.CTkImage(
                self.light_mode_arrow_up, dark_image=self.dark_mode_arrow_up
            ),
        )
        ampm_Arrow_Up.pack(side="right", padx=(0, 10))
        ampm_Arrow_Up.bind(
            "<MouseWheel>", lambda event: self.scroll_event(event, "ampm")
        )
        ampm_Arrow_Up.bind("<Down>", lambda event: self.increment(self.hrbtn, "ampm"))

        arrowupframe.pack(fill="x", padx=28)

        # =============================hours===============================
        timeframe = ctk.CTkFrame(
            main_time_frame, fg_color="transparent", border_width=1
        )

        self.hrbtn = ctk.CTkButton(
            timeframe,
            text=alar["time"].split(":")[0],
            width=55,
            fg_color="transparent",
            height=60,
            font=("arial", 40, "bold"),
        )
        self.hrbtn.pack(ipadx=10, ipady=10, padx=10, side="left")
        self.hrbtn.bind("<MouseWheel>", lambda event: self.scroll_event(event, "hour"))

        # =============================hours===============================
        ctk.CTkLabel(timeframe, text=":", font=("arial", 40, "bold")).pack(
            ipadx=5, ipady=10, side="left"
        )

        # =============================minute===============================

        self.minbtn = ctk.CTkButton(
            timeframe,
            text=alar["time"].split(":")[1].split()[0],
            width=55,
            fg_color="transparent",
            height=60,
            font=("arial", 40, "bold"),
        )
        self.minbtn.pack(ipadx=10, ipady=10, padx=10, side="left")
        self.minbtn.bind(
            "<MouseWheel>", lambda event: self.scroll_event(event, "minute")
        )

        # =============================minute===============================
        # =============================ampm===============================

        self.ampmbtn = ctk.CTkButton(
            timeframe,
            text=alar["time"].split()[1],
            width=75,
            fg_color="transparent",
            height=60,
            font=("arial", 40, "bold"),
        )
        self.ampmbtn.pack(ipadx=10, ipady=10, padx=10, side="left")
        self.ampmbtn.bind(
            "<MouseWheel>", lambda event: self.scroll_event(event, "ampm")
        )

        timeframe.pack(ipadx=0, ipady=5)
        # =============================ampm===============================

        arrowdownframe = ctk.CTkFrame(
            main_time_frame,
            fg_color="transparent",
        )
        hr_Arrow_down = ctk.CTkButton(
            arrowdownframe,
            width=20,
            fg_color="transparent",
            text="",
            command=lambda: self.decrement(self.hrbtn, "hour"),
            image=ctk.CTkImage(
                self.light_mode_arrow_down, dark_image=self.dark_mode_arrow_down
            ),
        )
        hr_Arrow_down.pack(side="left", padx=(0, 40))
        hr_Arrow_down.bind(
            "<MouseWheel>", lambda event: self.scroll_event(event, "hour")
        )

        min_Arrow_down = ctk.CTkButton(
            arrowdownframe,
            width=20,
            fg_color="transparent",
            text="",
            command=lambda: self.decrement(self.minbtn, "minute"),
            image=ctk.CTkImage(
                self.light_mode_arrow_down, dark_image=self.dark_mode_arrow_down
            ),
        )
        min_Arrow_down.pack(side="left", padx=(45, 0))
        min_Arrow_down.bind(
            "<MouseWheel>", lambda event: self.scroll_event(event, "minute")
        )

        ampm_Arrow_down = ctk.CTkButton(
            arrowdownframe,
            width=20,
            fg_color="transparent",
            text="",
            command=lambda: self.decrement(self.minbtn, "minute"),
            image=ctk.CTkImage(
                self.light_mode_arrow_down, dark_image=self.dark_mode_arrow_down
            ),
        )
        ampm_Arrow_down.pack(side="right", padx=(0, 10))
        ampm_Arrow_down.bind(
            "<MouseWheel>", lambda event: self.scroll_event(event, "ampm")
        )

        arrowdownframe.pack(fill="x", padx=28)
        main_time_frame.pack(padx=20, pady=20)

        # =============================time====================================
        # =============================Name field===============================
        name_frame = ctk.CTkFrame(card, fg_color="transparent")
        name_frame.pack(pady=(0, 30))

        text_label = ctk.CTkLabel(
            name_frame,
            text="    ",
            font=("arial", 25),
            image=CTkImage(
                dark_image=self.dark_mode_label,
                light_image=self.light_mode_label,
                size=(25, 25),
            ),
        )
        text_label.grid(row=0, column=0, pady=10)

        text_var = ctk.StringVar(name_frame)
        text_var.set(alar["text"])
        text_entry = ctk.CTkEntry(name_frame, textvariable=text_var)
        text_entry.grid(row=0, column=1, pady=5)

        # =============================Name field===============================
        # =============================music field===============================
        def get_music_files(folder_path):
            music_files = []
            for file in os.listdir(folder_path):
                if (
                    file.endswith(".mp3")
                    or file.endswith(".wav")
                    or file.endswith(".ogg")
                    or file.endswith(".aiff")
                    or file.endswith(".flac")
                    or file.endswith(".acc")
                    or file.endswith(".wma")
                ):
                    music_files.append(file)
            return music_files

        music_frame = ctk.CTkFrame(card, fg_color="transparent")
        music_frame.pack(pady=(0, 30))
        music_label = ctk.CTkLabel(
            music_frame, text="Select Music : ", font=("helvitica", 23)
        )
        music_label.pack(side="left", padx=5)
        music_files = get_music_files("Assets/music")
        curr_music = ctk.StringVar()
        curr_music.set(alar["music"])
        select_bell = ctk.CTkOptionMenu(
            music_frame, values=music_files, variable=curr_music, font=("helvitica", 16)
        )
        select_bell.pack(side="left")
        # =============================music field===============================
        # =============================days field===============================

        weekd_days_frame = ctk.CTkFrame(card, fg_color="transparent")
        weekd_days_frame.pack(pady=(0, 30))
        days_var = {}
        for i, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
            days_var[day] = ctk.BooleanVar(card, value=(day in alar["days"]))
            ctk.CTkCheckBox(
                weekd_days_frame,
                text=day,
                border_width=2,
                corner_radius=50,
                width=20,
                checkbox_height=30,
                checkbox_width=30,
                variable=days_var[day],
            ).grid(row=0, column=i + 1, pady=10, sticky="w", padx=5)
        # =============================days field===============================
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(pady=(0, 30))
        # =============================cancel button===============================
        cancel_button = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            fg_color="#383838",
            hover_color="#424242",
            image=CTkImage(
                dark_image=self.dark_mode_cross, light_image=self.light_mode_cross
            ),
            command=edit_alarm_window.destroy,
        )
        cancel_button.grid(row=0, column=0, pady=10, padx=10)
        # =============================cancel button===============================
        # =============================save button===============================

        save_button = ctk.CTkButton(
            btn_frame,
            text="Save",
            # fg_color="#4cc2ff",
            image=CTkImage(dark_image=self.save_icon),
            command=lambda: self.save_edited_alarm(
                self.hrbtn.cget("text"),
                self.minbtn.cget("text"),
                self.ampmbtn.cget("text"),
                text_var.get(),
                days_var,
                curr_music.get(),
                alar,
                scrol_frame,
                alarm,
                data,
                edit_alarm_window,
                alarm_frame,
            ),
        )
        save_button.grid(row=0, column=1, pady=10, padx=10)

        card.pack(padx=1005, pady=1005, ipadx=30)
        edit_alarm_window.place(relx=0.5, rely=0.5, anchor="center")
        # =============================save button===============================

    def save_alarm(
        self,
        hour,
        minute,
        am_pm,
        text,
        days_var,
        curr_mus,
        add_alarm_window,
        scrol_frame,
        alarm,
        data,
    ):
        alarm_time = f"{hour}:{minute} {am_pm}"
        music_selected = curr_mus
        days_selected = [day for day, var in days_var.items() if var.get()]

        if not days_selected:
            CTkMessagebox(
                title="warning", message="Select atleast one day!!!", icon="cancel"
            )
            return

        alarm_data = {
            "time": alarm_time,
            "text": text,
            "music": music_selected,
            "days": days_selected,
            "switch_state": True,  # default to True
        }

        alarm.append(alarm_data)
        self.save_data(alarm, data)

        self.display_single_alarm(
            scrol_frame, alarm, data, alarm_data, text, music_selected, days_selected
        )

        add_alarm_window.destroy()
        # self.display_alarms(scrol_frame, alarm, data)

    def sort_data(self, alarm):
        sorted(
            alarm,
            key=lambda item: (
                datetime.strptime(item["time"], "%I:%M %p"),
                item["name"],
                item["music"],
                item["days"],
                item["switch_state"],
            ),
        )

    def start_threading(self):
        # Start background thread
        self.check_alarm_thread1 = threading.Thread(target=self.check_alarm1)
        self.check_alarm_thread1.daemon = True
        self.check_alarm_thread1.start()

        self.check_alarm_thread2 = threading.Thread(target=self.check_alarm2)
        self.check_alarm_thread2.daemon = True
        self.check_alarm_thread2.start()

        self.check_alarm_thread3 = threading.Thread(target=self.check_alarm3)
        self.check_alarm_thread3.daemon = True
        self.check_alarm_thread3.start()

        self.check_alarm_thread4 = threading.Thread(target=self.check_alarm4)
        self.check_alarm_thread4.daemon = True
        self.check_alarm_thread4.start()

        self.check_alarm_thread5 = threading.Thread(target=self.check_alarm5)
        self.check_alarm_thread5.daemon = True
        self.check_alarm_thread5.start()

        self.check_alarm_thread6 = threading.Thread(target=self.check_alarm6)
        self.check_alarm_thread6.daemon = True
        self.check_alarm_thread6.start()

    def check_alarm1(self):
        current_time = time.strftime("%I:%M %p")
        current_day = time.strftime("%a")

        # Initialize pygame outside the loop (call it once)
        pygame.mixer.init()

        # Load the sound file once
        sound = pygame.mixer.Sound("Assets/music/Handbell.mp3")

        # Flag to track whether the music has been played for the current alarm
        music_played = False

        while not self.stop_thread:
            for alarm in self.alarms1:
                current_time = time.strftime("%I:%M %p")
                current_day = time.strftime("%a")
                sound1 = pygame.mixer.Sound(f"Assets/music/{alarm['music']}")

                if (
                    alarm["time"] == current_time
                    and current_day in alarm["days"]
                    and alarm["switch_state"]
                    and not music_played
                ):
                    sound.play()
                    print(sound1)
                    # music_played = True
                    time.sleep(60)
                    # current_time = time.strftime("%I:%M %p")
                    # current_day = time.strftime("%a")
            time.sleep(1)

            # current_time = time.strftime("%I:%M %p")
            # current_day = time.strftime("%a")

            # # Reset the flag when the alarm condition is no longer met
            # if music_played and all(
            #     alarm["time"] != current_time
            #     or current_day not in alarm["days"]
            #     or not alarm["switch_state"]
            #     for alarm in self.alarms
            # ):
            #     music_played = False

            # time.sleep(1)

    def check_alarm2(self):
        current_time = time.strftime("%I:%M %p")
        current_day = time.strftime("%a")

        # Initialize pygame outside the loop (call it once)
        pygame.mixer.init()

        # Load the sound file once
        sound = pygame.mixer.Sound("Assets/music/Handbell.mp3")

        # print(f"Current Time: {current_time}, Current Day: {current_day}")

        while not self.stop_thread:
            for alarm in self.alarms2:
                current_time = time.strftime("%I:%M %p")
                current_day = time.strftime("%a")
                if (
                    alarm["time"] == current_time
                    and current_day in alarm["days"]
                    and alarm["switch_state"]
                ):
                    sound.play()
                    time.sleep(120)

            time.sleep(1)

    def check_alarm3(self):
        current_time = time.strftime("%I:%M %p")
        current_day = time.strftime("%a")

        # Initialize pygame outside the loop (call it once)
        pygame.mixer.init()

        # Load the sound file once
        sound = pygame.mixer.Sound("Assets/music/Handbell.mp3")

        # print(f"Current Time: {current_time}, Current Day: {current_day}")

        while not self.stop_thread:
            for alarm in self.alarms3:
                current_time = time.strftime("%I:%M %p")
                current_day = time.strftime("%a")
                if (
                    alarm["time"] == current_time
                    and current_day in alarm["days"]
                    and alarm["switch_state"]
                ):
                    sound.play()
                    time.sleep(120)

            time.sleep(1)

    def check_alarm4(self):
        current_time = time.strftime("%I:%M %p")
        current_day = time.strftime("%a")

        # Initialize pygame outside the loop (call it once)
        pygame.mixer.init()

        # Load the sound file once
        sound = pygame.mixer.Sound("Assets/music/Handbell.mp3")

        # print(f"Current Time: {current_time}, Current Day: {current_day}")

        while not self.stop_thread:
            for alarm in self.alarms4:
                current_time = time.strftime("%I:%M %p")
                current_day = time.strftime("%a")
                if (
                    alarm["time"] == current_time
                    and current_day in alarm["days"]
                    and alarm["switch_state"]
                ):
                    sound.play()
                    time.sleep(120)

            time.sleep(1)

    def check_alarm5(self):
        current_time = time.strftime("%I:%M %p")
        current_day = time.strftime("%a")

        # Initialize pygame outside the loop (call it once)
        pygame.mixer.init()

        # Load the sound file once
        sound = pygame.mixer.Sound("Assets/music/Handbell.mp3")

        # print(f"Current Time: {current_time}, Current Day: {current_day}")

        while not self.stop_thread:
            for alarm in self.alarms5:
                current_time = time.strftime("%I:%M %p")
                current_day = time.strftime("%a")
                if (
                    alarm["time"] == current_time
                    and current_day in alarm["days"]
                    and alarm["switch_state"]
                ):
                    sound.play()
                    time.sleep(120)

            time.sleep(1)

    def check_alarm6(self):
        current_time = time.strftime("%I:%M %p")
        current_day = time.strftime("%a")

        # Initialize pygame outside the loop (call it once)
        pygame.mixer.init()

        # Load the sound file once
        sound = pygame.mixer.Sound("Assets/music/Handbell.mp3")

        # print(f"Current Time: {current_time}, Current Day: {current_day}")

        while not self.stop_thread:
            for alarm in self.alarms6:
                current_time = time.strftime("%I:%M %p")
                current_day = time.strftime("%a")
                if (
                    alarm["time"] == current_time
                    and current_day in alarm["days"]
                    and alarm["switch_state"]
                ):
                    sound.play()
                    time.sleep(120)

            time.sleep(1)

    def on_closing(self):
        # Stop the background thread
        self.stop_thread = True
        # Stop the Pygame mixer
        pygame.mixer.quit()

        self.width = self.master.winfo_width()
        self.height = self.master.winfo_height()
        self.x = self.master.winfo_x()
        self.y = self.master.winfo_y()

        self.other_data["width"] = self.width - 290
        self.other_data["height"] = self.height - 188
        self.other_data["x"] = self.x
        self.other_data["y"] = self.y

        self.save_other_data()

        # Close the application
        self.master.destroy()

    def display_single_alarm(
        self, scrol_frame, alarm, data, alarm_data, text, music_selected, days_selected
    ):
        alarm_frame = ctk.CTkFrame(scrol_frame, fg_color=("white", "#222327"))
        alarm_frame.grid(
            row=self.row,
            column=self.col,
            pady=15,
            padx=15,
            ipadx=15,
            ipady=15,
            sticky="snew",
        )

        # inner_alarm_frame = ctk.CTkFrame(alarm_frame)
        # inner_alarm_frame.place(relx=0.5, rely=0.5, anchor="center")

        time_name_and_btn_frame = ctk.CTkFrame(alarm_frame, fg_color="transparent")
        time_name_and_btn_frame.pack(
            expand=True,
            fill="both",
            padx=5,
        )

        # configure columns
        time_name_and_btn_frame.columnconfigure(0, weight=1)

        # time and name frame
        time_and_name_frame = ctk.CTkFrame(
            time_name_and_btn_frame, fg_color="transparent"
        )
        time_and_name_frame.pack(side=LEFT, expand=True, fill="both")

        # time and name frame widgets
        times = ctk.CTkLabel(
            time_and_name_frame,
            text=f"{alarm_data['time']}",
            font=("arial", 50, "bold"),
            text_color=("black", "white"),
            # bg_color="red",
        )
        times.pack(anchor="w", padx=(10, 0))

        text = ctk.CTkLabel(
            time_and_name_frame,
            text=f"{alarm_data['text']}",
            font=("arial", 20, "bold"),
            text_color=("black", "white"),
        )
        text.pack(anchor="w", padx=10)

        musics = ctk.CTkLabel(
            time_and_name_frame,
            # text=f"{alar['music']}",
            text=f"{alarm_data['music']}",
            font=("arial", 15, "normal"),
            text_color=("black", "white"),
        )
        musics.pack(anchor="w", padx=10)

        # btn frame for switch edit and delete
        btn_frame = ctk.CTkFrame(time_name_and_btn_frame, fg_color="transparent")
        # btn_frame.grid(row=0, column=1, sticky="nswe")
        btn_frame.pack(side=RIGHT, expand=True, fill="both", pady=(5, 0))

        switch_var = ctk.BooleanVar(value=alarm_data["switch_state"])
        # store variable in list
        # switch_vars.append(switch_var)

        # make colors dull if switch is off
        if not alarm_data["switch_state"]:
            text.configure(text_color=("grey", "grey"))
            times.configure(text_color=("grey", "grey"))

        switch_widget = ctk.CTkSwitch(
            btn_frame,
            text="",
            # bg_color="blue",
            switch_height=20,
            switch_width=40,
            width=4,
            corner_radius=50,
            variable=switch_var,
            command=lambda alar=alarm_data, sv=switch_var, alarm=alarm, data=data, text=text, times=times, musics=musics: self.toggle_switch(
                alar, sv, alarm, data, text, times, musics
            ),
        )
        switch_widget.pack(anchor="e", padx=5)

        delete_button = ctk.CTkButton(
            btn_frame,
            text="",
            width=10,
            fg_color="transparent",
            image=CTkImage(
                dark_image=self.dark_mode_delete, light_image=self.light_mode_delete
            ),
            command=lambda a=alarm_data, scrol_frame=scrol_frame, alarm=alarm, data=data, alarm_frame=alarm_frame: self.delete_alarm(
                a, scrol_frame, alarm, data, alarm_frame
            ),
        )
        delete_button.pack(anchor="e", padx=5)
        # grid(row=3, column=0, pady=5)
        self.switch_tooltip = CTkToolTip(
            delete_button,
            message="Delete",
            font=("arial", 15),
            delay=0.5,
            padx=5,
            pady=5,
        )

        edit_button = ctk.CTkButton(
            btn_frame,
            text="",
            width=10,
            fg_color="transparent",
            image=CTkImage(
                dark_image=self.dark_mode_edit, light_image=self.light_mode_edit
            ),
            command=lambda a=alarm_data, scrol_frame=scrol_frame, alarm=alarm, data=data, alarm_frame=alarm_frame: self.edit_alarm(
                a, scrol_frame, alarm, data, alarm_frame
            ),
        )
        edit_button.pack(anchor="e", padx=5)
        CTkToolTip(
            edit_button,
            message="Edit",
            font=("arial", 15),
            delay=0.5,
            padx=5,
            pady=5,
        )

        # days frame for days
        day_frame = ctk.CTkFrame(alarm_frame, fg_color="transparent")
        day_frame.pack(expand=True, fill="both")

        ctk.CTkLabel(
            day_frame,
            fg_color="transparent",
            corner_radius=50,
            text=f"{'        '.join(alarm_data['days'])}",
            text_color="grey",
        ).pack(anchor="w", padx=15)

        if self.col == self.column_length:
            self.col = 0
            self.row += 1
        else:
            self.col += 1

        self.arrange_elements(scrol_frame)

    def display_alarms(self, scrol_frame, alarm, data):
        # Clear existing widgets in the display frame
        for widget in scrol_frame.winfo_children():
            widget.destroy()

        # List to store switch variables
        switch_vars = []

        row = col = 0

        # Display alarms in the display frame
        for i, alar in enumerate(alarm):
            if col == self.column_length:
                col = 0
                row += 1
                self.col = 0
                self.row += 1
            # main alarm card frame
            alarm_frame = ctk.CTkFrame(scrol_frame, fg_color=("white", "#222327"))

            # inner_alarm_frame = ctk.CTkFrame(alarm_frame)
            # inner_alarm_frame.place(relx=0.5, rely=0.5, anchor="center")

            time_name_and_btn_frame = ctk.CTkFrame(alarm_frame, fg_color="transparent")
            time_name_and_btn_frame.pack(
                expand=True,
                fill="both",
                padx=5,
            )

            # configure columns
            time_name_and_btn_frame.columnconfigure(0, weight=1)

            # time and name frame
            time_and_name_frame = ctk.CTkFrame(
                time_name_and_btn_frame, fg_color="transparent"
            )
            time_and_name_frame.pack(side=LEFT, expand=True, fill="both")

            # time and name frame widgets
            times = ctk.CTkLabel(
                time_and_name_frame,
                text=f"{alar['time']}",
                font=("arial", 50, "bold"),
                text_color=("black", "white"),
                # bg_color="red",
            )
            times.pack(anchor="w", padx=(10, 0))

            text = ctk.CTkLabel(
                time_and_name_frame,
                text=f"{alar['text']}",
                font=("arial", 20, "bold"),
                text_color=("black", "white"),
            )
            text.pack(anchor="w", padx=10)

            musics = ctk.CTkLabel(
                time_and_name_frame,
                # text=f"{alar['music']}",
                text=f"{alar['music']}",
                font=("arial", 15, "normal"),
                text_color=("black", "white"),
            )
            musics.pack(anchor="w", padx=10)

            # btn frame for switch edit and delete
            btn_frame = ctk.CTkFrame(time_name_and_btn_frame, fg_color="transparent")
            # btn_frame.grid(row=0, column=1, sticky="nswe")
            btn_frame.pack(side=RIGHT, expand=True, fill="both", pady=(5, 0))

            switch_var = ctk.BooleanVar(value=alar["switch_state"])
            # store variable in list
            switch_vars.append(switch_var)

            # make colors dull if switch is off
            if not alar["switch_state"]:
                text.configure(text_color=("grey", "grey"))
                times.configure(text_color=("grey", "grey"))

            switch_widget = ctk.CTkSwitch(
                btn_frame,
                text="",
                # bg_color="blue",
                switch_height=20,
                switch_width=40,
                width=4,
                corner_radius=50,
                variable=switch_var,
                command=lambda alar=alar, sv=switch_var, alarm=alarm, data=data, text=text, times=times, musics=musics: self.toggle_switch(
                    alar, sv, alarm, data, text, times, musics
                ),
            )
            switch_widget.pack(anchor="e", padx=5)

            delete_button = ctk.CTkButton(
                btn_frame,
                text="",
                width=10,
                fg_color="transparent",
                image=CTkImage(
                    dark_image=self.dark_mode_delete, light_image=self.light_mode_delete
                ),
                command=lambda a=alar, scrol_frame=scrol_frame, alarm=alarm, data=data, alarm_frame=alarm_frame: self.delete_alarm(
                    a, scrol_frame, alarm, data, alarm_frame
                ),
            )
            delete_button.pack(anchor="e", padx=5)
            # grid(row=3, column=0, pady=5)
            self.switch_tooltip = CTkToolTip(
                delete_button,
                message="Delete",
                font=("arial", 15),
                delay=0.5,
                padx=5,
                pady=5,
            )

            edit_button = ctk.CTkButton(
                btn_frame,
                text="",
                width=10,
                fg_color="transparent",
                image=CTkImage(
                    dark_image=self.dark_mode_edit, light_image=self.light_mode_edit
                ),
                command=lambda a=alar, scrol_frame=scrol_frame, alarm=alarm, data=data, alarm_frame=alarm_frame: self.edit_alarm(
                    a, scrol_frame, alarm, data, alarm_frame
                ),
            )
            edit_button.pack(anchor="e", padx=5)
            CTkToolTip(
                edit_button,
                message="Edit",
                font=("arial", 15),
                delay=0.5,
                padx=5,
                pady=5,
            )

            # days frame for days
            day_frame = ctk.CTkFrame(alarm_frame, fg_color="transparent")
            day_frame.pack(expand=True, fill="both")

            # grid(row=1, column=0, sticky="w", padx=10)
            ctk.CTkLabel(
                day_frame,
                fg_color="transparent",
                corner_radius=50,
                text=f"{'        '.join(alar['days'])}",
                text_color="grey",
            ).pack(anchor="w", padx=15)
            # .grid(row=2, column=0, sticky="w", padx=10)

            alarm_frame.grid(
                row=row, column=col, pady=15, padx=15, ipadx=15, ipady=15, sticky="snew"
            )

            col += 1
            self.col += 1

        for c in range(self.column_length):
            scrol_frame.columnconfigure(c, weight=1)

    def rename_button(self, button, button_index):
        # current_text = button.cget("text")

        new_name = ctk.CTkInputDialog(
            title="Rename Button", text="Enter new name:"
        ).get_input()
        if new_name:
            button.configure(text=new_name)
            # Update the button name in the loaded data
            self.button_names[str(button_index)] = new_name
            # Save the updated data to the JSON file
            self.save_button_names()

    def toggle_switch(self, alar, switch_var, alarm, data, text, times, musics):
        alar["switch_state"] = switch_var.get()
        if alar["switch_state"]:
            # switch_tooltip.configure(message="True")
            text.configure(text_color=("black", "white"))
            times.configure(text_color=("black", "white"))
            musics.configure(text_color=("black", "white"))
        else:
            # switch_tooltip.configure(message="False")
            text.configure(text_color=("grey", "grey"))
            times.configure(text_color=("grey", "grey"))
            musics.configure(text_color=("grey", "grey"))
        self.save_data(alarm, data)

    def delete_alarm(self, alar, scrol_frame, alarm, data, alarm_frame):
        alarm.remove(alar)
        self.save_data(alarm, data)
        alarm_frame.destroy()
        self.arrange_elements(scrol_frame)
        # self.display_alarms(scrol_frame, alarm, data)

    def save_edited_alarm(
        self,
        hour,
        minute,
        am_pm,
        text,
        days_var,
        music,
        old_alarm,
        scrol_frame,
        alarm,
        data,
        edit_alarm_window,
        alarm_frame,
    ):
        alarm.remove(old_alarm)

        alarm_time = f"{hour}:{minute} {am_pm}"
        days_selected = [day for day, var in days_var.items() if var.get()]

        if not days_selected:
            CTkMessagebox(title="Error", message="Select atleast 1 day", icon="cancel")
            return

        edited_alarm = {
            "time": alarm_time,
            "text": text,
            "music": music,
            "days": days_selected,
            "switch_state": True,  # default to True
        }

        alarm.append(edited_alarm)
        self.save_data(alarm, data)

        edit_alarm_window.destroy()
        self.display_alarms(scrol_frame, alarm, data)

    def save_button_names(self):
        # Save the button names to a JSON file
        with open("Assets/json/button_names.json", "w") as file:
            json.dump(self.button_names, file, indent=2)

    def load_button_names(self):
        # Load button names from a JSON file
        try:
            with open("Assets/json/button_names.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def load_alarms(self, filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self, alarm, data):
        with open(data, "w") as file:
            json.dump(alarm, file, indent=2)

    def load_other_data(self):
        try:
            with open("Assets/json/other_data.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"theme": 2, "width": 600, "height": 600}

    def save_other_data(self):
        with open("Assets/json/other_data.json", "w") as file:
            json.dump(self.other_data, file, indent=2)


if __name__ == "__main__":
    root = ctk.CTk()
    app = BellSystemApp(root)

    # Bind the on_closing method to the close event of the main window
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    root.mainloop()
