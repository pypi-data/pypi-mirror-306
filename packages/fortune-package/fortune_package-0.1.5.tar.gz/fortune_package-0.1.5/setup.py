from setuptools import setup, find_packages

setup(
    name='fortune_package',
    version='0.1.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'fortune=fortune_package.fortune:main',
        ],
    },
    description='A fun package that provides fortunes and quotes',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
