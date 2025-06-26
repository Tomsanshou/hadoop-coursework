# -*- coding: utf-8 -*-
"""
Data Processing Utilities for E-commerce Order Analysis
电商订单分析数据处理工具

This module contains functions for data generation, loading, cleaning, and preprocessing.
本模块包含数据生成、加载、清洗和预处理功能。
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple

# Import configuration
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_GENERATION_CONFIG, ANALYSIS_CONFIG

class DataProcessor:
    """
    Data processing class for e-commerce order analysis
    电商订单分析数据处理类
    """
    
    def __init__(self):
        """
        Initialize the DataProcessor
        初始化数据处理器
        """
        self.logger = logging.getLogger(__name__)
        np.random.seed(ANALYSIS_CONFIG["random_seed"])
        random.seed(ANALYSIS_CONFIG["random_seed"])
    
    def generate_sample_data(self, output_file: Optional[Path] = None) -> pd.DataFrame:
        """
        Generate sample e-commerce order data
        生成示例电商订单数据
        
        Args:
            output_file: Path to save the generated data
        
        Returns:
            DataFrame containing sample order data
        """
        self.logger.info("Generating sample e-commerce order data")
        
        config = DATA_GENERATION_CONFIG
        
        # Generate date range
        start_date = datetime.strptime(config["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(config["end_date"], "%Y-%m-%d")
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate product data
        products = self._generate_products()
        
        # Generate customer data
        customers = self._generate_customers(config["num_customers"], config["cities"])
        
        # Generate orders
        orders = []
        for i in range(config["num_orders"]):
            order = self._generate_single_order(i+1, date_range, products, customers)
            orders.append(order)
        
        df = pd.DataFrame(orders)
        
        if output_file:
            df.to_csv(output_file, index=False, encoding='utf-8')
            self.logger.info(f"Sample data saved to {output_file}")
        
        self.logger.info(f"Generated {len(df)} sample orders")
        return df
    
    def _generate_products(self) -> List[Dict]:
        """
        Generate product catalog
        生成产品目录
        """
        products = []
        categories = DATA_GENERATION_CONFIG["product_categories"]
        
        product_names = {
            "Electronics": ["iPhone 14", "Samsung Galaxy", "MacBook Pro", "iPad", "AirPods", "Gaming Laptop"],
            "Clothing": ["T-Shirt", "Jeans", "Dress", "Jacket", "Sneakers", "Sweater"],
            "Books": ["Python Programming", "Data Science", "Machine Learning", "Web Development", "AI Handbook"],
            "Home & Garden": ["Coffee Maker", "Vacuum Cleaner", "Garden Tools", "Kitchen Set", "Sofa"],
            "Sports": ["Running Shoes", "Yoga Mat", "Dumbbells", "Tennis Racket", "Basketball"],
            "Beauty": ["Skincare Set", "Makeup Kit", "Perfume", "Hair Dryer", "Face Mask"],
            "Toys": ["LEGO Set", "Board Game", "Action Figure", "Puzzle", "Remote Car"],
            "Food": ["Organic Tea", "Chocolate", "Snack Box", "Coffee Beans", "Honey"],
            "Health": ["Vitamins", "Protein Powder", "First Aid Kit", "Thermometer", "Massage Gun"],
            "Automotive": ["Car Charger", "Dash Cam", "Car Cover", "Tire Pump", "Car Accessories"]
        }
        
        price_ranges = {
            "Electronics": (100, 5000),
            "Clothing": (20, 300),
            "Books": (15, 80),
            "Home & Garden": (30, 800),
            "Sports": (25, 500),
            "Beauty": (10, 200),
            "Toys": (15, 150),
            "Food": (5, 100),
            "Health": (20, 300),
            "Automotive": (25, 400)
        }
        
        for category in categories:
            for product_name in product_names[category]:
                min_price, max_price = price_ranges[category]
                products.append({
                    "category": category,
                    "name": product_name,
                    "base_price": round(np.random.uniform(min_price, max_price), 2)
                })
        
        return products
    
    def _generate_customers(self, num_customers: int, cities: List[str]) -> List[Dict]:
        """
        Generate customer data
        生成客户数据
        """
        customers = []
        for i in range(num_customers):
            customers.append({
                "customer_id": f"CUST_{i+1:06d}",
                "age": np.random.randint(18, 70),
                "gender": np.random.choice(["Male", "Female"], p=[0.48, 0.52]),
                "city": np.random.choice(cities)
            })
        return customers
    
    def _generate_single_order(self, order_id: int, date_range: pd.DatetimeIndex, 
                              products: List[Dict], customers: List[Dict]) -> Dict:
        """
        Generate a single order
        生成单个订单
        """
        # Select random customer and product
        customer = random.choice(customers)
        product = random.choice(products)
        
        # Generate order details
        quantity = np.random.randint(1, 6)
        unit_price = product["base_price"] * np.random.uniform(0.8, 1.2)  # Add price variation
        total_amount = quantity * unit_price
        
        # Add seasonal effects to order date probability
        order_date = np.random.choice(date_range)
        
        # Convert numpy datetime64 to pandas Timestamp for strftime
        if isinstance(order_date, np.datetime64):
            order_date = pd.Timestamp(order_date)
        
        return {
            "order_id": f"ORD_{order_id:08d}",
            "customer_id": customer["customer_id"],
            "product_category": product["category"],
            "product_name": product["name"],
            "quantity": quantity,
            "unit_price": round(unit_price, 2),
            "total_amount": round(total_amount, 2),
            "order_date": order_date.strftime("%Y-%m-%d"),
            "customer_age": customer["age"],
            "customer_gender": customer["gender"],
            "customer_city": customer["city"]
        }
    
    def load_data(self, file_path: Path) -> pd.DataFrame:
        """
        Load data from CSV file
        从CSV文件加载数据
        
        Args:
            file_path: Path to the CSV file
        
        Returns:
            DataFrame containing the loaded data
        """
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            self.logger.info(f"Loaded {len(df)} records from {file_path}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading data from {file_path}: {str(e)}")
            raise
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess the data with enhanced data quality checks
        清洗和预处理数据，增强数据质量检查
        
        Args:
            df: Raw DataFrame containing order data
        
        Returns:
            Cleaned DataFrame with improved data quality
        """
        self.logger.info("Starting enhanced data cleaning process")
        
        # Create a copy to avoid modifying original data
        cleaned_df = df.copy()
        initial_rows = len(cleaned_df)
        
        # Step 1: Data type conversion with error handling
        # 步骤1：数据类型转换，包含错误处理
        self.logger.info("Converting data types...")
        try:
            cleaned_df['order_date'] = pd.to_datetime(cleaned_df['order_date'], errors='coerce')
            cleaned_df['quantity'] = pd.to_numeric(cleaned_df['quantity'], errors='coerce')
            cleaned_df['unit_price'] = pd.to_numeric(cleaned_df['unit_price'], errors='coerce')
            cleaned_df['total_amount'] = pd.to_numeric(cleaned_df['total_amount'], errors='coerce')
            cleaned_df['customer_age'] = pd.to_numeric(cleaned_df['customer_age'], errors='coerce')
        except Exception as e:
            self.logger.warning(f"Data type conversion warning: {str(e)}")
        
        # Step 2: Handle missing values with intelligent strategies
        # 步骤2：使用智能策略处理缺失值
        self.logger.info("Handling missing values...")
        
        # Remove rows with missing critical identifiers
        # 删除关键标识符缺失的行
        critical_columns = ['order_id', 'customer_id', 'product_name']
        cleaned_df = cleaned_df.dropna(subset=critical_columns)
        
        # Fill missing numerical values with category-specific medians
        # 使用类别特定的中位数填充缺失的数值
        numerical_columns = ['quantity', 'unit_price', 'total_amount', 'customer_age']
        for col in numerical_columns:
            if cleaned_df[col].isnull().any():
                if col in ['unit_price', 'total_amount'] and 'product_category' in cleaned_df.columns:
                    # Use category-specific median for price-related columns
                    # 对价格相关列使用类别特定的中位数
                    cleaned_df[col] = cleaned_df.groupby('product_category')[col].transform(
                        lambda x: x.fillna(x.median())
                    )
                else:
                    # Use overall median for other columns
                    # 对其他列使用总体中位数
                    median_value = cleaned_df[col].median()
                    cleaned_df[col].fillna(median_value, inplace=True)
        
        # Step 3: Remove duplicates with logging
        # 步骤3：删除重复项并记录日志
        duplicates_before = cleaned_df.duplicated(subset=['order_id']).sum()
        cleaned_df = cleaned_df.drop_duplicates(subset=['order_id'])
        self.logger.info(f"Removed {duplicates_before} duplicate orders")
        
        # Step 4: Enhanced outlier detection and removal
        # 步骤4：增强的异常值检测和删除
        self.logger.info("Detecting and removing outliers...")
        
        # Calculate IQR-based outlier thresholds for total_amount
        # 计算基于IQR的total_amount异常值阈值
        Q1 = cleaned_df['total_amount'].quantile(0.25)
        Q3 = cleaned_df['total_amount'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Apply business logic constraints
        # 应用业务逻辑约束
        outlier_mask = (
            (cleaned_df['quantity'] > 0) & (cleaned_df['quantity'] <= 100) &
            (cleaned_df['unit_price'] > 0) & (cleaned_df['unit_price'] <= 50000) &
            (cleaned_df['total_amount'] > max(0, lower_bound)) & 
            (cleaned_df['total_amount'] <= min(500000, upper_bound)) &
            (cleaned_df['customer_age'] >= 18) & (cleaned_df['customer_age'] <= 100)
        )
        
        outliers_removed = len(cleaned_df) - outlier_mask.sum()
        cleaned_df = cleaned_df[outlier_mask]
        self.logger.info(f"Removed {outliers_removed} outlier records")
        
        # Step 5: Data validation and consistency checks
        # 步骤5：数据验证和一致性检查
        self.logger.info("Performing data validation...")
        
        # Validate total_amount = quantity * unit_price (with tolerance)
        # 验证total_amount = quantity * unit_price（允许误差）
        calculated_total = cleaned_df['quantity'] * cleaned_df['unit_price']
        tolerance = 0.01  # 1% tolerance for rounding errors
        inconsistent_mask = abs(cleaned_df['total_amount'] - calculated_total) > tolerance
        
        if inconsistent_mask.any():
            inconsistent_count = inconsistent_mask.sum()
            self.logger.warning(f"Found {inconsistent_count} records with inconsistent total_amount")
            # Fix inconsistent records by recalculating total_amount
            # 通过重新计算total_amount修复不一致的记录
            cleaned_df.loc[inconsistent_mask, 'total_amount'] = calculated_total[inconsistent_mask]
        
        # Step 6: Add enhanced derived columns
        # 步骤6：添加增强的派生列
        self.logger.info("Adding derived columns...")
        
        # Time-based features
        # 基于时间的特征
        cleaned_df['order_year'] = cleaned_df['order_date'].dt.year
        cleaned_df['order_month'] = cleaned_df['order_date'].dt.month
        cleaned_df['order_quarter'] = cleaned_df['order_date'].dt.quarter
        cleaned_df['order_weekday'] = cleaned_df['order_date'].dt.day_name()
        cleaned_df['order_week'] = cleaned_df['order_date'].dt.isocalendar().week
        cleaned_df['is_weekend'] = cleaned_df['order_date'].dt.weekday >= 5
        
        # Customer segmentation features
        # 客户细分特征
        cleaned_df['age_group'] = pd.cut(
            cleaned_df['customer_age'], 
            bins=[0, 25, 35, 45, 55, 100], 
            labels=['18-25', '26-35', '36-45', '46-55', '55+'],
            include_lowest=True
        )
        
        # Order value categories
        # 订单价值分类
        cleaned_df['order_value_category'] = pd.cut(
            cleaned_df['total_amount'],
            bins=[0, 100, 500, 1000, 5000, float('inf')],
            labels=['Low', 'Medium', 'High', 'Premium', 'Luxury'],
            include_lowest=True
        )
        
        # Product price tier
        # 产品价格层级
        cleaned_df['price_tier'] = pd.qcut(
            cleaned_df['unit_price'],
            q=4,
            labels=['Budget', 'Standard', 'Premium', 'Luxury'],
            duplicates='drop'
        )
        
        final_rows = len(cleaned_df)
        cleaning_efficiency = (final_rows / initial_rows) * 100
        
        self.logger.info(f"Enhanced data cleaning completed. Rows: {initial_rows} -> {final_rows} ({cleaning_efficiency:.1f}% retained)")
        
        return cleaned_df
    
    def save_data(self, df: pd.DataFrame, file_path: Path) -> None:
        """
        Save DataFrame to CSV file
        保存DataFrame到CSV文件
        
        Args:
            df: DataFrame to save
            file_path: Output file path
        """
        try:
            df.to_csv(file_path, index=False, encoding='utf-8')
            self.logger.info(f"Data saved to {file_path}")
        except Exception as e:
            self.logger.error(f"Error saving data to {file_path}: {str(e)}")
            raise
    
    def get_data_quality_report(self, df: pd.DataFrame) -> Dict:
        """
        Generate data quality report
        生成数据质量报告
        
        Args:
            df: DataFrame to analyze
        
        Returns:
            Dictionary containing data quality metrics
        """
        # Calculate missing values statistics
        missing_values = df.isnull().sum()
        total_cells = len(df) * len(df.columns)
        missing_cells = missing_values.sum()
        
        # Calculate overall data quality percentage
        # 计算整体数据质量百分比
        overall_quality = ((total_cells - missing_cells) / total_cells * 100) if total_cells > 0 else 0
        
        report = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "missing_values": missing_values.to_dict(),
            "missing_values_count": int(missing_cells),
            "duplicate_rows": df.duplicated().sum(),
            "data_types": df.dtypes.to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum(),
            "overall_quality": round(overall_quality, 2),
            "completeness_rate": round(overall_quality, 2),
            "date_range": {
                "start": df['order_date'].min(),
                "end": df['order_date'].max()
            } if 'order_date' in df.columns else None
        }
        
        return report