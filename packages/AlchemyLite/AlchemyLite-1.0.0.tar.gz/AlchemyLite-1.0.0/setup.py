from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='AlchemyLite',
    version='1.0.0',
    author='voskan',
    author_email='yura.voskanyan.2003@mail.ru',
    description='Library with built-in CRUD operations in SQLAlchemy',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/voskanyan777/alchemylite',
    packages=find_packages(),
    install_requires=['asyncpg>=0.30.0', 'psycopg>=3.2.3', 'psycopg-binary>=3.2.3',
                      'psycopg-pool>=3.2.3', 'psycopg2>=2.9.10', 'psycopg2-binary>=2.9.10',
                      'SQLAlchemy>=2.0.36'],
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='alchemylite crud_sqlalchemy sqlalchemy',
    project_urls={
        'Documentation': 'https://github.com/voskanyan777/alchemylite'
    },
    python_requires='>=3.10'
)
