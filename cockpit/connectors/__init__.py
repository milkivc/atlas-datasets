# Conectores para APIs - Associação MILK
# Versão: 1.0.0
# Licença: EUPL-1.2

"""
Pacote de conectores para integração com APIs externas.

Este pacote fornece classes para interagir com:
- GitHub API
- Codeberg API (Forgejo)
- DataCite API
- ORCID API
- ROR API
- OpenAIRE API
- INSPIRE API
"""

from .github_connector import GitHubConnector
from .codeberg_connector import CodebergConnector
from .datacite_connector import DataCiteConnector
from .orcid_connector import ORCIDConnector
from .ror_connector import RORConnector
from .openaire_connector import OpenAIREConnector
from .inspire_connector import INSPIREConnector

__all__ = [
    'GitHubConnector',
    'CodebergConnector',
    'DataCiteConnector',
    'ORCIDConnector',
    'RORConnector',
    'OpenAIREConnector',
    'INSPIREConnector'
]

__version__ = "1.0.0"
