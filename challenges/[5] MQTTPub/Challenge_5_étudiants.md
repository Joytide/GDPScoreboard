# Challenge 5 - MQTT Publish

Pour ce challenge, pas de broadcaster, mais vous devez vous-même aller valider le challenge avec votre micro-contrôleur. Vous devez tout d’abord vous connecter au réseau wifi avec le SSID et le mot de passe transmis dans le mail du TP2.

Puis vous allez devoir vous connecter au broker MQTT sur ``gdp.devinci.fr`` sur le port 1883 (le port par défaut des brokers MQTT), avec les noms d'équipe et les mots de passes fournis dans le mail pour ce TP.

Une fois connecté au broker, vous allez devoir publier sur les endpoints: 

- ``challenge5/<numéro de votre équipe>/temp`` 
- ``challenge5/<numéro de votre équipe>/hum``

La température et l'humidité récupérées grâce au DHT11. La validation sera automatique si ce sont les mêmes valeurs que mon DHT11.

**Note importante**: Pensez a bien rajouter un délai (au moins quelques secondes) entre chaque publication sur ces topics
