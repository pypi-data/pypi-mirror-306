import json
import os
from datetime import datetime
from typing import List

from assembling.dataset_labeler_abstract import BaseDatasetLabeler
from common.common import prepare_directory
from indicators.indicator_abstract import BaseIndicator


class DatasetCache:
    CONFIG_FILE_PREFIX = '_dataset_config.json'

    def __init__(self,
                 day_from: datetime,
                 day_to: datetime,
                 dataset_out_root_folder: str,
                 instruments: List[str],
                 aggregation_window: int,
                 dataset_labeler: BaseDatasetLabeler,
                 indicators: List[BaseIndicator],
                 dataset_unique_name: str):
        self.dataset_out_root_folder = dataset_out_root_folder
        self.instruments = instruments
        self.day_from = day_from
        self.day_to = day_to
        self.aggregation_window = aggregation_window
        self.dataset_labeler = dataset_labeler
        self.indicators = indicators
        self.dataset_unique_name = dataset_unique_name
        self.dataset_out_folder = os.path.join(self.dataset_out_root_folder, self.dataset_unique_name)

    def get_cached(self):
        config = self._generate_dataset_config()
        for file in os.listdir(self.dataset_out_root_folder):
            if file.endswith(self.CONFIG_FILE_PREFIX):
                with open(os.path.join(self.dataset_out_root_folder, file), 'r') as f:
                    existing_config = json.load(f)
                    if existing_config == config:
                        dataset_folder = file.replace(self.CONFIG_FILE_PREFIX, '')
                        print(
                            f"process-{os.getpid()}, time: {datetime.now()}, datasets exist: {self._get_short_info()}")

                        return os.path.join(self.dataset_out_root_folder, dataset_folder)

        prepare_directory(self.dataset_out_folder)
        return None

    def save_dataset(self, dataset, instrument):
        dataset_filename = f"{instrument}_{dataset['t_from']}.json"
        dataset_filepath = os.path.join(self.dataset_out_folder, dataset_filename)
        with open(dataset_filepath, 'w') as f:
            json.dump(dataset, f, indent=1)

    def save_config(self):
        config = self._generate_dataset_config()
        config_path = os.path.join(self.dataset_out_root_folder, f'{self.dataset_unique_name}{self.CONFIG_FILE_PREFIX}')
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=1)
        print(
            f"process-{os.getpid()}, time: {datetime.now()}, save datasets: {self._get_short_info()}")

        return self.dataset_out_folder

    def _get_short_info(self):
        indicators_str = ", ".join([
            f'{indicator.get_name()}({indicator.window_length})'
            for indicator in self.indicators
        ])

        return (f"from: {self.day_from.strftime('%Y-%m-%d')}, "
                f"to: {self.day_to.strftime('%Y-%m-%d')}, "
                f"window: {self.aggregation_window}, "
                f"labels: {self.dataset_labeler.training_window_length}-{self.dataset_labeler.prediction_window_length}, "
                f"indicators: {indicators_str}, "
                f"instruments: {self.instruments}")

    def _generate_dataset_config(self):
        config = {
            "day_from": self.day_from.strftime('%Y-%m-%d'),
            "day_to": self.day_to.strftime('%Y-%m-%d'),
            "instruments": self.instruments,
            "aggregation_window": self.aggregation_window,
            "labeling": {
                "name": self.dataset_labeler.get_name(),
                "training_window_length": self.dataset_labeler.training_window_length,
                "prediction_window_length": self.dataset_labeler.prediction_window_length,
            },
            "indicators": [
                {
                    "name": indicator.get_name(),
                    "window_length": indicator.window_length
                } for indicator in self.indicators
            ]
        }
        return config