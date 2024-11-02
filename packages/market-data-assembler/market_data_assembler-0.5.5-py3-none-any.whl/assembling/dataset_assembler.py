import os
from datetime import datetime
from typing import List

from assembling.dataset_cache import DatasetCache
from assembling.dataset_labeler_abstract import BaseDatasetLabeler
from assembling.dataset_timeframe_aggregator import DatasetTimeframeAggregator
from common.common import random_string, load_compressed_json, generate_date_range
from indicators.indicator_abstract import BaseIndicator


class CryptoSeriesDatasetAssembler:
    dataset_out_root_folder = './out/datasets'

    def __init__(
            self,
            instruments: List[str],
            day_from: datetime,
            day_to: datetime,
            aggregation_window: int,
            dataset_labeler: BaseDatasetLabeler,
            raw_series_folder: str,
            indicators: List[BaseIndicator] = None,
            dataset_cleanup_keys: List[str] = None
    ):
        self.instruments = instruments
        self.selected_days = generate_date_range(day_from, day_to)
        self.aggregation_window = aggregation_window
        self.indicators: List[BaseIndicator] = indicators or []
        self.dataset_labeler: BaseDatasetLabeler = dataset_labeler
        self.raw_series_folder = raw_series_folder
        self.dataset_unique_name = random_string()
        self.dataset_cleanup_keys = set(dataset_cleanup_keys) if dataset_cleanup_keys else set()

        self.cache = DatasetCache(
            day_from,
            day_to,
            self.dataset_out_root_folder,
            self.instruments,
            self.aggregation_window,
            self.dataset_labeler,
            self.indicators,
            self.dataset_unique_name
        )

    def generate_dataset(self):
        datasets_path = self.cache.get_cached()
        if datasets_path:
            return datasets_path

        for instrument in self.instruments:
            self._process_instrument(instrument)

        datasets_path = self.cache.save_config()

        return datasets_path

    def _process_instrument(self, instrument):
        self._reset_state()
        timeframe_aggregator = DatasetTimeframeAggregator(60 * self.aggregation_window)

        for file_path in self._filter_and_sort_files(instrument):
            series = load_compressed_json(file_path)
            for candle in series:
                aggregated_candle = timeframe_aggregator.aggregate(candle)
                self._process_aggregated_candle(aggregated_candle, instrument)

        # Process any remaining aggregated candles
        aggregated_candle = timeframe_aggregator.get_aggregated_tail()
        self._process_aggregated_candle(aggregated_candle, instrument)

    def _reset_state(self):
        self.dataset_labeler.reset()
        for indicator in self.indicators:
            indicator.reset()

    def _process_aggregated_candle(self, aggregated_candle, instrument):
        if not aggregated_candle:
            return

        for indicator in self.indicators:
            indicator_value = indicator.apply(aggregated_candle)
            aggregated_candle[indicator.get_name()] = indicator_value

        if all(value is not None for value in aggregated_candle.values()):
            labeled_window = self.dataset_labeler.apply(aggregated_candle)
            if labeled_window:
                self._cleanup_series(labeled_window)
                dataset = self._map_to_dataset(labeled_window, instrument)
                self.cache.save_dataset(dataset, instrument)

    def _map_to_dataset(self, labeled, instrument):
        series = labeled['series']
        labels = labeled['labels']
        t_from = series[0]['t']
        t_to = series[-1]['t']
        return {
            'instrument': instrument,
            't_from': t_from,
            't_to': t_to,
            'series': series,
            'labels': labels
        }

    def _cleanup_series(self, labeled):
        if not self.dataset_cleanup_keys:
            return
        for candle in labeled['series']:
            for key in self.dataset_cleanup_keys:
                candle.pop(key, None)

    def _filter_and_sort_files(self, instrument):
        all_files = os.listdir(self.raw_series_folder)
        instrument_files = []

        for f in all_files:
            if f.startswith(instrument):
                file_date = datetime.strptime(f.split('_')[1].split('.')[0], '%Y-%m-%d')
                if file_date in self.selected_days:
                    instrument_files.append((file_date, f))

        instrument_files.sort(key=lambda x: x[0])
        return [os.path.join(self.raw_series_folder, f[1]) for f in instrument_files]
