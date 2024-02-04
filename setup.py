from setuptools import find_packages, setup
from comm import VERSION

setup(
    name='eyes.yoga',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'numpy', 'pandas', 'websockets', 'apscheduler', 'gevent',
        'matplotlib', 'mplfinance', 'TA-lib',
        'aiomysql', 'pymysql', 'sqlalchemy', 'redis', 'hiredis', 
        'tda-api', 'toshare', 'click', 'async_timeout', 'aiohttp',
        'flask[async]', 'flask-httpauth', 'flask-login', 'flask-wtf',
        'flask-sqlalchemy', 'flask-apscheduler', 'flask-socketio', 
        'pytest', 'pytest-asyncio', 'pytest-mock', 'pytest-ordering', 'pytest-cov'
    ],
)
 