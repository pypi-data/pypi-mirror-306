__license__='''
Copyright 2024 European Commission
*
Licensed under the EUPL, Version 1.2;
You may not use this work except in compliance with the Licence.
You may obtain a copy of the Licence at:

*
   https://joinup.ec.europa.eu/software/page/eupl
*

Unless required by applicable law or agreed to in writing, software distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the Licence for the specific language governing permissions and limitations under the Licence.
'''

import os 
import sys

### path to the current user's working directory
CWD_PATH = os.getcwd()

### path to the euromod package
MODEL_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if MODEL_PATH not in sys.path:
    sys.path.insert(0, MODEL_PATH)

### path to the root folder where euromod package is installed
ROOT_PATH =  os.path.dirname(MODEL_PATH)
# if ROOT_PATH not in sys.path:
#     sys.path.insert(0, ROOT_PATH)
    
DLL_PATH = os.path.join(MODEL_PATH, "libs")
#DLL_PATH = r"C:\Program Files\EUROMOD\Executable"
