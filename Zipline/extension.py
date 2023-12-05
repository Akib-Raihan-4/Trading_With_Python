
import pandas as pd

from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities
register(
    'Korea_commodity',
    csvdir_equities(
        ['daily'],
        '/home/popeye/Anchorblock/Trading_With_Python/Zipline'
    ),
    calendar_name='XKRX',
)

