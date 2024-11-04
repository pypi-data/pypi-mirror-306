from setuptools import setup, find_packages

setup(
    name='fortune-package',
    version='0.1.4',
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
    author='Your Name',
    author_email='your_email@example.com',
    description='A fun package that provides fortunes and quotes',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/fortune_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
