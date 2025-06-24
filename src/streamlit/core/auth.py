import streamlit as st
import streamlit_authenticator as stauth


class Authenticator:
    """
    Minimal wrapper for streamlit-authenticator functionality.
    """

    def __init__(self, config) -> None:
        self._authenticator = stauth.Authenticate(
            credentials=config["credentials"],
            cookie_name=config["cookie"]["name"],
            key=config["cookie"]["key"],
            expiry_days=config["cookie"]["expiry_days"],
        )

    def require_login(self, location: str = "main") -> None:
        """
        Render the login form and enforce authentication.

        Args:
            location (str): Where to render the form: "main", "sidebar", or "unrendered".
        """
        # Display the login form
        self._authenticator.login(location)

        # Check authentication status
        auth_status = st.session_state.get("authentication_status")
        if auth_status is False:
            st.error("Username/password is incorrect")
            st.stop()
        elif auth_status is None:
            st.warning("Please enter your username and password")
            st.stop()

        return self._authenticator