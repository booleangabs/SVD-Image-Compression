"""MIT License

Copyright (c) 2023 Yano R. Vasconcelos, Eduardo G. de M. Albuquerque and José Gabriel P. Tavares

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import numpy as np


def compress_single_channel(channel, k):
    U, S, Vt = np.linalg.svd(channel)
    return U[:,:k] @ np.diag(S)[:k, :k] @ Vt[:k]


def compress_image_numpy(image, k):
    """Compress image using SVD

    Args:
        image (np.ndarray): Input image. Float32 and normalized
        k (int): Number of components to keep

    Returns:
        np.ndarray: Result image
    """
    channels = image[..., 0], image[..., 1], image[..., 2]
    compressed = [compress_single_channel(channels[i], k) for i in range(3)]
    compressed = np.dstack(compressed)
    
    return np.clip(compressed, 0, 1)