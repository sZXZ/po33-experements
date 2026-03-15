import sys

def scan_all_lags(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    diverse_data = data[2182:2182+10000]
    
    print(f"--- {filename} ---")
    best_lags = []
    
    for lag in range(4, 1024, 4):
        matches = 0
        for i in range(len(diverse_data) - lag):
            if diverse_data[i] == diverse_data[i+lag]:
                matches += 1
        
        score = matches / (len(diverse_data) - lag)
        if score > 0.15: # Significant correlation
            best_lags.append((lag, score))

    sorted_lags = sorted(best_lags, key=lambda x: x[1], reverse=True)
    for lag, score in sorted_lags[:10]:
        print(f"Lag {lag:4}: score {score:.4f}")

if __name__ == "__main__":
    scan_all_lags('small_file_repeating_data.bin')
    scan_all_lags('big_file_unique_data.bin')
