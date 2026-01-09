# report_generator.py
import pandas as pd
import io


class ReportGenerator:

    def generate_excel_report_4020(self, data_4020):
        df = pd.DataFrame(data_4020)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Evento4020', index=False)
        output.seek(0)
        return output

    def generate_excel_report_2055(self, df_2055):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_2055.to_excel(writer, sheet_name='Evento2055', index=False)
        output.seek(0)
        return output

    # 🔹 AJUSTADO
    def generate_excel_report_2010(self, df_2010):
        try:
            output = io.BytesIO()

            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_2010.to_excel(writer, sheet_name='Evento2010', index=False)
                worksheet = writer.sheets['Evento2010']

                for col_cells in worksheet.columns:
                    max_length = 0
                    col_letter = col_cells[0].column_letter
                    for cell in col_cells:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    worksheet.column_dimensions[col_letter].width = max_length + 3

            output.seek(0)
            return output

        except Exception as e:
            print(f"Erro ao gerar relatório Excel 2010: {e}")
            return None
