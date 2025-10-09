# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

# Importações
from report_generator import ReportGenerator
from xml_parser import parse_xml_4020, parse_xml_2055, validate_2055_records, parse_xml_2010


def main():
    st.set_page_config(
        page_title="Sistema REINF - Análise de Eventos",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Sistema de Análise REINF")
    st.markdown("---")

    # Criar abas para os diferentes eventos
    tab1, tab2, tab3 = st.tabs(["🗂️ Evento 4020 - Pagamentos",
                               "🌾 Evento 2055 - Aquisição Produto Rural",
                                "🏗️ Evento 2010 - Tomador de Serviços"])

    with tab1:
        st.header("Análise do Evento 4020 - Pagamentos")

        uploaded_file_4020 = st.file_uploader(
            "Carregue o arquivo XML do evento 4020",
            type=['xml'],
            key='4020_upload'
        )

        if uploaded_file_4020:
            try:
                xml_content = uploaded_file_4020.read().decode('utf-8')
                data_4020 = parse_xml_4020(xml_content)

                if data_4020:
                    st.success(
                        f"✅ Arquivo 4020 processado com sucesso! {len(data_4020)} registros encontrados.")

                    # Exibir dados
                    report_gen = ReportGenerator()
                    df_4020 = pd.DataFrame(data_4020)

                    # =============================================
                    # TOTALIZADOR - Evento 4020 (PADRÃO)
                    # =============================================
                    st.subheader("💰 Totalizador - Evento 4020")

                    # Métricas gerais - PADRÃO
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.metric("Total Bruto",
                                  f"R$ {df_4020['Valor_Bruto'].sum():,.2f}")
                    with col2:
                        st.metric("Total CSLL",
                                  f"R$ {df_4020['Valor_CSLL'].sum():,.2f}")
                    with col3:
                        st.metric("Total COFINS",
                                  f"R$ {df_4020['Valor_COFINS'].sum():,.2f}")
                    with col4:
                        st.metric(
                            "Total PP", f"R$ {df_4020['Valor_PP'].sum():,.2f}")
                    with col5:
                        st.metric(
                            "Total IR", f"R$ {df_4020['Valor_IR'].sum():,.2f}")

                    # =============================================
                    # PRIMEIRA TABELA: Dados principais com percentuais
                    # =============================================
                    st.subheader("📋 Dados do Evento 4020 com Percentuais")

                    # Calcular percentuais
                    df_4020['% CSLL'] = (
                        df_4020['Valor_CSLL'] / df_4020['Base_CSLL'].replace(0, pd.NA)) * 100
                    df_4020['% COFINS'] = (
                        df_4020['Valor_COFINS'] / df_4020['Base_COFINS'].replace(0, pd.NA)) * 100
                    df_4020['% PP'] = (
                        df_4020['Valor_PP'] / df_4020['Base_PP'].replace(0, pd.NA)) * 100
                    df_4020['% IR'] = (
                        df_4020['Valor_IR'] / df_4020['Base_IR'].replace(0, pd.NA)) * 100

                    # Preencher NaN com 0 onde a base era zero
                    df_4020[['% CSLL', '% COFINS', '% PP', '% IR']] = df_4020[[
                        '% CSLL', '% COFINS', '% PP', '% IR']].fillna(0)

                    # Colunas para exibição
                    display_cols_4020 = [
                        'CNPJ_Empresa', 'CNPJ_Beneficiario', 'Tipo_Inscricao_Estab', 'Numero_Inscricao_Estab',
                        'Natureza_Rendimento', 'Data_Pagamento', 'Valor_Bruto', 'Observacao',
                        'Base_CSLL', 'Valor_CSLL', '% CSLL',
                        'Base_COFINS', 'Valor_COFINS', '% COFINS',
                        'Base_PP', 'Valor_PP', '% PP',
                        'Base_IR', 'Valor_IR', '% IR'
                    ]

                    st.dataframe(
                        df_4020[display_cols_4020].style.format({
                            'Valor_Bruto': 'R$ {:,.2f}',
                            'Base_CSLL': 'R$ {:,.2f}',
                            'Valor_CSLL': 'R$ {:,.2f}',
                            '% CSLL': '{:.2f}%',
                            'Base_COFINS': 'R$ {:,.2f}',
                            'Valor_COFINS': 'R$ {:,.2f}',
                            '% COFINS': '{:.2f}%',
                            'Base_PP': 'R$ {:,.2f}',
                            'Valor_PP': 'R$ {:,.2f}',
                            '% PP': '{:.2f}%',
                            'Base_IR': 'R$ {:,.2f}',
                            'Valor_IR': 'R$ {:,.2f}',
                            '% IR': '{:.2f}%'
                        }),
                        use_container_width=True
                    )

                    # =============================================
                    # SEGUNDA TABELA: Agrupada por filial com totalizadores
                    # =============================================
                    st.subheader("🏢 Resumo por Filial - Evento 4020")

                    # Agrupar por filial
                    grouped_4020 = df_4020.groupby('Numero_Inscricao_Estab')

                    # Lista para armazenar todas as linhas do relatório
                    all_rows_4020 = []

                    for filial, group in grouped_4020:
                        # Adicionar registros da filial
                        for _, row in group.iterrows():
                            all_rows_4020.append({
                                'Filial': filial,
                                'CNPJ Beneficiário': row['CNPJ_Beneficiario'],
                                'Natureza Rendimento': row['Natureza_Rendimento'],
                                'Data Pagamento': row['Data_Pagamento'],
                                'Valor Bruto': row['Valor_Bruto'],
                                'Valor CSLL': row['Valor_CSLL'],
                                'Valor COFINS': row['Valor_COFINS'],
                                'Valor PP': row['Valor_PP'],
                                'Valor IR': row['Valor_IR']
                            })

                        # Adicionar total da filial
                        total_filial = {
                            'Filial': '',
                            'CNPJ Beneficiário': '**TOTAL FILIAL**',
                            'Natureza Rendimento': '',
                            'Data Pagamento': '',
                            'Valor Bruto': group['Valor_Bruto'].sum(),
                            'Valor CSLL': group['Valor_CSLL'].sum(),
                            'Valor COFINS': group['Valor_COFINS'].sum(),
                            'Valor PP': group['Valor_PP'].sum(),
                            'Valor IR': group['Valor_IR'].sum()
                        }
                        all_rows_4020.append(total_filial)

                        # Adicionar linha em branco
                        all_rows_4020.append({
                            'Filial': '',
                            'CNPJ Beneficiário': '',
                            'Natureza Rendimento': '',
                            'Data Pagamento': '',
                            'Valor Bruto': None,
                            'Valor CSLL': None,
                            'Valor COFINS': None,
                            'Valor PP': None,
                            'Valor IR': None
                        })

                    # Remover última linha em branco
                    if all_rows_4020 and all_rows_4020[-1]['Filial'] == '':
                        all_rows_4020.pop()

                    df_resumo_4020 = pd.DataFrame(all_rows_4020)
                    st.dataframe(
                        df_resumo_4020.style.format({
                            'Valor Bruto': 'R$ {:,.2f}',
                            'Valor CSLL': 'R$ {:,.2f}',
                            'Valor COFINS': 'R$ {:,.2f}',
                            'Valor PP': 'R$ {:,.2f}',
                            'Valor IR': 'R$ {:,.2f}'
                        }),
                        use_container_width=True
                    )

                    # =============================================
                    # TERCEIRA TABELA: Consolidação de impostos
                    # =============================================
                    st.subheader("📊 Consolidação de Impostos - Evento 4020")

                    totais_impostos = pd.DataFrame({
                        'Imposto': ['CSLL', 'COFINS', 'PP', 'IRRF'],
                        'Total Recolhido': [
                            df_4020['Valor_CSLL'].sum(),
                            df_4020['Valor_COFINS'].sum(),
                            df_4020['Valor_PP'].sum(),
                            df_4020['Valor_IR'].sum()
                        ]
                    })

                    st.dataframe(
                        totais_impostos.style.format({
                            'Total Recolhido': 'R$ {:,.2f}'
                        }),
                        use_container_width=True
                    )

                    # Botão para gerar relatório Excel
                    if st.button("📊 Gerar Relatório Excel 4020", key="btn_4020"):
                        excel_file = report_gen.generate_excel_report_4020(
                            data_4020)
                        st.success(f"Relatório gerado: {excel_file}")

                else:
                    st.warning("Nenhum dado encontrado no arquivo.")

            except Exception as e:
                st.error(f"❌ Erro ao processar arquivo 4020: {str(e)}")

    with tab2:
        st.header("Análise do Evento 2055 - Aquisição de Produto Rural")

        uploaded_files_2055 = st.file_uploader(
            "Carregue os arquivos XML do evento 2055 (múltiplos arquivos - um por filial)",
            type=['xml'],
            accept_multiple_files=True,
            key='2055_upload'
        )

        if uploaded_files_2055:
            all_data = []

            for uploaded_file in uploaded_files_2055:
                try:
                    xml_content = uploaded_file.read().decode('utf-8')
                    df_temp = parse_xml_2055(xml_content)

                    if not df_temp.empty:
                        all_data.append(df_temp)
                        st.success(
                            f"✅ {uploaded_file.name} processado com sucesso! {len(df_temp)} registros.")
                    else:
                        st.warning(
                            f"⚠️ {uploaded_file.name} processado, mas nenhum dado encontrado.")

                except Exception as e:
                    st.error(
                        f"❌ Erro ao processar {uploaded_file.name}: {str(e)}")

            if all_data:
                df_2055 = pd.concat(all_data, ignore_index=True)
                report_gen = ReportGenerator()

                # =============================================
                # TOTALIZADOR - Evento 2055 (PADRÃO)
                # =============================================
                st.subheader("💰 Totalizador - Evento 2055")

                # Métricas gerais - PADRÃO
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Bruto",
                              f"R$ {df_2055['Valor Bruto'].sum():,.2f}")
                with col2:
                    st.metric("Total Funrural",
                              f"R$ {df_2055['Funrural'].sum():,.2f}")
                with col3:
                    st.metric("Total Gilrat",
                              f"R$ {df_2055['Gilrat'].sum():,.2f}")
                with col4:
                    st.metric("Total Senar",
                              f"R$ {df_2055['Senar'].sum():,.2f}")

                # =============================================
                # PRIMEIRA TABELA: Dados principais
                # =============================================
                st.subheader("📋 Dados do Evento 2055")

                display_cols_2055 = [
                    'Filial', 'Período Apuração', 'Indicador Aquisição', 'Indicador Operação',
                    'Valor Bruto', 'Funrural', '% Funrural', 'Gilrat', '% Gilrat', 'Senar', '% Senar'
                ]

                st.dataframe(
                    df_2055[display_cols_2055].style.format({
                        'Valor Bruto': 'R$ {:,.2f}',
                        'Funrural': 'R$ {:,.2f}',
                        '% Funrural': '{:.2f}%',
                        'Gilrat': 'R$ {:,.2f}',
                        '% Gilrat': '{:.2f}%',
                        'Senar': 'R$ {:,.2f}',
                        '% Senar': '{:.2f}%'
                    }),
                    use_container_width=True
                )

                # =============================================
                # SEGUNDA TABELA: Agrupada por filial com totalizadores
                # =============================================
                st.subheader("🏢 Resumo por Filial - Evento 2055")

                # Agrupar por filial
                grouped_2055 = df_2055.groupby('Filial')

                # Lista para armazenar todas as linhas
                all_rows_2055 = []

                for filial, group in grouped_2055:
                    # Adicionar registros da filial
                    for _, row in group.iterrows():
                        all_rows_2055.append({
                            'Filial': filial,
                            'Período Apuração': row['Período Apuração'],
                            'Indicador Aquisição': row['Indicador Aquisição'],
                            'Indicador Operação': row['Indicador Operação'],
                            'Valor Bruto': row['Valor Bruto'],
                            'Funrural': row['Funrural'],
                            '% Funrural': row['% Funrural'],
                            'Gilrat': row['Gilrat'],
                            '% Gilrat': row['% Gilrat'],
                            'Senar': row['Senar'],
                            '% Senar': row['% Senar']
                        })

                    # Adicionar total da filial
                    total_filial = {
                        'Filial': '',
                        'Período Apuração': '**TOTAL FILIAL**',
                        'Indicador Aquisição': '',
                        'Indicador Operação': '',
                        'Valor Bruto': group['Valor Bruto'].sum(),
                        'Funrural': group['Funrural'].sum(),
                        '% Funrural': (group['Funrural'].sum() / group['Valor Bruto'].sum()) * 100 if group['Valor Bruto'].sum() > 0 else 0,
                        'Gilrat': group['Gilrat'].sum(),
                        '% Gilrat': (group['Gilrat'].sum() / group['Valor Bruto'].sum()) * 100 if group['Valor Bruto'].sum() > 0 else 0,
                        'Senar': group['Senar'].sum(),
                        '% Senar': (group['Senar'].sum() / group['Valor Bruto'].sum()) * 100 if group['Valor Bruto'].sum() > 0 else 0
                    }
                    all_rows_2055.append(total_filial)

                    # Adicionar linha em branco
                    all_rows_2055.append({
                        'Filial': '',
                        'Período Apuração': '',
                        'Indicador Aquisição': '',
                        'Indicador Operação': '',
                        'Valor Bruto': None,
                        'Funrural': None,
                        '% Funrural': None,
                        'Gilrat': None,
                        '% Gilrat': None,
                        'Senar': None,
                        '% Senar': None
                    })

                # Remover última linha em branco
                if all_rows_2055 and all_rows_2055[-1]['Filial'] == '':
                    all_rows_2055.pop()

                df_resumo_2055 = pd.DataFrame(all_rows_2055)
                st.dataframe(
                    df_resumo_2055.style.format({
                        'Valor Bruto': 'R$ {:,.2f}',
                        'Funrural': 'R$ {:,.2f}',
                        '% Funrural': '{:.2f}%',
                        'Gilrat': 'R$ {:,.2f}',
                        '% Gilrat': '{:.2f}%',
                        'Senar': 'R$ {:,.2f}',
                        '% Senar': '{:.2f}%'
                    }),
                    use_container_width=True
                )

                # =============================================
                # TERCEIRA SEÇÃO: Validações
                # =============================================
                st.subheader("✅ Validações - Evento 2055")
                validation_errors = validate_2055_records(df_2055)

                if validation_errors:
                    st.error(
                        "❌ Foram encontrados documentos que não atendem às regras de validação:")

                    # Converter erros para DataFrame
                    df_errors = pd.DataFrame(validation_errors)

                    # Exibir tabela de erros
                    st.dataframe(
                        df_errors[['Filial', 'Período', 'Indicador Aquisição', 'Indicador Operação',
                                   'Valor Bruto', 'Funrural', 'Gilrat', 'Senar', 'Erro']].style.format({
                                       'Valor Bruto': 'R$ {:,.2f}',
                                       'Funrural': 'R$ {:,.2f}',
                                       'Gilrat': 'R$ {:,.2f}',
                                       'Senar': 'R$ {:,.2f}'
                                   }),
                        use_container_width=True
                    )

                    # Resumo dos erros
                    st.warning(
                        f"**Total de documentos com problemas:** {len(validation_errors)}")
                else:
                    st.success(
                        "✅ Todos os registros estão validados conforme as regras!")

                # Botão para gerar relatório Excel
                if st.button("📊 Gerar Relatório Excel 2055", key="btn_2055"):
                    excel_file = report_gen.generate_excel_report_2055(df_2055)
                    st.success(f"Relatório gerado: {excel_file}")

    with tab3:
        st.header("🏗️ Análise do Evento 2010 - Tomador de Serviços")

        uploaded_file_2010 = st.file_uploader(
            "Carregue o arquivo XML do evento 2010",
            type=['xml'],
            key='2010_upload'
        )

        if uploaded_file_2010:
            try:
                xml_content = uploaded_file_2010.read().decode('utf-8')
                data_2010 = parse_xml_2010(xml_content)

                if data_2010:
                    st.success(
                        f"✅ Arquivo 2010 processado com sucesso! {len(data_2010)} registros encontrados.")

                    report_gen = ReportGenerator()
                    df_2010 = pd.DataFrame(data_2010)

                    # =============================================
                    # TOTALIZADOR - Evento 2010 (PADRÃO)
                    # =============================================
                    st.subheader("💰 Totalizador - Evento 2010")

                    # Métricas gerais - PADRÃO
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Bruto",
                                  f"R$ {df_2010['Valor_Bruto'].sum():,.2f}")
                    with col2:
                        st.metric("Total Base Retenção",
                                  f"R$ {df_2010['Base_Retencao'].sum():,.2f}")
                    with col3:
                        st.metric("Total INSS",
                                  f"R$ {df_2010['Valor_INSS'].sum():,.2f}")

                    # =============================================
                    # PRIMEIRA TABELA: Dados principais
                    # =============================================
                    st.subheader("📋 Dados do Evento 2010")

                    display_cols_2010 = [
                        'Filial', 'Periodo', 'Prestador', 'Servico',
                        'Documento', 'Valor_Bruto', 'Base_Retencao',
                        'Valor_INSS', 'Emissao'
                    ]

                    st.dataframe(
                        df_2010[display_cols_2010].style.format({
                            'Valor_Bruto': 'R$ {:,.2f}',
                            'Base_Retencao': 'R$ {:,.2f}',
                            'Valor_INSS': 'R$ {:,.2f}'
                        }),
                        use_container_width=True
                    )

                    # =============================================
                    # SEGUNDA TABELA: Agrupada por filial com totalizadores
                    # =============================================
                    st.subheader("🏢 Resumo por Filial - Evento 2010")

                    # Agrupar por filial
                    grouped_2010 = df_2010.groupby('Filial')

                    # Lista para armazenar todas as linhas do relatório
                    all_rows_2010 = []

                    for filial, group in grouped_2010:
                        # Adicionar registros da filial
                        for _, row in group.iterrows():
                            all_rows_2010.append({
                                'Filial': filial,
                                'Prestador': row['Prestador'],
                                'Servico': row['Servico'],
                                'Documento': row['Documento'],
                                'Emissao': row['Emissao'],
                                'Valor Bruto': row['Valor_Bruto'],
                                'Base Retenção': row['Base_Retencao'],
                                'Valor INSS': row['Valor_INSS']
                            })

                        # Adicionar total da filial
                        total_filial = {
                            'Filial': '',
                            'Prestador': '**TOTAL FILIAL**',
                            'Servico': '',
                            'Documento': '',
                            'Emissao': '',
                            'Valor Bruto': group['Valor_Bruto'].sum(),
                            'Base Retenção': group['Base_Retencao'].sum(),
                            'Valor INSS': group['Valor_INSS'].sum()
                        }
                        all_rows_2010.append(total_filial)

                        # Adicionar linha em branco
                        all_rows_2010.append({
                            'Filial': '',
                            'Prestador': '',
                            'Servico': '',
                            'Documento': '',
                            'Emissao': '',
                            'Valor Bruto': None,
                            'Base Retenção': None,
                            'Valor INSS': None
                        })

                    # Remover última linha em branco
                    if all_rows_2010 and all_rows_2010[-1]['Filial'] == '':
                        all_rows_2010.pop()

                    df_resumo_2010 = pd.DataFrame(all_rows_2010)
                    st.dataframe(
                        df_resumo_2010.style.format({
                            'Valor Bruto': 'R$ {:,.2f}',
                            'Base Retenção': 'R$ {:,.2f}',
                            'Valor INSS': 'R$ {:,.2f}'
                        }),
                        use_container_width=True
                    )

                    # =============================================
                    # TERCEIRA TABELA: Consolidação geral
                    # =============================================
                    st.subheader("📊 Consolidação Geral - Evento 2010")

                    totais_2010 = pd.DataFrame({
                        'Descrição': ['Valor Total Bruto', 'Valor Total Base de Retenção', 'Valor Total INSS'],
                        'Valor': [
                            df_2010['Valor_Bruto'].sum(),
                            df_2010['Base_Retencao'].sum(),
                            df_2010['Valor_INSS'].sum()
                        ]
                    })

                    st.dataframe(
                        totais_2010.style.format({
                            'Valor': 'R$ {:,.2f}'
                        }),
                        use_container_width=True
                    )

                    # Botão para gerar relatório Excel
                    if st.button("📊 Gerar Relatório Excel 2010", key="btn_2010"):
                        excel_file = report_gen.generate_excel_report_2010(
                            data_2010)
                        st.success(f"Relatório gerado: {excel_file}")

                else:
                    st.warning("Nenhum dado encontrado no arquivo.")

            except Exception as e:
                st.error(f"❌ Erro ao processar arquivo 2010: {str(e)}")


if __name__ == "__main__":
    main()
