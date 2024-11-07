from setuptools import setup, find_packages

setup(
    name="cololog",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "colorama",  # Добавляем colorama как зависимость
    ],
    description="Цветной регистратор с настраиваемыми уровнями и выводом в файл.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="AsQ",
    author_email="asqdanil@yandex.ru",
    url="https://github.com/AsQqqq/cololog",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
