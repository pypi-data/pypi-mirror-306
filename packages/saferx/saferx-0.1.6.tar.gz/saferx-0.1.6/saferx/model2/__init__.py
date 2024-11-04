# model2/__init__.py

import sys
from . import model  # 실제 model 모듈을 임포트하여 로드
sys.modules['model2.model'] = model  # 'model2.model'을 'saferx.model2.model'로 매핑

from .dataloader import DataProcessor  # DataProcessor 클래스는 데이터를 처리하는 기능을 포함합니다.
from .model import CNNGRUClassificationModel
from .predictor import Predictor
# from .predict import predict