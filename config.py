import os.path
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")
ROOT_DIR = os.path.dirname(__file__)
print(ROOT_DIR)
