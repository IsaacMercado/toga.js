import toga

def button_handler(evt):
    print("hello")

def build(app):

    container = toga.OptionContainer()

    box1 = toga.Box()

    button = toga.Button('Hello world', on_press=button_handler)
    button.style.padding = 50
    button.style.flex = 1

    label = toga.NumberInput(min_value=10.5, max_value=50.6, on_change=lambda app: print(app.value))
    label.text = 'Hola Mundo'

    selection = toga.Selection(items=['Casella','Pedro Infante','Camilo'], on_select= lambda app:print(app.value))
    selection.items = ['321','123','456','654','789','987']

    box1.add(button)
    box1.add(label)
    box1.add(selection)

    box2 = toga.Box()

    image = toga.Image('../../static/images/tiberius.svg')
    imageview = toga.ImageView(image)

    slider = toga.Slider(range=(30, 50), on_slide= lambda app:print(app.value))

    box2.add(imageview)
    box2.add(slider)

    container.add('Window 1', box1)
    container.add('Window 2', box2)

    return container

def main():
    return toga.App('First App', 'org.beeware.helloworld', startup=build)

main().main_loop()

