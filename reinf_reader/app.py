# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

from report_generator import ReportGenerator
from xml_parser import (
    parse_xml_4020,
    parse_xml_2055,
    validate_2055_records,
    parse_xml_2010
)


def main():
    st.set_page_config(
        page_title="Sistema REINF - Análise de Eventos",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Sistema de Análise REINF")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([
        "🗂️ Evento 4020 - Pagamentos",
        "🌾 Evento 2055 - Aquisição Produto Rural",
        "🏗️ Evento 2010 - Tomador de Serviços"
    ])

    # =====================================================
    # EVENTO 4020
    # =====================================================
    with tab1:
        st.header("Análise do Evento 4020 - Pagamentos")

        uploaded_file_4020 = st.file_uploader(
            "Carregue o arquivo XML do evento 4020",
            type=['xml'],
            key='4020_upload'
        )

        if uploaded_file_4020:
            xml_content = uploaded_file_4020.read().decode('utf-8')
            data_4020 = parse_xml_4020(xml_content)

            if data_4020:
                report_gen = ReportGenerator()
                df_4020 = pd.DataFrame(data_4020)

                # 🔹 TOTALIZADOR GERAL (INALTERADO)
                st.subheader("💰 Totalizador - Evento 4020")
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

                # 🔹 ALTERAÇÃO AQUI — COLUNAS DE %
                df_4020['% CSLL'] = (
                    df_4020['Valor_CSLL'] /
                    df_4020['Valor_Bruto'].replace(0, pd.NA)
                ) * 100

                df_4020['% COFINS'] = (
                    df_4020['Valor_COFINS'] /
                    df_4020['Valor_Bruto'].replace(0, pd.NA)
                ) * 100

                df_4020['% PP'] = (
                    df_4020['Valor_PP'] /
                    df_4020['Valor_Bruto'].replace(0, pd.NA)
                ) * 100

                df_4020['% IR'] = (
                    df_4020['Valor_IR'] /
                    df_4020['Valor_Bruto'].replace(0, pd.NA)
                ) * 100

                df_4020[['% CSLL', '% COFINS', '% PP', '% IR']] = (
                    df_4020[['% CSLL', '% COFINS', '% PP', '% IR']]
                    .fillna(0)
                    .round(2)
                )

                # 🔹 TABELA (INALTERADA, APENAS COM NOVAS COLUNAS)
                st.subheader("📋 Dados do Evento 4020")
                st.dataframe(df_4020, use_container_width=True)

                # 🔹 TOTALIZADOR POR FILIAL (INALTERADO)
                st.subheader(
                    "🏢 Totalizador de Tributos por Filial - Evento 4020")
                df_filial = (
                    df_4020
                    .groupby('Numero_Inscricao_Estab', as_index=False)
                    .agg({
                        'Valor_Bruto': 'sum',
                        'Valor_CSLL': 'sum',
                        'Valor_COFINS': 'sum',
                        'Valor_PP': 'sum',
                        'Valor_IR': 'sum'
                    })
                )

                st.dataframe(
                    df_filial.style.format({
                        'Valor_Bruto': 'R$ {:,.2f}',
                        'Valor_CSLL': 'R$ {:,.2f}',
                        'Valor_COFINS': 'R$ {:,.2f}',
                        'Valor_PP': 'R$ {:,.2f}',
                        'Valor_IR': 'R$ {:,.2f}'
                    }),
                    use_container_width=True
                )

    # =====================================================
    # EVENTO 2055 (INALTERADO)
    # =====================================================
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
                xml_content = uploaded_file.read().decode('utf-8')
                df_temp = parse_xml_2055(xml_content)
                if not df_temp.empty:
                    all_data.append(df_temp)

            if all_data:
                df_2055 = pd.concat(all_data, ignore_index=True)

                st.subheader("💰 Totalizador de Tributos - Evento 2055")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Funrural",
                              f"R$ {df_2055['Funrural'].sum():,.2f}")
                with col2:
                    st.metric("Total Gilrat",
                              f"R$ {df_2055['Gilrat'].sum():,.2f}")
                with col3:
                    st.metric("Total Senar",
                              f"R$ {df_2055['Senar'].sum():,.2f}")

                st.subheader("📋 Dados do Evento 2055")
                st.dataframe(df_2055, use_container_width=True)

                st.subheader("✅ Validações - Evento 2055")
                validation_errors = validate_2055_records(df_2055)

                if validation_errors:
                    st.error("Foram encontrados documentos com inconsistências")
                    st.dataframe(pd.DataFrame(validation_errors),
                                 use_container_width=True)
                else:
                    st.success("Todos os registros estão validados")

    # =====================================================
    # EVENTO 2010 (INALTERADO)
    # =====================================================
    with tab3:
        st.header("🏗️ Análise do Evento 2010 - Tomador de Serviços")

        uploaded_file_2010 = st.file_uploader(
            "Carregue o arquivo XML do evento 2010",
            type=['xml'],
            key='2010_upload'
        )

        if uploaded_file_2010:
            xml_content = uploaded_file_2010.read().decode('utf-8')
            data_2010 = parse_xml_2010(xml_content)

            if data_2010:
                df_2010 = pd.DataFrame(data_2010)

                df_2010['% Retencao'] = (
                    df_2010['Valor_INSS'] /
                    df_2010['Base_Retencao'].replace(0, pd.NA)
                ) * 100
                df_2010['% Retencao'] = df_2010['% Retencao'].fillna(0)

                st.subheader("💰 Totalizador - Evento 2010")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Valor Bruto Total",
                              f"R$ {df_2010['Valor_Bruto'].sum():,.2f}")
                with col2:
                    st.metric("Base de Retenção Total",
                              f"R$ {df_2010['Base_Retencao'].sum():,.2f}")
                with col3:
                    st.metric("INSS Total",
                              f"R$ {df_2010['Valor_INSS'].sum():,.2f}")

                st.subheader("📋 Dados do Evento 2010")
                st.dataframe(df_2010, use_container_width=True)

                st.subheader("⚠️ Inconsistências - Retenção acima de 11%")
                df_incons = df_2010[df_2010['% Retencao'] > 11]

                if not df_incons.empty:
                    st.error("Documentos com retenção superior a 11%")
                    st.dataframe(df_incons, use_container_width=True)
                else:
                    st.success("Nenhum documento com retenção superior a 11%")


if __name__ == "__main__":
    main()
