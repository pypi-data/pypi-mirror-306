import subprocess
import json
import hashlib
import os, shutil, inspect, sys, fnmatch
from pathlib import Path
from nicegui import ui, app, run, Client
from nicegui.element import Element
from starlette.requests import Request
from starlette.responses import JSONResponse

class React(Element):
    def __init__(
        self,
        react_project_path: str,
        main_component: str = None,
        component_id: str = None,
        env: dict = None, 
        use_legacy_peer_deps: bool = False,
        dev: bool = False
    ):
        # Use __file__ from the caller's globals
        caller_globals = sys._getframe(1).f_globals
        if '__file__' in caller_globals:
            caller_file = Path(caller_globals['__file__']).resolve()
            caller_dir = caller_file.parent
        else:
            caller_dir = Path.cwd()

        # Resolve react_project_path relative to the caller's directory
        react_project_path = (caller_dir / react_project_path).resolve()
        self.original_project_path = react_project_path
        print(f"React project path: {react_project_path}")

        # Check if react_project_path exists
        if not react_project_path.exists():
            raise FileNotFoundError(f"React project path does not exist: {react_project_path}")

        # Determine component_id based on react_project_path if not provided
        if component_id is None:
            component_id = react_project_path.stem  # Use the folder name
        self.component_id = component_id
        self.main_component = main_component
        self.use_legacy_peer_deps = use_legacy_peer_deps
        self.dev = dev
        self.env = env or {}

        # Generate a unique hash based on the component ID and the project path
        self.component_hash = self._generate_unique_dir(component_id)

        # Create cache directory
        if self.dev:
            # Use a subfolder in the react_project_path for caching (dev mode)
            self.cache_dir = react_project_path.parent / 'react_cache_dev' / self.component_hash
        else:
            self.cache_dir = Path.home() / '.nicegui' / 'react_cache' / self.component_hash

        # Copy project files into cache directory
        self.copy_project_files()

        # Now set react_project_path to cache_dir
        self.react_project_path = self.cache_dir

        # Set up other paths
        self.output_dir = self.cache_dir / 'public' / self.component_hash
        self.vite_config_path = self.cache_dir / 'vite.config.js'
        self.package_json_path = self.cache_dir / 'package.json'
        self.main_jsx = self.cache_dir / 'main.jsx'

        # Initialize the UI element 
        super().__init__('div')
        self._props['id'] = self.component_id

        # Initialize props storage and event handlers
        self.client = ui.context.client
        self.client_id = self.client.id
        self.react_props = {}
        self.event_handlers = {}
        self.event_endpoint = f'/react_event/{self.component_id}'
        async def handle_event(request: Request):
            await self._handle_event(request)
        app.add_api_route(self.event_endpoint, handle_event, methods=['POST'])
        self.events_to_listen = set()
        self._props['data-props'] = json.dumps(self.react_props)
        self._props['data-events'] = json.dumps(list(self.events_to_listen))

        # Display a loading indicator
        # self.loading_indicator = ui.spinner().classes('m-2')

        # Now, automatically bundle and render
        self.serve_public_folder() 
        self.setup_vite_project()
        self.bundle_react()
        self.serve_bundle()
        self.include_assets()
        #ui.timer(0.1, self._setup, once=True)

    async def _handle_event(self, request: Request):
        data = await request.json()
        full_event_name = data.get('event')
        event_data = data.get('data')
        tab_id = data.get('tab_id')
        # Extract component_id and event_name
        component_id, event_name = full_event_name.split('.', 1)
        if component_id != self.component_id:
            # The event is not for this component
            return JSONResponse({'status': 'ignored'})
        
        # Get client based on tab_id
        client = None
        for c in Client.instances.values():
            if c.tab_id == tab_id:
                client = c
                break

        if client is None:
            print(f'No client found with tab_id {tab_id}')
            return JSONResponse({'status': 'error', 'message': 'Client not found'})

        handler = self.event_handlers.get(event_name)
        if handler:
            if inspect.iscoroutinefunction(handler):
                with client:
                    await handler(event_data)
            else:
                with client:
                    handler(event_data)
        return JSONResponse({'status': 'success'})
    
    def props(self, **kwargs):
        """
        Sets or updates props for the React component.

        Args:
            **kwargs: Key-value pairs representing props.
        """
        # Update the props dictionary
        old_props = self.react_props.copy()
        self.react_props.update(kwargs)
        if old_props != self.react_props:
            # Update the data-props attribute
            self._props['data-props'] = json.dumps(self.react_props, sort_keys=True)
            # Trigger an update to the frontend
            self.update()
        return self
    
    def on(self, event_name, handler):
        """
        Registers an event handler for a specific event.
        """
        self.event_handlers[event_name] = handler
        # Update the events to listen
        previous_events = self.events_to_listen.copy()
        self.events_to_listen.add(event_name)
        if previous_events != self.events_to_listen:
            self._props['data-events'] = json.dumps(sorted(list(self.events_to_listen)))
            self.update()
        return self
    
    def _generate_unique_dir(self, component_id: str):
        unique_string = component_id + str(self.original_project_path)
        unique_hash = hashlib.md5(unique_string.encode()).hexdigest()
        return f'react_{unique_hash}'

    def copy_project_files(self):
        """
        Copies the user's project files into the cache directory.
        """
        # Compute hash of the user's project files
        current_hash = self.compute_project_hash()

        # Check if the hash matches the one in the cache directory
        hash_file_path = self.cache_dir / 'project_hash.txt'
        if hash_file_path.exists():
            with open(hash_file_path, 'r') as f:
                cached_hash = f.read()
            if cached_hash == current_hash:
                print("No changes detected in project files. Using cached version.")
                return
            else:
                print("Changes detected in project files. Updating cache.")

        # Ensure the cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Define patterns to ignore
        patterns = [
            'node_modules', 'build', '.git', '.cache', '.idea', '__pycache__',
            '*.pyc', '*.pyo', 'vite.config.js', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
        ]

        # Create the ignore_patterns function for use in copytree
        ignore_patterns = shutil.ignore_patterns(*patterns)

        # Copy project files to cache directory
        for item in self.original_project_path.iterdir():
            # Skip the cache directory to prevent infinite recursion
            if item.resolve() == self.cache_dir.resolve():
                continue

            # Skip ignored patterns
            if any(fnmatch.fnmatch(item.name, pattern) for pattern in patterns):
                continue

            s = item
            d = self.cache_dir / item.name
            if item.is_dir():
                if d.exists():
                    shutil.rmtree(d)
                shutil.copytree(s, d, ignore=ignore_patterns)
            else:
                shutil.copy2(s, d)

        # Save the new hash
        with open(hash_file_path, 'w') as f:
            f.write(current_hash)

    def compute_project_hash(self):
        """
        Computes a hash of the project files to detect changes.
        Excludes specified directories.
        """
        hash_md5 = hashlib.md5()
        for root, dirs, files in os.walk(self.original_project_path):
            dirs[:] = [d for d in dirs if d not in (
                'node_modules', 'public', 'build', '.git', '.cache', '.idea', '__pycache__'
            )]
            for file in files:
                if file in ('build_hash.txt', 'package-lock.json', 'project_hash.txt'):
                    continue
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def setup_vite_project(self):
        """
        Sets up the Vite project, including creating necessary configuration files
        and installing dependencies if not already present.
        """
        # Ensure package.json exists and contains required dependencies
        package_json_modified = self.ensure_package_json()

        # Create vite.config.js with appropriate base path
        # If 'public' folder exists, set base_path accordingly
        public_folder_path = self.original_project_path / 'public'
        if public_folder_path.exists() and public_folder_path.is_dir():
            base_path = f'/react_public/{self.component_id}'
        else:
            base_path = '/'  # Default base path

        print("Creating vite.config.js...")
        self.create_vite_config(base_path)

        # Create main.jsx
        print("Creating main.jsx entry point...")
        self.create_main_jsx()

        # Determine if npm install needs to be run
        npm_install_needed = False

        # Paths
        node_modules_path = self.react_project_path / 'node_modules'
        package_lock_path = self.react_project_path / 'package-lock.json'

        if package_json_modified:
            npm_install_needed = True
            print("Package.json was modified by the script, npm install is needed.")
        elif not node_modules_path.exists():
            npm_install_needed = True
            print("node_modules does not exist, npm install is needed.")
        elif not package_lock_path.exists():
            npm_install_needed = True
            print("package-lock.json does not exist, npm install is needed.")
        else:
            # Compare modification times
            package_json_mtime = self.package_json_path.stat().st_mtime
            package_lock_mtime = package_lock_path.stat().st_mtime

            if package_json_mtime > package_lock_mtime:
                npm_install_needed = True
                print("package.json is newer than package-lock.json, npm install is needed.")
            else:
                print("Dependencies already installed and up to date.")

        if npm_install_needed:
            print("Installing dependencies...")
            install_command = ['npm', 'install']
            if self.use_legacy_peer_deps:
                install_command.append('--legacy-peer-deps')
            subprocess.run(install_command, cwd=self.react_project_path, check=True)
        else:
            print("Skipping npm install.")

    def ensure_package_json(self):
        """
        Ensures that package.json exists and contains required dependencies.
        Returns True if package.json was modified by the script, False otherwise.
        """
        package_json_modified = False

        if not self.package_json_path.exists():
            print("Creating an essential package.json...")
            self.create_essential_package_json()
            package_json_modified = True
        else:
            print("Found existing package.json. Ensuring required dependencies are present.")
            with open(self.package_json_path, 'r') as f:
                package_json = json.load(f)

            dependencies = package_json.get('dependencies', {})
            dev_dependencies = package_json.get('devDependencies', {})
            scripts = package_json.get('scripts', {})

            # Keep a copy of the original package_json for comparison
            original_package_json = json.dumps(package_json, sort_keys=True, indent=2)

            # Determine the Vite version to use based on existing devDependencies
            existing_vite_version = dev_dependencies.get('vite')
            if existing_vite_version:
                vite_major_version = int(existing_vite_version.lstrip('^~>=<').split('.')[0])
            else:
                vite_major_version = 5  # Default to Vite 5 if not specified

            # Required dependencies and versions
            required_dependencies = {
                'react': '^18.3.1',
                'react-dom': '^18.3.1',
            }
            if vite_major_version >= 5:
                required_dev_dependencies = {
                    'vite': '^5.4.10',
                    'vite-plugin-jsx': '^0.0.6',
                    '@vitejs/plugin-react': '^4.0.0',
                    '@rollup/plugin-replace': '^4.0.0',
                }
            else:
                required_dev_dependencies = {
                    'vite': '^4.0.0',
                    'vite-plugin-jsx': '^0.0.6',
                    '@vitejs/plugin-react': '^4.0.0',
                    '@rollup/plugin-replace': '^4.0.0',
                }
            required_scripts = {
                'dev': 'vite',
                'build': 'vite build',
            }

            # Update dependencies
            for dep, version in required_dependencies.items():
                if dep not in dependencies:
                    dependencies[dep] = version
                elif dependencies[dep] != version:
                    print(f"Note: Dependency '{dep}' version '{dependencies[dep]}' differs from required version '{version}'. Using existing version.")
                # Do not set package_json_modified here

            for dep, version in required_dev_dependencies.items():
                if dep not in dev_dependencies:
                    dev_dependencies[dep] = version
                elif dev_dependencies[dep] != version:
                    print(f"Note: Dev dependency '{dep}' version '{dev_dependencies[dep]}' differs from required version '{version}'. Using existing version.")
                # Do not set package_json_modified here

            # Update scripts
            for script, command in required_scripts.items():
                if script not in scripts:
                    scripts[script] = command
                elif scripts[script] != command:
                    print(f"Note: Script '{script}' command '{scripts[script]}' differs from required command '{command}'. Using existing command.")
                # Do not set package_json_modified here

            # Reconstruct the package_json dictionary
            package_json['dependencies'] = dependencies
            package_json['devDependencies'] = dev_dependencies
            package_json['scripts'] = scripts

            # Convert the updated package_json to a JSON string
            updated_package_json = json.dumps(package_json, sort_keys=True, indent=2)

            # Compare the original and updated package_json content
            if original_package_json != updated_package_json:
                package_json_modified = True
                print("Updating package.json with required dependencies.")
                with open(self.package_json_path, 'w') as f:
                    f.write(updated_package_json)
            else:
                print("All required dependencies are already present in package.json.")

        return package_json_modified

    def create_essential_package_json(self):
        """
        Creates an essential package.json file for the React project.
        """
        package_json = {
            "name": "react-nicegui",
            "version": "1.0.0",
            "private": True,
            "scripts": {
                "dev": "vite",
                "build": "vite build"
            },
            "dependencies": {
                "react": "^18.3.1",
                "react-dom": "^18.3.1"
            },
            "devDependencies": {
                "vite": "^5.4.10",
                "vite-plugin-jsx": "^0.0.6",
                "@vitejs/plugin-react": "^4.3.3"
            }
        }
        with open(self.package_json_path, 'w') as f:
            json.dump(package_json, f, indent=2)

    def generate_define_env_variables(self):
        """
        Generates a string representing the define property in Vite config
        with the environment variables.
        """
        if not self.env:
            return ''
        
        env_entries = []
        for key, value in self.env.items():
            # Ensure that the key is a valid JavaScript identifier
            # and the value is properly JSON-encoded
            json_value = json.dumps(value)
            env_entries.append(f"'process.env.{key}': {json_value}")
        define_content = ',\n'.join(env_entries)
        return define_content

    def create_vite_config(self, base_path='/'):
        """
        Creates a basic Vite configuration file for React with the specified base path.
        
        Args:
            base_path (str): The base path for serving assets. Defaults to '/'.
        """
        # Determine the Vite plugin based on Vite version
        with open(self.package_json_path, 'r') as f:
            package_json = json.load(f)
        dev_dependencies = package_json.get('devDependencies', {})
        vite_version = dev_dependencies.get('vite', '^4.0.0')
        try:
            vite_major_version = int(vite_version.lstrip('^~>=<').split('.')[0])
        except (ValueError, IndexError):
            vite_major_version = 4  # Default to Vite 4 if parsing fails

        if vite_major_version >= 5:
            react_plugin_import = "@vitejs/plugin-react-swc"
            react_plugin = "react()"
        else:
            react_plugin_import = "@vitejs/plugin-react"
            react_plugin = "react()"

        # Adjust output directory relative path
        output_dir_relative = os.path.relpath(self.output_dir, start=self.react_project_path).replace('\\', '/')

        public_path = getattr(self, 'public_static_path', f'/react_public/{self.component_id}')

        # Generate the define property for environment variables
        define_env_variables = self.generate_define_env_variables()

        # If define_env_variables is not empty, include the define property
        if define_env_variables:
            define_section = f"define: {{\n{define_env_variables}\n}},"
        else:
            define_section = ""
            
        vite_config_content = f"""
    import {{ defineConfig }} from 'vite';
    import react from '{react_plugin_import}';
    import replace from '@rollup/plugin-replace';
    import jsx from 'vite-plugin-jsx';
    import path from 'path';
    
    export default defineConfig({{
        base: '', //{base_path}/',  // Set the base path for assets
        plugins: [
            {react_plugin},
            jsx(),
            replace({{
                preventAssignment: true,
                delimiters: ['', ''],
                include: ['**/*.jsx','**/*.tsx','**/*.ts'],
                //exclude: ['**/public/{self.component_id}/**','**/node_modules/**'], 
                values: {{
                    'assets/': '{public_path}/assets/',
                    '{public_path}/{public_path}': '{public_path}',
                }},
            }}),
        ],
        {define_section}
        mode: 'development',
        build: {{
            outDir: './{output_dir_relative}',
            manifest: true,
            sourcemap: false,
            minify: false,
            rollupOptions: {{
                input: './main.jsx',
            }},
        }},
    }});
    """
        with open(self.vite_config_path, 'w') as f:
            f.write(vite_config_content)
        print("vite.config.js created with base path:", base_path)


    def create_main_jsx(self):
        """
        Creates the main.jsx file that serves as the entry point for Vite.
        """
        if not self.main_component:
            raise ValueError("main_component must be specified when initializing the React class.")

        # Attempt to locate the component file
        component_file = None
        # Search for .jsx and .tsx files that match the main_component
        for ext in ('*.jsx', '*.tsx'):
            for jsx_file in self.react_project_path.rglob(ext):
                if jsx_file.stem == self.main_component:
                    component_file = jsx_file
                    break
            if component_file:
                break

        if not component_file:
            raise FileNotFoundError(f"Component '{self.main_component}' not found in '{self.react_project_path}'.")

        # Determine the import path relative to the main.jsx file
        import_path = component_file.relative_to(self.react_project_path)
        import_path = str(import_path).replace('\\', '/')
        if not import_path.startswith('.'):
            import_path = './' + import_path

        # Determine if the component is exported as default or named
        is_default_export = self.is_default_export(component_file)

        # Determine the React version
        with open(self.package_json_path, 'r') as f:
            package_json = json.load(f)
        dependencies = package_json.get('dependencies', {})
        react_version = dependencies.get('react', '^18.0.0')
        # Extract major version
        react_major_version = int(react_version.lstrip('^~>=<').split('.')[0])

        # Construct the import statement based on export type
        if is_default_export:
            import_statement = f"import {self.main_component} from '{import_path}';"
        else:
            import_statement = f"import {{ {self.main_component} }} from '{import_path}';"

        # JavaScript code for main.jsx with modifications
        main_jsx_content = f"""
        import React from 'react';
        import ReactDOM from {'"react-dom/client"' if react_major_version >= 18 else '"react-dom"'};
        {import_statement}

        document.addEventListener('DOMContentLoaded', function() {{
            const container = document.getElementById('{self.component_id}');

            function parseProps(propsString) {{
                try {{
                    return JSON.parse(propsString);
                }} catch (e) {{
                    console.error('Failed to parse props:', e);
                    return {{}};
                }}
            }}

            const initialProps = parseProps(container.getAttribute('data-props') || '{{}}');
            const initialEventsToListen = JSON.parse(container.getAttribute('data-events') || '[]');

            // Function to emit events to the backend
            function emit(event_name, event_data) {{
                const fullEventName = '{self.component_id}.' + event_name;
                const tabId = sessionStorage.getItem('__nicegui_tab_id');
                console.log('user tabId:', tabId);
                fetch('{self.event_endpoint}', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{
                        event: fullEventName,
                        data: event_data,
                        tab_id: tabId
                    }})
                }});
            }}

            const AppWrapper = () => {{
                const [props, setProps] = React.useState(initialProps);
                const [eventsToListen, setEventsToListen] = React.useState(initialEventsToListen);

                React.useEffect(() => {{
                    const observer = new MutationObserver(mutations => {{
                        mutations.forEach(mutation => {{
                            if (mutation.type === 'attributes') {{
                                if (mutation.attributeName === 'data-props') {{
                                    const newProps = parseProps(container.getAttribute('data-props') || '{{}}');
                                    setProps(newProps);
                                }} else if (mutation.attributeName === 'data-events') {{
                                    const newEventsToListen = JSON.parse(container.getAttribute('data-events') || '[]');
                                    setEventsToListen(newEventsToListen);
                                }}
                            }}
                        }});
                    }});
                    observer.observe(container, {{
                        attributes: true
                    }});
                    return () => observer.disconnect();
                }}, []);

                const eventHandlers = React.useMemo(() => {{
                    const handlers = {{}};
                    eventsToListen.forEach(eventName => {{
                        handlers[eventName] = (event) => {{
                            const eventData = event && event.nativeEvent ? event.nativeEvent : event;
                            emit(eventName, eventData);
                        }};
                    }});
                    return handlers;
                }}, [eventsToListen]);

                return <{self.main_component} {{...props}} {{...eventHandlers}} />;
            }};

            const root = {'ReactDOM.createRoot(container)' if react_major_version >= 18 else 'null'};
            {'root.render(<AppWrapper />);' if react_major_version >= 18 else 'ReactDOM.render(<AppWrapper />, container);'}
        }});
        """

        with open(self.main_jsx, 'w') as f:
            f.write(main_jsx_content)


    def is_default_export(self, component_file: Path) -> bool:
        """
        Determines whether the component is exported as default or named.
        """
        with open(component_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Simple check: look for 'export default' in the file
        if 'export default' in content:
            return True
        else:
            return False

    def bundle_react(self):
        """
        Runs Vite to bundle the React project into JavaScript files.
        """
        current_hash = self.compute_project_hash()
        hash_file_path = self.output_dir / 'build_hash.txt'

        if hash_file_path.exists():
            with open(hash_file_path, 'r') as f:
                stored_hash = f.read()
            if current_hash == stored_hash:
                print("No changes detected in React project. Skipping build.")
                return
            else:
                print("Changes detected in React project. Rebuilding...")
        else:
            print("No previous build hash found. Building project...")

        # Get Vite version
        vite_version = self.get_vite_version()

        print(f"Bundling the React project with Vite ({vite_version})...")
        try:
            result = subprocess.run(
                ['npx', 'vite', 'build', '--mode', 'development'],
                cwd=self.react_project_path,
                check=True,
                capture_output=True,
                text=True
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error during bundling:")
            print(e.stdout)
            print(e.stderr)
            raise

        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(hash_file_path, 'w') as f:
            f.write(current_hash)

    def get_vite_version(self):
        """
        Retrieves the Vite version from package.json.
        """
        with open(self.package_json_path, 'r') as f:
            package_json = json.load(f)
        dev_dependencies = package_json.get('devDependencies', {})
        vite_version = dev_dependencies.get('vite', 'unknown')
        return vite_version

    def serve_bundle(self):
        """
        Serves the bundled JavaScript files using NiceGUI with a unique path.
        """
        abs_path = self.output_dir.absolute()
        static_path = f'/react/{self.component_hash}'
        app.add_static_files(static_path, abs_path)
        self.static_path = static_path

    def get_hashed_files(self):
        """
        Reads the manifest.json file to get the hashed filenames of main.js and associated CSS files.
        """
        manifest_path = self.output_dir / 'manifest.json'
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest file not found: {manifest_path}")
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        main_js_entry = manifest.get('main.jsx')
        if not main_js_entry:
            raise KeyError("main.jsx not found in manifest.json")

        files = {
            'js': main_js_entry.get('file'),
            'css': main_js_entry.get('css', [])
        }
        return files

    def include_assets(self):
        """
        Includes the compiled JavaScript and CSS files into the HTML.
        """
        hashed_files = self.get_hashed_files()

        # Include CSS files
        for css_file in hashed_files.get('css', []):
            css_url = f"{self.static_path}/{css_file}"
            ui.add_head_html(f'<link rel="stylesheet" href="{css_url}" />')

        # Include JS file
        js_file = hashed_files.get('js')
        if js_file:
            script_url = f"{self.static_path}/{js_file}"
            ui.add_body_html(f'<script type="module" src="{script_url}"></script>')
        else:
            raise FileNotFoundError("Hashed JS file not found in manifest.json")

    def serve_public_folder(self):
        public_folder_path = self.original_project_path / 'public'
        if public_folder_path.exists() and public_folder_path.is_dir():
            web_path_public = f'/react_public/{self.component_id}'
            app.add_static_files(web_path_public, str(public_folder_path))
            print(f"Serving static files from '{public_folder_path}' at '{web_path_public}'")
            self.public_static_path = web_path_public
        else:
            print("No 'public' folder found in the React project.")
            self.public_static_path = ''  # Set to empty string if no public folder

