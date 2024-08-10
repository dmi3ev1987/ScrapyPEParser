import csv
import datetime as dt

from .constants import BASE_DIR, FORMAT


class PepParsePipeline:
    def __init__(self):
        self.date = dt.datetime.now().strftime(FORMAT)
        self.file_name = f'status_summary_{self.date}.csv'

        self.results_dir = BASE_DIR / 'results'
        self.results_dir.mkdir(exist_ok=True)

        self.file_path = self.results_dir / self.file_name

        self.status_counts = {}

    def open_spider(self, spider):
        self.file = open(self.file_path, 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Статус', 'Количество'])

    def process_item(self, item, spider):
        status = item['status']
        self.status_counts[status] = self.status_counts.get(status, 0) + 1
        return item

    def close_spider(self, spider):
        total_count = sum(self.status_counts.values())
        for status, count in self.status_counts.items():
            self.writer.writerow([status, count])
        self.writer.writerow(['Total', total_count])
        self.file.close()
