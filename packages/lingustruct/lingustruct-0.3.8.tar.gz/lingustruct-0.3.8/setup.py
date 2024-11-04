from setuptools import setup, find_packages

# README.md の内容を長い説明として読み込む
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='lingustruct',
    version='0.3.8',
    description='Framework for human and AI (LLM) collaboration in system design using LLM-optimized templates.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Yasunori Abe',
    author_email='osusume-co@lilseed.jp',
    url='https://pypi.org/project/lingustruct/',
    packages=find_packages(include=["lingustruct", "lingustruct.templates"]),
    license='Proprietary',
    install_requires=[
        'fastapi',
        'uvicorn',
        'jinja2',
        'pydantic',
        'weasyprint',
        'markdown',
        'openai',
        'jsonschema',
        'cryptography',
        'requests',
        'redis>=4.0.0',
    ],  # 'groq' を削除
    include_package_data=True,
    package_data={
        "lingustruct": [
            "templates/master_template.json",
            "templates/overview_template.json",
            "templates/*_s.json"
            "mappings/key_mapping.json"           
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
