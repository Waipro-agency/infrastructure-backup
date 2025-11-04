"""
Claude Opus 4 Configuration for WAIPRO Agency
Using OpenRouter API with existing keys
"""

import os
import requests
from typing import Optional, Dict, Any

class OpusClient:
    """Client for Claude Opus 4 via OpenRouter"""

    # Le tue chiavi OpenRouter esistenti
    OPENROUTER_KEYS = {
        "ward": "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",
        "claudio_no_limit": "sk-or-v1-ac9...35c",  # Inserisci chiave completa
        "claudio_desktop": "sk-or-v1-27b...6a5",   # Inserisci chiave completa
    }

    # Modelli Claude disponibili su OpenRouter
    MODELS = {
        "opus_4": "anthropic/claude-opus-4-20250514",  # Opus 4 (più potente)
        "sonnet_4": "anthropic/claude-sonnet-4-20250514",  # Sonnet 4 (bilanciato)
        "haiku_4": "anthropic/claude-haiku-4-20250514",    # Haiku 4 (veloce)
    }

    def __init__(self, api_key: str = None):
        """
        Inizializza il client Opus 4

        Args:
            api_key: Chiave API OpenRouter (default: usa 'ward')
        """
        self.api_key = api_key or self.OPENROUTER_KEYS["ward"]
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://waipro.base44.app",
            "X-Title": "WAIPRO Agency",
            "Content-Type": "application/json"
        }

    def chat_completion(
        self,
        messages: list,
        model: str = "opus_4",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Invia una richiesta a Claude Opus 4

        Args:
            messages: Lista di messaggi [{"role": "user", "content": "..."}]
            model: Modello da usare (opus_4, sonnet_4, haiku_4)
            temperature: Creatività (0.0-1.0)
            max_tokens: Lunghezza massima risposta

        Returns:
            Risposta dal modello

        Example:
            >>> client = OpusClient()
            >>> response = client.chat_completion([
            ...     {"role": "user", "content": "Ciao, come stai?"}
            ... ])
            >>> print(response["choices"][0]["message"]["content"])
        """

        model_id = self.MODELS.get(model, model)

        payload = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=payload
        )

        response.raise_for_status()
        return response.json()

    def simple_prompt(self, prompt: str, model: str = "opus_4") -> str:
        """
        Metodo semplificato per prompt veloci

        Args:
            prompt: Testo da inviare
            model: Modello da usare

        Returns:
            Risposta testuale

        Example:
            >>> client = OpusClient()
            >>> risposta = client.simple_prompt("Scrivi un post LinkedIn per WAIPRO")
            >>> print(risposta)
        """

        messages = [{"role": "user", "content": prompt}]
        response = self.chat_completion(messages, model=model)

        return response["choices"][0]["message"]["content"]


# ===== ESEMPI DI UTILIZZO =====

def esempio_base():
    """Esempio base di utilizzo Opus 4"""

    print("🚀 Test Claude Opus 4 - WAIPRO Agency\n")

    # Inizializza client
    client = OpusClient()

    # Test semplice
    risposta = client.simple_prompt(
        "Ciao Claude Opus 4! Presentati brevemente."
    )

    print(f"Risposta Opus 4:\n{risposta}\n")


def esempio_avanzato():
    """Esempio avanzato con conversazione"""

    client = OpusClient()

    conversazione = [
        {"role": "user", "content": "Sono Cristian, founder di WAIPRO. Aiutami a scrivere un post LinkedIn sul futuro dell'AI nelle agenzie digitali."},
    ]

    risposta = client.chat_completion(
        messages=conversazione,
        model="opus_4",
        temperature=0.8,  # Più creativo
        max_tokens=1000
    )

    post_linkedin = risposta["choices"][0]["message"]["content"]
    print(f"📱 Post LinkedIn generato:\n\n{post_linkedin}")


def esempio_integrazione_base44():
    """Esempio integrazione con Base44"""

    from base44_integration import Base44Client

    # Client Opus 4
    opus = OpusClient()

    # Client Base44 (assumendo che esista)
    # base44 = Base44Client()

    # Genera contenuto con Opus 4
    contenuto = opus.simple_prompt(
        "Scrivi un messaggio di benvenuto per un nuovo cliente WAIPRO"
    )

    # Invia a Base44
    # base44.create_activity({
    #     "type": "ai_generated_content",
    #     "content": contenuto,
    #     "model": "claude-opus-4"
    # })

    print(f"✅ Contenuto generato e pronto per Base44:\n{contenuto}")


if __name__ == "__main__":
    # Testa Opus 4
    esempio_base()
    print("\n" + "="*60 + "\n")
    esempio_avanzato()
