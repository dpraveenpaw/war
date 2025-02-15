#!/usr/bin/env python3
import re
from datetime import datetime
import argparse
from collections import defaultdict

class LogAnalyzer:
    def __init__(self):
        # Regular expression for common log formats (Apache, Nginx)
        self.log_pattern = re.compile(
            r'(?P<ip>[\d.]+)\s+'
            r'(?P<identity>\S+)\s+'
            r'(?P<user>\S+)\s+'
            r'\[(?P<timestamp>.*?)\]\s+'
            r'"(?P<request>.*?)"\s+'
            r'(?P<status>\d+)\s+'
            r'(?P<size>\S+)\s+'
            r'"(?P<referrer>.*?)"\s+'
            r'"(?P<user_agent>.*?)"'
        )
        self.error_counts = defaultdict(int)
        self.error_details = []

    def process_log_file(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    self.process_line(line.strip())
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return False
        return True

    def process_line(self, line):
        match = self.log_pattern.match(line)
        if match:
            status = match.group('status')
            # Check if status code is 5xx
            if status.startswith('5'):
                timestamp = match.group('timestamp')
                request = match.group('request')
                ip = match.group('ip')
                
                # Store error details
                self.error_counts[status] += 1
                self.error_details.append({
                    'timestamp': timestamp,
                    'status': status,
                    'ip': ip,
                    'request': request
                })

    def print_summary(self):
        print("\n=== Server Error (5xx) Summary ===")
        if not self.error_counts:
            print("No 5xx errors found.")
            return

        print("\nError Code Distribution:")
        for status, count in sorted(self.error_counts.items()):
            print(f"HTTP {status}: {count} occurrences")

        print("\nDetailed Error Entries:")
        for error in self.error_details:
            print(f"\nTimestamp: {error['timestamp']}")
            print(f"Status: {error['status']}")
            print(f"IP: {error['ip']}")
            print(f"Request: {error['request']}")
        
        print(f"\nTotal 5xx errors found: {sum(self.error_counts.values())}")

def main():
    parser = argparse.ArgumentParser(description='Extract HTTP 5xx errors from log files')
    parser.add_argument('logfile', help='Path to the log file')
    args = parser.parse_args()

    analyzer = LogAnalyzer()
    if analyzer.process_log_file(args.logfile):
        analyzer.print_summary()

if __name__ == "__main__":
    main()
