import csv
import datetime as dt

FORMAT = '%Y-%m-%d_%H-%M-%S'

# BASE_DIR = Path(__name__).absolute().parent
# BASE_DIR = Path(__file__).parent


class PepParsePipeline:
    def __init__(self):
        self.date = dt.datetime.now().strftime(FORMAT)
        self.file_name = f'results/status_summary_{self.date}.csv'
        self.file = open(self.file_name, 'w', newline='')
        self.writer = csv.writer(self.file)
        self.status_counts = {}

    def open_spider(self, spider):
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
