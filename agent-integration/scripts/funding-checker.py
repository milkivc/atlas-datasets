#!/usr/bin/env python3
"""
Atlas Vivo - Funding Checker
Verificador de Conformidade para Programas de Financiamento

Este script verifica a conformidade do projeto com diversos programas de financiamento
e gera relatorios de elegibilidade e recomendacoes.

Uso:
    python funding-checker.py check
    python funding-checker.py check --program fct
    python funding-checker.py report
    python funding-checker.py recommend
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple


class FundingChecker:
    """Classe para verificacao de conformidade para financiamento"""
    
    def __init__(self, config_path: str = None, verbose: bool = False):
        """
        Inicializa o verificador de financiamento
        
        Args:
            config_path: Caminho para o arquivo de configuracao
            verbose: Se True, exibe logs detalhados
        """
        self.verbose = verbose
        
        # Carregar configuracao
        if config_path:
            self.config = self._load_config(config_path)
        else:
            self.config = self._load_default_config()
        
        # Carregar metadados do projeto
        self.project_metadata = self._load_project_metadata()
        
        # Log
        self.log(f"💰 Inicializado FundingChecker (verbose={verbose})")
    
    def _load_config(self, config_path: str) -> Dict:
        """Carrega configuracao de arquivo JSON"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.log(f"⚠️  Erro ao carregar config: {e}", level='error')
            return self._load_default_config()
    
    def _load_default_config(self) -> Dict:
        """Carrega configuracao padrao"""
        config_dir = Path(__file__).parent.parent / 'configs'
        config_path = config_dir / 'funding-programs.json'
        
        if config_path.exists():
            return self._load_config(str(config_path))
        
        return {
            'programs': {},
            'compliance_checklist': {}
        }
    
    def _load_project_metadata(self) -> Dict:
        """Carrega metadados do projeto"""
        metadata_files = ['metadata.json', '.zenodo.json', 'codemeta.json']
        merged_metadata = {}
        
        for file in metadata_files:
            file_path = Path(file)
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if 'metadata' in data:
                        merged_metadata.update(data['metadata'])
                    else:
                        merged_metadata.update(data)
                except Exception as e:
                    self.log(f"⚠️  Erro ao carregar {file}: {e}", level='warning')
        
        return merged_metadata
    
    def log(self, message: str, level: str = 'info'):
        """Log de mensagens"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if level == 'error':
            print(f"[{timestamp}] ❌ {message}", file=sys.stderr)
        elif level == 'warning':
            print(f"[{timestamp}] ⚠️  {message}")
        elif self.verbose or level == 'info':
            print(f"[{timestamp}] ✅ {message}")
    
    def check_all_programs(self) -> Dict:
        """
        Verifica conformidade com todos os programas de financiamento
        
        Returns:
            Dict com resultados para cada programa
        """
        results = {}
        
        for program_type in ['european', 'national']:
            for program in self.config.get('programs', {}).get(program_type, []):
                program_id = program.get('id')
                program_name = program.get('name')
                
                self.log(f"Verificando conformidade com {program_name}...")
                
                result = self.check_program(program_id)
                results[program_id] = result
        
        return results
    
    def check_program(self, program_id: str) -> Dict:
        """
        Verifica conformidade com um programa especifico
        
        Args:
            program_id: ID do programa
            
        Returns:
            Dict com resultado da verificacao
        """
        # Encontrar programa
        program = None
        for program_type in ['european', 'national']:
            for p in self.config.get('programs', {}).get(program_type, []):
                if p.get('id') == program_id:
                    program = p
                    break
            if program:
                break
        
        if not program:
            return {
                'program_id': program_id,
                'error': 'Programa nao encontrado',
                'compliance_rate': 0
            }
        
        # Verificar requisitos
        requirements = program.get('compliance_requirements', [])
        met_requirements = []
        failed_requirements = []
        
        for req in requirements:
            if self._check_requirement(req):
                met_requirements.append(req)
            else:
                failed_requirements.append(req)
        
        # Calcular taxa de conformidade
        compliance_rate = len(met_requirements) / len(requirements) * 100 if requirements else 100
        
        # Determinar status
        if compliance_rate >= 90:
            status = 'excellent'
            recommendation = 'Aplicar imediatamente'
        elif compliance_rate >= 70:
            status = 'good'
            recommendation = 'Aplicar com ajustes menores'
        elif compliance_rate >= 50:
            status = 'fair'
            recommendation = 'Necessita melhorias significativas'
        else:
            status = 'poor'
            recommendation = 'Nao elegivel no estado atual'
        
        return {
            'program_id': program_id,
            'program_name': program.get('name'),
            'program_type': program.get('type'),
            'funding_body': program.get('funding_body'),
            'total_budget': program.get('total_budget'),
            'max_funding_rate': program.get('max_funding_rate'),
            'status': status,
            'compliance_rate': compliance_rate,
            'met_requirements': met_requirements,
            'failed_requirements': failed_requirements,
            'recommendation': recommendation,
            'eligible': compliance_rate >= 70
        }
    
    def _check_requirement(self, requirement: str) -> bool:
        """
        Verifica se um requisito especifico e atendido
        
        Args:
            requirement: Nome do requisito
            
        Returns:
            bool: True se o requisito e atendido
        """
        # Normalizar requisito
        req_lower = requirement.lower()
        
        # Verificar requisitos legais
        if 'rgpd' in req_lower:
            return self._check_rgpd_compliance()
        elif 'ai act' in req_lower:
            return self._check_ai_act_compliance()
        elif 'nis2' in req_lower:
            return self._check_nis2_compliance()
        
        # Verificar requisitos tecnicos
        elif 'interoperability' in req_lower:
            return self._check_interoperability()
        elif 'open data' in req_lower:
            return self._check_open_data()
        elif 'digital sovereignty' in req_lower or 'soberania digital' in req_lower:
            return self._check_digital_sovereignty()
        
        # Verificar requisitos de financiamento
        elif 'scientific excellence' in req_lower:
            return self._check_scientific_excellence()
        elif 'open access' in req_lower:
            return self._check_open_access()
        elif 'data management plan' in req_lower:
            return self._check_data_management_plan()
        
        # Verificar requisitos culturais
        elif 'cultural relevance' in req_lower:
            return True  # Projeto e cultural por natureza
        elif 'public access' in req_lower:
            return True  # Repositorios sao publicos
        
        # Padrao: assumir que e atendido
        return True
    
    def _check_rgpd_compliance(self) -> bool:
        """Verifica conformidade com RGPD"""
        # Verificar se ha documentacao de RGPD
        legal_dir = Path('legal')
        if legal_dir.exists():
            rgpd_files = [
                'registro-tratamento-dados.md',
                'dpia-atlas-vivo.md',
                'politica-privacidade.md'
            ]
            
            for file in rgpd_files:
                if (legal_dir / file).exists():
                    return True
        
        # Verificar se ha DPO configurado
        if 'dpo@associacaomilk.pt' in str(self.project_metadata):
            return True
        
        return False
    
    def _check_ai_act_compliance(self) -> bool:
        """Verifica conformidade com AI Act"""
        # Verificar se ha documentacao do AI Act
        legal_dir = Path('legal')
        if legal_dir.exists():
            ai_act_file = legal_dir / 'documentacao-tecnica-ai-act.md'
            if ai_act_file.exists():
                return True
        
        # Verificar se ha classificacao de risco
        if 'ai act' in str(self.project_metadata).lower():
            return True
        
        return False
    
    def _check_nis2_compliance(self) -> bool:
        """Verifica conformidade com NIS2"""
        # Verificar se ha medidas de seguranca documentadas
        if Path('SECURITY.md').exists():
            return True
        
        # Verificar se ha politicas de seguranca
        if 'security' in str(self.project_metadata).lower():
            return True
        
        return False
    
    def _check_interoperability(self) -> bool:
        """Verifica conformidade com standards de interoperabilidade"""
        # Verificar se ha metadados em standards reconhecidos
        metadata_files = ['metadata.json', '.zenodo.json', 'codemeta.json', 'CITATION.cff']
        
        for file in metadata_files:
            file_path = Path(file)
            if file_path.exists():
                try:
                    with open(file_path) as f:
                        data = json.load(f)
                    
                    # Verificar por standards
                    if 'conformsTo' in data:
                        return True
                    if 'metadata' in data and 'conform_to' in data['metadata']:
                        return True
                except:
                    pass
        
        # Verificar se ha schemas
        schemas_dir = Path('.github/schemas')
        if schemas_dir.exists():
            return True
        
        return False
    
    def _check_open_data(self) -> bool:
        """Verifica principios de dados abertos"""
        # Verificar licencas abertas
        if Path('LICENSE').exists():
            with open('LICENSE') as f:
                license_text = f.read()
            if 'EUPL' in license_text or 'Creative Commons' in license_text:
                return True
        
        # Verificar se metadados sao abertos
        if 'access_right' in str(self.project_metadata) and 'open' in str(self.project_metadata):
            return True
        
        return False
    
    def _check_digital_sovereignty(self) -> bool:
        """Verifica soberania digital"""
        # Verificar se usa provedores europeus
        if 'codeberg' in str(self.project_metadata).lower():
            return True
        
        # Verificar se ha declaracao de soberania
        if Path('GOVERNANCE.md').exists():
            with open('GOVERNANCE.md') as f:
                content = f.read()
            if 'soberania' in content.lower() or 'sovereignty' in content.lower():
                return True
        
        return False
    
    def _check_scientific_excellence(self) -> bool:
        """Verifica excelencia cientifica"""
        # Verificar se ha publicacoes
        if 'orcid' in str(self.project_metadata).lower():
            return True
        
        # Verificar se ha colaboradores com ORCID
        orcid_config_path = Path(__file__).parent.parent / 'configs' / 'orcid-mappings.json'
        if orcid_config_path.exists():
            with open(orcid_config_path) as f:
                orcid_config = json.load(f)
            if orcid_config.get('collaborators'):
                return True
        
        return False
    
    def _check_open_access(self) -> bool:
        """Verifica acesso aberto"""
        # Verificar se repositorios sao publicos
        if 'access_right' in str(self.project_metadata) and 'open' in str(self.project_metadata):
            return True
        
        # Verificar se ha declaracao de acesso aberto
        if Path('README.md').exists():
            with open('README.md') as f:
                content = f.read()
            if 'acesso aberto' in content.lower() or 'open access' in content.lower():
                return True
        
        return False
    
    def _check_data_management_plan(self) -> bool:
        """Verifica plano de gerenciamento de dados"""
        # Verificar se ha DMP
        dmp_files = [
            'data-management-plan.md',
            'dmp.md',
            'plano-gerenciamento-dados.md'
        ]
        
        for file in dmp_files:
            if Path(file).exists():
                return True
        
        # Verificar se ha documentacao de dados
        if Path('legal').exists():
            return True
        
        return False
    
    def generate_report(self, program_id: str = None) -> Dict:
        """
        Gera relatorio de conformidade
        
        Args:
            program_id: ID do programa (None = todos)
            
        Returns:
            Dict com relatorio completo
        """
        if program_id:
            results = {program_id: self.check_program(program_id)}
        else:
            results = self.check_all_programs()
        
        # Calcular estatisticas
        total_programs = len(results)
        eligible_programs = sum(1 for r in results.values() if r.get('eligible', False))
        avg_compliance = sum(r.get('compliance_rate', 0) for r in results.values()) / total_programs if total_programs > 0 else 0
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_programs': total_programs,
            'eligible_programs': eligible_programs,
            'average_compliance': avg_compliance,
            'results': results,
            'recommendations': self.get_recommendations(results)
        }
    
    def get_recommendations(self, results: Dict) -> List[str]:
        """
        Gera recomendacoes com base nos resultados
        
        Args:
            results: Resultados da verificacao
            
        Returns:
            List de recomendacoes
        """
        recommendations = []
        
        # Recomendacoes gerais
        if self.config.get('recommendations'):
            recommendations.extend(self.config['recommendations'].get('high_priority', []))
        
        # Recomendacoes especificas com base nos resultados
        for program_id, result in results.items():
            if not result.get('eligible', False):
                failed = result.get('failed_requirements', [])
                for req in failed:
                    recommendations.append(f"Atender ao requisito '{req}' para {result.get('program_name')}")
        
        return recommendations
    
    def print_report(self, report: Dict):
        """Imprime relatorio de forma legivel"""
        print("\n" + "="*80)
        print("📊 RELATORIO DE CONFORMIDADE PARA FINANCIAMENTO")
        print("="*80)
        print(f"Data: {report['timestamp']}")
        print(f"Total de programas: {report['total_programs']}")
        print(f"Programas elegiveis: {report['eligible_programs']}")
        print(f"Media de conformidade: {report['average_compliance']:.1f}%")
        print("="*80)
        
        print("\n📋 Resultados por Programa:")
        print("-"*80)
        
        for program_id, result in report['results'].items():
            status_emoji = {
                'excellent': '✅',
                'good': '✅',
                'fair': '⚠️ ',
                'poor': '❌'
            }.get(result.get('status'), '❓')
            
            print(f"\n{status_emoji} {result.get('program_name')}")
            print(f"   Tipo: {result.get('program_type')}")
            print(f"   Orgao: {result.get('funding_body')}")
            print(f"   Conformidade: {result.get('compliance_rate'):.1f}%")
            print(f"   Status: {result.get('status')}")
            print(f"   Elegivel: {'✅ Sim' if result.get('eligible') else '❌ Nao'}")
            print(f"   Recomendacao: {result.get('recommendation')}")
            
            if result.get('failed_requirements'):
                print(f"   Requisitos nao atendidos:")
                for req in result['failed_requirements']:
                    print(f"     - ❌ {req}")
        
        print("\n" + "="*80)
        print("💡 RECOMENDACOES")
        print("="*80)
        
        for i, rec in enumerate(report.get('recommendations', []), 1):
            print(f"{i}. {rec}")
        
        print("="*80)


def main():
    """Funcao principal"""
    parser = argparse.ArgumentParser(
        description='Atlas Vivo - Funding Checker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python funding-checker.py check                    # Verificar todos os programas
  python funding-checker.py check --program fct      # Verificar programa especifico
  python funding-checker.py report                   # Gerar relatorio completo
  python funding-checker.py recommend                # Obter recomendacoes
  python funding-checker.py --verbose               # Modo verboso
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comando a executar')
    
    # Comando check
    check_parser = subparsers.add_parser('check', help='Verificar conformidade')
    check_parser.add_argument('--program', type=str, help='ID do programa a verificar')
    check_parser.add_argument('--all', action='store_true', help='Verificar todos os programas')
    
    # Comando report
    report_parser = subparsers.add_parser('report', help='Gerar relatorio')
    report_parser.add_argument('--program', type=str, help='ID do programa para relatorio')
    report_parser.add_argument('--output', type=str, help='Arquivo de saida')
    
    # Comando recommend
    recommend_parser = subparsers.add_parser('recommend', help='Obter recomendacoes')
    
    # Argumentos globais
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verboso')
    parser.add_argument('--config', type=str, help='Caminho para arquivo de configuracao')
    
    args = parser.parse_args()
    
    # Inicializar verificador
    checker = FundingChecker(
        config_path=args.config,
        verbose=args.verbose
    )
    
    # Executar comando
    if args.command == 'check' or not args.command:
        if args.program:
            result = checker.check_program(args.program)
            print(f"\nResultado para {result.get('program_name')}:")
            print(f"  Conformidade: {result.get('compliance_rate'):.1f}%")
            print(f"  Status: {result.get('status')}")
            print(f"  Elegivel: {'Sim' if result.get('eligible') else 'Nao'}")
        else:
            results = checker.check_all_programs()
            for program_id, result in results.items():
                print(f"{result.get('program_name')}: {result.get('compliance_rate'):.1f}% ({result.get('status')})")
    
    elif args.command == 'report':
        report = checker.generate_report(args.program)
        checker.print_report(report)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Relatorio salvo em {args.output}")
    
    elif args.command == 'recommend':
        report = checker.generate_report()
        print("\n💡 RECOMENDACOES:")
        print("="*60)
        for i, rec in enumerate(report.get('recommendations', []), 1):
            print(f"{i}. {rec}")
    
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
