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
from skimage.metrics import (
    peak_signal_noise_ratio,
    structural_similarity
)

def get_metrics(uncompressed, compressed):
    metrics = {
        "psnr": 0,
        "ssim": 0,
        "compression": 0
    }
    if np.allclose(uncompressed, compressed, 1e-6):
        metrics["psnr"] = np.inf
    else:
        metrics["psnr"] = peak_signal_noise_ratio(uncompressed, compressed)
    metrics["ssim"] = structural_similarity(uncompressed, compressed)
    # TODO: add measure of memory usage after and before compression
    return metrics