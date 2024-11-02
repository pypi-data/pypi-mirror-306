import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)

import akshare as ak

stock_gdfx_free_top_10_em_df = ak.stock_gdfx_free_top_10_em(symbol="sh688981", date="20240630")
print(stock_gdfx_free_top_10_em_df)