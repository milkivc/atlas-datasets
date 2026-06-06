# Atlas Vivo MILK - Dados Territoriais

## Descrição
Este repositório contém **dados geoespaciais** do Atlas Vivo MILK, incluindo shapefiles, KML e CSV com informações sobre património cultural e territorial em Portugal. Os dados estão organizados para facilitar a interoperabilidade com plataformas como **Zenodo**, **ORCID**, e sistemas de financiamento europeus.

---

## Estrutura do Repositório
```
.
├── README.md                 # Este ficheiro
├── LICENSE                   # Licença CC-BY-SA-4.0
├── metadata.json             # Metadados padronizados
├── .github/
│   ├── workflows/
│   │   ├── validate-metadata.yml  # Validação de metadados
│   │   └── generate-doi.yml        # Geração de DOI via Zenodo
│   └── schemas/
│       └── metadata-schema.json   # Schema para validação
└── data/                     # Dados geoespaciais
    ├── shapefiles/
    ├── kml/
    └── csv/
```

---

## Licença
Este repositório está licenciado sob a **CC BY-SA 4.0**. Consulte o ficheiro [LICENSE](LICENSE) para mais detalhes.

---

## Autores
- [Associação MILK](https://orcid.org/0000-0000-0000-0000) - Movimentos de Intervenções e Linguagens Kulturais e Arte
- [Eduardo Maurício Vieira Cabral e Araujo](https://orcid.org/0000-0000-0000-0000)

---

## Como Contribuir
1. Faça um *fork* do repositório.
2. Crie uma *branch* para a sua contribuição (`git checkout -b feature/nova-funcionalidade`).
3. Adicione os seus dados ou alterações, garantindo que:
   - Os metadados estejam atualizados em `metadata.json`.
   - Os dados sigam a licença **CC BY-SA 4.0**.
   - Os ficheiros estejam organizados nas pastas corretas.
4. Submeta um *pull request* para a branch `main`.

---

## Integração com Zenodo e ORCID
- **Zenodo**: Cada *release* deste repositório gera automaticamente um **DOI** via [Zenodo GitHub App](https://zenodo.org/integrations/github).
- **ORCID**: Os autores estão vinculados aos seus perfis ORCID para garantir autoria e conformidade com padrões europeus.

---

## Conformidade
- **RGPD**: Todos os dados pessoais estão anonimizados ou com consentimento explícito.
- **AI Act**: Modelos de IA utilizados são *open-source* (ex: Mistral AI).
- **NIS2**: Logs de auditoria imutáveis para metadados críticos.
- **EU Tech Sovereignty**: Infraestrutura alinhada com provedores europeus (PTServidor, Forgejo).

---

## Links Úteis
- [Atlas Vivo MILK](https://github.com/milkivc/atlas-vivo-milk)
- [Documentação do Atlas](https://github.com/milkivc/atlas-docs)
- [Zenodo Community MILK](https://zenodo.org/communities/milk/)
- [ORCID Associação MILK](https://orcid.org/0000-0000-0000-0000)
