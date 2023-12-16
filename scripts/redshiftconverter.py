import subprocess
import PySimpleGUI as sg
import clipboard

def run_texture_processor(input_file, options):
    try:
        command = ['TextureProcessor.exe', input_file] + options
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def main():
    sg.theme('Dark')

    layout = [
        [sg.Text('Texture Processor', font=('Helvetica', 20))],
        [sg.Text('Select the directory containing texture files:')],
        [sg.InputText(key='input_dir'), sg.FolderBrowse()],
        [sg.Checkbox('-l: Force linear gamma', key='-l')],
        [sg.Checkbox('-s: Force sRGB gamma', key='-s')],
        [sg.Checkbox('-wx -wy: Filter MIP levels with wrapped filtering', key='-wx_wy')],
        [sg.Checkbox('-p: Photometric IES data', key='-p')],
        [sg.Checkbox('-isphere: Image Based Light (sphere projection)', key='-isphere')],
        [sg.Checkbox('-ihemisphere: Image Based Light (hemisphere projection)', key='-ihemisphere')],
        [sg.Checkbox('-imirrorball: Image Based Light (mirrorball projection)', key='-imirrorball')],
        [sg.Checkbox('-iangularmap: Image Based Light (angular map projection)', key='-iangularmap')],
        [sg.Checkbox('-ocolor: Sprite Cut-Out Map Opacity (from color intensity)', key='-ocolor')],
        [sg.Checkbox('-oalpha: Sprite Cut-Out Map Opacity (from alpha)', key='-oalpha')],
        [sg.Checkbox('-noskip: Disable skipping of already converted textures', key='-noskip')],
        [sg.Button('Convert'), sg.Button('Copy Directory to Clipboard'), sg.Button('Exit')],
        [sg.Text('', size=(50, 1), key='output_message')],
    ]

    window = sg.Window('Texture Processor', layout)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        elif event == 'Convert':
            input_dir = values['input_dir']
            options = []

            if values['-l']:
                options.append('-l')
            if values['-s']:
                options.append('-s')
            if values['-wx_wy']:
                options.extend(['-wx', '-wy'])
            if values['-p']:
                options.append('-p')
            if values['-isphere']:
                options.append('-isphere')
            if values['-ihemisphere']:
                options.append('-ihemisphere')
            if values['-imirrorball']:
                options.append('-imirrorball')
            if values['-iangularmap']:
                options.append('-iangularmap')
            if values['-ocolor']:
                options.append('-ocolor')
            if values['-oalpha']:
                options.append('-oalpha')
            if values['-noskip']:
                options.append('-noskip')

            success, message = run_texture_processor(input_dir, options)
            if success:
                window['output_message'].update(f'Conversion Successful: {message}')
            else:
                window['output_message'].update(f'Conversion Failed: {message}')
        elif event == 'Copy Directory to Clipboard':
            clipboard.copy(values['input_dir'])

    window.close()

if __name__ == '__main__':
    main()
