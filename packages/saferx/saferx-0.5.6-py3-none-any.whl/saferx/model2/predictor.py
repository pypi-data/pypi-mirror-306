import sys
import torch
import pandas as pd
import numpy as np
import pickle
from torch.utils.data import DataLoader, TensorDataset
import pkg_resources
from .dataloader import DataProcessor
from .model import CNNGRUClassificationModel  # 사용 중인 모델 이름을 적절히 수정

class Predictor:
    def __init__(self, device=None, model_path=None):
        # device가 None이면 GPU가 가능한지 확인하여 자동 설정
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if device is None else device

        # model_path가 None이면 기본 경로로 설정
        if model_path is None:
            model_path = pkg_resources.resource_filename('saferx', 'model2/model/final_model.pkl')

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

        # 모델 로드
        self.model = self.load_model_with_retry(model_path)
        self.model.to(self.device)
        self.model.eval()

    def load_model_with_retry(self, model_path):
        try:
            return self.load_model(model_path)
        except ModuleNotFoundError as e:
            # 필요한 모듈을 sys.modules에 추가하여 경로 문제 해결
            import saferx.model2 as model2_module
            sys.modules['model2'] = model2_module
            print(f"ModuleNotFoundError handled: {e}. Retrying model load.")
            return self.load_model(model_path)

    def load_model(self, model_path):
        # pickle을 사용해 모델을 CPU에서 강제로 로드
        with open(model_path, 'rb') as f:
            model = pickle.load(f, encoding='latin1')
        
        # 모델을 CPU로 설정
        model.to(torch.device('cpu'))
        return model

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
