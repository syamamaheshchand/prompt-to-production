"""
UC-0C app.py — Starter file.
Build this using the RICE + agents.md + skills.md + CRAFT workflow.
See README.md for run command and expected behaviour.
"""
import argparse
import csv
import sys
import os

def load_dataset(input_path: str) -> list:
    """
    Reads CSV, validates columns, reports null count and which rows.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
        
    dataset = []
    null_rows = []
    
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dataset.append(row)
            if not row.get('actual_spend') or row.get('actual_spend').strip() == '':
                null_rows.append({
                    'period': row.get('period'),
                    'ward': row.get('ward'),
                    'category': row.get('category'),
                    'notes': row.get('notes')
                })
                
    print(f"Dataset Loaded. Total rows: {len(dataset)}")
    print(f"Null 'actual_spend' values found: {len(null_rows)}")
    for nr in null_rows:
        print(f"  - Null at {nr['period']} | {nr['ward']} | {nr['category']} (Reason: {nr['notes']})")
        
    return dataset

def compute_growth(dataset: list, ward: str, category: str, growth_type: str) -> list:
    """
    Takes ward + category + growth_type, returns per-period table with formula shown.
    Refuses cross-aggregation.
    """
    if not ward or not category:
        raise ValueError("REFUSAL: Cannot aggregate across wards or categories. You must specify a specific ward and category.")
        
    if not growth_type:
        raise ValueError("REFUSAL: Growth type not specified. Cannot assume or guess (e.g., MoM vs YoY).")
        
    if growth_type != "MoM":
        # Starter file only strictly needs MoM for our UC-0C case, but extensible
        raise ValueError(f"REFUSAL: Unsupported growth type '{growth_type}'.")

    # Filter dataset
    filtered = []
    for row in dataset:
        if row.get('ward') == ward and row.get('category') == category:
            filtered.append(row)
            
    # Sort by period to ensure chronological order for MoM
    filtered.sort(key=lambda x: x.get('period', ''))
    
    results = []
    prev_spend = None
    
    for row in filtered:
        period = row.get('period')
        spend_str = row.get('actual_spend', '').strip()
        
        if not spend_str:
            # Handle Nulls
            notes = row.get('notes', 'No notes provided')
            result_row = {
                'ward': ward,
                'category': category,
                'period': period,
                'actual_spend': 'NULL',
                'growth_type': growth_type,
                'growth_pct': 'FLAGGED',
                'formula': f"Not computed due to null. Reason: {notes}"
            }
            prev_spend = None # Reset previous spend since the chain is broken
        else:
            current_spend = float(spend_str)
            if prev_spend is None:
                result_row = {
                    'ward': ward,
                    'category': category,
                    'period': period,
                    'actual_spend': current_spend,
                    'growth_type': growth_type,
                    'growth_pct': 'n/a',
                    'formula': "(current - previous) / previous * 100 [No prev month]"
                }
            else:
                growth_val = ((current_spend - prev_spend) / prev_spend) * 100
                result_row = {
                    'ward': ward,
                    'category': category,
                    'period': period,
                    'actual_spend': current_spend,
                    'growth_type': growth_type,
                    'growth_pct': f"{growth_val:+.1f}%",
                    'formula': f"({current_spend} - {prev_spend}) / {prev_spend} * 100"
                }
            prev_spend = current_spend
            
        results.append(result_row)
        
    return results

def main():
    parser = argparse.ArgumentParser(description="UC-0C Budget Growth Calculator")
    parser.add_argument("--input", required=True, help="Path to ward_budget.csv")
    parser.add_argument("--ward", required=False, help="Specific ward to analyze")
    parser.add_argument("--category", required=False, help="Specific category to analyze")
    parser.add_argument("--growth-type", dest="growth_type", required=False, help="Growth calculation type (e.g. MoM)")
    parser.add_argument("--output", required=True, help="Path to write output CSV")
    
    args = parser.parse_args()
    
    try:
        dataset = load_dataset(args.input)
        
        # This will raise exceptions based on our enforcement rules
        results = compute_growth(dataset, args.ward, args.category, args.growth_type)
        
        fieldnames = ['ward', 'category', 'period', 'actual_spend', 'growth_type', 'growth_pct', 'formula']
        
        with open(args.output, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow(r)
                
        print(f"\nSuccess! Wrote {len(results)} rows to {args.output}")
        
    except ValueError as ve:
        print(f"\n{ve}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
