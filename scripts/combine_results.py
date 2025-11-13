#!/usr/bin/env python3
"""
Combine and sort results from multiple JSON files

This script reads results from 'results_fullrun_Rsq.json' and 'results_derivatives.json',
combines them with appropriate suffixes, sorts by R² values, and saves to 'results_combined.json'.

Author: Generated for SmartAg Soil Chemistry Prediction Project
"""

import json
import os
from collections import OrderedDict

def load_json_file(filepath):
    """
    Load JSON file with error handling
    
    Args:
        filepath (str): Path to JSON file
        
    Returns:
        dict: Loaded JSON data or empty dict if file not found/invalid
    """
    if not os.path.exists(filepath):
        print(f"WARNING: File '{filepath}' not found")
        return {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"SUCCESS: Successfully loaded '{filepath}' with {len(data)} properties")
        return data
    except json.JSONDecodeError as e:
        print(f"ERROR: Error reading JSON from '{filepath}': {e}")
        return {}
    except Exception as e:
        print(f"ERROR: Error loading '{filepath}': {e}")
        return {}

def add_suffix_to_methods(data, suffix):
    """
    Add suffix to all method names in the data
    
    Args:
        data (dict): Results data with property -> method -> R² structure
        suffix (str): Suffix to append to method names
        
    Returns:
        dict: Data with suffixed method names
    """
    suffixed_data = {}
    
    for property_name, methods in data.items():
        suffixed_data[property_name] = {}
        
        for method_name, r2_value in methods.items():
            new_method_name = f"{method_name}{suffix}"
            suffixed_data[property_name][new_method_name] = r2_value
    
    return suffixed_data

def combine_results(fullrun_data, derivatives_data):
    """
    Combine results from fullrun and derivatives data
    
    Args:
        fullrun_data (dict): Results from fullrun JSON
        derivatives_data (dict): Results from derivatives JSON (will be suffixed)
        
    Returns:
        dict: Combined results with all methods for each property
    """
    # Add suffix to derivatives data
    derivatives_suffixed = add_suffix_to_methods(derivatives_data, '_deriv')
    
    # Get all unique property names
    all_properties = set(fullrun_data.keys()) | set(derivatives_suffixed.keys())
    
    combined_data = {}
    
    for property_name in all_properties:
        combined_data[property_name] = {}
        
        # Add fullrun methods
        if property_name in fullrun_data:
            combined_data[property_name].update(fullrun_data[property_name])
        
        # Add derivatives methods (with suffix)
        if property_name in derivatives_suffixed:
            combined_data[property_name].update(derivatives_suffixed[property_name])
    
    return combined_data

def sort_methods_by_r2(data):
    """
    Sort methods within each property by R² values (descending)
    
    Args:
        data (dict): Combined results data
        
    Returns:
        dict: Data with methods sorted by R² values
    """
    sorted_data = {}
    
    for property_name, methods in data.items():
        # Filter out None values and sort by R² (descending)
        valid_methods = {k: v for k, v in methods.items() if v is not None}
        invalid_methods = {k: v for k, v in methods.items() if v is None}
        
        # Sort valid methods by R² value (highest first)
        sorted_valid = dict(sorted(valid_methods.items(), key=lambda item: item[1], reverse=True))
        
        # Combine sorted valid methods with invalid methods at the end
        sorted_methods = OrderedDict()
        sorted_methods.update(sorted_valid)
        sorted_methods.update(invalid_methods)
        
        sorted_data[property_name] = sorted_methods
        
        # Print top 3 methods for this property
        top_methods = list(sorted_valid.items())[:3]
        if top_methods:
            print(f"\nTop 3 methods for {property_name}:")
            for i, (method, r2) in enumerate(top_methods, 1):
                print(f"  {i}. {method}: R² = {r2:.4f}")
        else:
            print(f"\nWARNING: No valid results found for {property_name}")
    
    return sorted_data

def save_combined_results(data, output_path):
    """
    Save combined results to JSON file
    
    Args:
        data (dict): Combined and sorted results
        output_path (str): Path to save the combined results
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"\nSUCCESS: Successfully saved combined results to '{output_path}'")
    except Exception as e:
        print(f"ERROR: Error saving combined results: {e}")

def clean_method_name_for_latex(method_name):
    """
    Clean method name for LaTeX table display
    
    Args:
        method_name (str): Original method name
        
    Returns:
        str: Cleaned method name suitable for LaTeX
    """
    # Remove common suffixes and prefixes
    cleaned = method_name
    
    # Remove _deriv suffix but keep track of it
    is_derivative = cleaned.endswith('_deriv')
    if is_derivative:
        cleaned = cleaned.replace('_deriv', '')
    
    # Replace underscores with spaces
    cleaned = cleaned.replace('_', ' ')
    
    # Handle common abbreviations and make them more readable
    replacements = {
        'Enhanced Neural Network': 'Enhanced NN',
        'Enhanced PLS': 'Enhanced PLS',
        'Random Forest': 'Random Forest',
        'MLPRegressor': 'MLP Regressor',
        'XGBRegressor': 'XGBoost',
        'LGBMRegressor': 'LightGBM',
        'ExtraTreesRegressor': 'Extra Trees',
        'HistGradientBoostingRegressor': 'Hist Gradient Boosting',
        'GradientBoostingRegressor': 'Gradient Boosting',
        'KNeighborsRegressor': 'K-Neighbors',
        'BaggingRegressor': 'Bagging',
        'AdaBoostRegressor': 'AdaBoost',
        'LinearRegression': 'Linear Regression',
        'BayesianRidge': 'Bayesian Ridge',
        'RidgeCV': 'Ridge CV',
        'LassoCV': 'Lasso CV',
        'ElasticNetCV': 'ElasticNet CV',
        'TransformedTargetRegressor': 'Transformed Target',
        'OrthogonalMatchingPursuitCV': 'OMP CV',
        'PCA': 'PCA',
        'noScale': 'No Scaling',
        'StndScale': 'Standard Scaling'
    }
    
    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)
    
    # Add derivative indicator
    if is_derivative:
        cleaned += ' (Deriv)'
    
    # Capitalize first letter of each word and clean up spacing
    cleaned = ' '.join(word.capitalize() if not word.isupper() else word for word in cleaned.split())
    
    return cleaned

def create_latex_table(property_name, methods_data, top_n=10):
    """
    Create a LaTeX table for the top methods for a specific property
    
    Args:
        property_name (str): Name of the soil property
        methods_data (dict): Dictionary of method names and R² values
        top_n (int): Number of top methods to include
        
    Returns:
        str: LaTeX table code
    """
    # Get top N methods with valid R² values
    valid_methods = [(method, r2) for method, r2 in methods_data.items() if r2 is not None and r2 > -1000]
    valid_methods = sorted(valid_methods, key=lambda x: x[1], reverse=True)[:top_n]
    
    if not valid_methods:
        return f"% No valid methods found for {property_name}\n\n"
    
    # Clean property name for display
    clean_property = property_name.replace('_', ' ').title()
    
    # Create table label
    table_label = property_name.lower().replace('_', '')
    
    # Start building the LaTeX table
    latex_table = []
    latex_table.append("\\begin{table}[htbp]")
    latex_table.append("\\centering")
    latex_table.append(f"\\caption{{Top models for predicting {clean_property}}}")
    latex_table.append(f"\\label{{tab:{table_label}}}")
    latex_table.append("\\begin{tabular}{@{}ll@{}}")
    latex_table.append("\\toprule")
    latex_table.append("\\textbf{Model} & \\textbf{R\\textsuperscript{2}} \\\\")
    latex_table.append("\\midrule")
    
    # Add data rows
    for method, r2 in valid_methods:
        clean_method = clean_method_name_for_latex(method)
        r2_formatted = f"{r2:.3f}"
        latex_table.append(f"{clean_method} & {r2_formatted} \\\\")
    
    # Close table
    latex_table.append("\\bottomrule")
    latex_table.append("\\end{tabular}")
    latex_table.append("\\end{table}")
    latex_table.append("")  # Empty line after table
    
    return "\n".join(latex_table)

def generate_all_latex_tables(data, output_file='results_latex_table.txt'):
    """
    Generate LaTeX tables for all properties and save to file

    Args:
        data (dict): Combined results data
        output_file (str): Output filename for LaTeX tables
    """
    print(f"\nGenerating LaTeX tables for all soil properties...")

    # Sort properties by best R² value for logical ordering
    property_performance = {}
    for prop, methods in data.items():
        valid_r2s = [r2 for r2 in methods.values() if r2 is not None and r2 > -1000]
        if valid_r2s:
            property_performance[prop] = max(valid_r2s)
        else:
            property_performance[prop] = -999

    sorted_properties = sorted(property_performance.items(), key=lambda x: x[1], reverse=True)

    # Generate all tables
    all_tables = []

    # Add header comment
    all_tables.append("% LaTeX Tables for Soil Property Prediction Results")
    all_tables.append("% Generated automatically from combined results")
    all_tables.append("% Summary table followed by detailed tables for each property")
    all_tables.append("")

    # Generate summary table first
    summary_table = create_best_methods_summary_table(data)
    all_tables.append(summary_table)
    all_tables.append("")

    # Add separator comment
    all_tables.append("% Detailed tables for each soil property (top 10 methods)")
    all_tables.append("")

    # Generate detailed tables for each property
    for prop, best_r2 in sorted_properties:
        print(f"  Creating detailed table for {prop} (best R² = {best_r2:.3f})")
        table_latex = create_latex_table(prop, data[prop], top_n=10)
        all_tables.append(table_latex)

    # Save to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_tables))
        print(f"SUCCESS: LaTeX tables saved to '{output_file}'")

        # Print summary
        valid_properties = sum(1 for prop, r2 in sorted_properties if r2 > -999)
        print(f"SUCCESS: Generated summary table + {valid_properties} detailed LaTeX tables")
        print(f"File contains complete LaTeX code ready for inclusion in documents")

    except Exception as e:
        print(f"ERROR: Failed to save LaTeX tables: {e}")

def create_best_methods_summary_table(data):
    """
    Create a LaTeX summary table showing the best method and R² score for each soil constituent
    Returns exactly 8 rows for the main soil constituents

    Args:
        data (dict): Combined results data

    Returns:
        str: LaTeX table code for the summary table
    """
    # Define the 8 main soil constituents we expect
    target_constituents = [
        'Clay_Content', 'pH', 'Organic_Carbon', 'Organic_Nitrogen',
        'Potassium', 'Magnesium', 'Calcium', 'Sodium'
    ]

    # Get best method for each target constituent
    best_methods = []
    for constituent in target_constituents:
        if constituent in data:
            valid_methods = {k: v for k, v in data[constituent].items() if v is not None and v > -1000}
            if valid_methods:
                best_method = max(valid_methods.items(), key=lambda x: x[1])
                best_methods.append((constituent, best_method[0], best_method[1]))
            else:
                # If no valid methods, use placeholder
                best_methods.append((constituent, "No valid results", 0.000))
        else:
            # If constituent not found in data
            best_methods.append((constituent, "Not available", 0.000))

    # Sort by R² score (descending)
    best_methods.sort(key=lambda x: x[2], reverse=True)

    # Create LaTeX table
    latex_lines = []
    latex_lines.append("% Best Methods Summary Table")
    latex_lines.append("% Shows the top-performing method for each of the 8 main soil constituents")
    latex_lines.append("")
    latex_lines.append("\\begin{table}[htbp]")
    latex_lines.append("\\centering")
    latex_lines.append("\\caption{Best performing models for each soil constituent}")
    latex_lines.append("\\label{tab:best_methods_summary}")
    latex_lines.append("\\begin{tabular}{@{}lll@{}}")
    latex_lines.append("\\toprule")
    latex_lines.append("\\textbf{Soil Constituent} & \\textbf{Best Model} & \\textbf{R\\textsuperscript{2}} \\\\")
    latex_lines.append("\\midrule")

    # Add exactly 8 data rows
    for property_name, method_name, r2_score in best_methods:
        # Clean property name
        clean_property = property_name.replace('_', ' ').title()
        # Clean method name (handle special cases)
        if method_name in ["No valid results", "Not available"]:
            clean_method = method_name
        else:
            clean_method = clean_method_name_for_latex(method_name)
        # Format R² score
        if r2_score == 0.000 and method_name in ["No valid results", "Not available"]:
            r2_formatted = "—"  # Em dash for missing values
        else:
            r2_formatted = f"{r2_score:.3f}"

        latex_lines.append(f"{clean_property} & {clean_method} & {r2_formatted} \\\\")

    # Close table
    latex_lines.append("\\bottomrule")
    latex_lines.append("\\end{tabular}")
    latex_lines.append("\\end{table}")

    return "\n".join(latex_lines)

def generate_summary_report(data):
    """
    Generate a summary report of the combined results

    Args:
        data (dict): Combined results data
    """
    print(f"\n{'='*80}")
    print("COMBINED RESULTS SUMMARY REPORT")
    print(f"{'='*80}")
    
    total_methods = 0
    total_properties = len(data)
    fullrun_methods = 0
    derivatives_methods = 0
    
    print(f"Total soil properties analyzed: {total_properties}")
    
    for property_name, methods in data.items():
        valid_methods = [v for v in methods.values() if v is not None]
        n_methods = len(methods)
        n_valid = len(valid_methods)
        
        # Count method types
        prop_fullrun = sum(1 for method in methods.keys() if not method.endswith('_deriv'))
        prop_derivatives = sum(1 for method in methods.keys() if method.endswith('_deriv'))
        
        total_methods += n_methods
        fullrun_methods += prop_fullrun
        derivatives_methods += prop_derivatives
        
        if valid_methods:
            best_r2 = max(valid_methods)
            worst_r2 = min(valid_methods)
            avg_r2 = sum(valid_methods) / len(valid_methods)
            
            print(f"\n{property_name}:")
            print(f"  Methods: {n_methods} total ({prop_fullrun} fullrun, {prop_derivatives} derivatives)")
            print(f"  Valid results: {n_valid}/{n_methods} ({(n_valid/n_methods)*100:.1f}%)")
            print(f"  R² range: {worst_r2:.4f} - {best_r2:.4f} (avg: {avg_r2:.4f})")
            
            # Find best method
            best_method = max(methods.items(), key=lambda x: x[1] if x[1] is not None else -1)
            print(f"  Best method: {best_method[0]} (R² = {best_method[1]:.4f})")
        else:
            print(f"\n{property_name}: No valid results")
    
    print(f"\n{'='*40}")
    print("OVERALL STATISTICS:")
    print(f"{'='*40}")
    print(f"Total methods tested: {total_methods}")
    print(f"  Fullrun methods: {fullrun_methods}")
    print(f"  Derivatives methods: {derivatives_methods}")
    print(f"Properties with results: {total_properties}")
    
    # Find overall best performing methods across all properties
    all_results = []
    for property_name, methods in data.items():
        for method_name, r2_value in methods.items():
            if r2_value is not None:
                all_results.append((property_name, method_name, r2_value))
    
    if all_results:
        # Sort by R² value
        all_results.sort(key=lambda x: x[2], reverse=True)
        
        print(f"\nTOP 10 BEST PREDICTIONS OVERALL:")
        print("-" * 60)
        for i, (prop, method, r2) in enumerate(all_results[:10], 1):
            method_type = "derivatives" if method.endswith('_deriv') else "fullrun"
            print(f"{i:2d}. {prop:15s} | {method:35s} | R² = {r2:.4f} ({method_type})")
        
        # Compare derivatives vs fullrun performance
        fullrun_r2s = [r2 for prop, method, r2 in all_results if not method.endswith('_deriv')]
        deriv_r2s = [r2 for prop, method, r2 in all_results if method.endswith('_deriv')]
        
        if fullrun_r2s and deriv_r2s:
            avg_fullrun = sum(fullrun_r2s) / len(fullrun_r2s)
            avg_deriv = sum(deriv_r2s) / len(deriv_r2s)
            
            print(f"\nPERFORMANCE COMPARISON:")
            print(f"Average R² - Fullrun methods: {avg_fullrun:.4f}")
            print(f"Average R² - Derivatives methods: {avg_deriv:.4f}")
            
            if avg_deriv > avg_fullrun:
                improvement = ((avg_deriv - avg_fullrun) / avg_fullrun) * 100
                print(f"RESULT: Derivatives show {improvement:.1f}% improvement over fullrun methods")
            else:
                decline = ((avg_fullrun - avg_deriv) / avg_fullrun) * 100
                print(f"RESULT: Derivatives show {decline:.1f}% decline compared to fullrun methods")

def main():
    """
    Main function to combine and sort results from multiple JSON files
    """
    print("COMBINING SOIL PROPERTY PREDICTION RESULTS")
    print("=" * 60)
    
    # File paths
    # Note: Input files should be in the current directory or results/ directory
    # Output files will be saved to results/ directory
    import os
    results_dir = 'results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    fullrun_file = 'results_fullrun_Rsq.json'
    derivatives_file = 'results_derivatives.json'
    output_file = os.path.join(results_dir, 'results_combined.json')
    
    # Load data from both files
    print("1. Loading JSON files...")
    fullrun_data = load_json_file(fullrun_file)
    derivatives_data = load_json_file(derivatives_file)
    
    if not fullrun_data and not derivatives_data:
        print("ERROR: No data loaded from either file. Exiting.")
        return
    
    # Combine results
    print("\n2. Combining results...")
    combined_data = combine_results(fullrun_data, derivatives_data)
    print(f"SUCCESS: Combined results for {len(combined_data)} soil properties")
    
    # Count total methods
    total_methods = sum(len(methods) for methods in combined_data.values())
    print(f"SUCCESS: Total methods: {total_methods}")
    
    # Sort methods by R² values
    print("\n3. Sorting methods by R² values...")
    sorted_data = sort_methods_by_r2(combined_data)
    
    # Save combined results
    print(f"\n4. Saving combined results...")
    save_combined_results(sorted_data, output_file)
    
    # Generate LaTeX tables (includes summary table)
    print("\n5. Generating LaTeX tables...")
    latex_output = os.path.join(results_dir, 'results_latex_table.txt')
    generate_all_latex_tables(sorted_data, latex_output)

    # Generate summary report
    print("\n6. Generating summary report...")
    generate_summary_report(sorted_data)

    print(f"\nPROCESS COMPLETED SUCCESSFULLY!")
    print(f"Combined results saved to: {output_file}")
    print(f"LaTeX tables (including summary table) saved to: {latex_output}")
    print(f"Ready for analysis and visualization.")

if __name__ == "__main__":
    main()