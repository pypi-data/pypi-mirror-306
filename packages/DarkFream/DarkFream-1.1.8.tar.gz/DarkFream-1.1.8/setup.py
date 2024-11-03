from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="DarkFream",
    version="1.1.8",
    author="vsp210",
    author_email="vsp210@gmail.com",
    description="Простой веб-фреймворк для создания веб-приложений",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vsp210/DarkFreamMega",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "Jinja2>=2.11.0",
        "peewee>=3.14.0",
        "bcrypt>=4.0.1",
    ],
    include_package_data=True,
    package_data={
        'DarkFream': ['templates/**/*.html'],
    },
)
