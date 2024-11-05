from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='dataguillm',
    version='1.2',
    author='Sagnik Banerjee',
    author_email='sagu7065@gmail.com',
    description='A package for Exploratory Data Analysis (EDA)',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Change to 'text/x-rst' if using reStructuredText
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'seaborn',
        'plotly',
        'scipy',
        'statsmodels',
        'datapane',
        'scikit-learn',
        'groq',
        'python-docx',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    license='MIT'
)
