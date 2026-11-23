def average_signal(signal: dict, size):
    avg_sig = {}
    keys = list(signal.keys())
    for n in range(keys[0], keys[-size]):
        avg_sig[n] = sum([signal[i] for i in keys[n:n+size]])/size
    return avg_sig

def sharpen_signal(signal: dict, der):
    keys = list(signal.keys())
    if der == "First":
        return {n: signal[n] - signal[n-1] for n in keys[1:]}
    else:
        return {n: signal[n+1] - 2 * signal[n] + signal[n-1] for n in keys[1:-1]}

def convolve_signals(x: dict, y: dict):
    keysx = list(x.keys())
    keysy = list(y.keys())
    minconv = keysx[0] + keysy[0]
    maxconv = keysx[-1] + keysy[-1]

    conv_sig = {}
    for n in range(minconv, maxconv + 1):
        conv_sig[n] = sum([x[k]*y[n-k] for k in x if (n - k) in y])
    return conv_sig