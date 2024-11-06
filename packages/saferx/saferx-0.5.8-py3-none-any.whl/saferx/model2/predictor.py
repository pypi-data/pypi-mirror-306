import sys
import torch
import pandas as pd
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
import pkg_resources
from .dataloader import DataProcessor
from .model import CNNGRUClassificationModel  # 모델 클래스 명확히 지정

class Predictor:
    def __init__(self, device=None, model_path=None):
        # device가 None이면 GPU가 가능한지 확인하여 자동 설정
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if device is None else device

        # model_path가 None이면 기본 경로로 설정
        if model_path is None:
            model_path = pkg_resources.resource_filename('saferx', 'model2/model/final_model_converted.pth')

        # seq_cols 및 target_cols 정의
        self.seq_cols = [
            'Daily_Entropy', 'Normalized_Daily_Entropy', 'Eight_Hour_Entropy', 'Normalized_Eight_Hour_Entropy',
            'first_TOTAL_ACCELERATION', 'Location_Variability', 'last_TOTAL_ACCELERATION', 'mean_TOTAL_ACCELERATION',
            'median_TOTAL_ACCELERATION', 'max_TOTAL_ACCELERATION', 'min_TOTAL_ACCELERATION', 'std_TOTAL_ACCELERATION',
            'nunique_TOTAL_ACCELERATION', 'delta_CALORIES', 'first_HEARTBEAT', 'last_HEARTBEAT', 'mean_HEARTBEAT',
            'median_HEARTBEAT', 'max_HEARTBEAT', 'min_HEARTBEAT', 'std_HEARTBEAT', 'nunique_HEARTBEAT',
            'delta_DISTANCE', 'delta_SLEEP', 'delta_STEP', 'sex', 'age', 'place_Unknown', 'place_hallway', 'place_other', 'place_ward'
        ]
        self.target_cols = ['BPRS_change', 'YMRS_change', 'MADRS_change', 'HAMA_change']

        # CNNGRUClassificationModel의 구조를 초기화하고 가중치를 로드
        self.model = CNNGRUClassificationModel(input_dim=31, cnn_out_channels=256, cnn_kernel_size=4, gru_hidden_dim=64, output_dim=4, dropout_prob=0.5)
        self.load_model(model_path)
        self.model.to(self.device)
        self.model.eval()

    def load_model(self, model_path):
        """
        변환된 .pth 파일로부터 state_dict를 로드합니다.
        """
        # state_dict를 로드하여 모델에 적용
        state_dict = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(state_dict)

    def preprocess_data(self, data_path):
        data = pd.read_csv(data_path)
        data = DataProcessor.preprocess_data(data)
        data = DataProcessor.reset_week_numbers(data)
        data = DataProcessor.transform_target(data)

        max_length = DataProcessor.find_max_sequence_length_by_week(data, self.seq_cols)
        results = DataProcessor.prepare_data_for_model_by_week(data, max_length, self.seq_cols, self.target_cols)
        X_tensor, _ = DataProcessor.convert_results_to_tensors(results)
        return DataLoader(TensorDataset(X_tensor), batch_size=16, shuffle=False)

    def predict(self, data_loader):
        predictions = []
        with torch.no_grad():
            for inputs in data_loader:
                inputs = inputs[0].to(self.device)
                outputs = self.model(inputs)
                binary_predictions = (outputs >= 0.5).cpu().numpy()
                predictions.extend(binary_predictions)

        return np.array(predictions)

    def save_predictions(self, predictions, output_path):
        df = pd.DataFrame(predictions, columns=self.target_cols)
        df.to_csv(output_path, index=False)
        print(f'Predictions saved at {output_path}')
