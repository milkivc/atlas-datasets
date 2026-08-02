```mermaid
flowchart TD
    A[Dataset Bruto] --> B[Validação de Dados]
    B --> C[Anonimização/Pseudonimização]
    C --> D[Classificação de Dados]
    D --> E[Verificação Legal]
    E --> F[Preparação de Metadata]
    F --> G[Upload para Codeberg]
    G --> H[Publicação no Zenodo]
    H --> I[Sincronização ORCID]
    I --> J[Registo SNIG/AMA]
    J --> K[Registo OAI-PMH]
    K --> L[Preservação SWHID]
    
    E -->|RGPD| E1[Anonimizado]
    E -->|AI Act| E2[Classificado]
    E -->|DPIA| E3[Aprovado]
    
    F -->|DataCite 4.4| F1[Metadata]
    F -->|INSPIRE| F2[Compliance]
    
    H -->|DOI| H1[Gerado]
    I -->|ORCID| I1[Sincronizado]
```