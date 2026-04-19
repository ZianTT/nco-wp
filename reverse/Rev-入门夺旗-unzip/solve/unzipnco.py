# unzip attachments.zip
import os

for _ in range(10):
    import zipfile
    with zipfile.ZipFile('attachment.zip', 'r') as zip_ref:
        zip_ref.extractall('./attachments')
    os.remove('attachment.zip')
    os.rename('./attachments/attachment.zip', './attachment.zip')
