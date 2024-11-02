import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
<<<<<<< HEAD
sys.path.append(project_path)
=======
sys.path.append(project_path)
>>>>>>> db26a62cb2cfa4a1158d6becb8d096c3316bcdc8
