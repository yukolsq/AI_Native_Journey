import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class DataAnalyzer:
    """
    A comprehensive data analysis and visualization class
    """
    
    def __init__(self, data: pd.DataFrame = None):
        """
        Initialize the DataAnalyzer with optional data
        
        Args:
            data (pd.DataFrame): Input dataset
        """
        self.data = data
        self.analysis_results = {}
        
    def create_sample_data(self) -> pd.DataFrame:
        """
        Create a sample dataset for demonstration
        
        Returns:
            pd.DataFrame: Sample dataset
        """
        np.random.seed(42)
        
        # Generate sample sales data
        n_records = 1000
        data = {
            'date': pd.date_range('2023-01-01', periods=n_records, freq='D'),
            'product_category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports'], n_records),
            'sales_amount': np.random.normal(150, 50, n_records),
            'quantity_sold': np.random.poisson(5, n_records),
            'customer_age': np.random.normal(35, 12, n_records),
            'customer_satisfaction': np.random.uniform(1, 5, n_records),
            'region': np.random.choice(['North', 'South', 'East', 'West'], n_records)
        }
        
        # Ensure positive values
        data['sales_amount'] = np.abs(data['sales_amount'])
        data['customer_age'] = np.clip(data['customer_age'], 18, 80)
        
        self.data = pd.DataFrame(data)
        return self.data
    
    def basic_statistics(self) -> Dict:
        """
        Calculate basic statistics for numerical columns
        
        Returns:
            Dict: Dictionary containing statistics
        """
        if self.data is None:
            raise ValueError("No data available. Please load or create data first.")
        
        numerical_cols = self.data.select_dtypes(include=[np.number]).columns
        stats = {}
        
        for col in numerical_cols:
            stats[col] = {
                'mean': self.data[col].mean(),
                'median': self.data[col].median(),
                'std': self.data[col].std(),
                'min': self.data[col].min(),
                'max': self.data[col].max(),
                'count': self.data[col].count(),
                'missing': self.data[col].isnull().sum()
            }
        
        self.analysis_results['basic_stats'] = stats
        return stats
    
    def correlation_analysis(self) -> pd.DataFrame:
        """
        Calculate correlation matrix for numerical columns
        
        Returns:
            pd.DataFrame: Correlation matrix
        """
        if self.data is None:
            raise ValueError("No data available. Please load or create data first.")
        
        numerical_data = self.data.select_dtypes(include=[np.number])
        correlation_matrix = numerical_data.corr()
        
        self.analysis_results['correlation'] = correlation_matrix
        return correlation_matrix
    
    def create_visualizations(self, save_plots: bool = True) -> None:
        """
        Create comprehensive visualizations
        
        Args:
            save_plots (bool): Whether to save plots to files
        """
        if self.data is None:
            raise ValueError("No data available. Please load or create data first.")
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 16))
        
        # 1. Sales Distribution
        plt.subplot(3, 3, 1)
        plt.hist(self.data['sales_amount'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title('Sales Amount Distribution')
        plt.xlabel('Sales Amount ($)')
        plt.ylabel('Frequency')
        
        # 2. Sales by Category
        plt.subplot(3, 3, 2)
        category_sales = self.data.groupby('product_category')['sales_amount'].sum()
        plt.pie(category_sales.values, labels=category_sales.index, autopct='%1.1f%%')
        plt.title('Total Sales by Product Category')
        
        # 3. Sales Trend Over Time
        plt.subplot(3, 3, 3)
        daily_sales = self.data.groupby('date')['sales_amount'].sum()
        plt.plot(daily_sales.index, daily_sales.values, linewidth=2)
        plt.title('Daily Sales Trend')
        plt.xlabel('Date')
        plt.ylabel('Total Sales ($)')
        plt.xticks(rotation=45)
        
        # 4. Correlation Heatmap
        plt.subplot(3, 3, 4)
        correlation_matrix = self.correlation_analysis()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Heatmap')
        
        # 5. Box Plot by Category
        plt.subplot(3, 3, 5)
        self.data.boxplot(column='sales_amount', by='product_category', ax=plt.gca())
        plt.title('Sales Amount by Category')
        plt.suptitle('')  # Remove default title
        
        # 6. Customer Age Distribution
        plt.subplot(3, 3, 6)
        plt.hist(self.data['customer_age'], bins=25, alpha=0.7, color='lightgreen', edgecolor='black')
        plt.title('Customer Age Distribution')
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        
        # 7. Satisfaction vs Sales Scatter
        plt.subplot(3, 3, 7)
        plt.scatter(self.data['customer_satisfaction'], self.data['sales_amount'], alpha=0.6)
        plt.title('Customer Satisfaction vs Sales Amount')
        plt.xlabel('Satisfaction Rating')
        plt.ylabel('Sales Amount ($)')
        
        # 8. Regional Sales
        plt.subplot(3, 3, 8)
        regional_sales = self.data.groupby('region')['sales_amount'].sum()
        plt.bar(regional_sales.index, regional_sales.values, color=['red', 'blue', 'green', 'orange'])
        plt.title('Total Sales by Region')
        plt.ylabel('Total Sales ($)')
        
        # 9. Quantity vs Sales
        plt.subplot(3, 3, 9)
        plt.scatter(self.data['quantity_sold'], self.data['sales_amount'], alpha=0.6, color='purple')
        plt.title('Quantity Sold vs Sales Amount')
        plt.xlabel('Quantity Sold')
        plt.ylabel('Sales Amount ($)')
        
        plt.tight_layout()
        
        if save_plots:
            plt.savefig('data_analysis_plots.png', dpi=300, bbox_inches='tight')
            print("Plots saved as 'data_analysis_plots.png'")
        
        plt.show()
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive analysis report
        
        Returns:
            str: Analysis report
        """
        if self.data is None:
            raise ValueError("No data available. Please load or create data first.")
        
        # Calculate statistics
        stats = self.basic_statistics()
        correlation_matrix = self.correlation_analysis()
        
        report = []
        report.append("=" * 60)
        report.append("DATA ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Dataset Shape: {self.data.shape}")
        report.append(f"Total Records: {len(self.data)}")
        report.append(f"Total Columns: {len(self.data.columns)}")
        report.append("")
        
        # Data types
        report.append("DATA TYPES:")
        report.append("-" * 20)
        for col, dtype in self.data.dtypes.items():
            report.append(f"{col}: {dtype}")
        report.append("")
        
        # Missing values
        missing_values = self.data.isnull().sum()
        if missing_values.sum() > 0:
            report.append("MISSING VALUES:")
            report.append("-" * 20)
            for col, missing in missing_values.items():
                if missing > 0:
                    report.append(f"{col}: {missing} ({missing/len(self.data)*100:.1f}%)")
        else:
            report.append("No missing values found!")
        report.append("")
        
        # Basic statistics
        report.append("BASIC STATISTICS:")
        report.append("-" * 20)
        for col, stat in stats.items():
            report.append(f"\n{col.upper()}:")
            for metric, value in stat.items():
                if isinstance(value, float):
                    report.append(f"  {metric}: {value:.2f}")
                else:
                    report.append(f"  {metric}: {value}")
        
        # Top correlations
        report.append("\nTOP CORRELATIONS:")
        report.append("-" * 20)
        correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                correlations.append((correlation_matrix.columns[i], correlation_matrix.columns[j], corr_value))
        
        # Sort by absolute correlation value
        correlations.sort(key=lambda x: abs(x[2]), reverse=True)
        for var1, var2, corr in correlations[:5]:
            report.append(f"{var1} vs {var2}: {corr:.3f}")
        
        return "\n".join(report)

def main():
    """
    Main function to demonstrate the data analysis capabilities
    """
    print("Creating Data Analyzer...")
    analyzer = DataAnalyzer()
    
    print("Generating sample dataset...")
    data = analyzer.create_sample_data()
    print(f"Dataset created with {len(data)} records")
    
    print("\nGenerating analysis report...")
    report = analyzer.generate_report()
    print(report)
    
    print("\nCreating visualizations...")
    analyzer.create_visualizations()
    
    print("\nAnalysis complete! Check the generated plots and report above.")

if __name__ == "__main__":
    main() 