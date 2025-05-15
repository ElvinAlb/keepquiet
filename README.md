# KeepQuiet

KeepQuiet est un projet de Sonomètre connecté.

Il peut-être utilisé par exemple dans des bars pour alerter sur un dépassement des décibels autorisés par la loi.

Le capteur de son capte toute les secondes les décibels environnants et l'affiche sur son écran.
Les données sont envoyés sur un topic MQTT, sont récupérées en local par le script keepquiet_listener et compilées dans un fichier JSONL.

Lorsque le son est trop fort pendant une durée prolongée, un buzzer s'allume et une led clignote.
De plus, un mail est envoyé pour alerter le propriétaire.

Enfin, un détecteur de movement permet de mettre le dispositif en veille lorsqu'il ne détecte aucune activité.
