from cleo import Command
from cleo import Application


class DownloadCommand(Command):
    """
    download std

    download
        {url? : which std do you want to download?}
    """

    def handle(self):
        name = self.argument("name")

        if name:
            text = "Hello {}".format(name)
        else:
            text = "Hello"

        if self.option("yell"):
            text = text.upper()

        self.line(text)


class SearchCommand(Command):
    """
    search some std

    greet
        {query? : What do you want to greet?}
        {from? : Who do you want to greet?}
    """

    def handle(self):
        name = self.argument("query")

        if name:
            text = "Hello {}".format(name)
        else:
            text = "Hello"

        if self.option("yell"):
            text = text.upper()

        self.line(text)


application = Application()
application.add(DownloadCommand())
application.add(SearchCommand())

if __name__ == "__main__":
    application.run()
