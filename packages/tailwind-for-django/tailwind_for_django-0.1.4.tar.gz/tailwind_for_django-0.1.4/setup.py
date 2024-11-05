from setuptools import setup, find_packages

setup(
    name='tailwind_for_django',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A library for easy setup of tailwind in django project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AndreaGallini/tailwind_for_django',
    author='Andrea Gallini',
    author_email='tuo_email@example.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
    ],
    install_requires=[
        'Django>=3.2',
    ],
)