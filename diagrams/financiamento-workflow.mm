```mermaid
flowchart TD
    A[Projeto ATLAS VIVO] --> B[Análise de Requisitos]
    B --> C[Verificação de Conformidade]
    C --> D[Identificação de Oportunidades]
    D --> E[Pré-seleção de Programas]
    E --> F[Geração de Documentação]
    F --> G[Submissão Automática]
    G --> H[Monitorização de Status]
    H --> I[Aprovação]
    
    C -->|RGPD| C1[Verificado]
    C -->|AI Act| C2[Verificado]
    C -->|ISO 42001| C3[Verificado]
    C -->|Interoperabilidade| C4[Verificado]
    
    D -->|Matriz de Financiamento| D1[Local, Municipal, Regional, Nacional, UE, Internacional]
    
    E -->|Heurísticas| E1[Score >=0.7]
    
    F -->|Templates| F1[Proposta Técnica]
    F -->|Templates| F2[Orçamento Detalhado]
    F -->|Templates| F3[Plano de Sustentabilidade]
    F -->|Templates| F4[Declaração de Conformidade]
```