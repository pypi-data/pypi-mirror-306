from PIL import Image
import os
from typing import List

# import matplotlib.pyplot as plt
# import numpy as np
# from scipy.ndimage import map_coordinates, gaussian_filter

def create_folder_path(out_folder_path):
    if not os.path.exists(out_folder_path):
        os.makedirs(out_folder_path)

def save_to_txt(data: List, file_path: str):
    with open(file_path, 'w') as f:
        for item in data:
            f.write(f"{item}\n")  # Write each item on a new line

def read_from_txt(file_path: str) -> List:
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def read_img(file_path):
    img = Image.open(file_path)
    return img

def save_img(img, file_path):
    # image = Image.fromarray(img.astype('uint8'))  # Convert NumPy array to PIL image

    # Save the image as a TIFF file
    img.save(file_path)

def delete_folder(folder_path):
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                delete_folder(file_path)
        os.rmdir(folder_path)

def plot_control_grids(source_grid, target_grid, transformed_image_shape, source_image=None):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    if source_image is not None:
        axes[0].imshow(source_image)
    else:
        axes[0].axis('equal')
    axes[0].plot(source_grid[:,:,1], source_grid[:,:,0],"y-.")
    axes[0].plot(source_grid[:,:,1].T, source_grid[:,:,0].T,"y-.")
    axes[0].plot(source_grid[:,:,1], source_grid[:,:,0],"b*")
    axes[0].grid(None)
    axes[0].set_title('source image space', fontsize=12)

    axes[1].plot(target_grid[:,:,1], target_grid[:,:,0],"y-.")
    axes[1].plot(target_grid[:,:,1].T, target_grid[:,:,0].T,"y-.")
    axes[1].plot(target_grid[:,:,1], target_grid[:,:,0],"b*")
    xr = transformed_image_shape[1]/2
    yr = transformed_image_shape[0]/2
    axes[1].plot([-xr,xr,xr,-xr,-xr], [-yr,-yr,yr,yr,-yr],"r-")
    axes[1].axis('equal')
    axes[1].grid(None)
    axes[1].set_title('target image space', fontsize=12)
    plt.show()

### --------- Test the functions --------- ###
def get_test_folder():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    test_folder = os.path.join(current_dir, "test_folder")
    return test_folder

def get_parent_folder():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(current_dir)
    return parent_dir

def test_io():
    test_folder = get_test_folder()
    # Test the functions
    create_folder_path(test_folder)
    txt_path = os.path.join(test_folder, "test.txt")
    save_to_txt(["Hello", "World"], txt_path)
    txt_content = read_from_txt(txt_path)
    assert txt_content == "Hello\nWorld\n"
    # clean up
    delete_folder(test_folder)

def test_image_io():
    parent_dir = get_parent_folder()
    img_folder = os.path.join(parent_dir, "data/2d_images")
    img_name = "ID_0000_Z_0142.tif"
    img_path = os.path.join(img_folder, img_name)
    img = read_img(img_path)
    assert img.size == (512, 512)

    test_folder = get_test_folder()
    create_folder_path(test_folder)
    img_out_path = os.path.join(test_folder, "test.tif")
    save_img(img, img_out_path)
    img_out = read_img(img_out_path)
    assert img_out.size == (512, 512)
    # clean up
    delete_folder(test_folder)

def test_elastic_deformation():
    test_folder = get_test_folder()
    create_folder_path(test_folder)

    parent_dir = get_parent_folder()
    img_folder = os.path.join(parent_dir, "data/2d_images")
    img_name = "ID_0000_Z_0142.tif"
    img_path = os.path.join(img_folder, img_name)
    img = read_img(img_path)
    img = np.array(img)
    n_rows, n_cols = 512, 512
    source_grid = np.mgrid[0:n_rows, 0:n_cols]
    target_grid = np.mgrid[0:n_rows, 0:n_cols]
    plot_control_grids(source_grid, target_grid, (200, 200), img)
    # deformed = generate_elastic_deformation(img)
    # img_out_path = os.path.join(test_folder, "test.tif")
    # save_img(deformed, img_out_path)

    # clean up
    # delete_folder(test_folder)


if __name__ == "__main__":
    test_io()
    test_image_io()
    # test_elastic_deformation()
