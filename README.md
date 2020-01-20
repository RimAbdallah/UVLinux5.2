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

  