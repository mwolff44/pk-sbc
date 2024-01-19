# Post Installation

## Étape optionnelle

Le pilote de journalisation *local* est recommandé car il effectue la rotation des journaux par défaut et utilise un format de fichier plus efficace.
Pour configurer le daemon Docker pour qu'il utilise par défaut un pilote de journalisation spécifique, définissez la valeur de log-driver avec le nom du pilote de journalisation dans le fichier daemon.json /etc/docker/daemon.json

```
{
"log-driver" : "local"
}
```

Redémarrez Docker pour que les changements soient pris en compte

```
sudo systemctl restart docker.service
```

Et pour vérifier

```
docker info --format '{{.LoggingDriver}}'
```
