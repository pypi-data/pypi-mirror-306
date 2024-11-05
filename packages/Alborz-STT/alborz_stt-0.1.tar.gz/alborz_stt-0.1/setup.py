from setuptools import setup,find_packages

setup(
  name='Alborz_STT',
  version="0.1",
  author="Alborz yzh",
  author_email="example@gmail.com",
  description="this is a speech to text pacakage create by alborz yzh"
)
packages = find_packages
install_requirements = [
  'selenium',
  'webdriver_manager'
]
