from assembling.dataset_assembler import CryptoSeriesDatasetAssembler
from providers.crypto_series_data_provider import CryptoSeriesDataProvider


class DatasetsProvider:
    def __init__(self, config, params):
        self.config = config
        self.params = params

    def generate_dataset(self):
        assembler_config = self.config['assembler']
        dataset_labeler_class = assembler_config['dataset_labeler']['class']
        indicators = [
            indicator_config['class'](self.params['indicators'][f"indicator_{indicator_config['class'].__name__}"])
            for indicator_config in assembler_config['indicators']
        ]
        organizer = CryptoSeriesDatasetAssembler(
            instruments=self.params['instruments'],
            day_from=assembler_config['day_from'],
            day_to=assembler_config['day_to'],
            aggregation_window=self.params['aggregation_window'],
            dataset_labeler=dataset_labeler_class(
                training_window_length=self.params['training_window_length'],
                prediction_window_length=self.params['prediction_window_length']
            ),
            raw_series_folder=CryptoSeriesDataProvider.raw_series_folder,
            indicators=indicators,
            dataset_cleanup_keys=['trades']
        )
        return organizer.generate_dataset()
