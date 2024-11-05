# csv2ies

Let's import users from a CSV file into an IES instance via it's REST API.

## Installation

`pip install csv2ies`

## Usage

- Needed user pools need to be created in user management beforehand.
- Open your folder with your CSV File in the terminal.
- Create an example config via `csv2ies config`
- Edit the created config.json file accordingly to your needs
- Add Aliases to match user pool names to anchors
- Run the import: `csv2ies run`

## CSV column names and quirks

Known column titles are (case-insensitve):
- "Nutzername", "Login"
- "Vorname", "Firstname"
- "Nachname", "Name", "Lastname"
- "E-Mail", "Email"
- "Geschlecht", "Anrede", "Gender"
- "Notiz", "Note"
- "Rolle", "roleList"
- "Bereich", "Zones"
- "Passwort", "Password"

Valid roles (Rolle) are:
- "Redakteur", "Nutzer", "User"
- "Admin", "Administrator"
- "Gast", "Extern", "Guest", "External"

If a user belongs to multiple Zones (Bereiche) values need to be separated by semicolons.
Zone names are case-sensitive!

Gender values are mapped from first letters (csse-insensitive):
- "h" & "m" map to male
- "f" & "w" map to female
- "d" & "n" map to diverse
- everything else results in unknown gender