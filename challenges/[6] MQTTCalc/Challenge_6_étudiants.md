# Challenge 6 - MQTT Calculator

Pour ce challenge, pas de broadcaster, mais vous devez vous-même aller valider le challenge avec votre micro-contrôleur. Vous devez tout d’abord vous connecter au réseau wifi avec le SSID et le mot de passe transmis dans le mail du TP2.

Puis vous allez devoir vous connecter au broker MQTT sur ``gdp.devinci.fr`` sur le port 1883 (le port par défaut des brokers MQTT), avec les noms d'équipe et les mots de passes fournis dans le mail pour ce TP.

Les 2 endpoints disponibles pour ce challenges sont:

- ``challenge6/<numéro de votre équipe>/task`` 
- ``challenge6/<numéro de votre équipe>/submit``

Le serveur vous donnera une tâche calculatoire sur le topic task, et vous demandera de la résoudre pour lui et de le publier sur le topic submit. Vous devez résoudre 10 opérations en 10 secondes.

