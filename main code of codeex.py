import customtkinter as ctk
from tkinter import messagebox, filedialog
import subprocess
import threading
import time
import requests
import json
import os
from datetime import datetime
import psutil
import pyttsx3
import re

class CodeexChat:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Codeex AI Chat - Powered by Ollama")
        self.window.geometry("1200x800")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Colors
        self.primary_color = "#1e3a8a"
        self.secondary_color = "#3b82f6"
        self.accent_color = "#60a5fa"
        self.bg_color = "#0f172a"
        self.chat_bg = "#1e293b"
        self.user_msg_color = "#3b82f6"
        self.ai_msg_color = "#64748b"
        
        # Variables
        self.conversation_history = []
        self.current_chat_file = None
        self.ollama_running = False
        self.model_name = "phi3:mini"
        self.tts_enabled = False
        self.tts_engine = None
        self.is_speaking = False
        self.available_models = []
        self.downloading_model = False
        
        # Initialize TTS
        self.init_tts()
        
        # Create directories
        os.makedirs("saved_chats", exist_ok=True)
        
        # Initialize UI
        self.setup_ui()
        
        # Auto-start Ollama
        self.auto_start_ollama()
        
    def init_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            # Set properties
            self.tts_engine.setProperty('rate', 150)  # Speed
            self.tts_engine.setProperty('volume', 0.9)  # Volume
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            # Set to female voice if available (usually index 1)
            if len(voices) > 1:
                self.tts_engine.setProperty('voice', voices[1].id)
        except Exception as e:
            print(f"TTS initialization error: {e}")
            self.tts_engine = None
    
    def speak_text(self, text):
        """Speak the given text"""
        if self.tts_enabled and self.tts_engine and not self.is_speaking:
            def speak():
                try:
                    self.is_speaking = True
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                    self.is_speaking = False
                except Exception as e:
                    print(f"TTS error: {e}")
                    self.is_speaking = False
            
            thread = threading.Thread(target=speak, daemon=True)
            thread.start()
    
    def stop_speaking(self):
        """Stop current speech"""
        if self.tts_engine and self.is_speaking:
            try:
                self.tts_engine.stop()
                self.is_speaking = False
            except:
                pass
    
    def toggle_tts(self):
        """Toggle text-to-speech on/off"""
        self.tts_enabled = not self.tts_enabled
        
        if self.tts_enabled:
            self.tts_button.configure(
                text="🔊 TTS: ON",
                fg_color="#059669"
            )
            if self.tts_engine:
                self.display_message("System", "🔊 Text-to-Speech enabled!", "system")
            else:
                self.display_message("System", "❌ TTS engine not available. Install pyttsx3.", "system")
                self.tts_enabled = False
        else:
            self.tts_button.configure(
                text="🔇 TTS: OFF",
                fg_color="#64748b"
            )
            self.stop_speaking()
            self.display_message("System", "🔇 Text-to-Speech disabled!", "system")
    
    def get_system_ram(self):
        """Get system RAM in GB"""
        try:
            ram_bytes = psutil.virtual_memory().total
            ram_gb = ram_bytes / (1024 ** 3)
            return ram_gb
        except:
            return 8  # Default assumption
    
    def get_recommended_models(self):
        """Get recommended models based on system RAM"""
        ram_gb = self.get_system_ram()
        
        models = {
            "tiny": ["phi3:mini", "tinyllama", "qwen2:0.5b"],
            "small": ["llama3.2:1b", "gemma2:2b", "phi3:medium"],
            "medium": ["llama3.2:3b", "gemma2:9b", "qwen2.5:7b", "mistral"],
            "large": ["llama3.1:8b", "llama3:8b", "mixtral:8x7b"],
            "xlarge": ["llama3.1:70b", "llama3:70b", "qwen2.5:72b"]
        }
        
        if ram_gb < 8:
            return models["tiny"], "Tiny Models (< 8GB RAM)"
        elif ram_gb < 16:
            return models["small"], "Small Models (8-16GB RAM)"
        elif ram_gb < 32:
            return models["medium"], "Medium Models (16-32GB RAM)"
        elif ram_gb < 64:
            return models["large"], "Large Models (32-64GB RAM)"
        else:
            return models["xlarge"], "XLarge Models (64GB+ RAM)"
    
    def get_installed_models(self):
        """Get list of installed models"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                models = []
                for line in lines:
                    if line.strip():
                        # Parse model name (first column)
                        parts = line.split()
                        if parts:
                            model_name = parts[0]
                            models.append(model_name)
                return models
            return []
        except Exception as e:
            print(f"Error getting models: {e}")
            return []
    
    def open_model_selector(self):
        """Open model selection and download window"""
        model_window = ctk.CTkToplevel(self.window)
        model_window.title("Model Selection - Codeex AI")
        model_window.geometry("700x600")
        model_window.configure(fg_color=self.bg_color)
        
        # Make it modal
        model_window.transient(self.window)
        model_window.grab_set()
        
        # Header
        header = ctk.CTkFrame(model_window, fg_color=self.primary_color, height=60)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="🤖 Model Selection & Download",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        title.pack(pady=15)
        
        # System Info
        ram_gb = self.get_system_ram()
        recommended_models, category = self.get_recommended_models()
        
        info_frame = ctk.CTkFrame(model_window, fg_color=self.chat_bg)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        info_text = f"💻 System RAM: {ram_gb:.1f} GB\n📊 Recommended Category: {category}"
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=13),
            text_color="#94a3b8",
            justify="left"
        )
        info_label.pack(pady=10, padx=10)
        
        # Tabs
        tabview = ctk.CTkTabview(model_window, fg_color=self.chat_bg)
        tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Installed Models Tab
        installed_tab = tabview.add("Installed Models")
        
        # Get installed models
        installed_models = self.get_installed_models()
        
        if installed_models:
            installed_scroll = ctk.CTkScrollableFrame(installed_tab, fg_color=self.bg_color)
            installed_scroll.pack(fill="both", expand=True, padx=10, pady=10)
            
            for model in installed_models:
                model_frame = ctk.CTkFrame(installed_scroll, fg_color=self.chat_bg)
                model_frame.pack(fill="x", pady=5, padx=5)
                
                model_label = ctk.CTkLabel(
                    model_frame,
                    text=f"📦 {model}",
                    font=ctk.CTkFont(size=14),
                    text_color="white",
                    anchor="w"
                )
                model_label.pack(side="left", padx=15, pady=10)
                
                select_btn = ctk.CTkButton(
                    model_frame,
                    text="Select",
                    width=100,
                    fg_color=self.secondary_color,
                    hover_color=self.accent_color,
                    command=lambda m=model: self.select_model(m, model_window)
                )
                select_btn.pack(side="right", padx=10, pady=5)
                
                # Highlight current model
                if model == self.model_name:
                    model_frame.configure(border_width=2, border_color="#059669")
                    select_btn.configure(text="✓ Current", fg_color="#059669")
        else:
            no_models_label = ctk.CTkLabel(
                installed_tab,
                text="No models installed.\nDownload from the 'Download Models' tab.",
                font=ctk.CTkFont(size=14),
                text_color="#94a3b8"
            )
            no_models_label.pack(pady=50)
        
        # Download Models Tab
        download_tab = tabview.add("Download Models")
        
        # Recommended models section
        recommended_label = ctk.CTkLabel(
            download_tab,
            text="⭐ Recommended for Your System:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        recommended_label.pack(pady=(10, 5), padx=10, anchor="w")
        
        recommended_scroll = ctk.CTkScrollableFrame(download_tab, fg_color=self.bg_color, height=150)
        recommended_scroll.pack(fill="x", padx=10, pady=5)
        
        for model in recommended_models:
            self.create_download_button(recommended_scroll, model, model_window, recommended=True)
        
        # All available models
        all_label = ctk.CTkLabel(
            download_tab,
            text="📚 Other Available Models:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        all_label.pack(pady=(15, 5), padx=10, anchor="w")
        
        all_models = [
            "llama3.2:1b", "llama3.2:3b", "llama3.1:8b", "llama3:8b", "llama3:70b",
            "phi3:mini", "phi3:medium", "gemma2:2b", "gemma2:9b",
            "qwen2.5:0.5b", "qwen2.5:7b", "qwen2.5:14b", "qwen2.5:72b",
            "mistral", "mixtral:8x7b", "codellama", "deepseek-coder",
            "tinyllama", "orca-mini", "neural-chat"
        ]
        
        all_scroll = ctk.CTkScrollableFrame(download_tab, fg_color=self.bg_color)
        all_scroll.pack(fill="both", expand=True, padx=10, pady=5)
        
        for model in all_models:
            if model not in installed_models:
                self.create_download_button(all_scroll, model, model_window, recommended=False)
        
        # Custom model input
        custom_frame = ctk.CTkFrame(download_tab, fg_color=self.chat_bg)
        custom_frame.pack(fill="x", padx=10, pady=10)
        
        custom_label = ctk.CTkLabel(
            custom_frame,
            text="Or enter custom model name:",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        custom_label.pack(pady=(10, 5), padx=10, anchor="w")
        
        custom_entry_frame = ctk.CTkFrame(custom_frame, fg_color="transparent")
        custom_entry_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        custom_entry = ctk.CTkEntry(
            custom_entry_frame,
            placeholder_text="e.g., llama3.2:1b",
            font=ctk.CTkFont(size=13),
            height=35
        )
        custom_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        custom_btn = ctk.CTkButton(
            custom_entry_frame,
            text="Download",
            width=120,
            height=35,
            fg_color="#7c3aed",
            hover_color="#8b5cf6",
            command=lambda: self.download_custom_model(custom_entry.get(), model_window)
        )
        custom_btn.pack(side="right")
        
        # Close button
        close_btn = ctk.CTkButton(
            model_window,
            text="Close",
            width=150,
            height=40,
            fg_color="#64748b",
            hover_color="#475569",
            command=model_window.destroy
        )
        close_btn.pack(pady=15)
    
    def create_download_button(self, parent, model_name, window, recommended=False):
        """Create a download button for a model"""
        model_frame = ctk.CTkFrame(parent, fg_color=self.chat_bg)
        model_frame.pack(fill="x", pady=3, padx=5)
        
        if recommended:
            model_frame.configure(border_width=1, border_color="#059669")
        
        label_text = f"{'⭐' if recommended else '📦'} {model_name}"
        model_label = ctk.CTkLabel(
            model_frame,
            text=label_text,
            font=ctk.CTkFont(size=13),
            text_color="white",
            anchor="w"
        )
        model_label.pack(side="left", padx=15, pady=8)
        
        download_btn = ctk.CTkButton(
            model_frame,
            text="Download",
            width=100,
            fg_color="#059669",
            hover_color="#10b981",
            command=lambda: self.download_model(model_name, window)
        )
        download_btn.pack(side="right", padx=10, pady=5)
    
    def select_model(self, model_name, window):
        """Select a model to use"""
        self.model_name = model_name
        self.display_message("System", f"✅ Switched to model: {model_name}", "system")
        window.destroy()
    
    def download_custom_model(self, model_name, window):
        """Download a custom model"""
        model_name = model_name.strip()
        if not model_name:
            messagebox.showwarning("Warning", "Please enter a model name!")
            return
        
        self.download_model(model_name, window)
    
    def download_model(self, model_name, window=None):
        """Download a model using ollama pull"""
        if self.downloading_model:
            messagebox.showinfo("Info", "Already downloading a model. Please wait...")
            return
        
        def download_thread():
            try:
                self.downloading_model = True
                self.display_message("System", f"📥 Downloading {model_name}... This may take several minutes.", "system")
                
                # Create progress window
                progress_window = ctk.CTkToplevel(self.window)
                progress_window.title("Downloading Model")
                progress_window.geometry("500x200")
                progress_window.configure(fg_color=self.bg_color)
                progress_window.transient(self.window)
                progress_window.grab_set()
                
                progress_label = ctk.CTkLabel(
                    progress_window,
                    text=f"Downloading {model_name}...\nPlease wait, this may take several minutes.",
                    font=ctk.CTkFont(size=14),
                    text_color="white"
                )
                progress_label.pack(pady=30)
                
                progress_bar = ctk.CTkProgressBar(progress_window, width=400)
                progress_bar.pack(pady=20)
                progress_bar.set(0)
                progress_bar.start()
                
                status_label = ctk.CTkLabel(
                    progress_window,
                    text="Downloading...",
                    font=ctk.CTkFont(size=12),
                    text_color="#94a3b8"
                )
                status_label.pack(pady=10)
                
                # Run download
                result = subprocess.run(
                    ['ollama', 'pull', model_name],
                    capture_output=True,
                    text=True
                )
                
                progress_bar.stop()
                progress_window.destroy()
                
                if result.returncode == 0:
                    self.display_message("System", f"✅ Successfully downloaded {model_name}!", "system")
                    self.model_name = model_name
                    messagebox.showinfo("Success", f"Model {model_name} downloaded successfully!\nIt's now set as your current model.")
                    if window:
                        window.destroy()
                else:
                    error_msg = result.stderr if result.stderr else "Unknown error"
                    self.display_message("System", f"❌ Failed to download {model_name}: {error_msg}", "system")
                    messagebox.showerror("Error", f"Failed to download model:\n{error_msg}")
                
            except Exception as e:
                self.display_message("System", f"❌ Error downloading model: {str(e)}", "system")
                messagebox.showerror("Error", f"Download failed:\n{str(e)}")
            finally:
                self.downloading_model = False
        
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
    
    def setup_ui(self):
        # Main container
        self.window.configure(fg_color=self.bg_color)
        
        # ==================== HEADER ====================
        header_frame = ctk.CTkFrame(self.window, fg_color=self.primary_color, height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Logo and Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚡ CODEEX AI CHAT",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=30, pady=20)
        
        # Model Selection Button
        self.model_button = ctk.CTkButton(
            header_frame,
            text=f"🤖 Model: {self.model_name}",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#7c3aed",
            hover_color="#8b5cf6",
            width=200,
            height=40,
            command=self.open_model_selector
        )
        self.model_button.pack(side="right", padx=(0, 20))
        
        # TTS Toggle Button in Header
        self.tts_button = ctk.CTkButton(
            header_frame,
            text="🔇 TTS: OFF",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#64748b",
            hover_color="#475569",
            width=120,
            height=40,
            command=self.toggle_tts
        )
        self.tts_button.pack(side="right", padx=(0, 10))
        
        # Status indicator
        self.status_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        self.status_frame.pack(side="right", padx=20)
        
        self.status_dot = ctk.CTkLabel(
            self.status_frame,
            text="●",
            font=ctk.CTkFont(size=24),
            text_color="red"
        )
        self.status_dot.pack(side="left", padx=5)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Initializing...",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        self.status_label.pack(side="left", padx=5)
        
        # ==================== SIDEBAR ====================
        sidebar = ctk.CTkFrame(self.window, width=280, fg_color=self.chat_bg)
        sidebar.pack(side="left", fill="y", padx=0, pady=0)
        sidebar.pack_propagate(False)
        
        # Sidebar title
        sidebar_title = ctk.CTkLabel(
            sidebar,
            text="💾 Chat History",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        sidebar_title.pack(pady=20, padx=20)
        
        # New Chat Button
        new_chat_btn = ctk.CTkButton(
            sidebar,
            text="➕ New Chat",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.secondary_color,
            hover_color=self.accent_color,
            height=40,
            command=self.new_chat
        )
        new_chat_btn.pack(pady=10, padx=20, fill="x")
        
        # Save Chat Button
        save_btn = ctk.CTkButton(
            sidebar,
            text="💾 Save Chat",
            font=ctk.CTkFont(size=14),
            fg_color="#059669",
            hover_color="#10b981",
            height=40,
            command=self.save_chat
        )
        save_btn.pack(pady=5, padx=20, fill="x")
        
        # Load Chat Button
        load_btn = ctk.CTkButton(
            sidebar,
            text="📂 Load Chat",
            font=ctk.CTkFont(size=14),
            fg_color="#7c3aed",
            hover_color="#8b5cf6",
            height=40,
            command=self.load_chat
        )
        load_btn.pack(pady=5, padx=20, fill="x")
        
        # Export Chat Button
        export_btn = ctk.CTkButton(
            sidebar,
            text="📄 Export to TXT",
            font=ctk.CTkFont(size=14),
            fg_color="#d97706",
            hover_color="#f59e0b",
            height=40,
            command=self.export_chat
        )
        export_btn.pack(pady=5, padx=20, fill="x")
        
        # Clear Chat Button
        clear_btn = ctk.CTkButton(
            sidebar,
            text="🗑️ Clear Display",
            font=ctk.CTkFont(size=14),
            fg_color="#dc2626",
            hover_color="#ef4444",
            height=40,
            command=self.clear_display
        )
        clear_btn.pack(pady=5, padx=20, fill="x")
        
        # Stop Speaking Button
        stop_speak_btn = ctk.CTkButton(
            sidebar,
            text="⏹️ Stop Speaking",
            font=ctk.CTkFont(size=14),
            fg_color="#f97316",
            hover_color="#fb923c",
            height=40,
            command=self.stop_speaking
        )
        stop_speak_btn.pack(pady=5, padx=20, fill="x")
        
        # Saved Chats List
        chats_label = ctk.CTkLabel(
            sidebar,
            text="Saved Conversations:",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        chats_label.pack(pady=(30, 10), padx=20, anchor="w")
        
        self.chats_listbox = ctk.CTkScrollableFrame(sidebar, fg_color="#0f172a")
        self.chats_listbox.pack(pady=5, padx=20, fill="both", expand=True)
        
        self.refresh_chat_list()
        
        # TTS Settings Frame
        tts_settings_frame = ctk.CTkFrame(sidebar, fg_color="#1e293b")
        tts_settings_frame.pack(pady=10, padx=20, fill="x")
        
        tts_settings_label = ctk.CTkLabel(
            tts_settings_frame,
            text="🎙️ Voice Settings",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white"
        )
        tts_settings_label.pack(pady=5)
        
        # Speed slider
        speed_label = ctk.CTkLabel(
            tts_settings_frame,
            text="Speed:",
            font=ctk.CTkFont(size=10),
            text_color="#94a3b8"
        )
        speed_label.pack(pady=(5, 0))
        
        self.speed_slider = ctk.CTkSlider(
            tts_settings_frame,
            from_=50,
            to=300,
            number_of_steps=25,
            command=self.update_tts_speed
        )
        self.speed_slider.set(150)
        self.speed_slider.pack(pady=5, padx=10, fill="x")
        
        # Volume slider
        volume_label = ctk.CTkLabel(
            tts_settings_frame,
            text="Volume:",
            font=ctk.CTkFont(size=10),
            text_color="#94a3b8"
        )
        volume_label.pack(pady=(5, 0))
        
        self.volume_slider = ctk.CTkSlider(
            tts_settings_frame,
            from_=0,
            to=1,
            number_of_steps=10,
            command=self.update_tts_volume
        )
        self.volume_slider.set(0.9)
        self.volume_slider.pack(pady=5, padx=10, fill="x")
        
        # Footer in sidebar
        footer_label = ctk.CTkLabel(
            sidebar,
            text="Created by heoster\n© 2024 Codeex",
            font=ctk.CTkFont(size=10),
            text_color="#64748b"
        )
        footer_label.pack(side="bottom", pady=15)
        
        # ==================== MAIN CHAT AREA ====================
        main_area = ctk.CTkFrame(self.window, fg_color=self.bg_color)
        main_area.pack(side="right", fill="both", expand=True, padx=0, pady=0)
        
        # Chat display
        chat_frame = ctk.CTkFrame(main_area, fg_color="transparent")
        chat_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            font=ctk.CTkFont(size=13),
            fg_color=self.chat_bg,
            text_color="white",
            wrap="word",
            state="disabled"
        )
        self.chat_display.pack(fill="both", expand=True)
        
        # Input area
        input_frame = ctk.CTkFrame(main_area, fg_color="transparent", height=100)
        input_frame.pack(fill="x", padx=20, pady=(0, 20))
        input_frame.pack_propagate(False)
        
        # Input field
        self.input_field = ctk.CTkTextbox(
            input_frame,
            font=ctk.CTkFont(size=14),
            fg_color=self.chat_bg,
            text_color="white",
            height=60,
            wrap="word"
        )
        self.input_field.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message_event)
        self.input_field.bind("<Shift-Return>", lambda e: None)
        
        # Send button
        send_btn = ctk.CTkButton(
            input_frame,
            text="Send ➤",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.secondary_color,
            hover_color=self.accent_color,
            width=120,
            height=60,
            command=self.send_message
        )
        send_btn.pack(side="right")
        
        # Welcome message
        self.display_message("System", "Welcome to Codeex AI Chat! 🚀\nInitializing Ollama service...", "system")
    
    def update_tts_speed(self, value):
        """Update TTS speech speed"""
        if self.tts_engine:
            self.tts_engine.setProperty('rate', int(value))
    
    def update_tts_volume(self, value):
        """Update TTS volume"""
        if self.tts_engine:
            self.tts_engine.setProperty('volume', float(value))
    
    def auto_start_ollama(self):
        """Automatically start Ollama and pull model"""
        def start_process():
            try:
                # Check if Ollama is already running
                if self.check_ollama_running():
                    self.update_status("Connected", "green")
                    self.display_message("System", "✅ Ollama service is already running!", "system")
                else:
                    self.display_message("System", "🔄 Starting Ollama service...", "system")
                    
                    # Start Ollama serve in background
                    if os.name == 'nt':  # Windows
                        subprocess.Popen(['ollama', 'serve'], 
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                    else:  # Linux/Mac
                        subprocess.Popen(['ollama', 'serve'], 
                                       stdout=subprocess.DEVNULL, 
                                       stderr=subprocess.DEVNULL)
                    
                    # Wait for service to start
                    time.sleep(3)
                    
                    if self.check_ollama_running():
                        self.update_status("Connected", "green")
                        self.display_message("System", "✅ Ollama service started successfully!", "system")
                    else:
                        self.update_status("Error", "red")
                        self.display_message("System", "❌ Failed to start Ollama. Please start it manually.", "system")
                        return
                
                # Check and pull model
                self.display_message("System", f"🔍 Checking for {self.model_name} model...", "system")
                
                if not self.check_model_exists():
                    self.display_message("System", f"📥 Downloading {self.model_name}... (This may take a while)", "system")
                    self.pull_model()
                else:
                    self.display_message("System", f"✅ Model {self.model_name} is ready!", "system")
                
                self.display_message("System", "🎉 All systems ready! Start chatting below.", "system")
                self.ollama_running = True
                
            except Exception as e:
                self.update_status("Error", "red")
                self.display_message("System", f"❌ Error: {str(e)}\nPlease install Ollama from: https://ollama.ai", "system")
        
        thread = threading.Thread(target=start_process, daemon=True)
        thread.start()
    
    def check_ollama_running(self):
        """Check if Ollama service is running"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def check_model_exists(self):
        """Check if model is already downloaded"""
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                return any(self.model_name in model.get('name', '') for model in models)
            return False
        except:
            return False
    
    def pull_model(self):
        """Pull the model"""
        try:
            subprocess.run(['ollama', 'pull', self.model_name], check=True)
            return True
        except:
            return False
    
    def update_status(self, text, color):
        """Update status indicator"""
        self.status_label.configure(text=text)
        self.status_dot.configure(text_color=color)
    
    def display_message(self, sender, message, msg_type="user"):
        """Display message in chat"""
        self.chat_display.configure(state="normal")
        
        timestamp = datetime.now().strftime("%H:%M")
        
        if msg_type == "system":
            self.chat_display.insert("end", f"\n[{timestamp}] 🔧 SYSTEM\n", "system_sender")
            self.chat_display.insert("end", f"{message}\n", "system_msg")
            self.chat_display.insert("end", "─" * 80 + "\n", "separator")
        elif msg_type == "user":
            self.chat_display.insert("end", f"\n[{timestamp}] 👤 YOU\n", "user_sender")
            self.chat_display.insert("end", f"{message}\n", "user_msg")
        else:  # AI
            self.chat_display.insert("end", f"\n[{timestamp}] 🤖 CODEEX AI\n", "ai_sender")
            self.chat_display.insert("end", f"{message}\n", "ai_msg")
            self.chat_display.insert("end", "─" * 80 + "\n", "separator")
            
            # Speak AI response if TTS is enabled
            if msg_type == "ai" and self.tts_enabled:
                self.speak_text(message)
        
        # Configure tags (without font parameter)
        self.chat_display.tag_config("system_sender", foreground="#fbbf24")
        self.chat_display.tag_config("system_msg", foreground="#fcd34d")
        self.chat_display.tag_config("user_sender", foreground="#60a5fa")
        self.chat_display.tag_config("user_msg", foreground="#93c5fd")
        self.chat_display.tag_config("ai_sender", foreground="#34d399")
        self.chat_display.tag_config("ai_msg", foreground="#d1d5db")
        self.chat_display.tag_config("separator", foreground="#374151")
        
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
    
    def send_message_event(self, event):
        """Handle Enter key press"""
        if not event.state & 0x1:  # Check if Shift is not pressed
            self.send_message()
            return "break"
    
    def send_message(self):
        """Send message to AI"""
        message = self.input_field.get("1.0", "end-1c").strip()
        
        if not message:
            return
        
        if not self.ollama_running:
            messagebox.showerror("Error", "Ollama service is not running!")
            return
        
        # Stop any ongoing speech
        self.stop_speaking()
        
        # Clear input
        self.input_field.delete("1.0", "end")
        
        # Display user message
        self.display_message("You", message, "user")
        
        # Add to history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Update model button text
        self.model_button.configure(text=f"🤖 Model: {self.model_name}")
        
        # Get AI response in thread
        thread = threading.Thread(target=self.get_ai_response, args=(message,), daemon=True)
        thread.start()
    
    def get_ai_response(self, message):
        """Get response from Ollama"""
        try:
            url = "http://localhost:11434/api/chat"
            
            data = {
                "model": self.model_name,
                "messages": self.conversation_history,
                "stream": True
            }
            
            response = requests.post(url, json=data, stream=True)
            
            full_response = ""
            
            # Add initial AI message header
            timestamp = datetime.now().strftime("%H:%M")
            self.window.after(0, lambda: self.start_ai_message(timestamp))
            
            # Stream response
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    if 'message' in json_response:
                        content = json_response['message'].get('content', '')
                        full_response += content
                        
                        # Update display in real-time
                        self.window.after(0, lambda c=content: self.append_to_last_message(c))
            
            # Add to history
            self.conversation_history.append({"role": "assistant", "content": full_response})
            
            # Add separator
            self.window.after(0, lambda: self.add_separator())
            
            # Speak the full response if TTS is enabled
            if self.tts_enabled and full_response:
                self.window.after(100, lambda: self.speak_text(full_response))
            
        except Exception as e:
            self.window.after(0, lambda: self.display_message("System", f"❌ Error: {str(e)}", "system"))
    
    def start_ai_message(self, timestamp):
        """Start a new AI message"""
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"\n[{timestamp}] 🤖 CODEEX AI\n", "ai_sender")
        self.chat_display.tag_config("ai_sender", foreground="#34d399")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
    
    def append_to_last_message(self, content):
        """Append content to last message (for streaming)"""
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", content, "ai_msg")
        self.chat_display.tag_config("ai_msg", foreground="#d1d5db")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
    
    def add_separator(self):
        """Add separator line"""
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", "\n" + "─" * 80 + "\n", "separator")
        self.chat_display.tag_config("separator", foreground="#374151")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
    
    def new_chat(self):
        """Start a new chat"""
        if len(self.conversation_history) > 0:
            if messagebox.askyesno("New Chat", "Start a new conversation? Current chat will be lost if not saved."):
                self.stop_speaking()
                self.conversation_history = []
                self.current_chat_file = None
                self.chat_display.configure(state="normal")
                self.chat_display.delete("1.0", "end")
                self.chat_display.configure(state="disabled")
                self.display_message("System", "New conversation started! 🎉", "system")
        else:
            self.stop_speaking()
            self.conversation_history = []
            self.current_chat_file = None
            self.chat_display.configure(state="normal")
            self.chat_display.delete("1.0", "end")
            self.chat_display.configure(state="disabled")
            self.display_message("System", "New conversation started! 🎉", "system")
    
    def clear_display(self):
        """Clear chat display without clearing history"""
        self.stop_speaking()
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self.display_message("System", "Display cleared! Conversation history maintained.", "system")
    
    def save_chat(self):
        """Save current chat"""
        if not self.conversation_history:
            messagebox.showinfo("Info", "No conversation to save!")
            return
        
        filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join("saved_chats", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
        
        self.current_chat_file = filepath
        self.refresh_chat_list()
        messagebox.showinfo("Success", f"Chat saved as:\n{filename}")
    
    def load_chat(self):
        """Load a saved chat"""
        filepath = filedialog.askopenfilename(
            initialdir="saved_chats",
            title="Select chat file",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.conversation_history = json.load(f)
                
                self.current_chat_file = filepath
                
                # Display loaded conversation
                self.chat_display.configure(state="normal")
                self.chat_display.delete("1.0", "end")
                self.chat_display.configure(state="disabled")
                
                for msg in self.conversation_history:
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    
                    if role == 'user':
                        self.display_message("You", content, "user")
                    else:
                        self.display_message("AI", content, "ai")
                
                messagebox.showinfo("Success", "Chat loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load chat:\n{str(e)}")
    
    def export_chat(self):
        """Export chat to text file"""
        if not self.conversation_history:
            messagebox.showinfo("Info", "No conversation to export!")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
            initialfile=f"codeex_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write("=" * 80 + "\n")
                    f.write("CODEEX AI CHAT TRANSCRIPT\n")
                    f.write(f"Created by: heoster\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Model: {self.model_name}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    for msg in self.conversation_history:
                        role = "YOU" if msg.get('role') == 'user' else "CODEEX AI"
                        content = msg.get('content', '')
                        f.write(f"{role}:\n{content}\n\n")
                        f.write("-" * 80 + "\n\n")
                
                messagebox.showinfo("Success", f"Chat exported to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export chat:\n{str(e)}")
    
    def refresh_chat_list(self):
        """Refresh the list of saved chats"""
        # Clear existing items
        for widget in self.chats_listbox.winfo_children():
            widget.destroy()
        
        # Get saved chats
        if os.path.exists("saved_chats"):
            chats = sorted([f for f in os.listdir("saved_chats") if f.endswith('.json')], reverse=True)
            
            for chat_file in chats[:10]:  # Show last 10 chats
                chat_btn = ctk.CTkButton(
                    self.chats_listbox,
                    text=chat_file.replace('chat_', '').replace('.json', ''),
                    font=ctk.CTkFont(size=11),
                    fg_color="#1e293b",
                    hover_color="#334155",
                    height=30,
                    anchor="w",
                    command=lambda f=chat_file: self.load_specific_chat(f)
                )
                chat_btn.pack(pady=2, padx=5, fill="x")
    
    def load_specific_chat(self, filename):
        """Load a specific chat file"""
        filepath = os.path.join("saved_chats", filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
            
            self.current_chat_file = filepath
            
            # Display loaded conversation
            self.chat_display.configure(state="normal")
            self.chat_display.delete("1.0", "end")
            self.chat_display.configure(state="disabled")
            
            for msg in self.conversation_history:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                
                if role == 'user':
                    self.display_message("You", content, "user")
                else:
                    self.display_message("AI", content, "ai")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load chat:\n{str(e)}")
    
    def run(self):
        """Run the application"""
        self.window.mainloop()

# Run the application
if __name__ == "__main__":
    app = CodeexChat()
    app.run()
