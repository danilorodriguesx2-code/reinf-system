# xml_parser.py
import pandas as pd
import xml.etree.ElementTree as ET


def parse_xml_4020(xml_content):
    """Parser para evento 4020 - Estrutura do seu XML"""
    try:
        namespaces = {
            'ns': 'http://www.reinf.esocial.gov.br/schemas/evt4020PagtoBeneficiarioPJ/v2_01_02',
            'reinf': 'http://www.reinf.esocial.gov.br/schemas/envioLoteEventosAssincrono/v1_00_00'
        }

        root = ET.fromstring(xml_content)
        records = []

        # Buscar eventos dentro da estrutura do lote
        eventos = root.findall('.//reinf:evento', namespaces)
        print(f"Encontrados {len(eventos)} eventos no lote")

        for evento in eventos:
            # Dentro de cada evento, buscar o evtRetPJ
            evt_ret_pj = evento.find('.//ns:evtRetPJ', namespaces)
            if evt_ret_pj is None:
                continue

            # Dados do evento
            ide_evento = evt_ret_pj.find('ns:ideEvento', namespaces)
            per_apur = ide_evento.find(
                'ns:perApur', namespaces).text if ide_evento is not None else "N/A"

            # Dados do contribuinte
            ide_contri = evt_ret_pj.find('ns:ideContri', namespaces)
            nr_insc_contri = ide_contri.find(
                'ns:nrInsc', namespaces).text if ide_contri is not None else "N/A"

            # Dados do estabelecimento
            ide_estab = evt_ret_pj.find('ns:ideEstab', namespaces)
            if ide_estab is not None:
                tp_insc_estab = ide_estab.find(
                    'ns:tpInscEstab', namespaces).text
                nr_insc_estab = ide_estab.find(
                    'ns:nrInscEstab', namespaces).text
            else:
                continue

            # Para cada beneficiário
            for ide_benef in ide_estab.findall('ns:ideBenef', namespaces):
                cnpj_benef = ide_benef.find('ns:cnpjBenef', namespaces).text

                # Para cada grupo de pagamento
                for ide_pgto in ide_benef.findall('ns:idePgto', namespaces):
                    nat_rend = ide_pgto.find('ns:natRend', namespaces).text

                    # Para cada informação de pagamento
                    for info_pgto in ide_pgto.findall('ns:infoPgto', namespaces):
                        dt_fg = info_pgto.find('ns:dtFG', namespaces).text
                        vlr_bruto = float(info_pgto.find(
                            'ns:vlrBruto', namespaces).text.replace(',', '.'))

                        observ = info_pgto.find('ns:observ', namespaces)
                        observ_text = observ.text if observ is not None and observ.text else ""

                        # Inicializar valores
                        base_ir = valor_ir = base_csll = valor_csll = base_cofins = valor_cofins = base_pp = valor_pp = 0.0

                        # Buscar retenções
                        retencoes = info_pgto.find('ns:retencoes', namespaces)
                        if retencoes is not None:
                            # IR
                            vlr_base_ir = retencoes.find(
                                'ns:vlrBaseIR', namespaces)
                            if vlr_base_ir is not None and vlr_base_ir.text:
                                base_ir = float(
                                    vlr_base_ir.text.replace(',', '.'))

                            vlr_ir = retencoes.find('ns:vlrIR', namespaces)
                            if vlr_ir is not None and vlr_ir.text:
                                valor_ir = float(vlr_ir.text.replace(',', '.'))

                            # CSLL
                            vlr_base_csll = retencoes.find(
                                'ns:vlrBaseCSLL', namespaces)
                            if vlr_base_csll is not None and vlr_base_csll.text:
                                base_csll = float(
                                    vlr_base_csll.text.replace(',', '.'))

                            vlr_csll = retencoes.find('ns:vlrCSLL', namespaces)
                            if vlr_csll is not None and vlr_csll.text:
                                valor_csll = float(
                                    vlr_csll.text.replace(',', '.'))

                            # COFINS
                            vlr_base_cofins = retencoes.find(
                                'ns:vlrBaseCofins', namespaces)
                            if vlr_base_cofins is not None and vlr_base_cofins.text:
                                base_cofins = float(
                                    vlr_base_cofins.text.replace(',', '.'))

                            vlr_cofins = retencoes.find(
                                'ns:vlrCofins', namespaces)
                            if vlr_cofins is not None and vlr_cofins.text:
                                valor_cofins = float(
                                    vlr_cofins.text.replace(',', '.'))

                            # PP
                            vlr_base_pp = retencoes.find(
                                'ns:vlrBasePP', namespaces)
                            if vlr_base_pp is not None and vlr_base_pp.text:
                                base_pp = float(
                                    vlr_base_pp.text.replace(',', '.'))

                            vlr_pp = retencoes.find('ns:vlrPP', namespaces)
                            if vlr_pp is not None and vlr_pp.text:
                                valor_pp = float(vlr_pp.text.replace(',', '.'))

                        record = {
                            'CNPJ_Empresa': nr_insc_contri,
                            'CNPJ_Beneficiario': cnpj_benef,
                            'Tipo_Inscricao_Estab': tp_insc_estab,
                            'Numero_Inscricao_Estab': nr_insc_estab,
                            'Natureza_Rendimento': nat_rend,
                            'Data_Pagamento': dt_fg,
                            'Valor_Bruto': vlr_bruto,
                            'Observacao': observ_text,
                            'Base_CSLL': base_csll,
                            'Valor_CSLL': valor_csll,
                            'Base_COFINS': base_cofins,
                            'Valor_COFINS': valor_cofins,
                            'Base_PP': base_pp,
                            'Valor_PP': valor_pp,
                            'Base_IR': base_ir,
                            'Valor_IR': valor_ir
                        }
                        records.append(record)

        print(f"Total de registros processados: {len(records)}")
        return records

    except Exception as e:
        print(f"Erro no parsing do XML 4020: {e}")
        import traceback
        print(f"Detalhes do erro: {traceback.format_exc()}")
        return []


def parse_xml_2055(xml_content):
    """Parser para evento 2055 - Aquisição de Produto Rural"""
    namespaces = {
        'ns': 'http://www.reinf.esocial.gov.br/schemas/evt2055AquisicaoProdRural/v2_01_02'
    }

    root = ET.fromstring(xml_content)
    records = []

    for evento in root.findall('.//ns:evtAqProd', namespaces):
        ide_estab = evento.find('.//ns:ideEstabAdquir', namespaces)
        nr_insc_adq = ide_estab.find('ns:nrInscAdq', namespaces).text

        ide_evento = evento.find('ns:ideEvento', namespaces)
        per_apur = ide_evento.find('ns:perApur', namespaces).text

        for produtor in ide_estab.findall('ns:ideProdutor', namespaces):
            # CORREÇÃO: Buscar o indOpcCP no local correto - dentro de ideProdutor, não detAquis
            ind_opc_cp = produtor.find('ns:indOpcCP', namespaces)
            ind_opc_cp_text = ind_opc_cp.text if ind_opc_cp is not None else "N"

            for det_aquis in produtor.findall('ns:detAquis', namespaces):
                record = {
                    'Período Apuração': per_apur,
                    'Filial': nr_insc_adq,
                    'Indicador Aquisição': det_aquis.find('ns:indAquis', namespaces).text,
                    'Indicador Operação': ind_opc_cp_text,  # Agora usando o valor correto
                    'Valor Bruto': float(det_aquis.find('ns:vlrBruto', namespaces).text.replace(',', '.')),
                    'Funrural': float(det_aquis.find('ns:vlrCPDescPR', namespaces).text.replace(',', '.')),
                    'Gilrat': float(det_aquis.find('ns:vlrRatDescPR', namespaces).text.replace(',', '.')),
                    'Senar': float(det_aquis.find('ns:vlrSenarDesc', namespaces).text.replace(',', '.'))
                }

                # Calcular percentuais
                if record['Valor Bruto'] > 0:
                    record['% Funrural'] = (
                        record['Funrural'] / record['Valor Bruto']) * 100
                    record['% Gilrat'] = (
                        record['Gilrat'] / record['Valor Bruto']) * 100
                    record['% Senar'] = (
                        record['Senar'] / record['Valor Bruto']) * 100
                else:
                    record['% Funrural'] = 0
                    record['% Gilrat'] = 0
                    record['% Senar'] = 0

                records.append(record)

    return pd.DataFrame(records)


def parse_xml_2010(xml_content):
    """Parser para evento 2010 - Tomador de Serviços"""
    try:
        namespaces = {
            'ns': 'http://www.reinf.esocial.gov.br/schemas/evtTomadorServicos/v2_01_02',
            'reinf': 'http://www.reinf.esocial.gov.br/schemas/envioLoteEventosAssincrono/v1_00_00'
        }

        root = ET.fromstring(xml_content)
        records = []

        # Buscar eventos dentro da estrutura do lote
        eventos = root.findall('.//reinf:evento', namespaces)
        print(f"Encontrados {len(eventos)} eventos 2010 no lote")

        for evento in eventos:
            # Dentro de cada evento, buscar o evtServTom
            evt_serv_tom = evento.find('.//ns:evtServTom', namespaces)
            if evt_serv_tom is None:
                continue

            # Dados do evento
            ide_evento = evt_serv_tom.find('ns:ideEvento', namespaces)
            per_apur = ide_evento.find(
                'ns:perApur', namespaces).text if ide_evento is not None else "N/A"

            # Para cada estabelecimento
            for ide_estab in evt_serv_tom.findall('.//ns:ideEstabObra', namespaces):
                nr_insc_estab = ide_estab.find(
                    'ns:nrInscEstab', namespaces).text

                # Para cada prestador de serviço
                for ide_prest in ide_estab.findall('ns:idePrestServ', namespaces):
                    cnpj_prestador = ide_prest.find(
                        'ns:cnpjPrestador', namespaces).text
                    vlr_total_bruto = float(ide_prest.find(
                        'ns:vlrTotalBruto', namespaces).text.replace(',', '.'))
                    vlr_total_base_ret = float(ide_prest.find(
                        'ns:vlrTotalBaseRet', namespaces).text.replace(',', '.'))
                    vlr_total_ret_princ = float(ide_prest.find(
                        'ns:vlrTotalRetPrinc', namespaces).text.replace(',', '.'))

                    # Para cada NFS
                    for nfs in ide_prest.findall('ns:nfs', namespaces):
                        num_docto = nfs.find('ns:numDocto', namespaces).text
                        dt_emissao_nf = nfs.find(
                            'ns:dtEmissaoNF', namespaces).text

                        # Para cada tipo de serviço
                        for info_tp_serv in nfs.findall('ns:infoTpServ', namespaces):
                            tp_servico = info_tp_serv.find(
                                'ns:tpServico', namespaces).text

                            record = {
                                'Filial': nr_insc_estab,
                                'Periodo': per_apur,
                                'Prestador': cnpj_prestador,
                                'Servico': tp_servico,
                                'Documento': num_docto,
                                'Valor_Bruto': vlr_total_bruto,
                                'Base_Retencao': vlr_total_base_ret,
                                'Valor_INSS': vlr_total_ret_princ,
                                'Emissao': dt_emissao_nf
                            }
                            records.append(record)

        print(f"Total de registros processados (2010): {len(records)}")
        return records

    except Exception as e:
        print(f"Erro no parsing do XML 2010: {e}")
        import traceback
        print(f"Detalhes do erro: {traceback.format_exc()}")
        return []


def validate_2055_records(df):
    """
    Valida registros do evento 2055 com as regras específicas:
    - Quando indicador_aquisicao = 4 OU indicador_operacao = "S": Funrural e Gilrat devem ser 0
    - Quando indicador_aquisicao = 1: Funrural e Gilrat devem ser > 0
    """
    errors = []

    for index, row in df.iterrows():
        error_messages = []

        Filial = row['Filial']
        Período_Apuração = row['Período Apuração']
        indicador_aquisicao = row['Indicador Aquisição']
        indicador_operacao = row['Indicador Operação']
        valor_bruto = row['Valor Bruto']
        funrural = row['Funrural']
        gilrat = row['Gilrat']
        senar = row['Senar']

        # REGRA 1: Quando indicador_aquisicao = 4 OU indicador_operacao = "S"
        if indicador_aquisicao == 4 or indicador_operacao == "S":
            # Funrural e Gilrat devem ser 0
            if funrural != 0:
                error_messages.append(
                    f"Funrural deve ser 0 (encontrado: R$ {funrural:.2f})")
            if gilrat != 0:
                error_messages.append(
                    f"Gilrat deve ser 0 (encontrado: R$ {gilrat:.2f})")

        # REGRA 2: Quando indicador_aquisicao = 1
        elif indicador_aquisicao == 1:
            # Funrural e Gilrat devem ser > 0
            if funrural <= 0:
                error_messages.append("Funrural deve ser maior que 0")
            if gilrat <= 0:
                error_messages.append("Gilrat deve ser maior que 0")

        # Se encontrou erros, adicionar à lista de erros
        if error_messages:
            errors.append({
                'Filial': row.get('Filial', 'N/A'),
                'Período': row.get('Período Apuração', 'N/A'),
                'Indicador Aquisição': indicador_aquisicao,
                'Indicador Operação': indicador_operacao,
                'Valor Bruto': valor_bruto,
                'Funrural': funrural,
                'Gilrat': gilrat,
                'Senar': senar,
                'Erro': ' | '.join(error_messages)
            })

    return errors
