#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digital Clock: Multi-Timezone Display
======================================
A real-time clock application that displays current time across multiple time zones
with customizable timezone selection and 24-hour format support.

Features:
- Real-time clock updates
- Multiple timezone support
- 12/24-hour format toggle
- Clean, readable display
- Threading for smooth updates
"""

import time
import threading
from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones
import customtkinter as ctk
from typing import List, Dict


class TimeZoneClock:
    """Main clock application using CustomTkinter."""
    
    # Popular timezones for quick access
    POPULAR_TIMEZONES = [
        "UTC",
        "US/Eastern",
        "US/Central",
        "US/Mountain",
        "US/Pacific",
        "Europe/London",
        "Europe/Paris",
        "Europe/Tokyo",
        "Asia/Shanghai",
        "Asia/Dubai",
        "Asia/Kolkata",
        "Asia/Singapore",
        "Australia/Sydney",
        "Australia/Melbourne",
        "Pacific/Auckland",
    ]
    
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock - Multi-Timezone")
        self.root.geometry("900x700")
        self.root.configure(fg_color="#1a1a1a")
        
        # Configuration
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # State
        self.timezone_labels: Dict[str, ctk.CTkLabel] = {}
        self.selected_timezones: List[str] = self.POPULAR_TIMEZONES[:6]
        self.is_24hour = True
        self.running = True
        self.update_thread = None
        
        # Build UI
        self._build_ui()
        
        # Start update loop
        self.start_clock()
    
    def _build_ui(self):
        """Construct the UI layout."""
        
        # Header
        header = ctk.CTkLabel(
            self.root,
            text="⏰ Global Time Zone Clock",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#00d4ff"
        )
        header.pack(pady=(20, 10))
        
        # Control Panel
        control_frame = ctk.CTkFrame(self.root, fg_color="#2a2a2a", corner_radius=10)
        control_frame.pack(padx=20, pady=10, fill="x")
        
        # Format Toggle
        format_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        format_frame.pack(side="left", padx=15, pady=10)
        
        format_label = ctk.CTkLabel(
            format_frame,
            text="Format:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        format_label.pack(side="left", padx=(0, 10))
        
        self.format_var = ctk.StringVar(value="24h")
        format_switch = ctk.CTkSwitch(
            format_frame,
            text="24-Hour",
            variable=self.format_var,
            onvalue="24h",
            offvalue="12h",
            command=self._toggle_format
        )
        format_switch.pack(side="left")
        
        # Timezone Selector
        selector_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        selector_frame.pack(side="right", padx=15, pady=10)
        
        selector_label = ctk.CTkLabel(
            selector_frame,
            text="Add Timezone:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        selector_label.pack(side="left", padx=(0, 10))
        
        available = sorted(list(available_timezones()))
        self.tz_menu = ctk.CTkComboBox(
            selector_frame,
            values=available,
            width=150,
            command=self._add_timezone
        )
        self.tz_menu.set("Select timezone")
        self.tz_menu.pack(side="left")
        
        # Main Clock Display
        self.clock_frame = ctk.CTkFrame(self.root, fg_color="#2a2a2a", corner_radius=15)
        self.clock_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Scrollable frame for timezones
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.clock_frame,
            fg_color="#2a2a2a",
            label_text="Active Timezones",
            label_font=ctk.CTkFont(size=14, weight="bold")
        )
        self.scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Initialize timezone displays
        self._update_timezone_displays()
    
    def _update_timezone_displays(self):
        """Create or update timezone display labels."""
        # Clear existing labels
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.timezone_labels.clear()
        
        # Create new labels for each selected timezone
        for tz in self.selected_timezones:
            tz_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#1a1a1a", corner_radius=10)
            tz_frame.pack(fill="x", pady=10, padx=10)
            
            # Timezone name
            name_label = ctk.CTkLabel(
                tz_frame,
                text=tz,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#00d4ff"
            )
            name_label.pack(anchor="w", padx=15, pady=(10, 5))
            
            # Time display
            time_label = ctk.CTkLabel(
                tz_frame,
                text="--:--:--",
                font=ctk.CTkFont(size=48, weight="bold"),
                text_color="#ffffff"
            )
            time_label.pack(anchor="w", padx=15, pady=(5, 10))
            
            self.timezone_labels[tz] = time_label
            
            # Delete button
            def make_delete_func(timezone):
                def delete_tz():
                    if timezone in self.selected_timezones:
                        self.selected_timezones.remove(timezone)
                        self._update_timezone_displays()
                return delete_tz
            
            btn_frame = ctk.CTkFrame(tz_frame, fg_color="transparent")
            btn_frame.pack(anchor="e", padx=15, pady=(0, 10))
            
            delete_btn = ctk.CTkButton(
                btn_frame,
                text="Remove",
                width=80,
                fg_color="#ff4444",
                hover_color="#cc0000",
                command=make_delete_func(tz)
            )
            delete_btn.pack()
    
    def _add_timezone(self, tz: str):
        """Add a new timezone to the display."""
        if tz and tz != "Select timezone" and tz not in self.selected_timezones:
            self.selected_timezones.append(tz)
            self._update_timezone_displays()
            self.tz_menu.set("Select timezone")
    
    def _toggle_format(self):
        """Toggle between 12-hour and 24-hour format."""
        self.is_24hour = self.format_var.get() == "24h"
    
    def _format_time(self, dt: datetime) -> str:
        """Format datetime according to selected format."""
        if self.is_24hour:
            return dt.strftime("%H:%M:%S")
        else:
            return dt.strftime("%I:%M:%S %p")
    
    def _update_clocks(self):
        """Update all clock displays."""
        while self.running:
            try:
                for tz in self.selected_timezones:
                    if tz in self.timezone_labels:
                        try:
                            zone = ZoneInfo(tz)
                            current_time = datetime.now(zone)
                            time_str = self._format_time(current_time)
                            self.timezone_labels[tz].configure(text=time_str)
                        except Exception as e:
                            print(f"Error updating {tz}: {e}")
                
                time.sleep(1)
            except Exception as e:
                print(f"Clock update error: {e}")
                break
    
    def start_clock(self):
        """Start the clock update thread."""
        self.update_thread = threading.Thread(target=self._update_clocks, daemon=True)
        self.update_thread.start()
    
    def stop_clock(self):
        """Stop the clock update thread."""
        self.running = False
        if self.update_thread:
            self.update_thread.join(timeout=2)
    
    def on_closing(self):
        """Handle window close event."""
        self.stop_clock()
        self.root.destroy()


def main():
    """Launch the timezone clock application."""
    print("🕐 Launching Multi-Timezone Digital Clock...")
    
    root = ctk.CTk()
    app = TimeZoneClock(root)
    
    # Handle window close
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
