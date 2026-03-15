import sys

def find_pattern_stride(filename):
    with open(filename, 'rb') as f:
        data = f.read()[0::2] # Left channel

    # Focus on the diverse area
    data = data[2048:]
    
    print(f"--- {filename} ---")
    best_lag = -1
    max_matches = 0
    
    # Check lags around 256
    for lag in range(250, 262):
        matches = 0
        for i in range(len(data) - lag):
            if data[i] == data[i+lag]:
                matches += 1
        
        print(f"Lag {lag}: {matches} matches")
        if matches > max_matches:
            max_matches = matches
            best_lag = lag

    print(f"Best lag: {best_lag}")

if __name__ == "__main__":
    find_pattern_stride('small_file_repeating_data.bin')
    find_pattern_stride('big_file_unique_data.bin')
