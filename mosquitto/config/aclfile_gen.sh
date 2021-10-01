#!/bin/bash

rm password.txt
rm passwd
rm aclfile

echo "admin:\$6\$ac4SGAqfvBYuclR/\$K1Z9YOndWYP5vk5dTD0uVoPAgqIFC2iyBWXYAzcME6y2AjOF1O+N5d2NLdCJ3Cqmyqsoi4+wl07/UpgS0Q6aMA==" >> passwd
echo -en "user admin\ntopic #\n\n" >> aclfile
# Génération de tous les identifiants et les mots de passe pour chacun des groupes
mkdir hashes
for group in $(seq -f "%2g" 1 80)
do
    # Génération mot de passe de 8 caractère alphanumériques
    password=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 8)
    printf "group$group:$password\n" >> hashes/$group.txt
    mosquitto_passwd -U "hashes/$group.txt"
    echo "Génération des configurations pour l'équipe $group. Mot de passe : $password"
    echo group$group : $password >> password.txt
    cat "hashes/$group.txt" >> passwd;
    echo -en $"user group$group\ntopic challenge4/$group/#\n\nuser group$group\ntopic challenge5/$group/#\n\nuser group$group\ntopic challenge6/$group/#\n\n\n" >> aclfile

done

rm -rf hashes