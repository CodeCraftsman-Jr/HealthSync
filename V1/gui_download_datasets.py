import os
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
import time
from kaggle.api.kaggle_api_extended import KaggleApi

DATASETS = [
    {
        'name': 'Chest X-ray',
        'kaggle': 'paultimothymooney/chest-xray-pneumonia',
        'dir': 'data/chest_xray',
        'file': 'chest-xray-pneumonia.zip'
    },
    {
        'name': 'ISIC Skin Lesion',
        'kaggle': 'kmader/skin-cancer-mnist-ham10000',
        'dir': 'data/isic',
        'file': 'skin-cancer-mnist-ham10000.zip'
    },
    {
        'name': 'Brain MRI',
        'kaggle': 'navoneel/brain-mri-images-for-brain-tumor-detection',
        'dir': 'data/brain_mri',
        'file': 'brain-mri-images-for-brain-tumor-detection.zip'
    },
]

class DownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Medical Dataset Downloader")
        self.status_labels = []
        self.buttons = []
        self.api = KaggleApi()
        self.api.authenticate()

        tk.Label(master, text="Download Medical Image Datasets from Kaggle", font=("Arial", 14, "bold")).pack(pady=10)
        for idx, ds in enumerate(DATASETS):
            frame = tk.Frame(master)
            frame.pack(fill=tk.X, padx=10, pady=5)
            label = tk.Label(frame, text=ds['name'], width=25, anchor='w')
            label.pack(side=tk.LEFT)
            status = tk.Label(frame, text="Ready", width=20, anchor='w')
            status.pack(side=tk.LEFT)
            btn = tk.Button(frame, text="Download", command=lambda i=idx: self.download_thread(i))
            btn.pack(side=tk.LEFT)
            self.status_labels.append(status)
            self.buttons.append(btn)
        tk.Button(master, text="Download All", command=self.download_all_thread).pack(pady=10)
        # Log window
        self.log = scrolledtext.ScrolledText(master, height=12, width=70, state='disabled', font=("Consolas", 9))
        self.log.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def log_message(self, msg):
        self.log.configure(state='normal')
        self.log.insert(tk.END, msg + '\n')
        self.log.see(tk.END)
        self.log.configure(state='disabled')
        self.master.update_idletasks()

    def download_thread(self, idx):
        threading.Thread(target=self.download_dataset, args=(idx,), daemon=True).start()

    def download_all_thread(self):
        threading.Thread(target=self.download_all, daemon=True).start()

    def download_dataset(self, idx):
        ds = DATASETS[idx]
        self.status_labels[idx]["text"] = "Downloading..."
        self.log_message(f"Starting download: {ds['name']}")
        try:
            os.makedirs(ds['dir'], exist_ok=True)
            # Get Kaggle dataset file list for size (use 'size' attribute)
            file_list = self.api.dataset_list_files(ds['kaggle']).files
            total_bytes = sum([getattr(f, 'size', 0) for f in file_list])
            if total_bytes == 0:
                self.log_message("Warning: Could not determine total size (dataset may be old or API limitation). Progress will show downloaded size only.")
            else:
                self.log_message(f"Total size: {total_bytes/1e6:.2f} MB")
            start_time = time.time()
            # Start download in background and monitor file size
            self.api.dataset_download_files(ds['kaggle'], path=ds['dir'], unzip=True, quiet=True)
            # Progress monitor: check zip file size every second
            zip_path = os.path.join(ds['dir'], ds['file'])
            prev_size = 0
            wait_time = 0
            while True:
                if os.path.exists(zip_path):
                    curr_size = os.path.getsize(zip_path)
                    elapsed = time.time() - start_time
                    speed = (curr_size-prev_size)/1024 if elapsed > 0 else 0
                    if total_bytes > 0:
                        percent = min(100, curr_size/total_bytes*100)
                        self.log_message(f"{ds['name']} - Downloaded: {curr_size/1e6:.2f} MB ({percent:.1f}%), Speed: {speed:.2f} KB/s")
                        if percent >= 100 or curr_size >= total_bytes:
                            break
                    else:
                        self.log_message(f"{ds['name']} - Downloaded: {curr_size/1e6:.2f} MB, Speed: {speed:.2f} KB/s")
                        # If file size hasn't changed for 30s, assume done
                        if curr_size == prev_size:
                            wait_time += 1
                        else:
                            wait_time = 0
                        if wait_time > 30:
                            break
                    prev_size = curr_size
                else:
                    wait_time += 1
                    if wait_time > 60:
                        self.log_message(f"Timeout: Download file did not appear for {ds['name']} after 60 seconds.")
                        break
                time.sleep(1)
            self.status_labels[idx]["text"] = "Downloaded"
            self.log_message(f"{ds['name']} download complete! Extracting...")
            self.log_message(f"{ds['name']} extracted to {ds['dir']}")
        except Exception as e:
            self.status_labels[idx]["text"] = f"Error"
            self.log_message(f"Error downloading {ds['name']}: {e}")
            messagebox.showerror("Download Error", f"{ds['name']} failed: {e}")

    def download_all(self):
        for idx in range(len(DATASETS)):
            self.download_dataset(idx)

if __name__ == "__main__":
    root = tk.Tk()
    gui = DownloaderGUI(root)
    root.mainloop()
