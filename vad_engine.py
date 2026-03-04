import numpy as np


def is_silent(audio, threshold=0.01):

    volume = np.abs(audio).mean()

    if volume < threshold:
        return True

    return False