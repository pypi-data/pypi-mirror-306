import torch
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import pkg_resources
from .dataloader import DataProcessor  # DataProcessor는 그대로 사용
from .model import CNNGRUClassificationModel

class Predictor:
    def __init__(self, device, model_path=None):
        """
        모델과 장치를 초기화합니다.
        """
        
        if model_path is None:
            model_path = pkg_resources.resource_filename('saferx', 'model2/model/final_model_revised.pkl')
        
        # 기본 seq_cols 및 target_cols 고정
        self.seq_cols = [
            'Daily_Entropy', 'Normalized_Daily_Entropy', 'Eight_Hour_Entropy', 'Normalized_Eight_Hour_Entropy',
            'first_TOTAL_ACCELERATION', 'Location_Variability', 'last_TOTAL_ACCELERATION', 'mean_TOTAL_ACCELERATION',
            'median_TOTAL_ACCELERATION', 'max_TOTAL_ACCELERATION', 'min_TOTAL_ACCELERATION', 'std_TOTAL_ACCELERATION',
            'nunique_TOTAL_ACCELERATION', 'delta_CALORIES', 'first_HEARTBEAT', 'last_HEARTBEAT', 'mean_HEARTBEAT',
            'median_HEARTBEAT', 'max_HEARTBEAT', 'min_HEARTBEAT', 'std_HEARTBEAT', 'nunique_HEARTBEAT',
            'delta_DISTANCE', 'delta_SLEEP', 'delta_STEP', 'sex', 'age', 'place_Unknown', 'place_hallway', 'place_other', 'place_ward'
        ]
        self.target_cols = ['BPRS_change', 'YMRS_change', 'MADRS_change', 'HAMA_change']

        self.device = device
        self.model = self.load_model(model_path)  # torch.load로 수정된 메서드 사용
        self.model.to(self.device)
        self.model.eval()  # 평가 모드로 전환

    def load_model(self, model_path):
        """
        GPU로 저장된 모델을 CPU에서 로드할 수 있도록 torch.load를 사용합니다.
        """
        # map_location을 통해 CPU로 강제 로드
        model = torch.load(model_path, map_location=torch.device('cpu'))
        return model

    # 이하 기존 메서드 유지
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
