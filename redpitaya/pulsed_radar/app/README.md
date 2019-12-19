# Param�tres de l'application RADAR

## Acquisition
* **tempo**: stock et transfert l'ensemble de la trame;
* **pos n**: stock le point n par trame.

## Configurations
### Configurations globales
* **input 0/1**: s�lectionne si la trame enti�re est transf�r�e au DAC (valeur
  0) ou seulement un point de la trame, de position donn�e par la commande pos
  (ci-dessus), qui est transf�r� (valeur 0).
* **period nbpoint**: Configure la dur�e d'une trame (exprim�e en nombre de
  point avec 8ns/point);
* **poff n**: dur�e entre la coupure de la r�ception et l'activation de
  l'�mission, puis entre la coupure de la transmission et la r�activation de la
  r�ception (voir Remarques plus bas).
* **pon n**: dur�e de l'�mission (en nombre de cycles d'horloges) (voir
  Remarques plus bas);

### bloc check
* **bypass_check 1/0**: D�fini si le bloc de d�tection de trames corrompues est
  utilis� ou pas;
* **start_offset n**: offset (en nombre de point) du d�but de la zone utilis�e pour
  le calcul;
* **limit**: valeur au dela de laquelle la trame est consid�r�e comme corrompu.

### bloc average
* **bypass_mean 1/0**: D�fini si le bloc d'average est utilis� ou non
* **iter n**: nombre d'accumulation r�alis� par le bloc d'average. Doit �tre une
puissante de 2

## Remarques

Les options **pon** et **poff** sont utilis�es pour piloter le switch. Celui ci contient
deux signaux pour activer ind�pendemment **RF1** et **RF2** et pour les router sur **RFC**
(cf. datasheet). 

Pour garantir l'isolation la r�ception est physiquement coup�e au niveau du
switch avant d'activer la transmission~:
* le signal allant aux m�langeur est d�connect�e de RFC (coupure de la r�ception);
* au bout de poff cycles d'horloges le signal venant du g�n�rateur est connect�
  � RFC (transmission);
* au bout de pon cycles d'horloges la voie du g�n�rateur est d�connect�e;
* au bout de poff cycles d'horloges la r�ception est � nouveau activ�e.

La dur�e totale est donc de (2 x poff) + pon cycles d'horloges.


## Remarques 2

Le fichier de lancement /opt/radar_red/bin/radar_red_us.sh contient un exemple de
s�quence de configuration en fin de fichier :

```
# periode d'interrogation
./radar_red_us period 512
# limite de seuil de rejet de la trame
./radar_red_us limit 55000
# offset de demarrage du calcul
./radar_red_us start_offset 350
# nombre de moyenne
./radar_red_us iter 16
# bloc average active
./radar_red_us bypass_mean 0
# bloc verification trames active
./radar_red_us bypass_check 0
```
