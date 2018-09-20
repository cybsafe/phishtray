class FancyPrint(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def echo(stuff_to_print, style):
        bash_color = getattr(FancyPrint, style, None)

        if not bash_color:
            print(stuff_to_print)
            return

        print('{}{}{}'.format(bash_color, stuff_to_print, FancyPrint.ENDC))