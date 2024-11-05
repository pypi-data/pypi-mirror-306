# FlaskMason

FlaskMason is a command-line tool designed to quickly scaffold Flask applications with a Django-like project structure. It automates the creation of a boilerplate project with organized blueprints, configuration files, and other essential components, allowing developers to focus on building features instead of setting up their environment.

## Features

- **Django-like Folder Structure**: Automatically creates a structured layout for your Flask projects, including blueprints for authentication, admin, and more.
- **Predefined Boilerplate Code**: Generates essential files with predefined content, reducing the need for repetitive setup.
- **Easy Installation**: Installs all necessary dependencies with a single command.

## Installation

You can install FlaskMason via pip. To install it along with its dependencies, run:

```bash
pip install flaskmason
```

## Usage

To create a new Flask project, simply run:

```bash
flaskmason <project_name>
```

This command will generate a new directory called `<project_name>` containing the following structure:

```
<project_name>/
├── app.py
├── config.py
├── requirements.txt
├── .env
├── blueprints/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── views.py
│   │   ├── models.py
│   │   └── forms.py
│   └── admin/
│       ├── __init__.py
│       ├── views.py
│       ├── models.py
│       └── forms.py
├── static/
└── templates/
```

### Example Commands

1. **Create a new Flask project**:
   ```bash
   flaskmason my_flask_project
   ```

2. **Change directory into the new project**:
   ```bash
   cd my_flask_project
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

## File Descriptions

- **app.py**: The main application file where the Flask app is created and configured.
- **config.py**: Contains configuration settings for the application, such as database URI and secret keys.
- **blueprints/**: Directory for organizing application features into blueprints, improving modularity and maintainability.
- **static/**: Directory for static files (CSS, JavaScript, images).
- **templates/**: Directory for HTML templates used in rendering views.

## Contributing

Contributions are welcome! If you have suggestions or find bugs, please open an issue or submit a pull request.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

[Your Name](https://github.com/Akash-nath29)

## Acknowledgements

- Thanks to the Flask community for providing an excellent framework for web development.

### Notes:
- **Personalize the Author Section**: Update the author section with your name and any other relevant details, like your LinkedIn or personal website, if desired.
- **Add More Details**: Feel free to expand on any sections, add more examples, or include additional features you plan to implement in the future.
- **Contribution Guidelines**: You might want to include more specific contribution guidelines if you expect contributions from others. 
