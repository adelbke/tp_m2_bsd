# Documentation Projet Sécurité

## standard de requête

Nous allons suivre le standard REST (c'est le plus simple des standards matechkiwch)

Le format utilisé est json,
exemple de requête:
```json
{
    sender: 'adel'
    algorithm: 'ceasar',
    message: 'Hello World',
    key: 6,
    type: 'encrypt'
}
```

- sender: représente le nom de l'expéditeur (utilisez vôtre prénom)
- algorithm: le nom de l'algorithme utilisé (où à utiliser) la liste standard des noms d'algorithms se trouve ici
- message: tout simplement le message à envoyer
- key: la clé, elle est dynamique et dépend de l'algo
- type (encrypt|decrypt): peut prendre deux valeurs 'encrypt' ou 'decrypt'
  - encrypt: signifie que le message envoyé doit être crypté par le recipient (message doit être en clair)
  - decrypt: signifie que le message envoyé doit être décrypté par le recipient (message doit être crypté)

### listes des Algorithmes

- ceasar: 'ceasar'
- vigenere: 'vigenere'
- substitution: 'substitution'
- transposition: 'transposition'
<!-- - des: 'des' -->
<!-- - rsa: 'rsa' -->

### types de la clé

- ceasar: nombre (type: number)
  - `key: 6`
- vigenere: string
  - `key: 'grou'`
- substitution: String
  - alphabet de chiffrement:
    - taille 26
    - sans duplication
  - `key: 'zyxwvutsrqponmlkjihgfedcba' `
- transposition: nombre (type: number)
  - `key: 6`
<!-- - des: 'des' -->



