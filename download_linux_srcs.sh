
# This utility script may be useful later to act as a host arch triplet guesser
# https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess

# This whole setup should get parameterized later but let's just get started shall we?

curl -O ./reciples/cmake/src/ https://github.com/Kitware/CMake/releases/download/v3.22.3/cmake-3.22.3.tar.gz
curl -O ./recipes/python/src/ https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tgz
curl -O ./recipes/python/src/ https://www.python.org/ftp/python/3.7.12/Python-3.7.12.tgz
