from setuptools import setup, find_packages

setup(
    name='scapyp',
    version='0.1.6',
    packages=find_packages(),
    description='A Python package for single-case data analysis.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mohammad Ahsan Khodami',
    author_email='ahsan.khodami@gmail.com',
    url='https://github.com/AhsanKhodami/scapyp',
    license='MIT',
    classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.10',
    'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3.10',
    install_requires=[
    'pandas>=1.0.0',
    'numpy>=1.18.0',
    'scipy>=1.4.0',
    'scikit-learn>=0.22.0',
    'statsmodels>=0.11.0',
    ]
)
