# 🖥️ Basic Python HTTP Server

This is a basic HTTP web server implemented in Python using sockets and multithreading. 

### Project Structure

```
├── handler.py      # Handles client HTTP requests
├── server.py       # Sets up the server socket and manages connections
└── public/         # Directory for static files 
```

---

### Requirements

* Python 3.9+
* Uses the standard library only. No external dependencies are required.

---

### How to Run

Run the server:

```bash
python server.py
```

Open [localhost:3000](http://localhost:3000) in your browser

---

### ⚠️ Limitations

* HTTPS not supported.
* Only supports `GET` requests.
* This is a basic implementation and is not ready for production environments. 