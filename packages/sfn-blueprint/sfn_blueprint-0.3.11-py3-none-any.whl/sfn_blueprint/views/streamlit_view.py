import streamlit as st
from .base_view import SFNBaseView
from typing import Any, List, Optional

class SFNStreamlitView(SFNBaseView):
    def display_title(self):
        st.title(self.title)

    def show_message(self, message: str, message_type: str = "info"):
        if message_type == "info":
            st.info(message)
        elif message_type == "success":
            st.success(message)
        elif message_type == "error":
            st.error(message)
        elif message_type == "warning":
            st.warning(message)
        else:
            st.write(message)

    def display_header(self, text: str):
        st.header(text)

    def display_subheader(self, text: str):
        st.subheader(text)

    def display_markdown(self, text: str):
        st.markdown(text)

    def create_columns(self, num_columns: int):
        return st.columns(num_columns)

    def file_uploader(self, label: str, accepted_types: List[str]) -> Any:
        return st.file_uploader(label, type=accepted_types)

    def display_dataframe(self, data: Any):
        st.dataframe(data)

    def display_spinner(self, text: str):
        return st.spinner(text)

    def radio_select(self, label: str, options: List[str], key: Optional[str] = None) -> str:
        return st.radio(label, options, key=key)

    def display_button(self, label: str, key: Optional[str] = None) -> bool:
        return st.button(label, key=key)

    def load_progress_bar(self, progress: float):
        st.progress(progress)

    def create_download_button(self, label: str, data: Any, file_name: str, mime_type: str):
        st.download_button(
            label=label,
            data=data,
            file_name=file_name,
            mime=mime_type
        )

    def create_container(self):
        return st.container()

    def stop_execution(self):
        st.stop()

    def rerun_script(self):
        st.rerun()

    def make_empty(self):
        return st.empty()


    def update_text(self, text_element: st.delta_generator.DeltaGenerator, new_text: str):
        text_element.text(new_text)

    
    def load_progress_bar(self, progress: float):
        """Display a progress bar with given progress (0-1)."""
        return st.progress(progress)

    def update_progress(self, progress_bar: Any, value: float):
        """Update a progress bar with a new value."""
        # In Streamlit, we can just set the value directly on the progress bar
        progress_bar.progress(min(1.0, max(0.0, value)))

    def create_progress_container(self):
        """Create a progress bar and status text container."""
        container = st.container()
        with container:
            progress_bar = self.load_progress_bar(0.0)
            status_text = self.make_empty()
        return progress_bar, status_text