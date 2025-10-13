
def local_file_valid_check(filename, file_path):

    with open(file_path, "r") as f:
        content = f.read().strip()

    if not content:
        print(f"{filename} is empty ❌ — resetting to defaults.")
        return False, "empty file"

    parts = content.split(",")
    if len(parts) != 2:
        print(f"{filename} invalid format ❌ — resetting to defaults.")
        return False, "invalid format"

    try:
        float(parts[0])
        float(parts[1])
        return True
    except ValueError:
        print(f"{filename} contains non-numeric values ❌ — resetting to defaults.")
        return False, "non-numeric values"


def create_default_file(file_path, filename):
    """Dosya oluşturur ve varsayılan değerleri ayarlar"""
    with open(file_path, "w") as f:
        f.write("0,0")
    theta0 = 0
    theta1 = 0
    print(f"{filename} created ✅")
    return theta0, theta1

def csv_file_valid_check(line):
    if not line:
        return False, "empty line"
    parts = line.strip().split(",")
    if len(parts) != 2:
        return False, "invalid format"
    try:
        float(parts[0])
        float(parts[1])
        return True
    except ValueError:
        return False, "non-numeric values"