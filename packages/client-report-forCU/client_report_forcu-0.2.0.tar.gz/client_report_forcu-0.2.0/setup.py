from setuptools import setup, find_packages
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name="client_report_forCU",
    version="0.2.0",
    description="Пакет для генерации отчётов о клиентах из CSV-файлов",
    author="Ruslan",
    author_email="r.khuseyinov@edu.centraluniversity.ru",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
    long_description=read_readme(),
    long_description_content_type='text/markdown',
)
