from tabulate import tabulate

headers = ["#", "id", "Image", "Text", "Found", "Error"]

def table(td):
    return tabulate([td], headers = headers, tablefmt="grid")
