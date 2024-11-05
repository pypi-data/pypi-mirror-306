# CantinaUtils

Le module python utilitaire de Cantina

## Documentation
### cantinaUtils.Database 
`Database.exec`:<br>
> #### Arguments :<br>
> <span style='color:red'>**body**:</span> (str) Le corps de la requête SQL.<br>
> <span style='color:red'>**args**:</span> (list) Les différents arguments utilisé dans l'argument **body**.

Cette fonction sert à executer une requête SQL, qui modifie la base de données (INSERT, UPDATE, DROP...)<br>
La fonction ne renvoie rien.

`Database.select`:<br>

> #### Arguments :
> <span style='color:red'>**body**:</span> (str) Le corps de la requête SQL.<br>
> <span style='color:red'>**args**:</span> (list) Les différents arguments utilisé dans l'argument **body**.<br>
> <span style='color:yellow'>**number_of_data**:</span> (int) Le nombre de ligne renvoyé par la fonction. Par défaut ou si précisé, `number_of_data=0` précise que la fonction doit renvoyé tout ce qu'elle trouve.

Cette fonction sert à executer une requête SQL, qui lis la base de données (SELECT)<br>
La fonction retourne des informations sous forme d'un tableau.


### cantinaUtils.email_utils
`send_verification_email`:
> #### Arguments : 
> <span style='color:red'>**database**:</span> (class) Argument qui permet d'avoir accès à la base de données depuis la fonction.

Cette fonction sert à envoyer un mail, avec un code unique, afin de vérifier l'adresse email de l'utilisateur.<br>
La fonction ne retourne pas d'informations mais peux retourner des erreurs.
> #### Erreurs:
> **error1**: Cette erreur annonce que la configuration pour l'utilisation d'un serveur SMTP n'existe pas ou est incomplète.<br>
> **error2**: Cette erreur annonce que la sujet ou le contenu de l'email n'est pas défini dans la base de données.


### cantinaUtils.verify_login
`verify_login`:
> #### Arguments:
> <span style='color:red'>**database**:</span> (class) Argument qui permet d'avoir accès à la base de données depuis la fonction.

Cette fonction sert à savoir si un utilisateur toute les conditions sont réunis pour dire si un utilisateur est connecté.<br>
La fonction renvoie `True` si l'utilisateurs est connecté et `False` si il ne l'est pas. La fonction peux renvoyer `desactivated` si les conditions sont réunis mais que le compte à été désactivé par un administrateur.

`verify_A2F`:
> #### Arguments:
> <span style='color:red'>**database**:</span> (class) Argument qui permet d'avoir accès à la base de données depuis la fonction.

Cette fonction sert à savoir si le code d'A2F fournis dans le champ `a2f-code` dans la page de connection est correspondant avec celui générer par notre système.<br>
La fonction renvoie `True` si le code est correspondant ou `False` si il ne correspont pas 