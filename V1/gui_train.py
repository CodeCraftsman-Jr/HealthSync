import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import sys
import io
import yaml
import re
from datasets import get_dataset
from utils.model import get_model
from utils.train import train_model

class TrainingLogger(io.StringIO):
    def __init__(self, text_widget, progress_label=None):
        super().__init__()
        self.text_widget = text_widget
        self.progress_label = progress_label
        self.ansi_escape = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')
        self.last_epoch = None
        self.last_step = None

    def write(self, s):
        # Remove ANSI codes and carriage returns
        clean = self.ansi_escape.sub('', s.replace('\r', ''))
        # Extract epoch/step info for progress label
        epoch_match = re.search(r"Epoch (\d+)/(\d+)", clean)
        step_match = re.search(r"\s*(\d+)/(\d+).* - accuracy: ([0-9.]+) - loss: ([0-9.eE+-]+)", clean)
        if epoch_match and self.progress_label:
            self.last_epoch = f"Epoch {epoch_match.group(1)} / {epoch_match.group(2)}"
            self.progress_label.config(text=self.last_epoch)
        if step_match and self.progress_label:
            self.last_step = f"Step {step_match.group(1)} / {step_match.group(2)} | Accuracy: {step_match.group(3)} | Loss: {step_match.group(4)}"
            self.progress_label.config(text=f"{self.last_epoch or ''} | {self.last_step}")
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, clean)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')
        self.text_widget.update_idletasks()

    def flush(self):
        pass

class TrainGUI:
    def __init__(self, master):
        self.master = master
        master.title("Model Training GUI")
        tk.Label(master, text="Medical Image Classifier Training", font=("Arial", 14, "bold")).pack(pady=10)
        self.progress_label = tk.Label(master, text="", font=("Arial", 12))
        self.progress_label.pack(pady=3)
        self.start_btn = tk.Button(master, text="Start Training", command=self.start_training_thread)
        self.start_btn.pack(pady=5)
        self.log = scrolledtext.ScrolledText(master, height=20, width=80, state='disabled', font=("Consolas", 10))
        self.log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def start_training_thread(self):
        self.start_btn.config(state='disabled')
        threading.Thread(target=self.train_model_with_logs, daemon=True).start()

    def train_model_with_logs(self):
        # Redirect stdout/stderr to GUI
        logger = TrainingLogger(self.log, self.progress_label)
        sys.stdout = logger
        sys.stderr = logger
        try:
            with open('config.yaml') as f:
                config = yaml.safe_load(f)
            dataset = get_dataset(config['dataset'], config)
            model = get_model(config['model'])
            train_model(model, dataset, config['training'])
            print("\nTraining complete!")
        except Exception as e:
            print(f"\nError: {e}")
            messagebox.showerror("Training Error", str(e))
        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            self.start_btn.config(state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    gui = TrainGUI(root)
    root.mainloop()
