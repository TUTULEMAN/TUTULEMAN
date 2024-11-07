import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split, GridSearchCV, TimeSeriesSplit
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.feature_selection import SelectFromModel
import xgboost as xgb
from sklearn.linear_model import LassoCV
import warnings
warnings.filterwarnings('ignore')

class EnhancedInterestRateAnalyzer:
    def __init__(self):
        """
        Initialize the enhanced analyzer with extended features
        """
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=3650)  # 10 years
        self.feature_importances = None
        self.selected_features = None
        
    def fetch_extended_data(self):
        """
        Fetch extended dataset with more economic indicators
        """
        # Extended financial instruments
        instruments = {
            # Interest Rate Related
            'Treasury_10Y': '^TNX',
            'Treasury_5Y': '^FVX',
            'Treasury_2Y': '^IRX',
            
            # Equity Indices
            'S&P500': '^GSPC',
            'Nasdaq': '^IXIC',
            'Russell2000': '^RUT',
            'VIX': '^VIX',
            
            # Commodities
            'Oil': 'CL=F',
            'Gold': 'GC=F',
            'Silver': 'SI=F',
            'Copper': 'HG=F',
            'Natural_Gas': 'NG=F',
            
            # Currency
            'Dollar_Index': 'DX-Y.NYB',
            'Euro_USD': 'EURUSD=X',
            'GBP_USD': 'GBPUSD=X',
            
            # Real Estate
            'Real_Estate': 'IYR'
        }
        
        df_list = []
        for name, ticker in instruments.items():
            try:
                data = yf.download(ticker, start=self.start_date, end=self.end_date)
                # Calculate multiple features for each instrument
                df_features = pd.DataFrame({
                    f'{name}_Close': data['Adj Close'],
                    f'{name}_Volume': data['Volume'],
                    f'{name}_High_Low_Range': data['High'] - data['Low'],
                    f'{name}_Daily_Return': data['Adj Close'].pct_change(),
                    f'{name}_Volatility': data['Adj Close'].pct_change().rolling(20).std(),
                    f'{name}_MA50': data['Adj Close'].rolling(50).mean(),
                    f'{name}_MA200': data['Adj Close'].rolling(200).mean()
                })
                df_list.append(df_features)
                print(f"Successfully processed {name} data")
            except Exception as e:
                print(f"Error processing {name}: {e}")
        
        self.df = pd.concat(df_list, axis=1)
        
        # Add derived features
        self.add_derived_features()
        
        # Handle missing values
        self.df = self.handle_missing_values()
        
        # Set target variable
        self.df['Target'] = self.df['Treasury_10Y_Close'].shift(-5)  # Predict 5 days ahead
        self.df = self.df.dropna()
        
    def add_derived_features(self):
        """
        Add sophisticated derived features
        """
        # Technical indicators
        for col in [col for col in self.df.columns if 'Close' in col]:
            base_name = col.replace('_Close', '')
            
            # Momentum indicators
            self.df[f'{base_name}_RSI'] = self.calculate_rsi(self.df[col])
            self.df[f'{base_name}_MACD'] = self.calculate_macd(self.df[col])
            
            # Trend indicators
            self.df[f'{base_name}_Trend_Strength'] = abs(
                self.df[f'{base_name}_MA50'] - self.df[f'{base_name}_MA200']
            ) / self.df[f'{base_name}_MA200']
            
        # Cross-asset correlations
        self.df['Gold_Oil_Ratio'] = self.df['Gold_Close'] / self.df['Oil_Close']
        self.df['SPX_Gold_Ratio'] = self.df['S&P500_Close'] / self.df['Gold_Close']
        self.df['VIX_SPX_Ratio'] = self.df['VIX_Close'] / self.df['S&P500_Close']
        
    @staticmethod
    def calculate_rsi(data, periods=14):
        """Calculate RSI indicator"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def calculate_macd(data, fast=12, slow=26):
        """Calculate MACD indicator"""
        exp1 = data.ewm(span=fast, adjust=False).mean()
        exp2 = data.ewm(span=slow, adjust=False).mean()
        return exp1 - exp2
        
    def handle_missing_values(self):
        """
        Sophisticated missing value handling
        """
        df_cleaned = self.df.copy()
        
        # Forward fill limited to 5 days
        df_cleaned = df_cleaned.fillna(method='ffill', limit=5)
        
        # Fill remaining NaNs with rolling median
        for col in df_cleaned.columns:
            if df_cleaned[col].isnull().any():
                df_cleaned[col] = df_cleaned[col].fillna(
                    df_cleaned[col].rolling(window=30, min_periods=1).median()
                )
        
        return df_cleaned
    
    def feature_selection(self, X, y):
        """
        Advanced feature selection
        """
        # Use Lasso for feature selection
        lasso = LassoCV(cv=5, random_state=42)
        lasso.fit(X, y)
        
        # Select features with non-zero coefficients
        feature_mask = np.abs(lasso.coef_) > 0
        selected_features = X.columns[feature_mask].tolist()
        
        # Also use Random Forest for feature importance
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X, y)
        
        # Combine both methods
        importance_mask = rf.feature_importances_ > np.mean(rf.feature_importances_)
        rf_selected = X.columns[importance_mask].tolist()
        
        # Take union of both methods
        self.selected_features = list(set(selected_features + rf_selected))
        return X[self.selected_features]
    
    def prepare_model_data(self):
        """
        Enhanced data preparation
        """
        # Remove target from features
        feature_cols = [col for col in self.df.columns if col != 'Target']
        
        # Split data
        X = self.df[feature_cols]
        y = self.df['Target']
        
        # Perform feature selection
        X = self.feature_selection(X, y)
        
        # Use robust scaling for better handling of outliers
        scaler = RobustScaler()
        X_scaled = scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
        
        # Use time series split
        return self.time_series_split(X_scaled, y)
    
    def time_series_split(self, X, y):
        """
        Time series aware splitting
        """
        split_index = int(len(X) * 0.8)
        X_train = X.iloc[:split_index]
        X_test = X.iloc[split_index:]
        y_train = y.iloc[:split_index]
        y_test = y.iloc[split_index:]
        return X_train, X_test, y_train, y_test
    
    def train_enhanced_model(self):
        """
        Train multiple models and create ensemble
        """
        X_train, X_test, y_train, y_test = self.prepare_model_data()
        
        models = {
            'rf': RandomForestRegressor(random_state=42),
            'gbm': GradientBoostingRegressor(random_state=42),
            'xgb': xgb.XGBRegressor(random_state=42)
        }
        
        # Parameter grids for each model
        param_grids = {
            'rf': {
                'n_estimators': [100, 200],
                'max_depth': [10, 20],
                'min_samples_split': [2, 5]
            },
            'gbm': {
                'n_estimators': [100, 200],
                'learning_rate': [0.01, 0.1],
                'max_depth': [3, 5]
            },
            'xgb': {
                'n_estimators': [100, 200],
                'learning_rate': [0.01, 0.1],
                'max_depth': [3, 5]
            }
        }
        
        best_models = {}
        for name, model in models.items():
            print(f"\nOptimizing {name}...")
            cv = TimeSeriesSplit(n_splits=5)
            grid_search = GridSearchCV(
                model, param_grids[name], cv=cv, scoring='neg_mean_squared_error',
                n_jobs=-1
            )
            grid_search.fit(X_train, y_train)
            best_models[name] = grid_search.best_estimator_
            
        # Create ensemble predictions
        predictions = {}
        for name, model in best_models.items():
            predictions[name] = model.predict(X_test)
        
        # Weighted ensemble based on validation performance
        weights = {}
        for name, pred in predictions.items():
            mse = mean_squared_error(y_test, pred)
            weights[name] = 1 / mse
            
        # Normalize weights
        weight_sum = sum(weights.values())
        weights = {k: v/weight_sum for k, v in weights.items()}
        
        # Final weighted prediction
        y_pred = sum(pred * weights[name] for name, pred in predictions.items())
        
        # Store feature importances from RF model
        self.feature_importances = pd.DataFrame({
            'feature': X_train.columns,
            'importance': best_models['rf'].feature_importances_
        }).sort_values('importance', ascending=False)
        
        return best_models, y_test, y_pred, X_test
    
    def evaluate_model(self, y_test, y_pred):
        """
        Comprehensive model evaluation
        """
        metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred)
        }
        
        # Calculate directional accuracy
        direction_correct = np.mean(
            (y_test.diff().dropna() * np.diff(y_pred)) > 0
        )
        metrics['directional_accuracy'] = direction_correct
        
        return metrics
    
    def plot_enhanced_analysis(self, y_test, y_pred):
        """
        Create enhanced visualizations
        """
        fig = make_subplots(rows=4, cols=1,
                           subplot_titles=('Predicted vs Actual Interest Rates',
                                         'Prediction Error Over Time',
                                         'Feature Importance',
                                         'Model Performance Metrics'))
        
        # Plot 1: Predicted vs Actual
        fig.add_trace(
            go.Scatter(x=y_test.index, y=y_test, name='Actual',
                      line=dict(color='blue')), row=1, col=1)
        fig.add_trace(
            go.Scatter(x=y_test.index, y=y_pred, name='Predicted',
                      line=dict(color='red')), row=1, col=1)
        
        # Plot 2: Prediction Error
        error = y_test - y_pred
        fig.add_trace(
            go.Scatter(x=y_test.index, y=error, name='Prediction Error',
                      line=dict(color='green')), row=2, col=1)
        
        # Plot 3: Feature Importance
        top_features = self.feature_importances.head(10)
        fig.add_trace(
            go.Bar(x=top_features['feature'], y=top_features['importance'],
                  name='Feature Importance'), row=3, col=1)
        
        # Plot 4: Performance Metrics
        metrics = self.evaluate_model(y_test, y_pred)
        fig.add_trace(
            go.Bar(x=list(metrics.keys()), y=list(metrics.values()),
                  name='Model Metrics'), row=4, col=1)
        
        fig.update_layout(height=1600, showlegend=True,
                         title_text="Enhanced Interest Rate Analysis Dashboard")
        return fig, metrics

    def run_enhanced_analysis(self):
        """
        Run the enhanced analysis pipeline
        """
        print("Fetching extended dataset...")
        self.fetch_extended_data()
        
        print("Training enhanced models...")
        models, y_test, y_pred, X_test = self.train_enhanced_model()
        
        print("Creating visualizations...")
        visualization, metrics = self.plot_enhanced_analysis(y_test, y_pred)
        
        return {
            'models': models,
            'metrics': metrics,
            'feature_importance': self.feature_importances,
            'visualization': visualization,
            'selected_features': self.selected_features
        }

# Example usage
if __name__ == "__main__":
    try:
        print("Initializing enhanced analyzer...")
        analyzer = EnhancedInterestRateAnalyzer()
        
        print("Running enhanced analysis...")
        results = analyzer.run_enhanced_analysis()
        
        print("\nModel Performance Metrics:")
        for metric, value in results['metrics'].items():
            print(f"{metric}: {value:.4f}")
        
        print("\nTop 10 Most Important Features:")
        print(results['feature_importance'].head(10))
        
        print("\nGenerating visualization...")
        results['visualization'].show()
        
    except Exception as e:
        print(f"An error occurred: {e}")
