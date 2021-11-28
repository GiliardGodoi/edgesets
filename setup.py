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
    dependency_links=[
        "git+https://github.com/GiliardGodoi/disjointset",
        "git+https://github.com/GiliardGodoi/pqueue",
        "git+https://github.com/GiliardGodoi/ggraphs"
    ],
    classifiers=['Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence']
)