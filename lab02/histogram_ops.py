import numpy as np

def calculate_histogram(image_channel):
    hist = np.zeros(256, dtype=int)
    for val in image_channel.flat:
        hist[val] += 1
    return hist

def linear_contrast_channel(channel):
    min_val = int(channel.min())
    max_val = int(channel.max())
    
    if max_val == min_val:
        return channel.copy()
    
    table = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        val = int(round((i - min_val) * 255.0 / (max_val - min_val)))
        if val < 0:
            val = 0
        elif val > 255:
            val = 255
        table[i] = val
        
    return table[channel]

def linear_contrast(image):
    if len(image.shape) == 2:
        return linear_contrast_channel(image)
    
    result = np.zeros_like(image)
    for c in range(image.shape[2]):
        result[:, :, c] = linear_contrast_channel(image[:, :, c])
    return result

def equalize_channel(channel):
    hist = calculate_histogram(channel)
    total_pixels = channel.size
    
    cdf = np.zeros(256, dtype=float)
    cumulative = 0
    for i in range(256):
        cumulative += hist[i]
        cdf[i] = cumulative
        
    non_zero_cdf = cdf[cdf > 0]
    if len(non_zero_cdf) == 0:
        return channel.copy()
    cdf_min = non_zero_cdf[0]
    
    table = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        if total_pixels == cdf_min:
            table[i] = 0
        else:
            val = int(round((cdf[i] - cdf_min) * 255.0 / (total_pixels - cdf_min)))
            if val < 0:
                val = 0
            elif val > 255:
                val = 255
            table[i] = val
            
    return table[channel]

def equalize_histogram_rgb(image):
    if len(image.shape) == 2:
        return equalize_channel(image)
        
    result = np.zeros_like(image)
    for c in range(3):
        result[:, :, c] = equalize_channel(image[:, :, c])
    return result

def rgb_to_hsv(image):
    img = image.astype(float) / 255.0
    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]
    
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    delta = max_c - min_c
    
    h = np.zeros_like(max_c)
    s = np.zeros_like(max_c)
    v = max_c
    
    mask = delta != 0
    
    mask_r = mask & (max_c == r)
    h[mask_r] = ((g[mask_r] - b[mask_r]) / delta[mask_r]) % 6.0
    
    mask_g = mask & (max_c == g)
    h[mask_g] = ((b[mask_g] - r[mask_g]) / delta[mask_g]) + 2.0
    
    mask_b = mask & (max_c == b)
    h[mask_b] = ((r[mask_b] - g[mask_b]) / delta[mask_b]) + 4.0
    
    h = h * 60.0
    
    mask_s = max_c != 0
    s[mask_s] = delta[mask_s] / max_c[mask_s]
    
    return h, s, v

def hsv_to_rgb(h, s, v):
    c = v * s
    x = c * (1.0 - np.abs((h / 60.0) % 2.0 - 1.0))
    m = v - c
    
    h_norm = (h % 360.0) / 60.0
    
    r1 = np.zeros_like(h)
    g1 = np.zeros_like(h)
    b1 = np.zeros_like(h)
    
    m0 = (h_norm >= 0) & (h_norm < 1)
    r1[m0] = c[m0]
    g1[m0] = x[m0]
    
    m1 = (h_norm >= 1) & (h_norm < 2)
    r1[m1] = x[m1]
    g1[m1] = c[m1]
    
    m2 = (h_norm >= 2) & (h_norm < 3)
    g1[m2] = c[m2]
    b1[m2] = x[m2]
    
    m3 = (h_norm >= 3) & (h_norm < 4)
    g1[m3] = x[m3]
    b1[m3] = c[m3]
    
    m4 = (h_norm >= 4) & (h_norm < 5)
    r1[m4] = x[m4]
    b1[m4] = c[m4]
    
    m5 = (h_norm >= 5) & (h_norm < 6)
    r1[m5] = c[m5]
    b1[m5] = x[m5]
    
    r = np.clip(np.round((r1 + m) * 255.0), 0, 255).astype(np.uint8)
    g = np.clip(np.round((g1 + m) * 255.0), 0, 255).astype(np.uint8)
    b = np.clip(np.round((b1 + m) * 255.0), 0, 255).astype(np.uint8)
    
    return np.dstack((r, g, b))

def equalize_histogram_hsv(image):
    if len(image.shape) == 2:
        return equalize_channel(image)
        
    h, s, v = rgb_to_hsv(image)
    v_uint8 = np.clip(np.round(v * 255.0), 0, 255).astype(np.uint8)
    v_eq = equalize_channel(v_uint8)
    v_new = v_eq.astype(float) / 255.0
    
    return hsv_to_rgb(h, s, v_new)
