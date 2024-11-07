# NiceGUI React Integration

Integrate React components into your NiceGUI applications.

## Introduction

I created this package to seamlessly embed React components within NiceGUI projects. It handles bundling your React code using Vite, serves the compiled assets, and provides a way to pass props from Python to React and handle events from React in Python.

## Features

- **Easy Integration**: Embed React components directly into NiceGUI applications.
- **Props and Events**: Pass props and handle events between Python and React.
- **Automatic Bundling**: Automatically bundles your React code using Vite.
- **Caching**: Efficiently caches builds to improve performance during development.

## Installation

Install the package via pip:

```bash
pip install nicegui-react
```


## Requirements
- Python 3.6 or higher
- NiceGUI installed
- Node.js and npm installed (for building the React project)

## Usage
Here's how to use the React class in your NiceGUI application:

```python
from nicegui import ui
from nicegui_react import React

@ui.page("/")
async def index():
    with ui.card():
        ui.label('Here is the React component:')
        ui.button('Click me', on_click=lambda: react.props(title="Updated Title"))

        with ui.card_section():
            react = React(
                react_project_path="./path_to_your_react_project",
                main_component="App"  # Replace with your main component's name
            ).style('width: 100%; height: 100%;').props(
                title="Hello from Python!"
            ).on('onClick', lambda event: ui.notify(f'Clicked on React component: {event}'))
```



## Parameters
- *react_project_path* (str): Path to your React project directory.
- *main_component* (str): Name of the main React component to render.
- *component_id* (str, optional): Unique identifier for the component instance.
- *env* (dict, optional): Environment variables to pass to the React app.
- *use_legacy_peer_deps* (bool, optional): Whether to use legacy peer dependencies during npm install.
- *dev* (bool, optional): If set to True, enables development mode.

## Methods
- props(**kwargs): Update the props passed to the React component.
- on(event_name, handler): Register an event handler for events emitted from React.

## Setting Up Your React Project
- Place your React project in a directory relative to your Python script.
- Ensure your package.json includes the necessary dependencies and scripts. The React class will help set this up if it's missing.
- Your main component should be properly exported.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are welcome.

## Contact
Feel free to reach out if you have any questions or suggestions.