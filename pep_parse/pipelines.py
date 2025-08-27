import csv
import datetime as dt
from pathlib import Path

from .constants import STATUSES

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:

    def open_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'status_summary_{now}.csv'
        file_path = results_dir / file_name
        self.f = open(file_path, 'w', encoding='utf-8')

    def close_spider(self, spider):
        writer = csv.writer(self.f, dialect='unix')
        writer.writerow(['Статус', 'Количество'])
        writer.writerows(STATUSES.items())
        writer.writerow(('Total', sum(STATUSES.values())))
        self.f.close()

    def process_item(self, item, spider):
        status = item['status']
        if STATUSES.get(status):
            STATUSES[status] += 1
        else:
            STATUSES[status] = 1
        return item


# Можно это через бд сделать, в тз не прописано.
