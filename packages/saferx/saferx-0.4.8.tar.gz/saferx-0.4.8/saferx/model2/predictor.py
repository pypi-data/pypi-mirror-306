import sys
import torch
import pandas as pd
import numpy as np
import pickle
from torch.utils.data import DataLoader, TensorDataset
from .dataloader import DataProcessor
from .model import CNNGRUClassificationModel
import pkg_resources

class Predictor:
    def __init__(self, device=None, model_path=None):
        """
        모델과 장치를 초기화합니다.
        """
        # device가 None이면 GPU가 가능한지 확인하여 자동 설정
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if device is None else device

        # pkg_resources를 통해 모델 경로 명확화
        if model_path is None:
            model_path = pkg_resources.resource_filename('saferx', 'model2/model/final_model.pkl')
        
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
        """
        저장된 모델을 로드합니다. 예외 발생 시 모듈 경로 설정 후 재시도합니다.
        """
        try:
            return self.load_model(model_path)
        except ModuleNotFoundError as e:
            # 필요한 모듈을 sys.modules에 추가하여 경로 문제 해결
            import saferx.model2 as model2_module
            sys.modules['model2'] = model2_module
            print(f"ModuleNotFoundError handled: {e}. Retrying model load.")
            return self.load_model(model_path)

    def load_model(self, model_path):
        """
        저장된 모델을 로드합니다.
        """
        # 필요한 모듈이 sys.modules에 추가되었는지 확인
        if 'model2' not in sys.modules:
            import saferx.model2 as model2_module
            sys.modules['model2'] = model2_module
        
        # torch.load를 사용하여 map_location을 통해 장치 지정
        model = torch.load(model_path, map_location=self.device)
        return model

    def preprocess_data(self, data_path):
        """
        데이터를 로드하고 전처리한 후 DataLoader로 반환합니다.
        """
        data = pd.read_csv(data_path)
        data = DataProcessor.preprocess_data(data)
        data = DataProcessor.reset_week_numbers(data)
        data = DataProcessor.transform_target(data)

        max_length = DataProcessor.find_max_sequence_length_by_week(data, self.seq_cols)
        results = DataProcessor.prepare_data_for_model_by_week(data, max_length, self.seq_cols, self.target_cols)
        X_tensor, _ = DataProcessor.convert_results_to_tensors(results)
        return DataLoader(TensorDataset(X_tensor), batch_size=16, shuffle=False)

    def predict(self, data_loader):
        """
        데이터를 예측하고 결과를 반환합니다.
        """
        predictions = []
        with torch.no_grad():
            for inputs in data_loader:
                inputs = inputs[0].to(self.device)
                outputs = self.model(inputs)
                binary_predictions = (outputs >= 0.5).cpu().numpy()
                predictions.extend(binary_predictions)

        return np.array(predictions)

    def save_predictions(self, predictions, output_path):
        """
        예측 결과를 파일로 저장합니다.
        """
        df = pd.DataFrame(predictions, columns=self.target_cols)
        df.to_csv(output_path, index=False)
        print(f'Predictions saved at {output_path}')
