"""
Claude Opus 4 - Configurazione API Anthropic Diretta
Per WAIPRO Agency - Alternativa a OpenRouter
"""

import os
import anthropic
from typing import Optional, List, Dict, Any

class AnthropicOpusClient:
    """
    Client per accedere direttamente a Claude Opus 4 via API Anthropic

    Requisiti:
    - Account Anthropic Console: https://console.anthropic.com/
    - API Key da: https://console.anthropic.com/settings/keys
    - Crediti sul account (aggiungi carta di credito)

    Installazione:
    pip install anthropic
    """

    MODELS = {
        "opus_4": "claude-opus-4-20250514",
        "sonnet_4": "claude-sonnet-4-20250514",
        "sonnet_3_5": "claude-3-5-sonnet-20241022",
        "haiku": "claude-3-5-haiku-20241022"
    }

    def __init__(self, api_key: Optional[str] = None):
        """
        Inizializza client Anthropic

        Args:
            api_key: Chiave API Anthropic (o usa variabile ANTHROPIC_API_KEY)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

        if not self.api_key:
            raise ValueError(
                "❌ API Key mancante!\n"
                "Opzioni:\n"
                "1. Passa api_key al costruttore\n"
                "2. Imposta variabile: export ANTHROPIC_API_KEY='sk-ant-...'\n"
                "3. Ottieni chiave da: https://console.anthropic.com/settings/keys"
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "opus_4",
        max_tokens: int = 4096,
        temperature: float = 1.0,
        system: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Invia messaggio a Claude Opus 4

        Args:
            messages: [{"role": "user", "content": "..."}, ...]
            model: Modello da usare (opus_4, sonnet_4, etc.)
            max_tokens: Lunghezza massima risposta
            temperature: Creatività (0.0-1.0)
            system: Prompt di sistema (opzionale)

        Returns:
            Risposta testuale

        Example:
            >>> client = AnthropicOpusClient(api_key="sk-ant-...")
            >>> risposta = client.chat([
            ...     {"role": "user", "content": "Ciao Opus 4!"}
            ... ])
            >>> print(risposta)
        """

        model_id = self.MODELS.get(model, model)

        params = {
            "model": model_id,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
            **kwargs
        }

        if system:
            params["system"] = system

        response = self.client.messages.create(**params)

        return response.content[0].text

    def simple_prompt(
        self,
        prompt: str,
        model: str = "opus_4",
        system: Optional[str] = None
    ) -> str:
        """
        Metodo semplificato per prompt singoli

        Args:
            prompt: Testo da inviare
            model: Modello da usare
            system: Prompt di sistema (opzionale)

        Returns:
            Risposta testuale

        Example:
            >>> client = AnthropicOpusClient()
            >>> risposta = client.simple_prompt(
            ...     "Scrivi un post LinkedIn per WAIPRO",
            ...     system="Sei Sofia, Social Media Manager di WAIPRO"
            ... )
        """

        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, model=model, system=system)

    def streaming_chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "opus_4",
        max_tokens: int = 4096,
        **kwargs
    ):
        """
        Risposta in streaming (mostra testo mentre viene generato)

        Example:
            >>> client = AnthropicOpusClient()
            >>> for chunk in client.streaming_chat([
            ...     {"role": "user", "content": "Scrivi una storia lunga"}
            ... ]):
            ...     print(chunk, end="", flush=True)
        """

        model_id = self.MODELS.get(model, model)

        with self.client.messages.stream(
            model=model_id,
            max_tokens=max_tokens,
            messages=messages,
            **kwargs
        ) as stream:
            for text in stream.text_stream:
                yield text


# ===== ESEMPI DI UTILIZZO =====

def esempio_setup():
    """Mostra come ottenere e configurare API key"""

    print("🔑 SETUP API KEY ANTHROPIC\n")
    print("1️⃣ Vai su: https://console.anthropic.com/")
    print("2️⃣ Registrati/Login")
    print("3️⃣ Vai in Settings > API Keys")
    print("4️⃣ Crea nuova API Key")
    print("5️⃣ Aggiungi carta di credito in Billing")
    print("\n📋 Configura la chiave:\n")
    print("export ANTHROPIC_API_KEY='sk-ant-api03-xxxxx'")
    print("\nOPPURE passa al costruttore:")
    print("client = AnthropicOpusClient(api_key='sk-ant-...')")


def esempio_uso_base():
    """Esempio base con Opus 4"""

    # IMPORTANTE: Sostituisci con la TUA chiave Anthropic!
    client = AnthropicOpusClient(api_key="TUA_CHIAVE_QUI")

    # Test semplice
    risposta = client.simple_prompt(
        "Presentati come Claude Opus 4 e spiega le tue capacità",
        model="opus_4"
    )

    print(f"🤖 Opus 4 risponde:\n{risposta}")


def esempio_integrazione_waipro():
    """Esempio integrato con agenti WAIPRO"""

    client = AnthropicOpusClient()

    # Sistema: definisci il ruolo dell'AI
    system_prompt = """
    Sei Sofia, Social Media Manager di WAIPRO Agency.
    WAIPRO è un'agenzia digitale innovativa che usa AI per aiutare i clienti.
    Il tuo stile è: professionale, creativo, orientato ai risultati.
    """

    # Genera contenuto LinkedIn
    post = client.simple_prompt(
        "Scrivi un post LinkedIn su come WAIPRO usa Claude Opus 4 per migliorare il lavoro dei clienti",
        system=system_prompt
    )

    print(f"📱 Post LinkedIn by Sofia:\n\n{post}")


def esempio_streaming():
    """Esempio con risposta in streaming"""

    client = AnthropicOpusClient()

    print("📝 Generazione storia in streaming...\n")

    for chunk in client.streaming_chat([
        {"role": "user", "content": "Racconta brevemente il futuro di WAIPRO Agency"}
    ]):
        print(chunk, end="", flush=True)

    print("\n\n✅ Completato!")


if __name__ == "__main__":
    print("="*60)
    print("  CLAUDE OPUS 4 - CONFIGURAZIONE ANTHROPIC DIRETTA")
    print("  Per WAIPRO Agency")
    print("="*60 + "\n")

    esempio_setup()

    print("\n" + "="*60)
    print("Decommentare gli esempi sotto dopo aver configurato la chiave API")
    print("="*60)

    # Decommentare dopo aver configurato la chiave:
    # esempio_uso_base()
    # esempio_integrazione_waipro()
    # esempio_streaming()
