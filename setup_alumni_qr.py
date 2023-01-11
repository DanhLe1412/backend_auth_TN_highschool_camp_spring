# Importing library
import qrcode


import pandas as pd
import os


df = pd.read_csv('./ds_alumni.csv')
os.makedirs('alumni_qr',exist_ok=True)
for index, row in df.iterrows():
    # Data to be encoded
    data = f"{(index+1)}"

    # Encoding data using make() function
    img = qrcode.make(data)

    # Saving as an image file
    filename = f'alumni_qr/{(index+1)}.png'
    img.save(filename)
