from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='kutumbh',
  version='0.0.2',
  description='Climatic data analysis and visualizations',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type="text/x-rst",
  url='',  
  author='amresssh',
  author_email='Amreshguptaomar@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='climate', 
  packages=find_packages(),
  install_requires=[
      'matplotlib',
      'numpy',
      'pandas',
      'scikit-learn'
  ] 
)
