import pandas as pd
from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities

# Replace 'your_bundle_name' with a unique name for your bundle
register(
    'btc_bundle',  
    csvdir_equities(
        ['daily'],
        'custom_data'  # Assuming 'custom_data' is the folder containing BTC_custom_data.csv
    ),
    calendar_name='us_futures',
)
