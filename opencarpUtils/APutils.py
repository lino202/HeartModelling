
import numpy as np
import scipy.stats as stat
import statistics

meshioOCCellsMap = {"tetra": "Tt", "line": "Ln"}

def writeStimVtxFile(arr, outName, stimType):
    with open(outName, 'w') as f:
        f.write("{0:d}\n".format(arr.shape[0]))
        f.write("{}\n".format(stimType))                         #For now it seems ok to only have Intra
        vtxs = list(map(lambda x: "{:d}\n".format(x),list(arr)))
        f.writelines(vtxs)



import numpy as np
from scipy.signal import find_peaks
from scipy.interpolate import interp1d

def calculate_multi_apd90(v, t, min_distance_ms=200, height_threshold=-20):
    """
    Detects beats and calculates APD90 for each AP in a continuous signal.
    """
    v = np.asarray(v)
    t = np.asarray(t)
    dt = t[1] - t[0]
    
    # 1. Detect peaks (upstrokes/maxima)
    distance_samples = int(min_distance_ms / dt)
    peaks, _ = find_peaks(v, height=height_threshold, distance=distance_samples)
    
    results = []
    
    for i in range(len(peaks)):
        idx_peak = peaks[i]
        
        # Define search window for baseline (look back) and end of beat (look forward)
        # Left bound: midpoint to previous peak or 50 ms before
        if i == 0:
            left_bound = max(0, idx_peak - int(50 / dt))
        else:
            left_bound = (peaks[i - 1] + idx_peak) // 2
            
        # Right bound: midpoint to next peak or end of trace
        if i == len(peaks) - 1:
            right_bound = min(len(v) - 1, idx_peak + int(400 / dt))
        else:
            right_bound = (idx_peak + peaks[i + 1]) // 2
            
        v_beat = v[left_bound:right_bound]
        t_beat = t[left_bound:right_bound]
        
        # Local peak index inside window
        local_peak_idx = idx_peak - left_bound
        
        # 2. Local Peak and Resting Potential
        v_peak = v_beat[local_peak_idx]
        v_rest = np.min(v_beat[:local_peak_idx])
        v_90 = v_peak - 0.90 * (v_peak - v_rest)
        
        # 3. Sub-sample upstroke target crossing
        up_v = v_beat[:local_peak_idx]
        up_t = t_beat[:local_peak_idx]
        f_up = interp1d(up_v, up_t, fill_value="extrapolate")
        t_start = float(f_up(v_90))
        
        # 4. Sub-sample downstroke target crossing
        down_v = v_beat[local_peak_idx:]
        down_t = t_beat[local_peak_idx:]
        f_down = interp1d(down_v[::-1], down_t[::-1], fill_value="extrapolate")
        t_end = float(f_down(v_90))
        
        apd90 = t_end - t_start
        results.append({
            "beat_number": i + 1,
            "peak_time": t[idx_peak],
            "apd90": apd90,
            "v_90": v_90
        })
        
    return results

# --- Example Usage ---
# Generate synthetic 3-beat trace (at ~2 Hz pacing)
t_signal = np.linspace(0, 1000, 10000)
v_signal = -80 + (
    120 * np.exp(-((t_signal - 100) / 4)**2) * (t_signal >= 100) + 100 * np.exp(-(t_signal - 100) / 120) * (t_signal >= 100) +
    120 * np.exp(-((t_signal - 500) / 4)**2) * (t_signal >= 500) + 100 * np.exp(-(t_signal - 500) / 120) * (t_signal >= 500) +
    120 * np.exp(-((t_signal - 850) / 4)**2) * (t_signal >= 850) + 100 * np.exp(-(t_signal - 850) / 120) * (t_signal >= 850)
)

beats_info = calculate_multi_apd90(v_signal, t_signal, min_distance_ms=250)

for beat in beats_info:
    print(f"Beat {beat['beat_number']}: Peak at {beat['peak_time']:.1f} ms | APD90 = {beat['apd90']:.2f} ms")