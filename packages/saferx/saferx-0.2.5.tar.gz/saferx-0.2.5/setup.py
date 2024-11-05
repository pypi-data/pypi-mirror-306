from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

from setuptools import setup, find_packages

setup(
    name='saferx',
    version='0.2.5',
    description='SAFER package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='rirakang',
    author_email='rirakang@gachon.ac.kr',
    url='https://github.com/gachon-CCLab/SAFER_LIB.git',
    install_requires=['torch', 'pandas', 'numpy', 'scikit-learn'],
    packages=find_packages(include=["*", "data_processing_m1", "data_processing_m2", "model1", "model2"]),
    include_package_data=True,
    package_data={
        'saferx': ['model2/model/final_model.pkl'],
        'saferx': ['model1/model/tft_model.pkl']
        # 추가하려는 파일의 상대 경로
    },
    python_requires=">=3.6",
)

