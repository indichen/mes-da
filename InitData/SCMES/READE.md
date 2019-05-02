# Install freetds for pymssql (Python for MSSQL)

```
brew install freetds
```

# Installation Oracle Client

1. Download Oracle client from [Instant Client for macOS (Intel x86)](https://www.oracle.com/technetwork/topics/intel-macsoft-096467.html) : As Oracle policy, the latest client version supports only (current version - 2) . Since Xinzhuang DB is Oracle 9i, we should use 11.2.0.4.0 (64-bit) . Just download the Basic package is fine. 

2. Unzip the downloaded package to a folder, say ${ORACLE_HOME}, and symlink some version-independent libraries
```
pushd ${ORACLE_HOME}
ln -sf libclntsh.dylib.11.1 libclntsh.dylib
ln -sf libocci.dylib.11.1 libocci.dylib
popd
```

3. Set following environment variables:
```bash
export ORACLE_HOME=${ORACLE_HOME}
export LD_LIBRARY_PATH=${ORACLE_HOME}:${LD_LIBRARY_PATH}
export DYLD_LIBRARY_PATH=${ORACLE_HOME}:${DYLD_LIBRARY_PATH}
```

4. There is an issue (bug?) in Oracle  client 11 that it requires the local hostname can be resolved. Therefore, set it in hosts file:
```
sudo sh -c 'echo 127.0.0.1 $(hostname) >> /etc/hosts'
```

# Create venv environment

```
python3 -m venv venv
source venv/bin/activate
pip install pymssql
pip install --upgrade pip pymssql "cx_oracle>=7.1.3"
```
