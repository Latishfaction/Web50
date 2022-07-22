def modifier(hello):
    def wrapper():
        print("This code is about to run")
        hello()
        print("Code run successfully✔")
    return wrapper


@modifier
def hello():
    print("Hello World🌎")

hello()
