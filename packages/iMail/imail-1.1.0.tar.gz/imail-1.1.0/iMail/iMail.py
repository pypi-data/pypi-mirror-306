# -*- coding: UTF-8 -*-

# MIT License
#
# Copyright (c) 2023 Zhiwei Li (https://github.com/mtics)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from iMail.utils import *


class EMAIL(object):

    def __init__(self, host, sender_addr, pwd, sender_name='no_reply', port=25):
        """
        Initialize the EMAIL class and set sender information.
        
        :param host: Email server address
        :param sender_addr: Sender's email address
        :param pwd: Sender's email password or authorization code
        :param sender_name: Sender's nickname
        :param port: Email server port, default is 25
        """
        # Check if the sender's address format is valid
        check_format(sender_addr)

        # Set sender information dictionary
        self.sender_info = {
            'host': host,
            'port': port,
            'address': sender_addr,
            'pwd': pwd,
            'sender': sender_name
        }

        # Initialize the list of receivers as empty
        self.receivers = []
        # Initialize the email message as None
        self.msg = None

    def set_receiver(self, receiver):
        """
        Set the receiver(s), can be a single email address or a list of addresses.
        
        :param receiver: Email address (string) or list of addresses
        :raises TypeError: If input is not a string or list
        """
        if isinstance(receiver, str):
            # Check the format of a single receiver address
            check_format(receiver)
            # Add to the list of receivers
            self.receivers.append(receiver)
        elif isinstance(receiver, list):
            # Use list comprehension to check and add receiver addresses
            self.receivers.extend([addr for addr in receiver if check_format(addr)])
        else:
            raise TypeError('set_receiver() only accepts str or list types')

    def new_mail(self, subject='Subject', encoding='utf-8'):
        """
        Create a new email, set the subject and sender information.
        
        :param subject: Email subject, default is 'Subject'
        :param encoding: Email encoding, default is 'utf-8'
        """
        # Create a multipart email object, allowing multiple formats
        self.msg = MIMEMultipart('related')
        # Set sender information
        self.msg['From'] = '{}<{}>'.format(self.sender_info['sender'], self.sender_info['address'])
        # Set email subject
        self.msg['Subject'] = Header(subject, encoding)
        # Set receiver information
        self.msg['To'] = ','.join(self.receivers)

    def add_text(self, content='', subtype='plain', encoding='utf-8'):
        """
        Add text content to the email.
        
        :param content: Text content
        :param subtype: Text type, 'plain' or 'html'
        :param encoding: Text encoding, default is 'utf-8'
        """
        # Create and attach text object
        self.msg.attach(MIMEText(content, subtype, encoding))

    def attach_images(self, images, compressed=True, quality=75):
        """
        Attach images to the email.
        
        :param images: Image path or list of paths
        :param compressed: Whether to compress images, default is True
        :param quality: Compression quality, default is 75
        """
        # Ensure images is a list
        images = [images] if isinstance(images, str) else images
        for image in images:
            # Compress image if needed
            image = compress_image(image, quality) if compressed else image
            # Attach image
            self._attach_image(image)
            # Remove temporary compressed file if needed
            if compressed:
                os.remove(image)

    def _attach_image(self, image_path):
        """
        Attach a single image to the email.
        
        :param image_path: Image file path
        """
        # Use context manager to open image file
        with open(image_path, 'rb') as image_data:
            msg_image = MIMEImage(image_data.read())
        # Set image attachment header information
        msg_image.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
        # Attach to the email
        self.msg.attach(msg_image)

    def attach_files(self, file_paths, limited_size=5, zip_name='tmp.zip', zip_path='./'):
        """
        Attach files to the email, files exceeding the size limit will be compressed.
        
        :param file_paths: File path or list of paths
        :param limited_size: Attachment size limit (MB), default is 5MB
        :param zip_name: Zip file name, default is 'tmp.zip'
        :param zip_path: Zip file save path, default is current directory
        """
        # Ensure file_paths is a list
        file_paths = [file_paths] if isinstance(file_paths, str) else file_paths
        # Package files into a zip
        zip_path = package_files(file_paths, zip_name=zip_name, save_path=zip_path)
        # Check if zip size exceeds limit
        if check_attach_size(file_size(zip_path), limited_size) == -1:
            # Add warning text if size exceeds limit
            self.add_text(content='Attachment size exceeded the maximum limit and could not be uploaded!')
        else:
            # Use context manager to open zip file
            with open(zip_path, 'rb') as file_data:
                attachment = MIMEApplication(file_data.read())
            # Set attachment header information
            attachment.add_header('Content-Disposition', 'attachment', filename=zip_name)
            # Attach to the email
            self.msg.attach(attachment)
        # Remove temporary zip file
        os.remove(zip_path)

    def send_mail(self):
        """
        Send the email.
        """
        try:
            # Connect to the email server using SMTP protocol
            with smtplib.SMTP(self.sender_info['host'], self.sender_info['port']) as stp:
                # Log in to the email server
                stp.login(self.sender_info['address'], self.sender_info['pwd'])
                # Send the email
                stp.sendmail(self.sender_info['address'], self.receivers, self.msg.as_string())
            # Print success message
            print('Email sent successfully!')
        except smtplib.SMTPException as e:
            # Print SMTP error message
            print('SMTP Error:', e)
