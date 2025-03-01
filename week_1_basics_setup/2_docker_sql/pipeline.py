import sys

import pandas as pd

day = sys.argv[1]

def load_data():
    pass

def clean_data():
    pass

def save_data():
    pass

def main():
    load_data()
    clean_data()
    save_data()

if __name__ == '__main__':
    main()
    print('Installed Pandas version:', pd.__version__)
    print('Day:', day)
