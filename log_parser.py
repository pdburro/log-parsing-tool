import argparse
import json
import xml.etree.ElementTree as ET

def parse_json(file_path, keyword=None):
    with open(file_path, "r") as file:
        data = json.load(file)

    logs = data.get("logs", [])  # Assuming logs are stored in a "logs" key
    filtered_logs = [log for log in logs if keyword is None or keyword in str(log)]

    return filtered_logs

def parse_xml(file_path, keyword=None):
    tree = ET.parse(file_path)
    root = tree.getroot()

    logs = []
    for log in root.findall("log"):  # Assuming each log is inside a <log> tag
        log_text = ET.tostring(log, encoding="unicode").strip()
        if keyword is None or keyword in log_text:
            logs.append(log_text)

    return logs

def main():
    parser = argparse.ArgumentParser(description="Parse log files (JSON/XML) and filter by keyword.")
    parser.add_argument("--input", required=True, help="Path to the log file (JSON or XML).")
    parser.add_argument("--format", required=True, choices=["json", "xml"], help="Log file format.")
    parser.add_argument("--filter", help="Keyword to filter logs.")
    parser.add_argument("--output", help="File to save the filtered results.")

    args = parser.parse_args()

    if args.format == "json":
        logs = parse_json(args.input, args.filter)
    else:
        logs = parse_xml(args.input, args.filter)

    if args.output:
        with open(args.output, "w") as out_file:
            out_file.write("\n".join(logs))
        print(f"Filtered logs saved to {args.output}")
    else:
        for log in logs:
            print(log)

if __name__ == "__main__":
    main()
