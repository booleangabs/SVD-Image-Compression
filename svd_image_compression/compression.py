import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as image

def compressing(U, S, VT, k):
    return (U[:,:k] @ np.diag(S[:k])) @ VT[:k]

def compress_image(img_name, _target_rank):

    R = img_name[:, :, 0]
    G = img_name[:, :, 1]
    B = img_name[:, :, 2]

    R_U, R_S, R_VT = np.linalg.svd(R)
    G_U, G_S, G_VT = np.linalg.svd(G)
    B_U, B_S, B_VT = np.linalg.svd(B)
    
    R_compressed = compressing(R_U, R_S, R_VT, _target_rank)
    G_compressed = compressing(G_U, G_S, G_VT, _target_rank)
    B_compressed = compressing(B_U, B_S, B_VT, _target_rank)
    
    compressed_float = np.dstack((R_compressed, G_compressed, B_compressed))
    compressed = (np.minimum(compressed_float, 1.0) * 0xff).astype(np.uint8)
    
    image.imsave("compressed.png", compressed)