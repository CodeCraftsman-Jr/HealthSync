import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

def download_and_unzip(dataset, kaggle_name, target_dir, file_name=None):
    os.makedirs(target_dir, exist_ok=True)
    api = KaggleApi()
    api.authenticate()
    
    if file_name is None:
        file_name = kaggle_name.split('/')[-1] + '.zip'
    zip_path = os.path.join(target_dir, file_name)
    
    if not os.path.exists(zip_path):
        print(f"Downloading {dataset} from Kaggle...")
        api.dataset_download_files(kaggle_name, path=target_dir, unzip=True)
    else:
        print(f"{file_name} already downloaded.")
        # Unzip if not already unzipped
        if not any(os.scandir(target_dir)):
            print("Unzipping existing file...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(target_dir)
    print(f"{dataset} extracted to {target_dir}")

def main():
    datasets = [
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
    for d in datasets:
        download_and_unzip(d['name'], d['kaggle'], d['dir'], d['file'])

if __name__ == "__main__":
    main()
