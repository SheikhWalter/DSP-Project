import math

def quantize_signal(signal_dict, levels=None, bits=None):
    # Calculate Levels or Bits based on user input
    if bits is not None and bits > 0:
        levels = 2 ** bits
    elif levels is not None and levels > 0:
        bits = int(math.ceil(math.log2(levels)))
    else:
        raise ValueError("Either valid bits or levels must be provided.")

    x_vals = list(signal_dict.values())
    x_min = min(x_vals)
    x_max = max(x_vals)

    # Step size Delta
    delta = (x_max - x_min) / levels

    quantized_sig = {}
    error_sig = {}
    encoded_sig = {}
    level_indices = {}

    for n, x in signal_dict.items():
        # Determine 1-based level index (k)
        if x == x_max:
            k = levels
        else:
            k = int((x - x_min) // delta) + 1
            if k > levels:
                k = levels

        # Midpoint reconstruction level
        q_k = x_min + (k - 0.5) * delta
        
        # Calculate quantization error and binary encoding
        err = q_k - x
        encoded_str = format(k - 1, f'0{bits}b')

        quantized_sig[n] = q_k
        error_sig[n] = err
        encoded_sig[n] = encoded_str
        level_indices[n] = k

    return quantized_sig, error_sig, encoded_sig, level_indices, delta