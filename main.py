import PySimpleGUI as sg


canvas_size = (600, 400) # [px]

coord_size = (100, 100) # [arb.]


layout = [[sg.Graph(canvas_size, (0, 0), coord_size,
                    background_color = "grey5")]]


window = sg.Window("Quantifying Chaos", layout,
                   background_color="grey15",
                   finalize=True,
                   margins=(10, 10))


while True:

    event, values = window.read(timeout=10)

    if event == sg.WIN_CLOSED:
        window.close()
        break;

    
