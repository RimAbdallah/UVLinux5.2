# UV 5.2
# Projet Linux Embarqué
# Étudiants:

   - Mahmoud SOUAYFAN
   - Etienne MONNIER
   - Reem ABDALLAH
   - Rami DUYÉ
   - Georges TANIOS


Vous trouverez ci-dessous les sections suivantes :

- ****Mise en place du système :**** cette section explique comment nous avons installé et configuré les différents éléments de ce projet,

- ****Documentation utilisateur :**** cette section présente les étapes pour l'utilisation du projet.

  

## Mise en place du système

  

### Buildroot

Buildroot est un ensemble de Makefile permettant d'automatiser le processus de build d'une distribution Linux embarquée.

  
L'image Docker qu'on utilise dans notre projet est offert par le lien git ci-joint [link](https://github.com/pblottiere/embsys/tree/master/labs/rpi3/docker), sous le nom "buildroot-video". Le fichier déjà cité, contient un systeme d'exploitation précompilé, ensuite ca sera embarqué sur notre carte SD correspondant a notre carte Raspberry Pi 3.
L'avantage de cet image c'est qu'il est compatible avec la caméra qu'on souhaite mainipuler, ensuite il nous reste d'interagir avec la camera en se servant de l'API [V4L](https://github.com/twam/v4l2grab).


****NB.**** Pour vérifier que tout est correctement configuré, on verifie que les options `BR2_PACKAGE_RPI_FIRMWARE_X`  et `BR2_PACKAGE_LIBV4L` sont activées dans le fichier de configuration de Buildroot (`/configs/embsys_defconfig`).

En resultat, on doit ouvrir un conteneur à l'aide de docker et extraire l'image.
  

### Docker

Selon [lebigdata.fr](https://www.lebigdata.fr/docker-definition) Docker est une plateforme logicielle open source permettant de créer, de déployer et de gérer des containers d’applications virtualisées sur un système d’exploitation. Les services ou fonctions de l’application et ses différentes bibliothèques, fichiers de configuration, dépendances et autres composants sont regroupés au sein du container. Chaque container exécuté partage les services du système d’exploitation.

![IMG_Docker](https://www.docker.com/sites/default/files/d8/2018-11/docker-containerized-and-vm-transparent-bg.png)

source : https://www.docker.com/

  

Commandes :

```

$ sudo docker pull pblottiere/embsys-rpi3-buildroot-video

$ sudo docker run -it pblottiere/embsys-rpi3-buildroot-video /bin/bash

# cd /root

# tar zxvf buildroot-precompiled-2017.08.tar.gz

```

Concrètement, on récupère l'image Docker puis on crée un conteneur. Ensuite, on extrait le système.

On peut alors réaliser les vérifications sur les fichiers de configuration. Comme le système est précompilé, cela signifie que nous n'avons pas besoin de faire la configuration et le build à la main (`make embsys_defconfig`, `make menuconfig` et `make`). 

On peut passer directement au flashage.


### Flashage de la carte SD

Afin de flasher la carte SD qui sera insérée dans la Raspberry Pi 3, on doit tout d'abord créer une image :

```

$ docker cp <container_id>:/root/buildroot-precompiled-2017.08/output/images/sdcard.img .

```

On peut alors flasher la carte avec la commande :

```

$ sudo dd if=sdcard.img of=/dev/sdb

```

****NB.**** Ici, la carte SD est considéré comme le second disque dur (nommé `/dev/sdb` par convention). Vérifier si c'est le cas sur votre machine avec la commande `lsblk`.

  

A l'issue de cette opération, la carte SD comporte normalement deux partitions.

On peut alors copier `start_x.elf` et `fixup_x.dat` depuis le conteneur sur la 1ère partition de la carte SD et modifier le fichier `config.txt` de la 1ère partition de la carte SD pour ajouter :

````

start_x=1

gpu_mem=128

````

La configuration et le flashage de la carte SD sont terminés.

  

### Configuration IP

Dans ce qui suit, on doit savoir l'address IP de la carte afin de se connecter.
Dans un premier temps nous avons essayer de faire une configuration statique d'IP.
  
pour le faire on entre dans  `/etc/network/interfaces`:

```

# interface file auto-generated by buildroot

  

auto lo

iface lo inet loopback

  

auto eth0

iface eth0 inet static

address 192.169.20.10

netmask 255.255.0.0

gateway 192.169.20.9(non necessaire)

```
mais sur ubuntu nous avons pas su configurer eth0, on a essayer sur un kali, la configuration est bien la bonne et 
on a reussit de se connecter en SSH puisqu'on possede pas de linux Kali propre a nous on a redecider de partir sur l'ip dynamique

alors dans le fichier interface on a remis 

 iface eth0 inet dhcp 
 pre-up /etc/network/nfs_check
 wait-delay 15 
Cette nouvelle configuration nous permet de reppasser sur de dynamique, en faisant ip a sur la carte on recupere l'addresse ip de la carte de 172.20.21.31/16
et on reussit a se connecter via SSH : ssh user@172.20.21.31/16

### Configuration et installation de V4L

V4L ( abréviation pour 'Video4Linux' ) est une API vidéo pour les systèmes Linux. on utilise dance ce aui suit le version 2 de cette Librairie: V4L2.
On pourra ainsi capturer les flux vidéo/image de la caméra de la RPI3.

> Installation et configuration sur la carte:
   - telecharger le projet en ecrivant le commande suivant en terminal: 
   ```
   $ git clone https://github.com/twam/v4l2grab
   ```

   - Entrer dans le fichier v4l2grab:
   ```
   $ sh autogen.sh
   ```
   - Commenter `#undef malloc` dans config.h.in

   - Remplacer `v4l2grab.c` avec un docker cp par celui qui est dans le ficher camera. Le but est de récuperer le code modifié par nous. 

   - Compilation pour la RPI3 :
   ```
   $ ./configure CC=/root/buildroot-precompiled-2017.08/output/host/usr/bin/arm-linux-gcc --host=linux

   $ make
   ```
   
   Une cross-compilation est réquis pour la compilation de notre system, car l'architecture de ce dernier est different que celui du raspberry.
   Ensuite le binaire généré ne sera pas notamment exécutable sur la machine.
   
   Une fichier executable sera genere suite a cette compilation. On peut alors copier l'executable sur la carte RPI3 (dans le dossir `/root`). 
   On utilise les commandes ci-dessous pour activer le module et prendre une photo:

   ```
   $ modprobe bcm2835-v4l2
   $ cd /root
   $ ./v4l2grab -d /dev/video0 -o img.jpg
   ```

## Comment Utiliser ?

### Contenu du dépôt Github

**UVLinux5.2/camera :** codes en C et exécutable (après cross-compilation) pour l'API V4L2 et le serveur de la caméra associé.

**UVLinux5.2/ClientServeur.PY :** codes du client et de deux serveurs en Python. Le client est celui utilisé sur la machine souhaitant communiquer avec la Raspberry, les deux serveurs ont servi pour les tests intermédiaires.

### Makefile

Un certain nombre de commandes peuvent être automatisées à l'aide d'un Makefile. On donne dans ce projet un exemple d'utilisation (qui peut sembler superflu, effectivement). On y a défini deux règles (`installation` et `client`), qui sont appelées par les commandes suivantes :
- `make installation` : Lorsque la carte SD est directement connectée à l'ordinateur, au moment du flashage par exemple, cette commande permet de copier le code Python pour l'exécutable pour le module V4L2 (permettant l'utilisation de la caméra et son serveur) au bon endroit sur la carte,
- `make client` : Lorsque l'on est connecté à la carte en ethernet, permet le lancement du client. Attention, cette commande ne doit être utilisée qu'une fois les serveurs lancés.

### Utilisation - Etapes

On part du principe que tout a été correctement configuré et que tous les fichiers nécessaires ont été copiées au bon endroit.

1. **Lancement serveurs :** Dans deux terminaux, se connecter en SSH (`ssh user@172.20.11.112`) puis passer superutilisateur (mot de passe `root1*`). Se placer dans le dossier `/root`et lancer les serveurs (`./v4l2grab` pour la caméra).
2. **Lancement client :** Dans un nouveau terminal, lancer directement le client (`make client`). Il suffit alors de suivre les instructions du client pour communiquer avec les deux serveurs.

### Remarque

En l'état actuel, les images sont enregistrées dans le même répertoire que celui où se trouve le client, sur l'ordinateur. Néanmoins, les images sont envoyées avec un certains retard à l'ordinateur hébergeant le client:
- Lorsqu'on envoie "1 s" la première fois : le serveur crée l'image 0, mais ne l'envoie pas au client.
- Lorsqu'on envoie "1 s" la deuxième fois : le serveur crée l'image 1, mais ne l'envoie pas au client.
- Lorsqu'on envoie "1 s" la troisième fois : le serveur crée l'image 2, mais il envoie l'image 1 au client et elle est bien reçue et sauvegardée dans le répertoire du client.
- Lorsqu'on envoie "1 s" la quatrième fois : le serveur crée l'image 3, il envoie l'image 2 au client et elle est bien reçue et sauvegardée dans le répertoire du client et ainsi de suite...

Ainsi, seulement l'image 1 et la dernière image créée seront perdues, les autres vont arriver avec du retard sur l'ordinateur client.