# Challenge 4 - MQTT subscription

Pour ce challenge, pas de broadcaster, mais vous devez vous-même aller valider le challenge avec votre micro-contrôleur. Vous devez tout d’abord vous connecter au réseau wifi avec le SSID et le mot de passe transmis dans le mail du TP2.

Puis vous allez devoir vous connecter au broker MQTT sur ``gdp.devinci.fr`` sur le port 1883 (le port par défaut des brokers MQTT), avec les noms d'équipe et les mots de passes fournis dans le mail pour ce TP.

Une fois connecté au broker, vous pourrez récupérer un token en subscribant au topic ``challenge4/<numéro de votre équipe>/token``. Donc si vous êtes l'équipe 8, vous pourrez récupérer votre token sur ``challenge4/8/token``. (Le token est composé comme d'habitude de 6 caractères ASCII).

Vous pouvez utilisez ce token pour valider le challenge 4 sur http://gdp.devinci.fr/deposit

