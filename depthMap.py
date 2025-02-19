from PIL import Image
import torch
from transformers import DepthProImageProcessorFast, DepthProForDepthEstimation
import numpy as np
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def createDepthMap(image, save_path='depthmap.jpg'):
    if not os.path.exists('image_processor'):
        image_processor = DepthProImageProcessorFast.from_pretrained("apple/DepthPro-hf")
        image_processor.save_pretrained('image_processor')
    else:
        image_processor = DepthProImageProcessorFast.from_pretrained('image_processor')

    if not os.path.exists('model'):
        model = DepthProForDepthEstimation.from_pretrained("apple/DepthPro-hf").to(device)
        model.save_pretrained('model')
    else:
        model = DepthProForDepthEstimation.from_pretrained('model')

    inputs = image_processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    post_processed_output = image_processor.post_process_depth_estimation(
        outputs, target_sizes=[(image.height, image.width)],
    )

    field_of_view = post_processed_output[0]["field_of_view"]
    focal_length = post_processed_output[0]["focal_length"]
    depth = post_processed_output[0]["predicted_depth"]
    depth = (depth - depth.min()) / (depth.max() - depth.min())
    depth = depth * 255.
    depth = depth.detach().cpu().numpy()
    depth = Image.fromarray(depth.astype("uint8"))
    depth.save(save_path)
    return depth

if __name__ == "__main__":
    image_path = input('image name: ')

    if not os.path.exists(image_path):
        raise ValueError('path does not exist')
    
    save_path = input('path to save depth map: ')

    # input RGB image, which is an array of size (width, height, 3)
    image = Image.open(image_path)
    # a 2D array of size (width, height), containing the z-coordinate of each pixel indicating how far the pixel is from the camera
    # We call this 2D array the "depth map" of the image
    depthMap = createDepthMap(image, save_path)
    print(np.array(depthMap))
    depthMap.show()
