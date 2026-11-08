from __future__ import annotations
import streamlit as st
from translator import Translator, TranslationError
from translator.config import get_model
from translator.database import init_db, save_translation, get_history, clear_history

st.set_page_config(page_title="FOMO Translator V2", page_icon="🌐", layout="wide")
init_db()
st.title("🌐 FOMO Translator V2")
st.caption(f"Model đang dùng: {get_model()}")

tab_en, tab_zh, tab_history = st.tabs(["Anh ↔ Việt", "Trung → Việt", "Lịch sử"])

def translation_panel(mode: str, key: str):
    source = st.text_area("Văn bản gốc", height=260, key=f"{key}_source",
                          placeholder="Nhập hoặc dán văn bản cần dịch...")
    if st.button("Dịch", key=f"{key}_translate", type="primary"):
        if not source.strip():
            st.warning("Vui lòng nhập văn bản.")
        else:
            try:
                with st.spinner("Đang dịch..."):
                    result = Translator().translate(source, mode)
                st.session_state[f"{key}_result"] = result
                save_translation(mode, source, result, get_model())
            except TranslationError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error(f"Có lỗi: {exc}")
    result = st.session_state.get(f"{key}_result", "")
    st.text_area("Bản dịch", value=result, height=260, key=f"{key}_output", disabled=True)
    if result:
        st.code(result, language=None)

with tab_en:
    translation_panel("en_vi", "envi")
with tab_zh:
    translation_panel("zh_vi", "zhvi")
with tab_history:
    st.subheader("Lịch sử dịch gần đây")
    if st.button("Làm mới lịch sử"):
        st.rerun()
    rows = get_history(200)
    if rows:
        for item in rows:
            with st.expander(f'{item["created_at"]} · {item["mode"]} · {item["source_text"][:70]}'):
                st.markdown("**Văn bản gốc**")
                st.write(item["source_text"])
                st.markdown("**Bản dịch**")
                st.write(item["translated_text"])
    else:
        st.info("Chưa có lịch sử.")
    if st.button("Xóa toàn bộ lịch sử"):
        clear_history()
        st.success("Đã xóa lịch sử.")
        st.rerun()
