import pandas as pd
import joblib

class PredictionModel:
    def __init__(self, X, info_df):
        self.X = X
        self.info_df = info_df

    def predictions(self):
        self.X = pd.DataFrame(self.X)
        
        dt_loaded_model = joblib.load('decision_tree_model.pkl')
        hgb_loaded_model = joblib.load('hist_gradient_boosting_model.pkl')
        rf_loaded_model = joblib.load('random_forest_model.pkl')

        dt_predictions = []
        hgb_predictions = []
        rf_predictions = []
        for record in self.X.values:
            dt_prediction = dt_loaded_model.predict([record])[0]
            hgb_prediction = hgb_loaded_model.predict([record])[0]
            rf_prediction = rf_loaded_model.predict([record])[0]
            dt_predictions.append(dt_prediction)
            hgb_predictions.append(hgb_prediction)
            rf_predictions.append(rf_prediction)

        predictions_df = pd.DataFrame({
            'DecisionTree_Prediction': dt_predictions,
            'HistGradientBoosting_Prediction': hgb_predictions,
            'RandomForest_Prediction': rf_predictions
        })

        return predictions_df

    def merge_csv(self):
        self.merged_df = pd.concat([self.info_df, self.predictions_df], axis=1)
        return self.merged_df

    def run(self):
        self.predictions_df = self.predictions()
        self.merged_pd = self.merge_csv()
        self.csv_filename = 'merged_data.csv'
        self.merged_df.to_csv(self.csv_filename, index=False)
        return self.csv_filename