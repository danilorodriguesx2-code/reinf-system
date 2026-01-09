# app_debug.py (modo diagnóstico)
import streamlit as st
import traceback
import sys

# tentaremos importar o app real de forma protegida para capturar erros de import
try:
    st.set_page_config(page_title="REINF - Debug",
                       page_icon="📊", layout="wide")
except Exception:
    # se houver tentativa de set_page_config dupla, ignore aqui (para depuração)
    pass

st.title("Debug Streamlit - REINF")
st.write("Inicializando imports...")

try:
    # Importar módulos do seu projeto com timeout/try para capturar erros
    import importlib
    # Tente importar os módulos que podem falhar
    report_generator = importlib.import_module("report_generator")
    xml_parser = importlib.import_module("xml_parser")
    st.success("✅ Imports realizados com sucesso: report_generator, xml_parser")
except Exception as e:
    tb = traceback.format_exc()
    print("ERRO nos imports:\n", tb, file=sys.stderr)
    st.error("❌ Erro durante imports. Veja o terminal para o traceback.")
    st.code(tb)
    # pare por aqui, porque imports falharam
    st.stop()

# Agora testar execução da função main do seu app (se existir)
try:
    # se seu app original tem main em app.py, importamos e chamamos com proteção
    app_module = importlib.import_module("app")
    if hasattr(app_module, "main"):
        st.write("Chamando app.main() para testar execução...")
        try:
            app_module.main()
            st.success("✅ app.main() executado (debug).")
        except Exception:
            tb = traceback.format_exc()
            print("ERRO em app.main():\n", tb, file=sys.stderr)
            st.error("❌ Erro ao executar app.main(). Ver detalhes abaixo:")
            st.code(tb)
    else:
        st.warning("Módulo app não possui função main().")
except Exception:
    tb = traceback.format_exc()
    print("ERRO ao importar app.py:\n", tb, file=sys.stderr)
    st.error("❌ Erro ao importar app.py. Ver detalhes abaixo:")
    st.code(tb)
