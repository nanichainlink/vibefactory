I have now restored the VibeFactory application and updated it based on your feedback. The application will now save generated projects into a `projects` directory and provide a button in the sidebar to run each one in a new terminal.

The currently running application is the old GPS app. Please stop it by pressing `Ctrl+C` in its terminal.

After stopping it, please run these two commands in order to install the correct dependencies and start the VibeFactory application.



.venv\Scripts\python.exe -m streamlit run app.py



1. __Install the correct dependencies:__ `pip install -r requirements.txt`
2. __Run the VibeFactory application:__ `streamlit run app.py`
