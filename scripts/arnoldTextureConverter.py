import subprocess
import PySimpleGUI as sg
import clipboard
import os

def run_arnold_texture_converter(input_dir, options):
    try:
        exe_path = os.path.join(os.path.dirname(__file__), 'ArnoldTextureConverter.exe')
        command = [exe_path] + options + [input_dir]
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
        [sg.Text('Arnold Texture Converter', font=('Helvetica', 20), text_color='white')],
        [sg.Text('Select the directory containing texture files:')],
        [sg.InputText(key='input_dir'), sg.FolderBrowse()],
        [sg.Checkbox('-v: Verbose status messages', key='-v')],
        [sg.InputText('-o', size=(15, 1)), sg.InputText('', key='-output')],
        [sg.InputText('--threads', size=(15, 1)), sg.InputText('', key='-threads')],
        [sg.Checkbox('-u: Update mode', key='-u')],
        # Add more options and checkboxes here as needed
        [sg.Button('Convert'), sg.Button('Copy Directory to Clipboard'), sg.Button('Exit')],
        [sg.Text('', size=(50, 1), key='output_message')],
    ]

    window = sg.Window('Arnold Texture Converter', layout)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        elif event == 'Convert':
            input_dir = values['input_dir']
            options = []

            if values['-v']:
                options.append('-v')
            if values['-output']:
                options.extend(['-o', values['-output']])
            if values['-threads']:
                options.extend(['--threads', values['-threads']])
            # Add more options handling here as needed

            success, message = run_arnold_texture_converter(input_dir, options)
            if success:
                window['output_message'].update(f'Conversion Successful: {message}')
            else:
                window['output_message'].update(f'Conversion Failed: {message}')
        elif event == 'Copy Directory to Clipboard':
            clipboard.copy(values['input_dir'])

    window.close()

if __name__ == '__main__':
    main()
