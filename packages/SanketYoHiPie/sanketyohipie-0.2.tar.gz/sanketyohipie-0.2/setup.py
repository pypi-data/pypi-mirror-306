from setuptools import setup,find_packages

setup(
    name='SanketYoHiPie',
    version='0.2',
    author='Sanket3yoprogrammer',
    author_email='sanket@example.com',
    description='A simple Python library for handling STT functionality',
)
packages = find_packages(),
install_requirements = [
    'selenium',
    'webdriver_manager',
]