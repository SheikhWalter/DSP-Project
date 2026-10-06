def add_signals(signals):
    indices = signals[0].keys()
    for i in range(1, len(signals)):
        indices = sorted(set(indices) | set(signals[i].keys()))

    sum_signal = {}
    for i in indices:
        sum_signal[i] = sum([sig[i] if i in sig.keys() else 0 for sig in signals])

    return sum_signal

def subtract_signals(signals):
    indices = signals[0].keys()
    for i in range(1, len(signals)):
        indices = sorted(set(indices) | set(signals[i].keys()))

    sub_signal = {}
    for i in indices:
        sub_signal[i] = signals[0][i] - sum([sig[i] if i in sig.keys() else 0 for sig in signals[1:]])

    return sub_signal

def amplify_signal(signal, value):
    return {n: x*value for n,x in signal.items()}

def shift_signal(signal, k):
    return {n-k: signal[n] for n in signal.keys()}

def reverse_signal(signal):
    return {-n: signal[n] for n in list(signal.keys())[::-1]}