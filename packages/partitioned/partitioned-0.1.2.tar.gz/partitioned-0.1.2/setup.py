from setuptools import setup

setup(
    name='partitioned',
    version='0.1.2',
    py_modules=['partitioned'],
    author='Benjamin Skubi',
    author_email='skubi@ohsu.edu',
    description='Determine if a series of lines is partitioned (all identical lines sequential).',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bskubi/partitioned',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'partitioned=partitioned:main',  # Replace `main` with your function name
        ],
    },
)
