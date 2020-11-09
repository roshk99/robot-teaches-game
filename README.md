# robot-teaches-game

## Notes
- Install VS Code
- Install Python 3
- Do the set-up instructions from https://code.visualstudio.com/docs/python/tutorial-flask starting with the Prerequisites and Create Project Environment sections
- Install Flask with `pip3 install flask` inside the `env`
- Run the app with `python -m flask run`
- https://stackoverflow.com/questions/56199111/visual-studio-code-cmd-error-cannot-be-loaded-because-running-scripts-is-disabl
- https://github.com/bevacqua/dragula/
- Alt + Shift + F is auto-indent
- Flask Login with Database https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
- DB to CSV with https://www.rebasedata.com/convert-sqlite-to-csv-online

```
python -m venv env
python -m pip install --upgrade pip
pip install flask
flask db init
flask db migrate -m "users table"
flask db upgrade
flask db migrate -m "trials table"
flask db upgrade
flask db migrate -m "demos table"
flask db upgrade

(Select Interpretor and Ctrl + Shift + `)
python -m flask run

pip install numpy scipy matplotlib
```