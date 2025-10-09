# report_generator.py
import pandas as pd
from datetime import datetime
import io


class ReportGenerator:
    def __init__(self):
        pass

    def generate_excel_report_4020(self, data_4020):
        """Gera relatório Excel para evento 4020"""
        try:
            df = pd.DataFrame(data_4020)

            # Criar um arquivo Excel em memória
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Evento4020', index=False)

                # Formatação básica
                workbook = writer.book
                worksheet = writer.sheets['Evento4020']

                # Formato monetário
                money_format = workbook.add_format(
                    {'num_format': 'R$ #,##0.00'})
                percent_format = workbook.add_format({'num_format': '0.00%'})

                # Aplicar formatação às colunas de valores
                colunas_monetarias = ['Valor_Bruto', 'Base_CSLL', 'Valor_CSLL', 'Base_COFINS',
                                      'Valor_COFINS', 'Base_PP', 'Valor_PP', 'Base_IR', 'Valor_IR']

                for i, col in enumerate(df.columns):
                    if col in colunas_monetarias:
                        worksheet.set_column(i, i, 15, money_format)
                    elif col.startswith('%'):
                        worksheet.set_column(i, i, 12, percent_format)

            output.seek(0)

            # Salvar o arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_4020_{timestamp}.xlsx"

            with open(filename, 'wb') as f:
                f.write(output.getvalue())

            return filename

        except Exception as e:
            print(f"Erro ao gerar relatório Excel 4020: {e}")
            return None

    def generate_excel_report_2055(self, df_2055):
        """Gera relatório Excel para evento 2055"""
        try:
            # Criar um arquivo Excel em memória
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_2055.to_excel(writer, sheet_name='Evento2055', index=False)

                # Formatação básica
                workbook = writer.book
                worksheet = writer.sheets['Evento2055']

                # Formato monetário
                money_format = workbook.add_format(
                    {'num_format': 'R$ #,##0.00'})
                percent_format = workbook.add_format({'num_format': '0.00%'})

                # Aplicar formatação às colunas de valores
                colunas_monetarias = ['Valor Bruto',
                                      'Funrural', 'Gilrat', 'Senar']
                colunas_percentuais = ['% Funrural', '% Gilrat', '% Senar']

                for i, col in enumerate(df_2055.columns):
                    if col in colunas_monetarias:
                        worksheet.set_column(i, i, 15, money_format)
                    elif col in colunas_percentuais:
                        worksheet.set_column(i, i, 12, percent_format)

            output.seek(0)

            # Salvar o arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_2055_{timestamp}.xlsx"

            with open(filename, 'wb') as f:
                f.write(output.getvalue())

            return filename

        except Exception as e:
            print(f"Erro ao gerar relatório Excel 2055: {e}")
            return None

    def generate_excel_report_2010(self, data_2010):
        """Gera relatório Excel para evento 2010"""
        try:
            df = pd.DataFrame(data_2010)

            # Criar um arquivo Excel em memória
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Evento2010', index=False)

                # Formatação básica
                workbook = writer.book
                worksheet = writer.sheets['Evento2010']

                # Formato monetário
                money_format = workbook.add_format(
                    {'num_format': 'R$ #,##0.00'})

                # Aplicar formatação às colunas de valores
                colunas_monetarias = ['Valor_Bruto',
                                      'Base_Retencao', 'Valor_INSS']

                for i, col in enumerate(df.columns):
                    if col in colunas_monetarias:
                        worksheet.set_column(i, i, 15, money_format)
                    elif col == 'Emissao':
                        worksheet.set_column(i, i, 12)  # Formato data

            output.seek(0)

            # Salvar o arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_2010_{timestamp}.xlsx"

            with open(filename, 'wb') as f:
                f.write(output.getvalue())

            return filename

        except Exception as e:
            print(f"Erro ao gerar relatório Excel 2010: {e}")
            return None
