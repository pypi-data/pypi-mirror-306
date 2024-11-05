# from .data_processing_m1 import LocationProcessor, SensorDataProcessor, DataProcessor
# from .data_processing_m2 import LocationProcessor, SensorDataProcessor, DataProcessor
# 다른 모듈도 필요에 따라 추가


from .data_processing_m1 import LocationProcessor as M1LocationProcessor
from .data_processing_m1 import SensorDataProcessor as M1SensorDataProcessor
from .data_processing_m1 import DataProcessor as M1DataProcessor

from .data_processing_m2 import LocationProcessor as M2LocationProcessor
from .data_processing_m2 import SensorDataProcessor as M2SensorDataProcessor
from .data_processing_m2 import DataProcessor as M2DataProcessor


from .model1 import SuicideDataset,DataHandler
from .model1 import PredictionHandler
from .model1 import TemporalFusionTransformer

from .model2 import DataProcessor
from .model2 import CNNGRUClassificationModel
from .model2 import Predictor