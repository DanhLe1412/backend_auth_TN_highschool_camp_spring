import gdown
import pandas as pd
import os


df = pd.read_csv('./ds_alumni.csv',index_col=False)
os.makedirs('alumni',exist_ok=True)
for index, row in df.iterrows():
    url = row['image_drive_link']
    str_id = url.split('/')[-1][8:]
    output = f"alumni/{(index+1)}.jpg"
    # gdown.download(url, output, quiet=False)
    cmd = f"gdown --id {str_id} --output {output}"
    os.system(cmd)
    df.at[index,'image_path'] = output
df.to_csv('ds_alumni_full.csv', index=False)
