# Langage TOAM 
## Introduction
Ce langage a été réalisé dans le cadre du cours de Théorie des Langages dispensé par M.BAUDOIN dans le cadre de la promotion 3ème Année d'Architecture des Logiciels à l'ESGI Paris pour l'année 2023-2024.

Il porte ce nom car ses auteurs sont **To**m BOURLARD et N**oam** DE MASURE.

En effet, c'est très original.

Fait important, ce langage est typé, ce qui a été la plus grosse partie de ce projet.
## Syntaxe
Vous remarquerez que la syntaxe de ce langage n'est carrément pas inspirée du langage que l'on utilise pour effectuer le lexing, à savoir le Python.

## Fonctionnalités
### Print
La fonction `print` permet d'afficher une chaîne de caractères dans la console.
```
print("Hello, World!"); // Affiche "Hello, World!" dans la console
```
### Scan
Toam dispose de deux scans différents, le toamScan et le scan.
```
int a = 0;
toamScan(a);
```
```
int a = 0;
a = scan();
```

### Tableaux
On peut déclarer un tableau de la manière suivante :
```
int[] tab = [1,2,3];
```
On peut accéder à un élément du tableau de la manière suivante :
```
int a = tab[0]; // a = 1
```
On peut modifier un élément du tableau de la manière suivante :
```
tab[0] = 5;
```
On peut ajouter un élément à la fin du tableau de la manière suivante :
```
tab[] = 5;
```
### Fonction
On peut déclarer une fonction de la manière suivante :
```
function int fibo(int n) {
    if (n <= 1) {
        return n;
    };
    int a = fibo(n - 1);
    int b = fibo(n - 2);
    return a + b;
};
```
### For
On peut utiliser une boucle for de la manière suivante :
```
for (int i = 0; i < 10; i++) {
    print(i);
};
```
### While
On peut utiliser une boucle while de la manière suivante :
```
int i = 0;
while (i < 10) {
    print(i);
    i++;
};
```
### If
On peut utiliser une condition if de la manière suivante :
```
int a = 5;
if (a == 5) {
    print("a est égal à 5");
} else {
    print("a n'est pas égal à 5");
};
```
### Pointeurs
On peut utiliser des pointeurs de la manière suivante :
```
int a = 5;
int* pa = &a;
print(*pa); // 5
```
### Types
- int
- string
- char
- double
- float
- bool
- void
### Import
Il est possible d'importer un fichier grâce à son chemin absolu depuis le dossier `project`
```
import "project/src/utils.toam";
```
### Scopes
Il est possible d'utiliser une variable globale dans les fonctions, mais il n'est pas possible d'utiliser une variable créée dans une fonction à l'extérieur de celle-ci.
```
function int increment(int x) {
    int a = x+1; // utilisation de la variable paramètre
    print("little j = ");
    int j = 4; // création d'une variable locale
    print(j);
    return a;
};

int x = 0;
int j = 5;
int newX = increment(x);
print(j); // 5
if(true) {
    j = 6; 
};
print(j); // 6
```


## Exemples
### Hello World
```
print("Hello, World!"); // Affiche "Hello, World!" dans la console
```
### Fibonacci
```
/*
    Ceci est un bloc de commentaire
*/
function int fibo(int n) {
    if (n <= 1) {
        return n;
    };
    int a = fibo(n - 1);
    int b = fibo(n - 2);
    return a + b;
};
int result = fibo(12); // result = 144
```
### Import
import.toam
```
import "utils.toam";

int[] tab = initArray(10);
print(tab);
print(len(tab));

print(pow(2, 3));

hello();
```
utils.toam
```
function int pow(int x, int y) {
    int result = 1;
    while (y > 0) {
        result = result * x;
        y--;
    };
    return result;
};

function void hello() {
    print("Hello, World!");
};

function int[] initArray(int size) {
    int[] result = [];
    int i = 0;
    while (i < size) {
        result[] = 0;
        i++;
    };
    return result;
};
```
### Pointeurs
```
function void addAtEnd(int[]* tab) {
    *tab[] = 5;
};

int[] tab = [1,2,3];

int a = 5;
int b = 6;
int* pa = &a;
print(*pa); // 5
*pa = 7;
print(a); // 7

// print before update
print(tab); // [1,2,3]
addAtEnd(&tab);
// print after update
print(tab); // [1,2,3,5]
```
### Concaténation
```
int x = 0;
string a = "a";
print(a+x); // a0
print("Hello world, valeur de a = " + a + " et valeur de x = " + x); // Hello world, valeur de a = a et valeur de x = 0
int t = 5;
int v = 5;
print("Valeur de t+v = "+(t+v)); // Valeur de t+v = 10
bool b = true;
print("Valeur de b = "+b); // Valeur de b = True
print("Oui"+(b+t)); // Oui6
```