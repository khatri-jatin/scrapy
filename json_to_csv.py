import pandas as pd
df = pd.read_json('output.json')

# Convert to CSV
df.to_csv('output.csv', index=False)