import csv
import datetime as dt
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    statuses = defaultdict(int)

    def __init__(self):
        self.results_dir = BASE_DIR / 'results'
        self.results_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        now = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'status_summary_{now}.csv'
        file_path = self.results_dir / file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            result = [
                ('Статус', 'Количество')
            ]
            result.extend(self.statuses.items())
            result.append(('Total', sum(self.statuses.values())))
            writer.writerows(result)

    def process_item(self, item, spider):
        status = item['status']
        self.statuses[status] += 1
        return item
