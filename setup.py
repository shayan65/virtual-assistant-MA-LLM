from setuptools import setup, find_packages

def load_requirements(filename='requirements.txt'):
    """Load requirements from a requirements file."""
    with open(filename, 'r') as f:
        lineiter = (line.strip() for line in f)
        return [line for line in lineiter if line and not line.startswith("#")]

setup(
    name='virtual-assitant-MA-LLM',
    version='0.1.0',
    description='A description of your project',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=load_requirements(),
    entry_points={
        # Define your application's entry points here if necessary
        # For example:
        # 'console_scripts': [
        #     'my-command = my_package.module:function',
        # ],
    },
    # Include additional parameters here as needed
)