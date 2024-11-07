from setuptools import setup, find_packages

setup(
    name='prlps_fakeua',
    version='0.0.1b',
    author='prolapser',
    packages=find_packages(),
    url='https://github.com/prolapser/prlps_fakeua',
    license='LICENSE.txt',
    description='генерация заголовков браузеров и user-agent',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'httpx'
    ],
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
