
# Generic Data Agent

This Flask-based API allows you to securely access the contents of specified files over HTTPS. It enforces secure communication, checks access permissions using a secret key, and ensures only authorized files are accessible.

## Features
- **HTTPS Enforcement**: Redirects all HTTP requests to HTTPS to ensure secure communication.
- **File Access Control**: Only allows access to files explicitly listed in a configuration file.
- **Secret Key Authentication**: Requires a valid secret key in the request headers to authorize access.
- **Logging**: Logs important events, warnings, and errors for debugging and monitoring.

---

## Prerequisites
- Python 3.7 or higher
- SSL certificates (server.crt and server.key) for HTTPS

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   - Ensure `requirements.txt` includes the following dependencies:
     ```
     Flask
     Werkzeug
     ```

4. **Set Up Environment Variables**:
   - You need to set the `SECRET_KEY` and `CONFIG_PATH` environment variables.
   - **On macOS/Linux**:
     ```bash
     export SECRET_KEY="your_secret_key"
     export CONFIG_PATH="/path/to/your/config.json"
     ```
   - **On Windows**:
     ```bash
     set SECRET_KEY=your_secret_key
     set CONFIG_PATH=C:\path\to\your\config.json
     ```

5. **Prepare Your Configuration File**:
   - Create a `config.json` file with the following structure:
     ```json
     {
       "allowed_files": [
         "/path/to/your/file1.txt",
         "/path/to/your/file2.txt"
       ]
     }
     ```
   - Replace `/path/to/your/file1.txt` and `/path/to/your/file2.txt` with the absolute paths to the files you want to allow access to.

---

## Usage

### Running the Flask App

1. **Development Mode**:
   - Run the Flask app directly (for development or testing purposes):
     ```bash
     python your_script.py
     ```

2. **Production Mode with Gunicorn**:
   - Use Gunicorn to run the app in a production environment:
     ```bash
     gunicorn -w 4 -b 0.0.0.0:8080 --certfile=/path/to/server.crt --keyfile=/path/to/server.key your_script:app
     ```
   - **Options**:
     - `-w 4`: Number of worker processes (adjust based on your server's resources).
     - `-b 0.0.0.0:8080`: Binds the server to all interfaces on port 443 for HTTPS.
     - `--certfile` and `--keyfile`: Paths to your SSL certificate and key.
     - `--config`: Path to the config.json with the whitelisted files
---

## Auto-Execution at Startup

### Windows

1. **Create a Batch File**:
   - Create a `.bat` file, for example, `start_flask_app.bat` with the following content:
     ```batch
     @echo off
     cd C:\path\to\your\project
     call venv\Scripts\activate
     set SECRET_KEY=your_secret_key
     set CONFIG_PATH=C:\path\to\your\config.json
     gunicorn -w 4 -b 0.0.0.0:443 --certfile=server.crt --keyfile=server.key your_script:app
     ```
   - Save this file in a location you can easily access.

2. **Schedule the Batch File to Run at Startup**:
   - Open **Task Scheduler**.
   - Click on **Create Task**.
   - Under the **General** tab, name your task (e.g., "Start Flask App").
   - Under the **Triggers** tab, click **New** and select **At startup**.
   - Under the **Actions** tab, click **New**, select **Start a program**, and browse to your `.bat` file.
   - Click **OK** to save and enable the task.

---

### macOS

1. **Create a Shell Script**:
   - Create a shell script, for example, `start_flask_app.sh` with the following content:
     ```bash
     #!/bin/bash
     cd /path/to/your/project
     source venv/bin/activate
     export SECRET_KEY="your_secret_key"
     export CONFIG_PATH="/path/to/your/config.json"
     gunicorn -w 4 -b 0.0.0.0:443 --certfile=server.crt --keyfile=server.key your_script:app
     ```
   - Make the script executable:
     ```bash
     chmod +x start_flask_app.sh
     ```

2. **Add the Script to Startup Items**:
   - Open **System Preferences** > **Users & Groups**.
   - Select your user and go to the **Login Items** tab.
   - Click the **+** button and add the `start_flask_app.sh` script.

---

### Linux

1. **Create a Systemd Service**:
   - Create a new service file, for example, `/etc/systemd/system/flask_app.service`:
     ```ini
     [Unit]
     Description=Flask Secure File Access API
     After=network.target

     [Service]
     User=your_username
     WorkingDirectory=/path/to/your/project
     Environment="SECRET_KEY=your_secret_key"
     Environment="CONFIG_PATH=/path/to/your/config.json"
     ExecStart=/path/to/your/project/venv/bin/gunicorn -w 4 -b 0.0.0.0:443 --certfile=server.crt --keyfile=server.key your_script:app
     Restart=always

     [Install]
     WantedBy=multi-user.target
     ```

   - **Replace**:
     - `your_username` with your Linux username.
     - `/path/to/your/project` with the path to your project directory.

2. **Enable and Start the Service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable flask_app.service
   sudo systemctl start flask_app.service
   ```

---

## API Endpoints

### `/getfile_content`
- **Method**: `GET`
- **Description**: Retrieves the content of a specified file.
- **Headers**:
  - `Secret-Key`: Your secret key for authentication.
- **Query Parameters**:
  - `filepath`: The absolute path of the file to be accessed.
- **Response**:
  - **200 OK**: Returns the content of the file.
  - **403 Forbidden**: If the secret key is invalid or the file is not allowed.
  - **404 Not Found**: If the file does not exist.
  - **500 Internal Server Error**: If an error occurs while reading the file.

**Example Request**:
```bash
curl -X GET "https://localhost/getfile_content?filepath=/path/to/your/file.txt" -H "Secret-Key: your_secret_key"
```

---

## Security Considerations
- **Always use HTTPS**: The app enforces HTTPS to encrypt data in transit.
- **Protect Your Secret Key**: Never expose your secret key publicly.
- **Restrict File Access**: Only add files to `allowed_files` in `config.json` that are safe to share.

---

## Logging
- The app uses Python's `logging` module to log important events.
- Logs are printed to the console. You can configure it to log to a file for more persistent logging.

---

## License
- This project is licensed under the MIT License. You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, under the following conditions:

    - The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
    - THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
---

## Contact
- **Author**: Jonathan Stross
- **Email**: jonathan.stross@pathlock.com
- **GitHub**: [Albastross](https://github.com/yourusername)

Feel free to open issues or contribute to this project!
