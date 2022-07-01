## Requirements
1. Java SE Runtime
2. python3

## Setup
1. Create and Activate `venv` 
``` bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies
``` bash
pip install -r requirements.txt
```

3. DB2 server url/port/user is set in `properties.settings`. Sample config:
``` ini
username=<user>
password=<passwd>
rechnername=<computer name>
database=<database name>
```
the final DB2 address is `"{rechnername}.is.inf.uni-due.de:50{gruppennummer}/{database}"`
