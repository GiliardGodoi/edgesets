from setuptools import setup, find_packages

setup(
    name="edgesets",
    version='0.0.0',
    author='@GiliardGodoi',
    author_email='giliard.godoi@gmail.com',
    description="A tree representation for Evolutionary Algorithms",
    long_description=open('README.md').read(),
    keywords=['Edge Sets', 'Tree representation', 'Evolutionary Algorithms'],
    url='https://github.com/GiliardGodoi/edgesets',
    license='MIT License',
    packages=find_packages(),
    classifiers=['Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence']
)