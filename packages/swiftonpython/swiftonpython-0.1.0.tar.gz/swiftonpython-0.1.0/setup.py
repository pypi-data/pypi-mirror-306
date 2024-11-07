from setuptools import setup, find_packages
import os

# Đặt tên thư viện
lib_name = 'swiftonpython'

setup(
    name=lib_name,
    version='0.1.0',
    author='Bobby',
    author_email='akirasumeragi699@gmail.com',
    description='A Python wrapper for Swift code execution',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hqmdokkai/swiftonpython.git',
    packages=find_packages(),  # Tự động tìm các gói có __init__.py
    package_data={
        # Bao gồm tất cả các tệp trong thư mục `swiftonpython`
        'swiftonpython': ['*.so', '*.py', '*.swift']
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
)
