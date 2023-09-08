import pandas as pd

def napari_get_reader(path):
    return reader_function

def reader_function(path):
    points = pd.read_csv(str(path), header=0, index_col=0).to_numpy()
    points = points[:, [2, 1, 0]]
    color = 'blue' if '_00_' in str(path) else 'red'
    return [(points, {'size': 3, 'face_color': color}, "points")]

