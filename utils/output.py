# utils/output.py
import json
import csv
from io import StringIO


def format_as_normal(data):
    output = []
    for d in data:
        lines = []
        for key, value in d.items():
            if isinstance(value, dict):
                lines.append(f"{key.title()}:")
                for sub_key, sub_val in value.items():
                    lines.append(f"  {sub_key.title()}: {sub_val}")
            else:
                lines.append(f"{key.title()}: {value}")
        output.append("\n".join(lines))
        output.append("\n" + "-" * 40 + "\n")
    return "\n".join(output)


def flatten_for_csv(entry):
    """
    Flatten nested dictionaries for CSV.
    For example: {"anonymity": {"vpn": False}} -> {"anonymity_vpn": False}
    """
    flat = {}
    for key, value in entry.items():
        if isinstance(value, dict):
            for sub_key, sub_val in value.items():
                flat[f"{key}_{sub_key}"] = sub_val
        else:
            flat[key] = value
    return flat


def format_as_csv(data):
    if not data:
        return ""
    flat_data = [flatten_for_csv(d) for d in data]
    # Collect all possible fields across entries
    fieldnames = sorted({key for d in flat_data for key in d.keys()})
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for d in flat_data:
        writer.writerow(d)
    return output.getvalue()


def format_as_json(data):
    return json.dumps(data, indent=4)


def write_formatted_output(data, file_path, fmt_type="normal"):
    fmt_type = fmt_type.lower()
    if fmt_type == "csv":
        formatted = format_as_csv(data)
    elif fmt_type == "json":
        formatted = format_as_json(data)
    else:
        formatted = format_as_normal(data)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(formatted)
    print(f"Output saved to {file_path} in {fmt_type.upper()} format.")
