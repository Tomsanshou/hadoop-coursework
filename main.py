#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for E-commerce Order Analysis Project
电商订单分析项目主程序

Author: Your Name
Date: 2024
Description: This is the main script to run the complete e-commerce order analysis.
"""

import sys
import logging
import time
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import pandas as pd

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from config import *
from src.data_utils import DataProcessor
from src.analysis import OrderAnalyzer
from src.visualization import DataVisualizer
from src.evaluation import ProjectEvaluator

def setup_logging():
    """
    Setup logging configuration
    设置日志配置
    """
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG["level"]),
        format=LOGGING_CONFIG["format"],
        handlers=[
            logging.FileHandler(LOGGING_CONFIG["log_file"]),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def print_progress_header():
    """
    Print a beautiful header for the analysis
    打印分析的美观标题
    """
    print("\n" + "="*80)
    print("🚀 E-COMMERCE ORDER ANALYSIS PROJECT 🚀")
    print("🚀 电商订单分析项目 🚀")
    print("="*80)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

def print_step_header(step_num: int, step_name: str, step_name_cn: str):
    """
    Print step header with progress indication
    打印带进度指示的步骤标题
    """
    print(f"\n{'='*20} STEP {step_num}/6: {step_name.upper()} {'='*20}")
    print(f"{'='*20} 步骤 {step_num}/6: {step_name_cn} {'='*20}")

def main():
    """
    Main function to run the complete analysis pipeline
    主函数：运行完整的分析流程
    """
    start_time = time.time()
    logger = setup_logging()
    
    # Print beautiful header
    print_progress_header()
    
    logger.info("Starting E-commerce Order Analysis Project")
    logger.info("开始电商订单分析项目")
    
    try:
        # Step 1: Data Processing
        print_step_header(1, "Data Processing", "数据处理")
        logger.info("Step 1: Data Processing / 步骤1：数据处理")
        
        processor = DataProcessor()
        
        # Generate sample data if not exists
        if not SAMPLE_DATA_FILE.exists():
            print("📊 Generating sample data... / 生成示例数据...")
            logger.info("Generating sample data / 生成示例数据")
            with tqdm(total=100, desc="Generating data") as pbar:
                processor.generate_sample_data(output_file=SAMPLE_DATA_FILE)
                pbar.update(100)
            print("✅ Sample data generated successfully! / 示例数据生成成功！")
        
        # Load and clean data
        print("📥 Loading and cleaning data... / 加载和清洗数据...")
        logger.info("Loading and cleaning data / 加载和清洗数据")
        
        with tqdm(total=100, desc="Processing data") as pbar:
            df = processor.load_data(SAMPLE_DATA_FILE)
            pbar.update(30)
            
            # Get data quality report before cleaning
            quality_report_before = processor.get_data_quality_report(df)
            pbar.update(20)
            
            cleaned_df = processor.clean_data(df)
            pbar.update(30)
            
            # Get data quality report after cleaning
            quality_report_after = processor.get_data_quality_report(cleaned_df)
            pbar.update(10)
            
            processor.save_data(cleaned_df, PROCESSED_DATA_FILE)
            pbar.update(10)
        
        print(f"✅ Data processing completed! / 数据处理完成！")
        print(f"   📈 Original records: {len(df):,} / 原始记录数: {len(df):,}")
        print(f"   📈 Cleaned records: {len(cleaned_df):,} / 清洗后记录数: {len(cleaned_df):,}")
        print(f"   📈 Data quality improvement: {quality_report_after['overall_quality']:.1f}% / 数据质量提升: {quality_report_after['overall_quality']:.1f}%")
        
        # Step 2: Data Analysis
        print_step_header(2, "Data Analysis", "数据分析")
        logger.info("Step 2: Data Analysis / 步骤2：数据分析")
        
        analyzer = OrderAnalyzer(cleaned_df)
        
        # Perform various analyses with progress tracking
        analysis_results = {}
        analysis_tasks = [
            ("basic_statistics", "Basic Statistics / 基本统计"),
            ("analyze_time_series", "Time Series Analysis / 时间序列分析"),
            ("analyze_customers", "Customer Analysis / 客户分析"),
            ("analyze_products", "Product Analysis / 产品分析")
        ]
        
        with tqdm(total=len(analysis_tasks), desc="Running analyses") as pbar:
            for method_name, description in analysis_tasks:
                print(f"   🔍 {description}")
                method = getattr(analyzer, method_name)
                analysis_results[method_name] = method()
                pbar.update(1)
                time.sleep(0.5)  # Small delay for better UX
        
        print("✅ Data analysis completed! / 数据分析完成！")
        
        # Step 3: Data Visualization
        print_step_header(3, "Data Visualization", "数据可视化")
        logger.info("Step 3: Data Visualization / 步骤3：数据可视化")
        
        visualizer = DataVisualizer(cleaned_df)
        
        # Generate visualizations with progress tracking
        visualization_tasks = [
            ("plot_sales_trend", "Sales Trend Chart / 销售趋势图"),
            ("plot_customer_analysis_dashboard", "Customer Dashboard / 客户仪表板"),
            ("plot_product_performance_heatmap", "Product Heatmap / 产品热力图")
        ]
        
        with tqdm(total=len(visualization_tasks), desc="Creating visualizations") as pbar:
            for method_name, description in visualization_tasks:
                print(f"   📊 {description}")
                try:
                    method = getattr(visualizer, method_name)
                    method()
                    print(f"     ✅ {description} created successfully!")
                except AttributeError:
                    print(f"     ⚠️  Method {method_name} not found, skipping...")
                except Exception as e:
                    print(f"     ❌ Error creating {description}: {str(e)}")
                    logger.warning(f"Visualization error: {str(e)}")
                pbar.update(1)
                time.sleep(0.3)
        
        print("✅ Data visualization completed! / 数据可视化完成！")
        
        # Step 4: Generate Report
        print_step_header(4, "Generate Report", "生成报告")
        logger.info("Step 4: Generate Report / 步骤4：生成报告")
        
        print("📝 Generating comprehensive report... / 生成综合报告...")
        with tqdm(total=100, desc="Generating report") as pbar:
            report_data = {
                "basic_stats": analysis_results.get("basic_statistics", {}),
                "time_analysis": analysis_results.get("analyze_time_series", {}),
                "customer_analysis": analysis_results.get("analyze_customers", {}),
                "product_analysis": analysis_results.get("analyze_products", {}),
                "data_quality": {
                    "before_cleaning": quality_report_before,
                    "after_cleaning": quality_report_after
                }
            }
            pbar.update(50)
            
            analyzer.generate_report(report_data)
            pbar.update(50)
        
        print("✅ Report generation completed! / 报告生成完成！")
        
        # Step 5: Project Evaluation
        print_step_header(5, "Project Evaluation", "项目评估")
        logger.info("Step 5: Project Evaluation / 步骤5：项目评估")
        
        print("🎯 Evaluating project quality... / 评估项目质量...")
        evaluator = ProjectEvaluator()
        
        with tqdm(total=100, desc="Evaluating project") as pbar:
            evaluation_score = evaluator.evaluate_project(cleaned_df)
            pbar.update(100)
        
        print("✅ Project evaluation completed! / 项目评估完成！")
        
        # Step 6: Final Summary
        print_step_header(6, "Final Summary", "最终总结")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Calculate some key metrics for summary
        total_revenue = cleaned_df['total_amount'].sum()
        avg_order_value = cleaned_df['total_amount'].mean()
        unique_customers = cleaned_df['customer_id'].nunique()
        unique_products = cleaned_df['product_name'].nunique()
        
        logger.info(f"Analysis completed successfully! / 分析成功完成！")
        logger.info(f"Project evaluation score: {evaluation_score:.2f}/100")
        logger.info(f"项目评估得分: {evaluation_score:.2f}/100")
        
        # Print beautiful completion summary
        print("\n" + "="*80)
        print("🎉 E-COMMERCE ORDER ANALYSIS COMPLETED! 🎉")
        print("🎉 电商订单分析完成！ 🎉")
        print("="*80)
        
        print("\n📊 ANALYSIS SUMMARY / 分析摘要:")
        print(f"   • Total orders processed / 处理订单总数: {len(cleaned_df):,}")
        print(f"   • Total revenue analyzed / 分析总收入: ¥{total_revenue:,.2f}")
        print(f"   • Average order value / 平均订单价值: ¥{avg_order_value:.2f}")
        print(f"   • Unique customers / 独特客户数: {unique_customers:,}")
        print(f"   • Unique products / 独特产品数: {unique_products:,}")
        
        print("\n🎯 PROJECT METRICS / 项目指标:")
        print(f"   • Project quality score / 项目质量得分: {evaluation_score:.2f}/100")
        print(f"   • Data quality improvement / 数据质量提升: {quality_report_after['overall_quality']:.1f}%")
        print(f"   • Execution time / 执行时间: {execution_time:.2f} seconds")
        
        print("\n📁 OUTPUT FILES / 输出文件:")
        print(f"   • Charts directory / 图表目录: {CHARTS_DIR}")
        print(f"   • Reports directory / 报告目录: {REPORTS_DIR}")
        print(f"   • Processed data / 处理后数据: {PROCESSED_DATA_FILE}")
        
        print("\n🚀 NEXT STEPS / 下一步:")
        print("   • Review generated charts in the charts/ directory")
        print("   • 查看charts/目录中生成的图表")
        print("   • Check comprehensive report in reports/ directory")
        print("   • 查看reports/目录中的综合报告")
        print("   • Run Jupyter notebook for interactive analysis")
        print("   • 运行Jupyter笔记本进行交互式分析")
        
        print("\n" + "="*80)
        print(f"🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🕐 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80 + "\n")
        
        return {
            'success': True,
            'execution_time': execution_time,
            'evaluation_score': evaluation_score,
            'records_processed': len(cleaned_df),
            'total_revenue': total_revenue
        }
        
    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        
        print("\n" + "="*80)
        print("❌ ANALYSIS FAILED! / 分析失败！")
        print("="*80)
        print(f"💥 Error: {str(e)}")
        print(f"💥 错误: {str(e)}")
        print(f"⏱️  Execution time before failure: {execution_time:.2f} seconds")
        print(f"⏱️  失败前执行时间: {execution_time:.2f} seconds")
        print("="*80 + "\n")
        
        logger.error(f"Error occurred during analysis: {str(e)}")
        logger.error(f"分析过程中发生错误: {str(e)}")
        
        return {
            'success': False,
            'error': str(e),
            'execution_time': execution_time
        }

if __name__ == "__main__":
    main()