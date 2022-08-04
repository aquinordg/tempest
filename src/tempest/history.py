class History:

    def __init__(self):
        pass


if __name__ == '__main__':
    import sys
    import pandas as pd
    import numpy as np

    assert len(sys.argv) > 4

    count = int(sys.argv[1])
    seed = int(sys.argv[2])
    cfilename = sys.argv[3]

    tfilenames = sys.argv[4:]

    print(tfilenames)
