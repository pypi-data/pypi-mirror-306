import os
import re
from PIL import Image
import zipfile

def check_format(mail_addr):
    """
    Validates an email address format.
    
    :param mail_addr: str, the email address to be checked
    :return: True if valid, raises ValueError if invalid
    """
    # Ensure the input is a string
    if not isinstance(mail_addr, str):
        raise TypeError('Email address must be a string.')

    # Regular expression for validating an email address
    mail_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    # Check if the email address matches the regex
    if re.fullmatch(mail_regex, mail_addr):
        return True
    else:
        raise ValueError(f'{mail_addr} is not a valid email address. Please check your input!')

def file_size(file_path):
    """
    Returns the file size in MB.
    
    :param file_path: str, the file's path
    :return: float, the file size in MB
    """
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'{file_path} does not exist.')

    # Calculate and return the file size in MB
    return os.stat(file_path).st_size / (1024 ** 2)

def check_attach_size(attach_size, limited_size=5):
    """
    Checks if the attachment size exceeds the limit.
    
    :param attach_size: float, the total size of attachments in MB
    :param limited_size: float, maximum size of attachments for a single email in MB
    :return: int, -1 if size exceeds limit, 1 if within limit
    """
    return -1 if attach_size >= limited_size else 1

def compress_image(img_src, quality=75):
    """
    Compresses an image to a specified quality.
    
    :param img_src: str, image source path
    :param quality: int, quality of image compression (1-100)
    :return: str, path to the compressed image
    """
    # Check if the path is a valid image file
    if os.path.isdir(img_src) or not img_src.lower().endswith(('png', 'jpg', 'jpeg')):
        raise ValueError(f'{img_src} is not a valid image file.')

    # Define the destination path for the compressed image
    img_name = os.path.basename(img_src)
    img_dst = f'tmp_{os.path.splitext(img_name)[0]}.{img_name.split(".")[-1]}'

    # Open the image and determine its format
    with Image.open(img_src) as img:
        img_format = 'JPEG' if img_src.lower().endswith('jpg') else img.format

        # Save the compressed image
        try:
            img.save(img_dst, img_format, quality=quality, optimize=True, progressive=True)
        except IOError:
            # Adjust the maximum block size for large images
            Image.MAX_IMAGE_PIXELS = img.size[0] * img.size[1]
            img.save(img_dst, img_format, quality=quality, optimize=True, progressive=True)

    return img_dst

def package_files(files, zip_name='tmp', save_path='./', format='zip'):
    """
    Packages multiple files into a zip archive.
    
    :param files: list, paths of files to be zipped
    :param zip_name: str, name of the zip file
    :param save_path: str, directory to save the zip file
    :param format: str, format of the archive, default is 'zip'
    :return: str, path to the created zip file
    """
    # Ensure the save path exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Define the full path for the zip file
    zip_path = os.path.join(save_path, f'{zip_name}.{format}')

    # Create a zip file and add files to it
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_obj:
        for file in files:
            if os.path.isfile(file):
                zip_obj.write(file, os.path.basename(file))
            else:
                raise FileNotFoundError(f'{file} does not exist.')

    return zip_path

