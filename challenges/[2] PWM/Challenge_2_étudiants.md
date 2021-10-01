# Challenge 2 PWM (TP1 ou TP2)

De nouveau, vous allez avoir à votre disposition dans les salles (géré par les moniteurs), un
potentiomètre (lire la datasheet, ce sont des Trimpot P104) sur lequel vous aller pouvoir lire la
valeur de sortie, entre 0 et 1024, qui correspondent à 0V et 3.3V). Vous allez également pouvoir
vous brancher sur un NodeMCU, qui attend avec un baud rate de 9600 sur son port RX original,
un string correspondant à la valeur du potentiomètre.

Le NodeMCU des moniteurs attends un string comme ceci: ``[Num d'équipe]#[tension du
potentiomètre]/``

Donc si vous lisez 780 et que votre équipe est la 96, vous envoyez le string: ``96#780/``
Le NodeMCU vérifiera que vous avez bien lu la bonne valeur en la lisant aussi et en comparant les
2 valeurs. (Avec une tolérance de 0.1V).

N'hésitez pas à faire des essais d'abord avec vos potentiomètre !

Point important: quand vous ferrez vos essais, s'ils ne marchent pas la première fois, débrancher et brancher les 2 NodeMCU, et pensez à mettre les grounds en commun.



#### Comme précédemment :

- Il y aura au minimum 1 broadcaster par salle.
- Le NodeMCU est identique aux NodeMCU que vous avez.
- Pensez à mettre les grounds (G ou GND sur les board) en commun quand vous venez faire
  un essai.
- Envoyer une (2 maximum) seule personne de votre équipe faire la lecture avec le NodeMCU SANS ORDINATEUR, ne venez pas à 4. Vos tests doivent être faits à votre place. 
- N’essayer pas de demander la valeur aux équipes, on changera la résistance du
  potentiomètre régulièrement.

