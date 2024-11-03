from setuptools import setup, find_packages

setup(
    name='rexeloft_llc',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'nltk',
        'googletrans==4.0.0rc1',
        'fuzzywuzzy',
        'requests',
        'vaderSentiment',
        'python-Levenshtein'
    ],
    entry_points={
        'console_scripts': [
            'intelix-chat=rexeloft_llc.main:main',
        ],
    },
    author='Rexeloft LLC',
    description='A free chatbot (intelix) Python library made by Rexeloft LLC [Beta]',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="MIT",
    python_requires='>=3.6',
    url="https://github.com/OfficialDex",
    keywords=[
        'chatbot', 
        'chat',
        'Ai',
        'smart',
        'bot',
        'new',
        'Artifical intelligence',
        'intelix',
        'rexeloft',
        'intelligence'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
