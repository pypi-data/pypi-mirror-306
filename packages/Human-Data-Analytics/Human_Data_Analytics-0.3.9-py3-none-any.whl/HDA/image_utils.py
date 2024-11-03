import cv2, os
import numpy as np
from typing import List
import tensorflow as tf
import pandas as pd

def display_image(path) -> None:
    """
    Display the image at the given path
    Args:
    path:
        (str): full path to the image
        (numpy.ndarray): image as a numpy array
    """
    if isinstance(path, str):
        image = cv2.imread(path)
    else:
        image = path
    # print(image.shape)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return image
    

def crop_image(path,
                top:int = 0.05,
                bottom:int = 0.05,
                left:int = 0.05,
                right:int = 0.05,
                display:bool = False,
                save_path = False) -> None:
    """
    Crop the image at the given path by the given percentage
    and display the image if display is set to True
    Args:
        path:
            (str): full path to the image
            (numpy.ndarray): image as a numpy array
        top(int): percentage to crop from the top
        bottom(int): percentage to crop from the bottom
        left(int): percentage to crop from the left
        right(int): percentage to crop from the right
        display(bool): whether to display the image or not
        save_path: path to save the cropped image, if False, the image will not be saved
    """
    if isinstance(path, str):
        image = cv2.imread(path)
    else:
        image = path
    # print(image.shape)

    # get the dimensions of the image
    height, width = image.shape[:2]

    # crop the image
    start_row, start_col = int(height * top), int(width * left)
    end_row, end_col = int(height * (1 - bottom)), int(width * (1 - right))
    cropped_image = image[start_row:end_row, start_col:end_col]

    # remember to use cv2.waitKey(0) + cv2.destroyAllWindows() to close the window after the image is displayed
    if display:
        cv2.imshow("image", image)
        cv2.imshow("cropped image", cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # save the cropped image
    if save_path:
        cv2.imwrite(os.path.join(os.environ.get("DATA_PATH"),'_cropped.'.join(save_path.split('.'))), cropped_image)
        return None
    else:
        return cropped_image

def resize_image(path, 
                 width:int = 500, 
                 height:int = 500, 
                 display:bool = False,
                 save_path = False) -> None:
    """
    Resize the image at the given path to the given width and height
    and display the image if display is set to True
    Args:
        path:
            (str): full path to the image
            (numpy.ndarray): image as a numpy array
        width(int): width of the resized image
        height(int): height of the resized image
        display(bool): whether to display the image or not
        save_path: path to save the resized image, if False, the image will not be saved
    """
    if isinstance(path, str):
        image = cv2.imread(path)
    else:
        image = path
    # print(image.shape)
    
    resized_image = cv2.resize(image, (width, height))
    if display:
        cv2.imshow("resized image", resized_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # save the resized image
    if save_path:
        cv2.imwrite(os.path.join(os.environ.get("DATA_PATH"),'_resized.'.join(save_path.split('.'))), resized_image)
        return None
    else:
        return resized_image

def CLAHE(path, 
          display:bool = False, 
          save_path = False) -> None:
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to the image at the given path
    and display the image if display is set to True
    Args:
        path:
            (str): full path to the image
            (numpy.ndarray): image as a numpy array
        display(bool): whether to display the image or not
        save_path: path to save the CLAHE image, if False, the image will not be saved
    """
    if isinstance(path, str):
        image = cv2.imread(path)
    else:
        image = path
    
    # define the clahe object and apply it to the image
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    lab[...,0] = clahe.apply(lab[...,0])

    clahe_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    if display:
        cv2.imshow("image", image)
        cv2.imshow("enhanced image with CLAHE", clahe_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # save the clahe image
    if save_path:
        cv2.imwrite(os.path.join(os.environ.get("DATA_PATH"),'_clahe.'.join(save_path.split('.'))), clahe_image)
        return None
    else:
        return clahe_image
    
def create_patches(image, 
                   patch_size:int = 224, 
                   num_patches_per_side:int = 3,
                   display:bool = False, 
                   save_path = False) -> List[tf.Tensor]:
    """
    Create 9 overlapped patches of size 224x224 from the image at the given path
    and display the image if display is set to True
    Args:
        path(numpy.ndarray): image as a numpy array
        patch_size(int): size of the patch
        num_patches_per_side(int): number of patches to create 
        display(bool): whether to display the image or not
        save_path: path to save the patches, if False, the patches will not be saved
    """
    # get the dimensions of the image
    height, _ = image.shape[:2]

    stride = (patch_size*num_patches_per_side - height) // (num_patches_per_side - 1)
    # create num_patches_per_side**2 overlapped patches of size 224x224
    
    patches = []
    for i in range(num_patches_per_side):
        for j in range(num_patches_per_side):
            start_row, start_col = i * (patch_size - stride), j * (patch_size - stride)
            end_row, end_col = start_row + patch_size, start_col + patch_size
            patches.append(image[start_row:end_row, start_col:end_col])
    
    if display:
        for i, patch in enumerate(patches):
            cv2.imshow(f"patch {i+1}", patch)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    # save the patches
    if save_path:
        for i, patch in enumerate(patches):
            cv2.imwrite(os.path.join(os.environ.get("DATA_PATH"),f'_patch_{i+1}.'.join(save_path.split('.'))), patch)
        return None
    else:
        return patches
    
def load_images_from_folder(folder:str, 
                            normalize:bool = False,
                            convert_to_tensor:bool = False):
    """
    Load all the images from the given folder
    Args:
        folder(str): path to the folder containing the images
        normalize(bool): whether to normalize the images or not
    """
    image_list = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if normalize:
            img = normalize_image(img)
        if img is not None:
            image_list.append(img)
    if convert_to_tensor:
        image_array = np.array(image_list)
        return tf.convert_to_tensor(image_array, dtype=tf.float32)
    else:
        return image_list

def normalize_image(image):
    """
    Normalize the image
    Args:
        image(numpy.ndarray): image as a numpy array
    """
    return image / 255.0

def load_labels(label_path:str, gender:bool=False) -> np.ndarray:
    """
    Load the labels from the given path
    Args:
        label_path(str): path to the file containing the labels

    Returns:
        np.ndarray: labels with shape (num_samples,)
    """
    df = pd.read_csv(label_path)
    if gender:
        return df["male"].values
    else:
        return df["Bone Age (months)"].values

def trasform_patched_labels(labels:np.ndarray, num_patches_per_side:int)->np.ndarray:
    """
    Transform the labels to match the patches
    Args:
        labels(np.ndarray): labels with shape (num_samples,)
        num_patches_per_side(int): number of patches per side
    
    Returns:
        np.ndarray: patched labels with shape (num_samples*num_patches_per_side**2,)
                    e.g. [1 2 3] into [1 1 1 1 2 2 2 2 3 3 3 3] if num_patches_per_side = 2
    """
    return np.repeat(labels, num_patches_per_side**2)


if __name__ == "__main__":
    # try to see if the functions work
    
    image_path = os.path.join(os.environ.get("DATA_PATH"),"train/boneage-training-dataset/1377.png")
    image = display_image(image_path)
    cropped_image = crop_image(image, display = True)
    resized_image = resize_image(cropped_image, display = True)
    modified_image = CLAHE(resized_image, display = True)
    patches = create_patches(modified_image, display = True)
    # print("This file is not meant to be run directly.")
