from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

class DataPreprocessing:
    def __init__(self, X):
        self.X = X

    def impute_missing_values(self, strategy='mean'):
        imputer = SimpleImputer(strategy=strategy)
        X_imputed = imputer.fit_transform(self.X)
        return X_imputed

    def standardize_features(self):
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(self.X)
        return X_scaled
    
    def run(self):
        self.imputed = self.impute_missing_values()  # Fix: Remove self.X from impute_missing_values
        self.cleaned_df = self.standardize_features()  # Fix: Remove self.imputed from standardize_features
        return self.cleaned_df
