from setuptools import setup, find_packages

install_requirements = [
    'selenium',
    'webdriver_manager'  # Corrected spelling
]

setup(
    name='FridaySTT',
    version='0.1',
    author='Vivek Badiger',
    author_email='vivekbadiger666@gmail.com',
    description='This is SPEECH TO TEXT created by Vivek Badiger.',
    packages=find_packages(),  # Include this to find packages automatically
    install_requires=install_requirements  # Include the install_requires parameter
)

