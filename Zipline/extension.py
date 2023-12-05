import pandas as pd
from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities


register(
    'btc_bundle',  
    csvdir_equities(
        ['daily'],
        './custom_data'
    ),
    calendar_name='us_futures',
)
