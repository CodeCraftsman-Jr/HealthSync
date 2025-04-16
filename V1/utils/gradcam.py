import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import urllib.request

def generate_gradcam(model, config):
    import os
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    import tensorflow as tf
    import urllib.request
    
    # Ensure we have a valid sample image
    sample_img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sample_xray.jpg')
    
    # Download a sample image if it doesn't exist
    if not os.path.exists(sample_img_path):
        print("Downloading a sample chest X-ray image...")
        # Public domain chest X-ray image URL
        img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Chest_X-ray_PA_3-8-2010.png/1024px-Chest_X-ray_PA_3-8-2010.png"
        try:
            urllib.request.urlretrieve(img_url, sample_img_path)
            print(f"Sample image saved to {sample_img_path}")
        except Exception as e:
            print(f"Failed to download sample image: {e}")
    
    # Determine which image to use: user-specified, dataset, or sample
    img = None
    img_path = None
    user_img = config.get('gradcam_image', None)
    # Try user-specified image
    if user_img:
        candidate = user_img if os.path.isabs(user_img) else os.path.join(os.path.dirname(os.path.dirname(__file__)), user_img)
        tmp = cv2.imread(candidate) if os.path.exists(candidate) else None
        if tmp is not None:
            img, img_path = tmp, candidate
    # Try dataset images
    if img is None:
        dataset_root = config.get('dataset_root', 'data/chest_xray/TB_Chest_Radiography_Database/Normal')
        for root, dirs, files in os.walk(dataset_root):
            for fname in files:
                if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                    candidate = os.path.join(root, fname)
                    tmp = cv2.imread(candidate)
                    if tmp is not None:
                        img, img_path = tmp, candidate
                        break
            if img is not None:
                break
    # Fallback to sample image
    if img is None:
        if os.path.exists(sample_img_path):
            img = cv2.imread(sample_img_path)
            img_path = sample_img_path
            if img is None:
                raise FileNotFoundError(f"Could not load any valid image for Grad-CAM, even the sample image at {sample_img_path}")
        else:
            raise FileNotFoundError(f"Sample image missing at {sample_img_path}")
    print(f"Using image for Grad-CAM: {img_path}")
    img = cv2.resize(img, tuple(config['model']['input_shape'][:2]))
    img_array = np.expand_dims(img / 255.0, axis=0)

    print("Generating predictions...")
    preds = model.predict(img_array)
    class_idx = np.argmax(preds[0])
    class_output = model.output[:, class_idx]
    
    print("Finding last convolutional layer...")
    last_conv_layer = None
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            last_conv_layer = layer.name
            break
    if last_conv_layer is None:
        raise ValueError("No Conv2D layer found in model for Grad-CAM.")
    
    print("Creating gradient model...")
    grad_model = tf.keras.models.Model([
        model.input], [model.get_layer(last_conv_layer).output, model.output])
    
    print("Computing gradients...")
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        loss = predictions[:, class_idx]
    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    
    print("Generating heatmap...")
    heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)
    heatmap = np.maximum(heatmap, 0) / np.max(heatmap)
    heatmap = cv2.resize(heatmap.numpy(), (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    print("Creating visualization...")
    superimposed_img = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)
    plt.figure(figsize=(10, 8))
    plt.imshow(superimposed_img[..., ::-1])
    plt.axis('off')
    plt.title(f'Grad-CAM for {os.path.basename(img_path)}')
    plt.tight_layout()
    plt.show()
    
    # Save the visualization
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gradcam_output.jpg')
    cv2.imwrite(output_path, superimposed_img)
    print(f"Grad-CAM visualization saved to {output_path}")
