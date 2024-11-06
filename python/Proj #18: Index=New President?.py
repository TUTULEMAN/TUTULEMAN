'''
--------------------------------------------------------------------------------------------------------------------------------------------------------------
|  Abstract:                                                                                                                                                  |
|  This aims to look into the movement in different economic metrics to measure and predict its influence on the presidential votes across 50 US States.      |
|    => alpha=53%                                                                                                                                             |
|    => Not that confident of an approach apparently:)                                                                                                        |
--------------------------------------------------------------------------------------------------------------------------------------------------------------
'''              
----------------------
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

class ElectionAnalyzer:
    def __init__(self):
        self.state_votes_df = None
        self.economic_df = None
        self.combined_df = None
        
        # All US states including DC
        self.states = [
            'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
            'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia',
            'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
            'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
            'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
            'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
            'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
            'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
            'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
            'West Virginia', 'Wisconsin', 'Wyoming'
        ]
        
        # Election years from 1976 to 2020
        self.election_years = list(range(1976, 2021, 4))
        
    def load_state_voting_data(self, filepath=None):
        """
        Load or create historical state voting data from 1976-2020
        Structure: Year, State, Winner Party, Margin of Victory, Total Votes
        """
        # Create sample historical data structure
        # In real implementation, load from CSV or API
        data = []
        
        # Generate sample data for each state and election year
        for year in self.election_years:
            for state in self.states:
                # Simplified logic for sample data generation
                # In reality, this would be actual historical data
                if year == 2020:
                    # 2020 actual results (simplified)
                    if state in ['California', 'New York', 'Illinois']:
                        winner = 'D'
                        margin = np.random.uniform(55, 65)
                    elif state in ['Texas', 'Florida', 'Ohio']:
                        winner = 'R'
                        margin = np.random.uniform(51, 58)
                    else:
                        winner = np.random.choice(['D', 'R'])
                        margin = np.random.uniform(50, 60)
                else:
                    # Historical data simulation
                    winner = np.random.choice(['D', 'R'])
                    margin = np.random.uniform(50, 65)
                
                total_votes = int(np.random.uniform(100000, 5000000))
                
                data.append({
                    'year': year,
                    'state': state,
                    'winner_party': winner,
                    'margin': margin,
                    'total_votes': total_votes
                })
        
        self.state_votes_df = pd.DataFrame(data)
        
    def load_economic_indicators(self, filepath=None):
        """
        Load or create economic indicators data from 1976-2020
        """
        data = []
        
        # Generate historical economic data
        for year in self.election_years:
            # Simplified historical trends
            if year >= 2008:
                # Post-2008 financial crisis era
                gdp_growth = np.random.uniform(-2, 3)
                interest_rate_change = np.random.uniform(-0.5, 0.5)
                unemployment_rate_change = np.random.uniform(-1, 2)
            else:
                # Pre-2008 era
                gdp_growth = np.random.uniform(2, 5)
                interest_rate_change = np.random.uniform(-0.25, 1)
                unemployment_rate_change = np.random.uniform(-0.5, 1)
            
            data.append({
                'year': year,
                'gdp_growth': gdp_growth,
                'interest_rate_change': interest_rate_change,
                'gold_price_change': np.random.uniform(-15, 25),
                'oil_price_change': np.random.uniform(-30, 40),
                'unemployment_rate_change': unemployment_rate_change,
                'inflation_rate': np.random.uniform(1, 5),
                'consumer_confidence': np.random.uniform(70, 120),
                'stock_market_return': np.random.uniform(-10, 20),
                'real_income_growth': np.random.uniform(-2, 4)
            })
            
        self.economic_df = pd.DataFrame(data)
        
    def combine_datasets(self):
        """
        Merge voting data with economic indicators
        """
        if self.state_votes_df is None or self.economic_df is None:
            raise ValueError("Please load both datasets first")
            
        self.combined_df = pd.merge(
            self.state_votes_df,
            self.economic_df,
            on='year',
            how='left'
        )
        
    def analyze_state_trends(self):
        """
        Analyze historical voting trends by state
        """
        if self.combined_df is None:
            raise ValueError("Please combine datasets first")
            
        state_analysis = self.combined_df.groupby('state').agg({
            'winner_party': [
                ('most_common_winner', lambda x: x.value_counts().index[0]),
                ('democratic_wins', lambda x: (x == 'D').sum()),
                ('republican_wins', lambda x: (x == 'R').sum())
            ],
            'margin': [
                ('avg_margin', 'mean'),
                ('margin_volatility', 'std'),
                ('closest_race', 'min'),
                ('biggest_landslide', 'max')
            ],
            'total_votes': [
                ('avg_turnout', 'mean'),
                ('turnout_trend', lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0] * 100)
            ]
        })
        
        return state_analysis
    
    def train_prediction_model(self):
        """
        Train a random forest model to predict state winners
        """
        if self.combined_df is None:
            raise ValueError("Please combine datasets first")
            
        # Prepare features and target
        features = [
            'margin', 'gdp_growth', 'interest_rate_change', 'gold_price_change',
            'oil_price_change', 'unemployment_rate_change', 'inflation_rate',
            'consumer_confidence', 'stock_market_return', 'real_income_growth'
        ]
        
        # Create state dummies
        state_dummies = pd.get_dummies(self.combined_df['state'], prefix='state')
        X = pd.concat([self.combined_df[features], state_dummies], axis=1)
        y = (self.combined_df['winner_party'] == 'D').astype(int)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            min_samples_split=10,
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        # Feature importance
        importance_df = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return model, accuracy, report, importance_df
    
    def analyze_swing_states(self):
        """
        Identify and analyze swing states
        """
        state_stats = self.combined_df.groupby('state').agg({
            'winner_party': lambda x: len(x.unique()),  # Number of different winners
            'margin': 'std'  # Volatility in margin
        }).sort_values('margin', ascending=False)
        
        swing_states = state_stats[
            (state_stats['winner_party'] > 1) &
            (state_stats['margin'] > state_stats['margin'].median())
        ]
        
        return swing_states
    
    def visualize_economic_impact(self):
        """
        Create visualizations of economic indicators vs election results
        """
        if self.combined_df is None:
            raise ValueError("Please combine datasets first")
            
        # Create correlation matrix
        economic_cols = [
            'gdp_growth', 'interest_rate_change', 'gold_price_change',
            'oil_price_change', 'unemployment_rate_change', 'inflation_rate',
            'consumer_confidence', 'stock_market_return', 'real_income_growth'
        ]
        
        correlation_matrix = self.combined_df[economic_cols + ['margin']].corr()
        
        # Create multiple visualizations
        fig = plt.figure(figsize=(20, 10))
        
        # Correlation heatmap
        plt.subplot(1, 2, 1)
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation between Economic Indicators and Victory Margin')
        
        # Economic trends over time
        plt.subplot(1, 2, 2)
        economic_trends = self.economic_df.set_index('year')[
            ['gdp_growth', 'unemployment_rate_change', 'inflation_rate']
        ]
        economic_trends.plot(marker='o')
        plt.title('Key Economic Indicators Over Time')
        plt.grid(True)
        
        plt.tight_layout()
        return plt

def main():
    # Initialize analyzer
    analyzer = ElectionAnalyzer()
    
    # Load data
    analyzer.load_state_voting_data()
    analyzer.load_economic_indicators()
    analyzer.combine_datasets()
    
    # Train prediction model
    model, accuracy, report, feature_importance = analyzer.train_prediction_model()
    print(f"Model Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(report)
    print("\nTop 10 Most Important Features:")
    print(feature_importance.head(10))
    
    # Analyze state trends
    state_analysis = analyzer.analyze_state_trends()
    print("\nState Voting Patterns:")
    print(state_analysis)
    
    # Identify swing states
    swing_states = analyzer.analyze_swing_states()
    print("\nSwing States Analysis:")
    print(swing_states)
    
    # Visualize economic impacts
    analyzer.visualize_economic_impact()
    plt.show()

if __name__ == "__main__":
    main()
