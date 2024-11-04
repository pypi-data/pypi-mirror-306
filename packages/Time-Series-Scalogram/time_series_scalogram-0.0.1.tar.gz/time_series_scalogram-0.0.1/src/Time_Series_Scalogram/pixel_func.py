import numpy as np

def func(x):

    try:

        scan = {
            'value': np.sum(np.abs(np.log10(x)) > 0.02)/len(x),
        }

    except:
        scan = {
            'value': np.nan
        }

    return scan