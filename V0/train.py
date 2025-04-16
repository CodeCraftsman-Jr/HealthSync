import yaml
from datasets import get_dataset
from utils.model import get_model
from utils.train import train_model

with open('config.yaml') as f:
    config = yaml.safe_load(f)

dataset = get_dataset(config['dataset'], config)
model = get_model(config['model'])
train_model(model, dataset, config['training'])
