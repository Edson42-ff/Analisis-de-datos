# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

def load_data(path: str) -> pd.DataFrame:
    """Load CSV and remove Unnamed index column if exists."""
    df = pd.read_csv(path)
    df = df.drop(columns=[c for c in df.columns if c.lower().startswith('unnamed')], errors='ignore')
    return df

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        'Edad': 'age',
        'Género': 'gender',
        'Ingresos': 'income',
        'Altura': 'height',
        'Ciudad': 'city',
        'Nivel_Educación': 'education',
        'Hijos': 'children'
    }
    return df.rename(columns=mapping)

def replace_negatives_with_zero(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Replace negative numeric values with 0."""
    df = df.copy()
    for col in columns:
        df[col] = df[col].apply(lambda x: 0 if pd.notna(x) and x < 0 else x)
    return df

def fix_age_outliers(df: pd.DataFrame, col: str = 'age', min_age: int = 0, max_age: int = 120,
                     strategy: str = 'median') -> tuple:
    """Fix outliers in age using bounds. Returns (df, count_fixed, replacement_value)."""
    df = df.copy()
    invalid = (df[col] < min_age) | (df[col] > max_age)
    if strategy == 'median':
        replacement = int(df.loc[~invalid, col].median())
    elif strategy == 'mean':
        replacement = int(df.loc[~invalid, col].mean())
    else:
        replacement = np.nan
    df.loc[invalid, col] = replacement
    return df, int(invalid.sum()), replacement

def fill_missing_with_mode(df: pd.DataFrame, col: str) -> tuple:
    """Fill missing categorical values using mode. Returns (df, mode_used)."""
    df = df.copy()
    mode = df[col].mode(dropna=True)
    if len(mode) > 0:
        fill_value = mode.iloc[0]
        df[col] = df[col].fillna(fill_value)
    else:
        fill_value = None
    return df, fill_value

def normalize_education(df: pd.DataFrame, col: str = 'education') -> pd.DataFrame:
    """Correct spelling / standardize education values."""
    df = df.copy()
    replacements = {
        'Bachelors': 'Bachelor',
        'Bachelor': 'Bachelor',
        'Master': 'Master',
        'mastre': 'Master',
        'PhD': 'PhD',
        'pHd': 'PhD',
        'no education': 'No Education'
    }
    df[col] = df[col].replace(replacements)
    return df

def clean_dataset(path: str, export_path: str = None) -> pd.DataFrame:
    df = load_data(path)
    df = rename_columns(df)
    df = normalize_education(df)
    df = replace_negatives_with_zero(df, ['income', 'children'])
    df, fixed_count, replacement = fix_age_outliers(df)
    df, gender_mode = fill_missing_with_mode(df, 'gender')
    df, city_mode = fill_missing_with_mode(df, 'city')
    df, edu_mode = fill_missing_with_mode(df, 'education')
    if export_path:
        df.to_csv(export_path, index=False)
    return df

if __name__ == '__main__':
    input_path = r"C:\Users\sefse\Downloads\pipol_datos.csv"
    df_clean = clean_dataset(input_path, export_path='pipol_datos_clean.csv')
    print(df_clean.head())
    print('\nMissing values after cleaning:\n', df_clean.isna().sum())
