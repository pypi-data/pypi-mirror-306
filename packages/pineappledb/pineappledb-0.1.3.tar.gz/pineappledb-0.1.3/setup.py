from setuptools import setup, find_packages

setup(
    name='pineappledb',
    version='0.1.3',
    author='Ciber Cleaner',
    author_email='tuyishimireemmanuel24@gmail.com',
    description='A SQLite database browser and management tool.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/millbox5/pineapple.git',  # Update with your repo URL
    packages=find_packages(include=['pineapple', 'pineapple.*']),
    install_requires=[
        'Flask',
        'Flask-Cors',
        'Peewee',
        'Werkzeug',
        'pygments',
        # Add other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)