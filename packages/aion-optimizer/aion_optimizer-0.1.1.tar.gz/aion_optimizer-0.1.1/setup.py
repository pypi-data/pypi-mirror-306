from setuptools import setup, find_packages

setup(
    name="aion_optimizer",
    version="0.1.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        'numpy>=1.19.0',
        'pandas>=1.2.0',
        'scikit-learn>=0.24.0',
        'scipy',
        'xgboost',
        'catboost'
    ],
    author="Lalit Lohani",
    author_email="lohanilalit.01@gmail.com",
    description="An automated machine learning optimization package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    include_package_data=True,  
    package_data={
        '': ['*.json'],
    },
)
