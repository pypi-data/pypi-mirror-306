
import io
import numpy as np
import pandas as pd


def dedupe(arr) :

    """
    Parameters
    ----------
    arr : sequence
    
    Returns
    -------
    list
    """
    
    deduped = []
    for elt in arr :
        if elt not in deduped :
            deduped.append(elt)

    return deduped


def remove_all(arr, target_elt) : 
    
    """
    Parameters
    ----------
    arr : sequence
    
    Returns
    -------
    list
    """
    
    removed = []
    for elt in arr :
        if elt != target_elt :
            removed.append(elt)
        
    return removed


def replace_all(arr, from_elt, to_elt) :
    
    """
    Parameters
    ----------
    arr : sequence
    
    Returns
    -------
    list
    """
    
    replaced = []
    for elt in arr :
        if elt == from_elt :
            replaced.append(to_elt)
        else :
            replaced.append(elt)
        
    return replaced


def round_all(arr) : 
    
    """
    Parameters
    ----------
    arr : sequence
    
    Returns
    -------
    list
    """
    
    rounded = []
    for elt in arr :
        rounded.append(round(elt))
        
    return rounded


def tabular_to_df(tabular) :

    """
    Parameters
    ----------
    tabular : str
        Tabular text.
    
    Returns
    -------
    pandas.DataFrame
    """
    
    return pd.read_table(io.StringIO(tabular), header=None)


def rgba_to_rgb(rgba):
    
    """
    Parameters
    ----------
    rgba : numpy.ndarray
        RGB color.
    
    Returns
    -------
    numpy.ndarray
        RGBA color.
    """
    
    row, col, channel = rgba.shape

    if channel == 3:
        return rgba
    elif channel != 4 :
        raise ValueError('RGBA image has 4 channels.')
        
    r, g, b, a = rgba[:,:,0], rgba[:,:,1], rgba[:,:,2], rgba[:,:,3]
    a = np.asarray(a, dtype='float32') / 255.0
    
    rgb = np.zeros([row, col, 3], dtype='float32' )
    
    R, G, B = [255,255,255]

    rgb[:,:,0] = r * a + (1.0 - a) * R
    rgb[:,:,1] = g * a + (1.0 - a) * G
    rgb[:,:,2] = b * a + (1.0 - a) * B

    return np.asarray(rgb, dtype='uint8' )

