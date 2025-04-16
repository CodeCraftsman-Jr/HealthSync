import os
import yaml
from utils.model import get_model
from utils.gradcam import generate_gradcam

# Always use config.yaml in the same directory as this script
config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
if not os.path.exists(config_path):
    # Create a default config if missing
    with open(config_path, 'w') as f:
        f.write('''dataset: chest_xray\nmodel:\n  name: basic_cnn\n  input_shape: [224, 224, 3]\n  num_classes: 2\ntraining:\n  batch_size: 32\n  epochs: 10\n  learning_rate: 0.0001\n''')

with open(config_path) as f:
    config = yaml.safe_load(f)

model = get_model(config['model'])
generate_gradcam(model, config)
