# GDP Scoreboard

Basic scoreboard and challenges for GDP electronic project, 

Install mosquitto and generate the mosquitto aclfile and passwords for the teams

```bash
sudo apt install mosquitto
sudo systemctl disable mosquitto
sudo systemctl stop mosquitto

cd mosquitto/config
sh aclfile_gen.sh
```

Copy and update to your liking (changing passwords for example) the docker-compose example:

```bash
cp docker-compose.example.yml docker-compose.yml
```

Launch

```bash
sudo docker-compose build MAxime aurelien mehdi césar
```

