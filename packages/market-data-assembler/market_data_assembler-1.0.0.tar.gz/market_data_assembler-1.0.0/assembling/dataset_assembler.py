import os
from datetime import datetime
from typing import List

from aggregator.missing_candles_enricher import MissingCandlesEnricher
from assembling.aggregation_config import AggregationConfig, AggregationConfigInstance
from assembling.dataset_cache import DatasetCache
from common.common import random_string, load_compressed_json, generate_date_range
from labeling.dataset_labeler_abstract import BaseDatasetLabeler


class CryptoSeriesDatasetAssembler:
    """Assembles a dataset from cryptocurrency series data."""

    dataset_out_root_folder = './out/datasets'

    def __init__(
            self,
            instruments: List[str],
            day_from: datetime,
            day_to: datetime,
            dataset_labeler: BaseDatasetLabeler,
            aggregations_configs: List[AggregationConfig],
            raw_series_folder: str,
    ):

        self.instruments = instruments
        self.selected_days = generate_date_range(day_from, day_to)
        self.dataset_labeler: BaseDatasetLabeler = dataset_labeler
        self.raw_series_folder = raw_series_folder
        self.dataset_unique_name = random_string()

        self.aggregations = AggregationConfigInstance.from_config_list(aggregations_configs)
        self.main_aggregation = AggregationConfigInstance.find_main_aggregation_config(self.aggregations)
        self.missing_candles_enricher = MissingCandlesEnricher(window=self.main_aggregation.get_window_sec())

        self.cache = DatasetCache(
            day_from,
            day_to,
            self.dataset_out_root_folder,
            self.instruments,
            self.aggregations,
            self.dataset_labeler,
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
        for file_path in self._filter_and_sort_files(instrument):
            series = load_compressed_json(file_path)
            for raw_candle in series:
                self._process_raw_candle(raw_candle, instrument)

    def _process_raw_candle(self, raw_candle, instrument):
        enriched_candles = self.missing_candles_enricher.generate(raw_candle)
        for candle in enriched_candles:
            self._process_aggregations(candle, instrument)

    def _reset_state(self):
        self.last_candle_time = 0
        self.missing_candles_enricher.reset()
        for aggregator in self.aggregations:
            aggregator.ohlc.reset()
            for indicator in aggregator.indicators:
                indicator.reset()

    def _update_aggregations(self, raw_candle):
        for aggregator in self.aggregations:
            aggregator.ohlc.aggregate(raw_candle)
            aggregated_candle = aggregator.ohlc.get_last_aggregated()
            for indicator in aggregator.indicators:
                indicator.apply(aggregated_candle)

    def _process_aggregations(self, candle, instrument):
        self._update_aggregations(candle)

        if self.main_aggregation.ohlc.is_fully_aggregated() and self._all_aggregations_ready():
            labels = self.dataset_labeler.apply(self.aggregations)
            dataset = self._map_dataset(labels, instrument)
            self.cache.save_dataset(dataset, instrument)

    def _all_aggregations_ready(self):
        return all(
            aggregator.ohlc.is_ready() and all(indicator.is_ready() for indicator in aggregator.indicators)
            for aggregator in self.aggregations
        )

    def _map_dataset(self, dataset, instrument):
        labels = dataset['labels']
        date_range = self.main_aggregation.get_time_period()
        aggregations = []

        for aggregator in self.aggregations:
            series = self._to_ohlc_dataset_map(aggregator.ohlc.get_history())

            indicators = [
                {
                    "indicator_class": indicator.__class__.__name__,
                    "window_length": indicator.window_length,
                    "values": indicator.get_history()
                }
                for indicator in aggregator.indicators
            ]

            aggregations.append({
                'ohlc': {
                    'window_sec': aggregator.ohlc.window_sec,
                    'history_size': aggregator.ohlc.history_size,
                    'series': series
                },
                'indicators': indicators
            })

        dataset = {
            'instrument': instrument,
            'from': date_range['from'],
            'to': date_range['to'],
            'labels': labels,
            'aggregations': aggregations
        }

        return dataset

    @staticmethod
    def _to_ohlc_dataset_map(candles: List):
        series = {}
        for candle in candles:
            for c_key, c_value in candle.items():
                if c_key in ['o', 'c', 'h', 'l', 'v']:
                    series.setdefault(c_key, []).append(c_value)
        return series

    def _filter_and_sort_files(self, instrument):
        all_files = os.listdir(self.raw_series_folder)
        selected_days_naive = [day.replace(tzinfo=None) for day in self.selected_days]

        instrument_files = []
        for f in all_files:
            if f.startswith(instrument):
                date_str = f.split('_')[1].split('.')[0]
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                if file_date in selected_days_naive:
                    instrument_files.append((file_date, f))

        instrument_files.sort(key=lambda x: x[0])
        return [os.path.join(self.raw_series_folder, f[1]) for f in instrument_files]
