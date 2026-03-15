import sys

def check_uniqueness(filename):
    with open(filename, 'r') as f:
        content = f.read()

    patterns = content.split('// Pattern ')[1:]
    pattern_bodies = []
    for p in patterns:
        body = "\n".join(p.split('\n')[1:]).strip()
        if body:
            pattern_bodies.append(body)

    print(f"--- {filename} ---")
    print(f"Total patterns: {len(pattern_bodies)}")
    print(f"Unique patterns: {len(set(pattern_bodies))}")
    
    counts = {}
    for p in pattern_bodies:
        counts[p] = counts.get(p, 0) + 1
        
    for p, count in counts.items():
        if count > 1:
            print(f"Notes matching {count} times found.")

if __name__ == "__main__":
    check_uniqueness(sys.argv[1])
