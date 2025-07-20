import json
import sys

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_json(a, b, path=''):
    diffs = []
    if type(a) != type(b):
        # Types differ: record path
        diffs.append(path if path else 'root')
        return diffs

    if isinstance(a, dict):
        all_keys = set(a.keys()) | set(b.keys())
        for key in sorted(all_keys):
            sub_path = f"{path}.{key}" if path else key
            if key not in a:
                diffs.append(sub_path)
            elif key not in b:
                diffs.append(sub_path)
            else:
                diffs.extend(compare_json(a[key], b[key], sub_path))

    elif isinstance(a, list):
        max_len = max(len(a), len(b))
        for i in range(max_len):
            sub_path = f"{path}[{i}]"
            if i >= len(a):
                diffs.append(sub_path)
            elif i >= len(b):
                diffs.append(sub_path)
            else:
                diffs.extend(compare_json(a[i], b[i], sub_path))
    else:
        if a != b:
            diffs.append(path)
    return diffs

if __name__ == "__main__":
    # Change these to your actual filenames
    file_a = "a.json"
    file_b = "b.json"

    if len(sys.argv) == 3:
        file_a = sys.argv[1]
        file_b = sys.argv[2]

    json_a = load_json(file_a)
    json_b = load_json(file_b)

    differences = compare_json(json_a, json_b)
    for diff in differences:
        print(diff)


#python deep_json_diff.py a.json b.json
#use this command to run
#also change the names of the json files to a.json and b.json