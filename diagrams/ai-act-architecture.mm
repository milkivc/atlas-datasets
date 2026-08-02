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