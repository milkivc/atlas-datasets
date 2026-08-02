```mermaid
flowchart TD
    A[Monitorização Contínua] --> B[Anomaly Detection]
    B --> C{Shadow AI?}
    C -->|Sim| D[Isolar Sistema]
    C -->|Não| E[LogProbs Analysis]
    E --> F{Ameaça Detetada?}
    F -->|Sim| G[Contenção Automática]
    F -->|Não| H[Continuar Monitorização]
    
    D --> I[Notificar Segurança]
    D --> J[Investigação Forense]
    G --> K[Notificar Segurança]
    G --> L[Recuperação Automática]
    
    B -->|Heisenberg Check| B1[Δx * Δp >= ħ/2]
    E -->|Quantum Encryption| E1[h = 6.626e-34]
```