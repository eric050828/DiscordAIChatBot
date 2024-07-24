import requests
import subprocess

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from config import config
from logger import logger
from utils.path import path


class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard")
        self.geometry(f"{config.GUI.width}x{config.GUI.height}")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.create_widgets()
        
    def create_widgets(self):
        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        # navigation label
        ctk.CTkLabel(self.navigation_frame, text="Control Panel", image=None,compound="center",
                     font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        # frames
        self.create_dashboard_frame()
        self.create_settings_frame()
        # dashboard
        self.dashboard_btn = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Dashboard",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                           anchor="w", command=self.dashboard_btn_event)
        self.dashboard_btn.grid(row=1, column=0, sticky="ew")
        # settings
        self.settings_btn = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                          fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                          image=None, anchor="w", command=self.settings_btn_event)
        self.settings_btn.grid(row=2, column=0, sticky="ew")
        # appearance_mode_menu
        ctk.CTkOptionMenu(self.navigation_frame, values=["System", "Light", "Dark"], 
                          command=self.change_appearance_mode_event).grid(row=6, column=0, sticky="s")
        # set default
        self.select_frame_by_name("dashboard")
        ctk.set_appearance_mode(config.GUI.appearance_mode)
    
    def create_dashboard_frame(self):
        self.dashboard_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.dashboard_frame.grid_rowconfigure(6, weight=1)
        self.dashboard_frame.grid_columnconfigure(0, weight=3)
        self.dashboard_frame.grid_columnconfigure((1, 2), weight=1)
        # Dashboard
        ctk.CTkLabel(self.dashboard_frame, text="Dashboard", font=ctk.CTkFont(size=20, weight="bold"))\
            .grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        ctk.CTkLabel(self.dashboard_frame, text="Start/Stop Discord bot").grid(row=1, column=0)
        self.bot_switch = ctk.CTkSwitch(self.dashboard_frame, text="", command=self.toggle_bot)
        self.bot_switch.grid(row=1, column=1, sticky="nsew")
        # Connections
        ctk.CTkLabel(self.dashboard_frame, text="Connections", font=ctk.CTkFont(size=20, weight="bold"))\
            .grid(row=3, column=0, padx=10, pady=10, sticky="nw")
        for i, option in enumerate(config.parser.options("server")):
            url = config.parser.get("server", option)
            ctk.CTkLabel(self.dashboard_frame, text=option).grid(row=4+i, pady=5, column=0, sticky="new")
            test_res = ctk.CTkLabel(self.dashboard_frame, text="wating for test...")
            test_res.grid(row=4+i, pady=5, column=2, sticky="nw")
            ctk.CTkButton(self.dashboard_frame, text="test",
                command=lambda url=url, output=test_res: self.test_api_connection(url, output))\
                .grid(row=4+i, padx=10, pady=5, column=1, sticky="nw")
            if config.GUI.check_conn_before_open:
                self.test_api_connection(url, test_res)

    def create_settings_frame(self):
        self.settings_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.settings_frame, text="Settings", font=ctk.CTkFont(size=20, weight="bold"))\
            .grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        # config
        config_tabview = ctk.CTkTabview(self.settings_frame, anchor="w")
        config_tabview.grid(row=1, column=0, sticky="nsew")
        for section in config.parser.sections():
            section_tab = config_tabview.add(section)
            section_tab.grid_columnconfigure(0, weight=2)
            section_tab.grid_columnconfigure(1, weight=3)
            for i, option in enumerate(config.parser.options(section)):
                ctk.CTkLabel(section_tab, text=option).grid(row=i, column=0, sticky="nsew")
                option_input = ctk.CTkEntry(section_tab)
                option_input.grid(row=i, column=1, padx=10, sticky="nsew")
                option_input.insert(0, config.parser.get(section, option))
                option_input.bind("<Return>", 
                                  lambda event, s=section, o=option, ei=option_input: self.auto_save(s, o, ei))
        
    def auto_save(self, section, option, entry):
        new_val = entry.get()
        old_val = config.parser.get(section, option)
        if new_val == old_val: return
        config.parser.set(section, option, new_val)
        config.save()
        CTkMessagebox(master=self, message="change saved.", icon="check")
        logger.info(f"config {section}.{option} changed: {old_val} -> {new_val}")
        
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.dashboard_btn.configure(fg_color=("gray75", "gray25") if name == "dashboard" else "transparent")
        self.settings_btn.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")

        # show selected frame
        if name == "dashboard":
            self.dashboard_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.dashboard_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()
    
    def dashboard_btn_event(self):
        self.select_frame_by_name("dashboard")
        
    def settings_btn_event(self):
        self.select_frame_by_name("settings")
    
    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        config.parser.set("GUI", "appearance_mode", new_appearance_mode)
        config.save()
    
    def toggle_bot(self):
        if self.bot_switch.get() == 1:
            self.start_bot_event()
        else:
            self.stop_bot_event()
        
    def start_bot_event(self):
        self.bot_process = subprocess.Popen(
            [path("venv", "Scripts", "python.exe"), path("src", "main.py")],
        )
        logger.info(f"Discord bot starting")
            
    def stop_bot_event(self):
        self.bot_process.kill()
        logger.info("Discord bot stopped")

    def test_api_connection(self, url, ouput_widget):
        logger.info(f"'{url}' API connection testing...")
        try:
            response = requests.get(url, timeout=5)
            
            ouput_widget.configure(
                text="Connected",
                text_color="green"
            )
        except requests.RequestException as e:
            logger.error(f"API connect testing error: {e}")
            ouput_widget.configure(
                text=f"Disconnected",
                text_color="red"
            )
        finally:
            logger.info(f"'{url}' API connection comleted")
            

if __name__ == "__main__":
    try:
        gui = GUI()
        gui.mainloop()
    except:
        gui.stop_bot_event()