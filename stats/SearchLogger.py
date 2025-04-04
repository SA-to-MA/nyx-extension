import os
import csv
from datetime import datetime

class SearchLogger:
    def __init__(self, domain_file, problem_file, constants):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(root_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)

        timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"search_stats_{timestamp_str}.csv"
        self.log_path = os.path.join(log_dir, log_filename)
        self.log_file = open(self.log_path, mode="w", newline='')
        self.csv_writer = csv.writer(self.log_file)

        # Write metadata
        self.csv_writer.writerow(["# Domain file:", domain_file])
        self.csv_writer.writerow(["# Problem file:", problem_file])
        self.csv_writer.writerow(["# Constants.TIMEOUT", constants.TIMEOUT])
        self.csv_writer.writerow(["# Constants.DELTA_T", constants.DELTA_T])
        self.csv_writer.writerow(["# Constants.TIME_HORIZON", constants.TIME_HORIZON])
        self.csv_writer.writerow(["# Constants.DEPTH_LIMIT", constants.DEPTH_LIMIT])
        self.csv_writer.writerow(["# Constants.METRIC_MINIMIZE", constants.METRIC_MINIMIZE])
        self.csv_writer.writerow([])  # Empty line before header

        # Write header
        self.csv_writer.writerow([
            "timestamp", "nodes_expanded", "max_depth", "queue_size",
            "min_metric", "max_metric", "tracked_goals"
        ])

        print(f"📊 Search stats log saved at: {os.path.abspath(self.log_path)}")

    def log_stats(self, timestamp, nodes_expanded, max_depth, queue_size, min_metric, max_metric, tracked_goals):
        self.csv_writer.writerow([
            round(timestamp, 2),
            nodes_expanded,
            max_depth,
            queue_size,
            round(min_metric, 4),
            round(max_metric, 4),
            tracked_goals
        ])

    def close(self):
        self.log_file.close()
