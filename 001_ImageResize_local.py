# Ignore  the warnings
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

import boto3
import os, glob, time
import MultiProcessUtil

from PIL import Image
from contextlib import contextmanager

@contextmanager
def timer(name):
    t0 = time.time()
    yield
    print(f'[{name}] done in {time.time() - t0:.0f} s')
    
def generate_hash(file):
    out_file  = 'resized/' + file
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    try:
        img = Image.open(file)
        img = img.resize((224, 224), Image.LANCZOS)
        img.save(out_file)
    except FileNotFoundError as e:
        print("{}".format(e))
        
files = glob.glob('input/**/*.jpeg', recursive=True)
print(len(files))
with timer('Local Resize'):
    res = MultiProcessUtil.manager(files, generate_hash, 300)


