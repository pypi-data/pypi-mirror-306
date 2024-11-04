from setuptools import setup, find_packages

with open("README.md", "r") as README:
    description = README.read()

setup(
    name='emrrunner',
    version='v1.0.8',
    author='Haabiy',
    author_email='abiy.dema@gmail.com',  
    description='A powerful CLI tool and API for managing Spark jobs on Amazon EMR clusters',
    long_description=description,
    long_description_content_type="text/markdown",
    url='https://github.com/Haabiy/EMRRunner',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'Flask>=2.0.0',
        'boto3>=1.26.0',
        'python-dotenv>=0.19.0',
        'marshmallow>=3.14.0',
        'argparse>=1.4.0',
    ],
    entry_points={
        'console_scripts': [
            'emrrunner=app.cli:cli_main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
        'Framework :: Flask',
    ],
    keywords='aws emr spark hadoop data-processing etl cli api flask',
    python_requires='>=3.9',
    project_urls={
        'Bug Reports': 'https://github.com/Haabiy/EMRRunner/issues',
        'Source': 'https://github.com/Haabiy/EMRRunner',
        'Documentation': 'https://github.com/Haabiy/EMRRunner#readme'
    }
)