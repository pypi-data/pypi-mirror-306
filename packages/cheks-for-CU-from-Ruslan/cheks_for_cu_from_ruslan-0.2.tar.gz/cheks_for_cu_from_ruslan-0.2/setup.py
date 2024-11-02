from setuptools import setup, find_packages

def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name='cheks_for_CU_from_Ruslan',
    version='0.2',
    description='Пакет для создания чеков',
    author='Ruslan',
    author_email='r.khuseyinov@edu.centraluniversity.ru',
    packages=find_packages(),  # Находит все пакеты в проекте
    install_requires=[
        'json',  # Зависимости вашего проекта
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
