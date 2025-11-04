#!/usr/bin/env python3
"""
MCP Server per WAIPRO Agency - Claude Desktop Integration
Permette a Claude Desktop di caricare file e comunicare con il sistema WAIPRO
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

class WaiproMCPServer:
    """
    MCP Server per gestire file upload e configurazioni WAIPRO

    Funzionalità:
    - Upload file JSON (Google Cloud credentials)
    - Lettura/scrittura file configurazione
    - Gestione credenziali sicure
    - Comunicazione con server VPS
    """

    def __init__(self, workspace_dir: str = "/home/user/infrastructure-backup"):
        self.workspace_dir = Path(workspace_dir)
        self.uploads_dir = self.workspace_dir / "uploads"
        self.config_dir = self.workspace_dir / "google_cloud_integration"

        # Crea directory se non esistono
        self.uploads_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)

    def handle_file_upload(self, filename: str, content: str) -> Dict[str, Any]:
        """
        Gestisce upload di file da Claude Desktop

        Args:
            filename: Nome del file
            content: Contenuto del file (JSON, testo, etc.)

        Returns:
            Risultato dell'operazione
        """
        try:
            file_path = self.uploads_dir / filename

            # Determina se è JSON
            if filename.endswith('.json'):
                # Valida JSON
                json_data = json.loads(content)

                # Salva con formattazione
                with open(file_path, 'w') as f:
                    json.dump(json_data, f, indent=2)

                return {
                    "status": "success",
                    "message": f"File JSON salvato: {file_path}",
                    "path": str(file_path),
                    "type": "json",
                    "data": json_data
                }
            else:
                # Salva come testo
                with open(file_path, 'w') as f:
                    f.write(content)

                return {
                    "status": "success",
                    "message": f"File salvato: {file_path}",
                    "path": str(file_path),
                    "type": "text"
                }

        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "message": f"Errore parsing JSON: {str(e)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Errore upload: {str(e)}"
            }

    def get_uploaded_files(self) -> List[Dict[str, Any]]:
        """Ottiene lista file caricati"""
        files = []
        for file_path in self.uploads_dir.iterdir():
            if file_path.is_file():
                files.append({
                    "name": file_path.name,
                    "path": str(file_path),
                    "size": file_path.stat().st_size,
                    "modified": file_path.stat().st_mtime
                })
        return files

    def read_file(self, filename: str) -> Dict[str, Any]:
        """Legge un file caricato"""
        try:
            file_path = self.uploads_dir / filename

            if not file_path.exists():
                return {
                    "status": "error",
                    "message": f"File non trovato: {filename}"
                }

            with open(file_path, 'r') as f:
                content = f.read()

            # Se è JSON, parse e ritorna
            if filename.endswith('.json'):
                return {
                    "status": "success",
                    "data": json.loads(content),
                    "type": "json"
                }
            else:
                return {
                    "status": "success",
                    "content": content,
                    "type": "text"
                }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Errore lettura: {str(e)}"
            }

    def configure_google_cloud(self, json_file: str) -> Dict[str, Any]:
        """
        Configura Google Cloud usando il file JSON caricato

        Args:
            json_file: Nome del file JSON delle credenziali

        Returns:
            Configurazione completata
        """
        try:
            # Leggi il file JSON
            result = self.read_file(json_file)

            if result["status"] == "error":
                return result

            credentials = result["data"]

            # Estrai informazioni importanti
            project_id = credentials.get("project_id")
            client_email = credentials.get("client_email")

            # Crea file di configurazione
            config = {
                "provider": "google_cloud",
                "project_id": project_id,
                "service_account": client_email,
                "credentials_file": str(self.uploads_dir / json_file),
                "setup_date": os.popen("date +%Y-%m-%d").read().strip(),
                "status": "configured"
            }

            config_path = self.config_dir / "google_cloud_config.json"
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)

            return {
                "status": "success",
                "message": "Google Cloud configurato!",
                "project_id": project_id,
                "service_account": client_email,
                "config_path": str(config_path)
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Errore configurazione: {str(e)}"
            }

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gestisce richieste MCP

        Args:
            request: Richiesta JSON con formato:
                {
                    "action": "upload|list|read|configure",
                    "data": {...}
                }
        """
        action = request.get("action")
        data = request.get("data", {})

        if action == "upload":
            return self.handle_file_upload(
                data.get("filename"),
                data.get("content")
            )

        elif action == "list":
            return {
                "status": "success",
                "files": self.get_uploaded_files()
            }

        elif action == "read":
            return self.read_file(data.get("filename"))

        elif action == "configure":
            return self.configure_google_cloud(data.get("json_file"))

        else:
            return {
                "status": "error",
                "message": f"Azione non supportata: {action}"
            }


def main():
    """Avvia MCP server in modalità stdio"""
    server = WaiproMCPServer()

    print("🚀 WAIPRO MCP Server - Pronto per Claude Desktop!", file=sys.stderr)
    print("📁 Workspace:", server.workspace_dir, file=sys.stderr)
    print("📤 Upload directory:", server.uploads_dir, file=sys.stderr)
    print("", file=sys.stderr)

    # Loop di ascolto per richieste JSON
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = server.handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except json.JSONDecodeError:
            print(json.dumps({
                "status": "error",
                "message": "Invalid JSON"
            }))
        except Exception as e:
            print(json.dumps({
                "status": "error",
                "message": str(e)
            }))


if __name__ == "__main__":
    main()
