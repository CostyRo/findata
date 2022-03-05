if [[ ! -d "/opt" ]]; then
  mkdir /opt
fi

cd ..

sudo mv findata /opt

if ! [ "$(python3 -V)" ]; then
  echo Installing python3.8...
  sudo apt install python3.8
fi

pip install click yfinance matplotlib openpyxl

echo alias "findata=\"python3 /opt/findata/findata.py\"" >> ~/.bashrc
