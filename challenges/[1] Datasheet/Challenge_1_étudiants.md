# Challenge 1 Datasheet (Séance 1) 

## Informations sur vos mallettes

Vos mallettes contiennent:

- Un NodeMCU (Rappel: il marche en 3.3V, mais peut prendre du 10V maximum en entrée)
- Un câble microUSB pour connecter le NodeMCU à vos PC
- Une breadboard ou plaque d'essaie (Pour voir comment ca fonctionne: https://www.robot-maker.com/ouvrages/2-1-utiliser-breadboard/)
- Des capteurs et actionneurs (Bouton, LEDs, potentiomètre, résistance)



**Rappel!** Les LEDs doivent toujours être branchées derrière une résistance 150Ohm (https://www.digikey.fr/fr/resources/conversion-calculators/conversion-calculator-resistor-color-code pour les reconnaître)



Venez chercher des fils (normalement avec la plaque d'essai, uniquement des fils mâle-mâle sont nécessaires).

(Si jamais il vous manque du matériel sur cette liste ou comparé à votre voisin, faite le nous savoir)

## Challenge

Vous avez à votre disposition dans les salles (géré par les moniteurs), un NodeMCU "broadcaster", qui envoie avec un baud rate de 9600 sur le pin ``TXD1`` un token (de 6 caractères) vous permettant de valider le challenge. Votre but est de trouver la datasheet du NodeMCU sur internet, d'identifier le bon pin sur lequel le broadcaster envoi le token et de programmer votre NodeMCU pour qu'il puisse lire le token sur ce pin.



#### Quelques informations supplémentaires:

- Il y aura au minimum 1 broadcaster par salle.
- Le broadcaster est identique aux NodeMCU que vous avez.
- Pensez à mettre les grounds (G ou GND sur les board) en commun quand vous venez faire un essai de lecture.
- Envoyer une seule personne de votre équipe faire la lecture avec le NodeMCU et son ordinateur, ne venez pas à 4.
- N’essayer pas d’utiliser le token d’une autre équipe, ils sont uniques.

