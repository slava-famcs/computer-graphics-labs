import numpy as np

def apply_convolution_channel(channel, kernel):
    h, w = channel.shape
    kh, kw = kernel.shape
    pad_h = kh // 2
    pad_w = kw // 2
    
    padded = np.pad(channel, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge').astype(float)
    
    output = np.zeros((h, w), dtype=float)
    for i in range(kh):
        for j in range(kw):
            output += kernel[i, j] * padded[i:i + h, j:j + w]
            
    return np.clip(np.round(output), 0, 255).astype(np.uint8)

def apply_convolution(image, kernel):
    if len(image.shape) == 2:
        return apply_convolution_channel(image, kernel)
    
    result = np.zeros_like(image)
    for c in range(image.shape[2]):
        result[:, :, c] = apply_convolution_channel(image[:, :, c], kernel)
    return result

def box_blur(image, size=3):
    kernel = np.ones((size, size), dtype=float) / (size * size)
    return apply_convolution(image, kernel)

def create_gaussian_kernel(size=5, sigma=1.0):
    k = size // 2
    y, x = np.ogrid[-k:k+1, -k:k+1]
    kernel = np.exp(-(x * x + y * y) / (2.0 * sigma * sigma))
    sum_val = kernel.sum()
    if sum_val != 0:
        kernel = kernel / sum_val
    return kernel

def gaussian_blur(image, size=5, sigma=1.0):
    kernel = create_gaussian_kernel(size, sigma)
    return apply_convolution(image, kernel)
