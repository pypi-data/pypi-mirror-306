from setuptools import setup
# Load the long_description from README.md
with open("README.rst", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(name="basic_vector3d_package",
      version="1.0.2",
      description="this is a test package with respect to basic calc for vector 3d",
      packages=["BasicCalc"],
      author="iCur",
      author_email="moon_8295@163.com",
      long_description=long_description,
      python_requires='>=3.6',
      url="https:www.iCuriosity.com",
      )
