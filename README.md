# BBG-Wiki chatbot

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:bbglab/eduCGI.git
   ```

2. Navigate to the project directory:

   ```bash
   cd bbgwiki_chatbot
   ```

3. Create and activate virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

4. Fill in the API keys in `env_example` and copy it to `.env`:

   ```bash
   cp env_example .env
   ```

5. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Clone the BBG-Wiki repository:

   ```bash
   git clone git@github.com:bbglab/eduCGI.git
   ```

## Usage

1. Run the streamlit app:

   ```bash
   streamlit run src/apps/streamlit/streamlit_app.py
   ```

2. Copy the local URL provided in the terminal (e.g., <http://localhost:8501>)
and paste it into your preferred web browser.

3. Log in using the default credentials:

   Username: __bbgwiki_chatbot__  
   Password: __pass_bbgwiki__ (or whatever password was hashed using `src/streamlit/tools/hash_password.py` and set in `src/streamlit/streamlit.yaml`)