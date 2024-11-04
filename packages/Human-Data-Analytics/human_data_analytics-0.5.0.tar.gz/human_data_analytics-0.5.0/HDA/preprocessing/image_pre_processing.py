import os
from typing import List, Dict
import numpy as np
from pandas import Series
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
import gc
import random

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from ..image_utils import crop_image, resize_image, normalize_image, CLAHE, create_patches
from .data_augmentation import data_augmentation

def pre_process(image_n : str, path : str, num_patches_per_side:int = 3, 
                                        crop_list: Dict[str,int] = {'top': 0.2, 'bottom':0.05, 'left':0.2, 'right':0.2}) -> np.ndarray:
    '''
    function that preprocesses an image given its filename
    '''

    image_path = os.path.join(path, image_n)
    cropped_image = crop_image(image_path, **crop_list)
    resized_image = resize_image(cropped_image)
    modified_image = CLAHE(resized_image)
    patches = create_patches(modified_image, num_patches_per_side = num_patches_per_side)
    normalized_patches = [normalize_image(patch) for patch in patches]

    return normalized_patches

def display_image_preprocess(extracted_image_path: str, num_patches_per_side:int = 3, 
                                            crop_list: Dict[str,int] = {'top': 0.05, 'bottom':0.05, 'left':0.05, 'right':0.05}
                                                                                                    ) -> tuple[np.ndarray, List[np.ndarray]]:
  
  """
  function that preprocesses an image given its filename with the aim to"""
  
  images_filename = sorted(os.listdir(extracted_image_path),
                                  key = lambda x: int(x.split('.')[0]))[0]
  processed = pre_process(images_filename, extracted_image_path, num_patches_per_side = num_patches_per_side, crop_list=crop_list)

  image = cv2.imread(os.path.join(extracted_image_path, images_filename), cv2.IMREAD_COLOR)
  image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

  return image_rgb, processed

def plot_processed_image(extracted_image_path: str, num_patches_per_side:int = 3, 
                            crop_list: Dict[str,int] = 
                                                 {
                                                  'top': 0.2, 'bottom':0.05, 
                                                    'left':0.2, 'right':0.2
                                                                            }) -> None:
    """
    Plot the original image and a composite image of patches extracted from it.

    Parameters:
    - extracted_image_path: Path to the image from which patches are extracted.
    - rows: Number of rows of patches in the composite image.
    - cols: Number of columns of patches in the composite image.
    """

    # Load the original image and patches
    large_image, small_images = display_image_preprocess(extracted_image_path, num_patches_per_side = num_patches_per_side, **crop_list)
    patch_per_side = num_patches_per_side
    rows, cols = (patch_per_side, patch_per_side)
    
    if large_image.shape[2] == 3:
        large_image = cv2.cvtColor(large_image, cv2.COLOR_BGR2RGB)

    #Calculate target size for each patch and resize
    large_height, large_width, _ = large_image.shape
    small_height, small_width = large_height // rows, large_width // cols
    small_images_resized = [cv2.resize(img, (small_width, small_height)) for img in small_images]

    #Space between patches
    padding = 10
    composite_height = (rows * small_height) + ((rows + 1) * padding)
    composite_width = (cols * small_width) + ((cols + 1) * padding)


    composite_image = np.zeros((composite_height, composite_width, 3))

    #Place each patch in the composite image
    for i, img in enumerate(small_images_resized[:rows * cols]):
        row = i // cols
        col = i % cols
        start_y = row * (small_height + padding) + padding
        start_x = col * (small_width + padding) + padding
        composite_image[start_y:start_y + small_height, start_x:start_x + small_width] = img

    fig, axes = plt.subplots(1, 2, figsize=(15, 7))

    axes[0].imshow(large_image)
    axes[0].axis('off')
    axes[0].set_title("Original Image")

    axes[1].imshow(composite_image)
    axes[1].axis('off')
    axes[1].set_title("Processed Patches")

    plt.tight_layout()
    plt.show()

# def data_generator_patch(extracted_image_path: str,
#                          gender: Series, label: Series,
#                           train: bool = True, admissible_augmentations = [0,3,4], prob = [1/3]*3) -> tuple[tuple[tf.Tensor, tf.Tensor], tf.Tensor]:

#     images_filenames = sorted(os.listdir(extracted_image_path),
#                               key = lambda x: int(x.split('.')[0]))

#     index_list = list(range(len(images_filenames)))
#     np.random.shuffle(index_list)

#     if train:
#         all_samples = np.random.choice(admissible_augmentations, p = prob, size = len(index_list)*4)

#     for num, index in enumerate(index_list):
#         processed = pre_process(images_filenames[index], extracted_image_path)

#         if train:
#             indeces = random.sample(range(len(processed)), 4)
#             processed = [processed[i] for i in indeces]
#             sample_step = all_samples[4*num:4*num+4]
#             processed_patch = data_augmentation(processed, sample_step)
#         else:
#             processed_patch = processed

#         del processed

#         for patch in processed_patch:
#             yield (patch, gender[index]), label[index]

#         del processed_patch

#         if num % 1000 == 0:
#             gc.collect()

def data_generator_patch(extracted_image_path: str,
                         gender: Series, label: Series,
                          train: bool = True, admissible_augmentations = [0,3,4],
                             prob: List[int] = [1/3]*3, num_patches_per_side: int = 3,
                                        data_size:int = 16000, crop_list: Dict[str,int] = 
                                                 {
                                                  'top': 0.2, 'bottom':0.05, 'left':0.2, 'right':0.2
                                                                                                    }) -> tuple[tuple[tf.Tensor, tf.Tensor], tf.Tensor]:

    images_filenames = sorted(os.listdir(extracted_image_path),
                              key = lambda x: int(x.split('.')[0]))

    index_list_ = list(range(len(images_filenames)))

    if train:
        index_list = np.random.choice(index_list_, size = data_size)
        all_samples = np.random.choice(admissible_augmentations, p = prob, size = len(index_list))
    else:
        index_list = index_list_
        
    for num, index in enumerate(index_list):
        processed = pre_process(images_filenames[index], extracted_image_path, num_patches_per_side = num_patches_per_side, crop_list = crop_list)
        
        if train:
            index = random.sample(range(len(processed)), 1)[0]
            processed = processed[index:index+1]
            sample_step = all_samples[num:num+1]
            processed_patch = data_augmentation(processed, sample_step)
        else:
            processed_patch = processed

        for patch in processed_patch:
            yield (patch, gender[index]), label[index]

        del processed

        del processed_patch

        if num % 1000 == 0:
            gc.collect()