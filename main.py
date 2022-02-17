from application import Application
from commands import Commands
from console import Console
from dialog_with_user import DialogWithUser
from hospital import Hospital

if __name__ == "__main__":
    hospital = Hospital([1 for x in range(200)])
    console = Console()
    dialog_with_user = DialogWithUser(console)
    commands = Commands(hospital, dialog_with_user)
    app = Application(dialog_with_user, commands)

    app.main()
