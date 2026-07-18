# Atlas Vivo System Architecture Diagram

## Diagram

```mermaid
graph TD
    A[Utilizadores] -->|Submissão| B[Frontend Atlas Vivo]
    B -->|API| C[Backend Services]
    C -->|Git API| D[Codeberg]
    C -->|Zenodo API| E[Zenodo]
    C -->|ORCID API| F[ORCID]
    D -->|Sync| G[GitHub Mirror]
    E -->|DOI| F
    C -->|Metadados| H[SNIG/AMA]
```

## Version Info
- **Version**: 1.0.0
- **Date**: 2026-07-18
- **Author**: Vibe Work Agent
- **Source**: Extracted from documentacao-tecnica-ai-act.md