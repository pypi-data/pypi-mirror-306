import os
from typing import List
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

def pre_process(image_n : str, path : str) -> np.ndarray:
    '''
    function that preprocesses an image given its filename
    '''

    image_path = os.path.join(path, image_n)
    cropped_image = crop_image(image_path)
    resized_image = resize_image(cropped_image)
    modified_image = CLAHE(resized_image)
    patches = create_patches(modified_image)
    normalized_patches = [normalize_image(patch) for patch in patches]

    return normalized_patches

def display_image_preprocess(extracted_image_path: str) -> tuple[np.ndarray, List[np.ndarray]]:
  
  """
  function that preprocesses an image given its filename with the aim to"""
  
  images_filename = sorted(os.listdir(extracted_image_path),
                                  key = lambda x: int(x.split('.')[0]))[0]
  processed = pre_process(images_filename, extracted_image_path)

  image = cv2.imread(os.path.join(extracted_image_path, images_filename), cv2.IMREAD_COLOR)
  image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

  return image_rgb, processed

def plot_processed_image(extracted_image_path: str) -> None:
  """
  Plot the original image and the patches enhanced and extracted from it
  
  """

  #Load entire images and patches
  large_image, small_images = display_image_preprocess(extracted_image_path)

  large_image = cv2.cvtColor(large_image, cv2.COLOR_BGR2RGB) if large_image.shape[2] == 3 else large_image

  #Get dimensions of the original image
  large_height, large_width, _ = large_image.shape

  #Calculate target size for each patch and resize
  small_height, small_width = large_height // 3, large_width // 3
  small_images_resized = [cv2.resize(img, (small_width, small_height)) for img in small_images]

  #Space between patches
  padding = 10  
  composite_height = (3 * small_height) + (4 * padding)  
  composite_width = (3 * small_width) + (4 * padding)    

  #Empty image to compose the patches
  composite_image = np.zeros((composite_height, composite_width, 3))

  #Place each patch inside the composite image
  for i, img in enumerate(small_images_resized):
      row = i // 3
      col = i % 3
      # Compute starting coordinates in the composite image and place each patch to its place in the composite image
      start_y = row * (small_height + padding) + padding
      start_x = col * (small_width + padding) + padding
      composite_image[start_y:start_y + small_height, start_x:start_x + small_width] = img

  fig, axes = plt.subplots(1, 2, figsize=(10, 5))

  axes[0].imshow(large_image)
  axes[0].axis('off')
  axes[0].set_title("Original Image")

  axes[1].imshow(composite_image)
  axes[1].axis('off')
  axes[1].set_title("Processed Patches")

  plt.tight_layout()
  plt.show()

def data_generator_patch(extracted_image_path: str,
                         gender: Series, label: Series,
                          train: bool = True, ammissible_augmentations = [0,2,3,4], prob = [0.25, 0.25, 0.25, 0.25]) -> tuple[tuple[tf.Tensor, tf.Tensor], tf.Tensor]:

    images_filenames = sorted(os.listdir(extracted_image_path),

                                  key = lambda x: int(x.split('.')[0]))

    index_list = list(range(len(images_filenames)))
    np.random.shuffle(index_list)

    if train:
        all_samples = np.random.choice(ammissible_augmentations, p = prob, size = len(index_list)*4)

    for num, index in enumerate(index_list):
        processed = pre_process(images_filenames[index], extracted_image_path)

        if train:
            indeces = random.sample(range(len(processed)), 4)
            processed = [processed[i] for i in indeces]
            sample_step = all_samples[4*num:4*num+4]
            processed_patch = data_augmentation(processed, sample_step)
        else:
            processed_patch = processed

        del processed

        for patch in processed_patch:
            yield (patch, gender[index]), label[index]

        del processed_patch

        if num % 1000 == 0:
            gc.collect()