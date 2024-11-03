from setuptools import setup, find_packages

setup(
    name='datarefi',  
    version='1.3',  
    description='A no-code solution for performing data cleaning like misssing value imputation,outlier handling,normalisation,transformation and quality check with an intuitive interface for interactive DataFrame manipulation and easy CSV export.',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
    author='Shahana Farvin', 
    author_email='shahana50997@gmail.com',  
    url='https://github.com/Shahanafarvin/DataRefine',  
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pandas>=1.0.0",
        "scikit-learn>=0.22.0",
        "numpy",
        "scipy",
        "streamlit",
        "setuptools",
        "plotly"
    ],
    entry_points={
        'console_scripts': [
            'DataRefine = DataRefine.scripts.run_app:main',
        ],
    },

    python_requires='>=3.8',  
    classifiers=[
        'Development Status :: 5 - Production/Stable',  
        'Intended Audience :: Developers',  
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',  
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='data transformation, missing value imputation, outlier handling,normalisation, transformation, machine learning, data preprocessing, pandas, scikit-learn, feature engineering, data science, Python ',  
    project_urls={
        'Documentation': 'https://github.com/Shahanafarvin/DataRefine/blob/main/README.md',
        'Source': 'https://github.com/Shahanafarvin/DataRefine/tree/main/datarefine',
        'Tracker': 'https://github.com/Shahanafarvin/DataRefine/issues',
    },
)