# Ornithoptere

Ce projet permet de piloter un ornithoptère (ou autre dispositif) à l'aide de modules radio NRF24L01 et d'un microcontrôleur compatible MicroPython (ESP32, ESP8266, etc).

## ⚠️ **Important pour tous les développeurs**

Ce projet utilise **pre-commit** pour maintenir la qualité du code. À chaque `git commit`, votre code sera automatiquement formaté, vérifié et testé.

**📋 Configuration requise :** Suivez le [guide de setup](./docs/setup.md) avant de commencer à développer.

## 🚀 Lancer le projet

1. Suivez le guide de configuration dans [setup.md](./docs/setup.md) pour installer les dépendances et configurer l'environnement de développement.
2. Connectez vos modules et microcontrôleurs selon le schéma proposé.
3. Déployez le code sur vos cartes à l'aide des scripts dans le dossier `scripts/`.

## 📄 Documentation technique

- [Explication du code et architecture détaillée](./docs/code_explanation.md)
- [Documentation des scripts de gestion et monitoring](./docs/scripts.md)

## 📚 Ressources

- [Guide de configuration et installation](./docs/setup.md) ← **Débutez ici**
- [Documentation MicroPython](https://docs.micropython.org/en/latest/reference/repl.html)

## 🔌 Schéma de l'ESP32

![Pinout diagram](./docs/pinout.png)

---

Pour toute question sur le fonctionnement interne, consultez la documentation technique ci-dessus.
