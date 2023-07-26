[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)

# pks-sip-proxy

## Description

Le projet permet d'interconnecter des IPBX et des opérateurs télécoms dans le but de recevoir et d'émettre des appels.

## Fonctionnement

=> PRECISER LES INFOS LORS DE LA CREATION D'UN CLIENT

## Process de routage des appels

Le routage des appels vers leur destinataire est réalisé en 3 étapes distinctes : 

1. authentification et autorisation de la source émettrice de la requête
2. recherche de la destination de la requête
3. routage de la requête vers le destinataire

De manière transparente, des contrôles de conhérence des messages SIP et les mécanismes de résolution du NAT sont appliqués.

### Authentification et autorisation de l'appel

L'authentification et l'autorisation des appels, que la source soit un client/IPBX ou un fournisseur, se fait en vérifiant l'adresse IP source de la requête.

Une nouvelle requête après avoir passée les vérifications de base est envoyée dans la route "auth".

Donc, quand une nouvelle requête arrive dans le proxy SIP, son adresse source est évaluée pour déterminer si la passerelle éméttrice est autorisée à émettre des appels via notre proxy.

Le module de Kamailio utilisé pour l'authentification des requêtes est le module "[permissions](https://kamailio.org/docs/modules/5.6.x/modules/permissions.html)". Son rôle est de vérifier une adresse IP et un port fournis à la fonction de controle au contenu d'une base de données. De plus, les données étant chargées en mémoire RAM, le processus est extrêmement efficace.

Une déclaration préalable des adresses IP des passerelles est donc obligatoire avec quelques paramètres complémentaires permettant de déterminer si la requête vient d'un fournisseur ou d'un client/IPBX et de connaître l'identifiant unique de la passerelle.

Le paramètre "[grp](https://kamailio.org/docs/modules/5.6.x/modules/permissions.html#permissions.p.grp_col)" de la table `address` permet de déterminer si la passerelle appartient à un fournisseur ou un client. 
Nous utilisons une valeur spécifique "grp" pour regrouper les passerelles par groupe. Nous avons défini 2 groupes :

* IPBX /clients : l'id étant 1
* Fournisseurs : l'id étant 2


La colonne "[tag](https://kamailio.org/docs/modules/5.6.x/modules/permissions.html#permissions.p.tag_col)" permettant de compléter la variable "peer_tag" représente l'identifiant unique de la passerelle. 

Comme nous n'utilisons que la fonctionnalité fournie par la table `address`, nous ne chargeons que ce backend spécifique.

```
modparam("permissions", "load_backends", 1)
```

Un exemple de la table `address` avec des données pour illustrer ce principe : 

```tsv
id(int,auto) grp(int) ip_addr(string) mask(int) port(int) tag(string,null) 
1 1 10.1.1.1 32 5060 456
2 2 8.1.2.2 32 5060 20
```
> Explications : 
> * 1ère ligne : l'adresse IP/mask 10.1.1.1/32 et le port 5060 concerne la passerelle ayant l'id unique 456 et appartient à un client/IPBX
> * 2nde ligne : l'adresse IP/mask 8.1.2.2/32 et le port 5060 concerne la passerelle ayant l'id unique 20 et appartient à un fournisseur


Le fonction `allow_source_address_group` nous permet de déterminer si l'adresse IP et le port source du message correspond à une entrée de le table `address`. Dans le cas contraire, la requête est ignorée.

### Recherche de la destination de la requête

Ensuite, quand le requête a été authentifiée, nous allons déterminer la destination de ce message. Nous allons utiliser le module de Kamailio "[dialplan](https://kamailio.org/docs/modules/5.6.x/modules/dialplan.html)". Nous allons devoir router les requêtes venant des fournisseurs et des clients.

Les requêtes des fournisseurs vont être routées vers les clients selon la SDA (coutenue dans la request URI du message). Les requêtes des IPBX/clients, vont être routées selon le numéro appelé.

Pour cela, nous allons comparer le contenu de la partie "username" de la R-URI avec la colonne "match_op" du module "dialplan". Si une correspondance est trouvée, alors le destination contenue dans le champs "attr" va permettre d'obtenir la destination de la requète.

Il est important de noter que le "dialplan_id" est utilisé par la fonction `dp_match`pour savoir si la règle concerne des SDA ou des routages d'appels vers les fournisseurs. Ainsi, pour les requêtes fournisseurs, uniquement le dialplan_id "SDA" sera évalué tandis que pour les requêtes clientes, les 2 dialplans seront utilisés permettant de garder les appels internes dans le réseau au lieu de les faire sortir par un fournisseur pour les voir ensuite revenir par le même fournisseur ou un autre.

Un exemple de la table `dialplan` avec des données pour illustrer ce principe : 

```tsv
id(int,auto) dpid(int) pr(int) match_op(int) match_exp(string) match_len(int) subst_exp(string) repl_exp(string) attrs(string) 
1 1 1 1 ^3320202020[0-9]$ 1 0 0 23
2 2 1 1 +33[1-9][0-9]+$ 12 0 0 21
3 2 1 1 ^\\+33[1-9][0-9]+$ 12 1 1 201
```
> Explications : 
> Cette table est plus complexe que la table `address`, mais une fois apprivoisée, on comprend sa puissance. Tout d'abord une explication des champs est nécessaire : 
> * id : identifiant unique de la ligne
> * dpid : dialplan_id permettant de déterminer si la ligne définie une règle pour une SDA - valeur 1 - ou pour une destination vers un opérateur - valeur 2 -
> * pr : définit la priorité de la règle
> * match_op : définit le type de correspondance à appliquer à cette règle
>     * 0 - comparaison de chaîne de caractères;
>     * 1 - correspondance en utilisant une expression régulière (pcre);
>     * 2 - correspondance selon fnmatch (shell-like pattern).
> * match_exp : expression de correspondance de la règle
> * match_len : définit une éventuelle longueur de préfixe fixe pour la correspondance. 0 définit une règle de longueur variable.
> * subst_exp : définit une règle de correspondance pour appliquer la règle de substitution associée
> * subst_exp : règle de substitution
> * attrs : définit la liste des attributs récupérée si la règle correspond au préfixe. Dans notre cas, ce sera l'id (un entier) définissant le groupe de passerelles à utiliser
>
> Expliquons maintenant les 2 règles présentées : 
> * 1ère ligne : pour le groupe de règles "SDA", les numéros de 33202020200 à 33202020200 seront routés vers le groupe de passerelles 23
> * 2nde ligne : pour le groupe de règles "opérateur / offnet", les numéros FR au format E.164 seront routés vers le groupe de passerelles 21
> 
> Note : nous n'utilisons pas la fonctionnalités de substitution.

### Distribution de l'appel via les passerelles

Enfin, le routage final de la requête est réalisé par le module de Kamailio "[dispatcher](https://kamailio.org/docs/modules/5.6.x/modules/dispatcher.html)". Ce module contient la liste de passerelles ainsi que les règles de distribution. Une attention particulière à la variable "socketname" peut être nécessaire afin de s'assurer du bon routage des messages et de la mise en oeuvre adéquate des processus de résolution de traversée du NAT.

Le "setid" correspond au client ou au fournisseur et regroupe ses passerelles.

Nous pouvons utiliser un fichier plat ou une table de base de données comme les 2 modules précédents. Afin de rester cohérent, et de préparer une future administration via une interface graphique, la base de données est utilisée.

```
id(int,auto) setid(int) destination(string) flags(int) priority(int) attrs(string) description(string) 
1 23 sip:1.1.1.1:5060 0 0 prov=ovh ovh
2 21 sip:8.1.1.1:5060 0 0 socketname=ipbx;cust=celea celea
```

> Explications : 
>La configuration est assez simple et doit-être lue ainsi : 
>* id: identifiant unique de la ligne
>* setid: identifie l'identifiant du groupe de gateway. Il correspond à la valeur du champs `attrs` de la table `dialpan`
>* destination: représente l'uri SIP de la passerelle.
>Le champs attrs est optionnel et dans l'exemple permet de spécifier le nom d'une socket spécifique (si on imagine qu'on écoute sur des ports différents pour les requêtes clients/IPBX et les requêtes fournisseurs). Si aucune valeur n'est indiquée, il faut ajouter null !
>Le champs description est optionnel, et s'il est nul, il faut indiquer la valeur null !
>On peut aussi ajouter des noms d'attributs pour déterminer le nom du client/fournisseur comme dans l'exemple avec la variable cust. Elle n'a qu'une valeur indicative dans notre cas, mais on pourrait par la suite effectuer des traitements complémentaires.

Note : l'algorithme choisit pour la distribution des appels sur plusieurs gateway est le round-robin, permettant une répartition à peu près équivalente, est simple et performant. Dans l'avenir, d'autres choix pourront-être faits.

## Installation

L'installation est assez simple. Soit des conteneurs sont utilisés soit une machine virtuelle avec comme système d'exploitation Debian 11.
Le déploiement via les conteneurs est assez simple ainsi que les mises à jour. Il faut dans un premier temps récupérer les images, définir les bonnes variables d'environnement puis lancer les conteneurs.
Dans le cas d'un déploiement sur une VM, il faut installer les dépendances Kamailio via les paquets Debian officiels. Puis, définir les variables d'environnement et redémarrer Kamailio.

## Usage

La liste des commandes ci-dessous permet d'effectuer les opérations de modifications live et de vérifier les différents états.

## Support

L'utilisation des issues de Gitlab est une bonne pratique permettant une traçabilité des demandes et liées celles-ci à des modifications de code.

## Roadmap

TDB

## Authors

Mathias WOLFF

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

Le projet est soumis à la license AGPL.

