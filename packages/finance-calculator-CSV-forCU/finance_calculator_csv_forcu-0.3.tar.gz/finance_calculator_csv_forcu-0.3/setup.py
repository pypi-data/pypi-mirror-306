from setuptools import setup, find_packages

def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name='finance-calculator_CSV_forCU',
    version='0.3',
    description='Пакет для анализа доходов и расходов',
    author='Ruslan',
    author_email='r.khuseyinov@edu.centraluniversity.ru',
    packages=find_packages(),  # Находит все пакеты в проекте
    install_requires=[
        'pandas',  # Зависимости вашего проекта
    ],
    entry_points={
        'console_scripts': [
            'finance-calculator=finance_calculator.main:main',  # Команда для запуска из командной строки
        ],
    },
    python_requires='>=3.6',  # Минимальная версия Python
    long_description=read_readme(),
    long_description_content_type='text/markdown',
)
