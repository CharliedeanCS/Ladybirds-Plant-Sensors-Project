


brew install FreeTDS
export CFLAGS="-I$(brew --prefix openssl)/include"export 
export LDFLAGS="-L$(brew --prefix openssl)/lib -L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I$(brew --prefix openssl)/include"

pip install --pre --no-binary :all: pymssql --no-cache
