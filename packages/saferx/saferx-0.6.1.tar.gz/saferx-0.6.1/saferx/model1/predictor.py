import pandas as pd
import numpy as np
import torch
import pkg_resources
from .dataloader import DataHandler
from .model import TemporalFusionTransformer
import sys

class PredictionHandler:
    def __init__(self, data_paths, batch_size=16, device=None, model_path=None):
        # GPU가 있으면 'cuda', 없으면 'cpu'로 자동 설정
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if device is None else torch.device(device)
        
        if model_path is None:
            # pkg_resources를 사용하여 패키지 내부 경로에서 모델 파일 로드
            model_path = pkg_resources.resource_filename('saferx', 'model1/model/tft_model_converted.pth')
        self.model_path = model_path
        self.data_paths = data_paths
        self.batch_size = batch_size

        # 데이터 로드 및 전처리
        self.data_handler = DataHandler()
        self.data_handler.load_data(data_paths)
        self.data_handler.preprocess_data()  # 전처리 적용

        # 데이터 로더 생성
        self.train_dataloader, self.val_dataloader = self.data_handler.get_dataloaders(batch_size=batch_size)
        static_input_size = len(self.data_handler.static_variables)
        sequence_input_size = len(self.data_handler.sequence_variables)
        # 모델 초기화
        self.model = TemporalFusionTransformer(
            hidden_size=16,
            lstm_layers=2,
            dropout=0.1,
            output_size=1,
            attention_head_size=4,
            static_input_size=static_input_size,
            sequence_input_size=sequence_input_size
        )

        # .pth 파일에서 state_dict를 로드하여 모델 초기화
        state_dict = torch.load(self.model_path, map_location=self.device)
        self.model.load_state_dict(state_dict)

        # 모델을 디바이스로 이동 (GPU 또는 CPU)
        self.model.to(self.device)
        self.model.eval()

    def predict(self):
        predictions = []
        try:
            self.model.eval()
            with torch.no_grad():
                for batch in self.val_dataloader:
                    static_data, sequence_data, _ = batch
                    static_data, sequence_data = static_data.to(self.device), sequence_data.to(self.device)
                    outputs, _, _ = self.model(static_data, sequence_data)
                    # 이진 결과로 변환
                    predictions.append((outputs >= 0.5).cpu().numpy())
            return np.concatenate(predictions, axis=0)
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

    def count_predictions(self):
        """
        예측 결과에서 0과 1의 개수를 계산.

        :return: 0과 1의 개수를 포함하는 튜플 (count_0, count_1).
        """
        predictions = self.predict()
        if predictions is not None:
            count_0 = np.sum(predictions == False)
            count_1 = np.sum(predictions == True)
            
            print(f"Number of 0s: {count_0}")
            print(f"Number of 1s: {count_1}")
            
            return count_0, count_1
        else:
            print("No predictions to count.")
            return None, None
