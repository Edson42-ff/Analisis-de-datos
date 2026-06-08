import pandas as pd
import re

df = pd.read_csv("members.csv")

pattern_plus62 = r"\+62"
df["contains_62"] = df["Phone Number"].str.contains(pattern_plus62, regex=True)

pattern_symbols = r"[\(\)\-]"
df["contains_symbols"] = df["Phone Number"].str.contains(pattern_symbols, regex=True)

pattern_spaces = r"\s"
df["contains_spaces"] = df["Phone Number"].str.contains(pattern_spaces, regex=True)

print(df[["Phone Number", "contains_62", "contains_symbols", "contains_spaces"]])