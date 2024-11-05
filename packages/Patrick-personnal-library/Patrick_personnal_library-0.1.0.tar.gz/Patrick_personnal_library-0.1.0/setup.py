from setuptools import setup, find_packages

setup(
    name='Patrick_personnal_library',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Liste des dépendances
    ],
    author='Patrick',
    author_email='pdionne.83@gmail.com',
    description="tout ce que j'ai besoin",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Psychopatd/Patrick_personnal_library.git',  # URL de votre projet
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)