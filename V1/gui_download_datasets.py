import os
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
import time
from kaggle.api.kaggle_api_extended import KaggleApi

DATASETS = [
    # Existing datasets
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
    # Respiratory conditions
    {
        'name': 'COVID-19 X-rays',
        'kaggle': 'tawsifurrahman/covid19-radiography-database',
        'dir': 'data/covid19_xray',
        'file': 'covid19-radiography-database.zip'
    },
    {
        'name': 'Tuberculosis X-rays',
        'kaggle': 'tawsifurrahman/tuberculosis-tb-chest-xray-dataset',
        'dir': 'data/tb_xray',
        'file': 'tuberculosis-tb-chest-xray-dataset.zip'
    },
    {
        'name': 'Lung Cancer CT',
        'kaggle': 'mohamedhanyyy/chest-ctscan-images',
        'dir': 'data/lung_cancer_ct',
        'file': 'chest-ctscan-images.zip'
    },
    # Neurological conditions
    {
        'name': 'Alzheimer MRI',
        'kaggle': 'sachinkumar413/alzheimer-mri-dataset',
        'dir': 'data/alzheimer_mri',
        'file': 'alzheimer-mri-dataset.zip'
    },
    {
        'name': 'Stroke CT',
        'kaggle': 'felipekitamura/stroke-ct',
        'dir': 'data/stroke_ct',
        'file': 'stroke-ct.zip'
    },
    {
        'name': 'Parkinson Disease',
        'kaggle': 'kmader/parkinsons-drawings',
        'dir': 'data/parkinsons',
        'file': 'parkinsons-drawings.zip'
    },
    # Cardiovascular conditions
    {
        'name': 'Heart Disease ECG',
        'kaggle': 'shayanfazeli/heartbeat',
        'dir': 'data/heart_ecg',
        'file': 'heartbeat.zip'
    },
    {
        'name': 'Coronary Artery CT',
        'kaggle': 'aysendegerli/coronary-artery-disease',
        'dir': 'data/coronary_artery',
        'file': 'coronary-artery-disease.zip'
    },
    {
        'name': 'Cardiac MRI',
        'kaggle': 'andrewmvd/cardiac-mri',
        'dir': 'data/cardiac_mri',
        'file': 'cardiac-mri.zip'
    },
    # Gastrointestinal conditions
    {
        'name': 'Liver Ultrasound',
        'kaggle': 'yousefessam/liver-ultrasound-dataset',
        'dir': 'data/liver_ultrasound',
        'file': 'liver-ultrasound-dataset.zip'
    },
    {
        'name': 'Colon Cancer Histology',
        'kaggle': 'andrewmvd/cancer-hist',
        'dir': 'data/colon_cancer',
        'file': 'cancer-hist.zip'
    },
    {
        'name': 'Gastric Cancer Endoscopy',
        'kaggle': 'francismon/endoscopic-images',
        'dir': 'data/gastric_endoscopy',
        'file': 'endoscopic-images.zip'
    },
    # Dermatological conditions
    {
        'name': 'Melanoma Classification',
        'kaggle': 'shonenkov/melanoma-merged-external-data-512x512-jpeg',
        'dir': 'data/melanoma',
        'file': 'melanoma-merged-external-data-512x512-jpeg.zip'
    },
    {
        'name': 'Skin Disease Classification',
        'kaggle': 'shubhamgoel27/dermnet',
        'dir': 'data/skin_disease',
        'file': 'dermnet.zip'
    },
    {
        'name': 'Psoriasis Images',
        'kaggle': 'fanconic/skin-cancer-malignant-vs-benign',
        'dir': 'data/psoriasis',
        'file': 'skin-cancer-malignant-vs-benign.zip'
    },
    # Ophthalmological conditions
    {
        'name': 'Diabetic Retinopathy',
        'kaggle': 'tanlikesmath/diabetic-retinopathy-resized',
        'dir': 'data/diabetic_retinopathy',
        'file': 'diabetic-retinopathy-resized.zip'
    },
    {
        'name': 'Glaucoma Detection',
        'kaggle': 'sshikamaru/glaucoma-detection',
        'dir': 'data/glaucoma',
        'file': 'glaucoma-detection.zip'
    },
    {
        'name': 'Cataract Detection',
        'kaggle': 'jr2ngb/cataractdataset',
        'dir': 'data/cataract',
        'file': 'cataractdataset.zip'
    },
    # Orthopedic conditions
    {
        'name': 'Knee X-ray',
        'kaggle': 'shashwatwork/knee-osteoarthritis-dataset-with-severity',
        'dir': 'data/knee_xray',
        'file': 'knee-osteoarthritis-dataset-with-severity.zip'
    },
    {
        'name': 'Bone Fracture X-ray',
        'kaggle': 'vuppalaadithyasairam/bone-fracture-detection-using-xrays',
        'dir': 'data/bone_fracture',
        'file': 'bone-fracture-detection-using-xrays.zip'
    },
    {
        'name': 'Spine MRI',
        'kaggle': 'ahmedhamada0/brain-tumor-detection',
        'dir': 'data/spine_mri',
        'file': 'brain-tumor-detection.zip'
    },
    # Dental conditions
    {
        'name': 'Dental X-ray',
        'kaggle': 'tawsifurrahman/dental-panoramic-xray',
        'dir': 'data/dental_xray',
        'file': 'dental-panoramic-xray.zip'
    },
    {
        'name': 'Dental Caries',
        'kaggle': 'iarunava/dental-caries',
        'dir': 'data/dental_caries',
        'file': 'dental-caries.zip'
    },
    {
        'name': 'Oral Cancer',
        'kaggle': 'stefanodangelo/oral-cancer-dataset',
        'dir': 'data/oral_cancer',
        'file': 'oral-cancer-dataset.zip'
    },
    # Endocrine conditions
    {
        'name': 'Thyroid Ultrasound',
        'kaggle': 'ahmedhamada0/brain-tumor-detection',
        'dir': 'data/thyroid_ultrasound',
        'file': 'brain-tumor-detection.zip'
    },
    {
        'name': 'Diabetes Retinal Screening',
        'kaggle': 'amanneo/diabetic-retinopathy-detection',
        'dir': 'data/diabetes_retinal',
        'file': 'diabetic-retinopathy-detection.zip'
    },
    # Gynecological conditions
    {
        'name': 'Cervical Cancer',
        'kaggle': 'eduardoabasololopez/cervical-cancer-screening',
        'dir': 'data/cervical_cancer',
        'file': 'cervical-cancer-screening.zip'
    },
    {
        'name': 'Breast Cancer Histology',
        'kaggle': 'paultimothymooney/breast-histopathology-images',
        'dir': 'data/breast_cancer',
        'file': 'breast-histopathology-images.zip'
    },
    {
        'name': 'Breast Mammography',
        'kaggle': 'cheddad/miniddsm2',
        'dir': 'data/breast_mammography',
        'file': 'miniddsm2.zip'
    },
    # Urological conditions
    {
        'name': 'Kidney Stone CT',
        'kaggle': 'nazmul0087/ct-kidney-dataset-normal-cyst-tumor-and-stone',
        'dir': 'data/kidney_stone',
        'file': 'ct-kidney-dataset-normal-cyst-tumor-and-stone.zip'
    },
    {
        'name': 'Prostate Cancer MRI',
        'kaggle': 'ahmedhamada0/brain-tumor-detection',
        'dir': 'data/prostate_cancer',
        'file': 'brain-tumor-detection.zip'
    },
    # Pediatric conditions
    {
        'name': 'Pediatric Pneumonia',
        'kaggle': 'andrewmvd/pediatric-pneumonia-chest-xray',
        'dir': 'data/pediatric_pneumonia',
        'file': 'pediatric-pneumonia-chest-xray.zip'
    },
    {
        'name': 'Childhood Bone Age',
        'kaggle': 'kmader/rsna-bone-age',
        'dir': 'data/bone_age',
        'file': 'rsna-bone-age.zip'
    },
    # Infectious diseases
    {
        'name': 'Malaria Cell Images',
        'kaggle': 'iarunava/cell-images-for-detecting-malaria',
        'dir': 'data/malaria',
        'file': 'cell-images-for-detecting-malaria.zip'
    },
    {
        'name': 'COVID-19 CT Scans',
        'kaggle': 'plameneduardo/sarscov2-ctscan-dataset',
        'dir': 'data/covid19_ct',
        'file': 'sarscov2-ctscan-dataset.zip'
    },
    # Hematological conditions
    {
        'name': 'Blood Cell Classification',
        'kaggle': 'paultimothymooney/blood-cells',
        'dir': 'data/blood_cells',
        'file': 'blood-cells.zip'
    },
    {
        'name': 'Leukemia Classification',
        'kaggle': 'andrewmvd/leukemia-classification',
        'dir': 'data/leukemia',
        'file': 'leukemia-classification.zip'
    },
    # Miscellaneous
    {
        'name': 'Ultrasound Nerve Segmentation',
        'kaggle': 'c2cult/ultrasound-nerve-segmentation',
        'dir': 'data/nerve_ultrasound',
        'file': 'ultrasound-nerve-segmentation.zip'
    },
    {
        'name': 'Medical MNIST',
        'kaggle': 'andrewmvd/medical-mnist',
        'dir': 'data/medical_mnist',
        'file': 'medical-mnist.zip'
    },
    {
        'name': 'CT Liver Segmentation',
        'kaggle': 'andrewmvd/ct-liver-segmentation',
        'dir': 'data/liver_segmentation',
        'file': 'ct-liver-segmentation.zip'
    },
    {
        'name': 'MRI Brain Segmentation',
        'kaggle': 'mateuszbuda/lgg-mri-segmentation',
        'dir': 'data/brain_segmentation',
        'file': 'lgg-mri-segmentation.zip'
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
