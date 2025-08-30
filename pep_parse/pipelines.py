import csv
import datetime as dt
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    STATUSES = defaultdict(int, {
        'Active': 0,
        'Accepted': 0,
        'Deferred': 0,
        'Draft': 0,
        'Final': 0,
        'Provisional': 0,
        'Rejected': 0,
        'Superseded': 0,
        'Withdrawn': 0
    })

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
            result.extend(self.STATUSES.items())
            result.append(('Total', sum(self.STATUSES.values())))
            writer.writerows(result)

    def process_item(self, item, spider):
        status = item['status']
        self.STATUSES[status] += 1
        return item
