# API Keys Management - Infrastructure Backup

## 📋 Panoramica

Questo repository centralizza **tutta la documentazione delle API Keys** utilizzate dall'infrastruttura Waipro Agency. Ogni chiave API è organizzata in modo strutturato con dettagli completi per facilitare la gestione, la consultazione e lo storico.

## 📁 Struttura delle Cartelle

```
api_keys/
├── README.md (questo file - indice principale)
├── API_KEYS_HISTORY.md (storico completo di tutte le chiavi)
├── openrouter/
│   ├── ward.md
│   ├── claudio_no_limit.md
│   └── claudio_desktop.md
├── stripe/ (future integrazioni)
└── altre_piattaforme/ (future integrazioni)
```

## 🔑 Chiavi API Attualmente Gestite

### OpenRouter API Keys

| Nome Chiave | File Documentazione | Status | Data Creazione | Ultima Modifica |
|-------------|-------------------|---------|----------------|------------------|
| **Ward** | [ward.md](./openrouter/ward.md) | ✅ Attiva | 26 Ottobre 2025 | 26 Ottobre 2025 |
| CLAUDIO NO LIMIT | [claudio_no_limit.md](./openrouter/claudio_no_limit.md) | ✅ Attiva | 23 Ottobre 2025 | - |
| Claudio desktop \| no limit | [claudio_desktop.md](./openrouter/claudio_desktop.md) | ✅ Attiva | 23 Ottobre 2025 | - |

## 📝 Processo di Storicizzazione

### Quando Creare una Nuova API Key:

1. **Genera la chiave** sulla piattaforma appropriata (es. OpenRouter)
2. **Crea un nuovo file** nella sottocartella corrispondente (es. `openrouter/nome_chiave.md`)
3. **Documenta tutti i dettagli** seguendo il template standard:
   - Nome completo della chiave
   - Chiave API completa (da proteggere)
   - Scopo e motivazione della creazione
   - Data e ora di attivazione
   - Note operative
   - Limiti di credito (se applicabili)
   - Storia degli utilizzi
   - Status attuale

4. **Aggiorna questo README** aggiungendo la chiave nella tabella sopra
5. **Aggiorna API_KEYS_HISTORY.md** con l'entry cronologica
6. **Commit con messaggio descrittivo**: `docs: add [nome_chiave] API key documentation`

### Template Standard per Documentazione Chiave:

```markdown
# [Nome Chiave API]

## 🔑 Dettagli Chiave

- **Nome**: [Nome]
- **Piattaforma**: [es. OpenRouter]
- **Tipo**: [es. API Key]
- **Chiave Completa**: `[chiave-api-completa]`
- **Chiave Parziale**: `[sk-or-v1-xxx...xxx]`

## 📅 Date Importanti

- **Data Creazione**: [data e ora]
- **Ultimo Utilizzo**: [data e ora]
- **Scadenza**: [se applicabile]

## 🎯 Scopo e Motivazione

[Descrizione dettagliata del perché questa chiave è stata creata]

## ⚙️ Configurazione

- **Limite Credito**: [unlimited / importo specifico]
- **Reset Limite**: [N/A / periodico]
- **Modelli Accessibili**: [tutti / specifici]

## 📊 Statistiche Utilizzo

- **Totale Speso**: $X.XX
- **Questa Settimana**: $X.XX
- **Questo Mese**: $X.XX

## 🔧 Note Operative

[Note importanti per l'utilizzo, configurazioni speciali, integrazioni, ecc.]

## 📝 Storia e Changelog

- **[Data]**: Creazione chiave
- **[Data]**: [Eventi/modifiche successive]

## ⚠️ Status Attuale

- ✅ **ATTIVA** / ❌ **DISABILITATA** / 🔄 **IN REVISIONE**
```

## 🔒 Sicurezza

- **IMPORTANTE**: Questo repository è privato. Non condividere mai le chiavi API pubblicamente.
- Le chiavi devono essere trattate come credenziali sensibili.
- In caso di compromissione, disabilitare immediatamente la chiave e crearne una nuova.
- Aggiornare sempre lo status nel documento quando una chiave viene disabilitata.

## 📚 Risorse Correlate

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [WAIPRO_INTEGRATION_GUIDE.md](../WAIPRO_INTEGRATION_GUIDE.md)
- [DEEP_AGENT_GPT_PROMPT.md](../DEEP_AGENT_GPT_PROMPT.md)

## 🔄 Aggiornamenti e Manutenzione

- **Responsabile**: Team Waipro Agency
- **Frequenza Revisione**: Mensile
- **Ultimo Aggiornamento**: 26 Ottobre 2025, 13:40 CET

---

**Repository Unico di Riferimento**: `Waipro-agency/infrastructure-backup`

Tutta la documentazione delle API keys deve essere centralizzata qui. Non creare duplicati in altri repository.
