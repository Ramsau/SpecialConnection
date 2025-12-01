## setup the signalbot
https://pypi.org/project/signalbot/

## create virtualenv
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## create bot service
Put specialconnection.service at /etc/systemd/system/specialconnection.service
then:
```bash
sudo systemctl daemon-reload
sudo systemctl start specialconnection
sudo systemctl enable specialconnection
```
