# Flask Portfolio App

This project is a basic Flask portfolio website for Yash. It includes:

- a Flask app
- a static portfolio page
- Gunicorn support for Linux deployment
- Nginx reverse proxy configuration
- EC2 deployment instructions
- HTTPS setup with SSL using Certbot

## Project structure

```text
.
|-- app.py
|-- wsgi.py
|-- requirements.txt
|-- templates/
|   `-- index.html
|-- static/
|   `-- style.css
|-- deploy/
|   |-- nginx-portfolio.conf
|   `-- portfolio.service
`-- README.md
```

## Run locally

On Windows:

```powershell
cd C:\Users\Lenovo\Documents\Playground
.\.venv\Scripts\activate
pip install -r requirements.txt
flask --app app run
```

Open:

```text
http://127.0.0.1:5000
```

## Push to GitHub

Create a new GitHub repository, then run these commands in the project folder:

```bash
git init
git add .
git commit -m "Initial Flask portfolio app"
git branch -M main
git remote add origin https://github.com/Yashu-sudo/devops-Learning.git
git push -u origin main
```

Repository URL:

```text
https://github.com/Yashu-sudo/devops-Learning.git
```

## Deploy to AWS EC2

These steps assume:

- you are using Ubuntu on EC2
- your EC2 public IP `3.235.134.54` or domain `yashopslib.work.gd` points to the server
- you connect with SSH

### 1. Launch the EC2 instance

Create an Ubuntu EC2 instance and allow these inbound rules in the Security Group:

- `22` for SSH
- `5000` for initial Gunicorn testing
- `80` for HTTP
- `443` for HTTPS

### 2. Connect to the server

```bash
ssh -i your-key.pem ubuntu@3.235.134.54
```

### 3. Install required packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx
```

### 4. Copy the project to EC2

If you already pushed to GitHub:

```bash
git clone https://github.com/Yashu-sudo/devops-Learning.git
cd devops-Learning
```

Or copy it manually using `scp`.

### 5. Create the virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Stage 1: Run the app directly on port 5000

Start Gunicorn directly:

```bash
gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app
```

Now open:

```text
http://3.235.134.54:5000
```

If this works, your app is running correctly on EC2.

## Stage 2: Run Gunicorn as a systemd service

Copy the service file from [deploy/portfolio.service](C:\Users\Lenovo\Documents\Playground\deploy\portfolio.service) to your server:

```bash
sudo cp deploy/portfolio.service /etc/systemd/system/portfolio.service
```

Before starting it, update these paths inside the service file if your project is not located here:

```text
/home/ubuntu/devops-Learning
```

Then reload systemd and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start portfolio
sudo systemctl enable portfolio
sudo systemctl status portfolio
```

## Stage 3: Put Nginx in front of Gunicorn

Copy the Nginx config from [deploy/nginx-portfolio.conf](C:\Users\Lenovo\Documents\Playground\deploy\nginx-portfolio.conf):

```bash
sudo cp deploy/nginx-portfolio.conf /etc/nginx/sites-available/portfolio
```

Edit the config:

```bash
sudo nano /etc/nginx/sites-available/portfolio
```

Change this line:

```nginx
server_name yashopslib.work.gd 3.235.134.54;
```

Use either:

- your EC2 public IP `3.235.134.54` for testing
- your real domain `yashopslib.work.gd` once DNS is ready

Enable the config:

```bash
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/portfolio
```

Optional: remove the default Nginx site:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

Test and reload Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Now visit:

```text
http://3.235.134.54
```

At this stage:

- Nginx listens on port `80`
- Nginx forwards traffic to Gunicorn on port `5000`

After Nginx is working, you can remove port `5000` from the EC2 Security Group so Gunicorn is no longer publicly exposed.

## Stage 4: Enable HTTPS with SSL

For SSL, you should use a real domain name pointed to your EC2 public IP. HTTPS is best configured after DNS is already working.

Example:

```text
yashopslib.work.gd -> 3.235.134.54
```

Install Certbot:

```bash
sudo apt update
sudo apt install -y certbot python3-certbot-nginx
```

Run Certbot:

```bash
sudo certbot --nginx -d yashopslib.work.gd
```

Follow the prompts to:

- enter your email
- agree to terms
- optionally redirect HTTP to HTTPS

After success, your site will be available on:

```text
https://yashopslib.work.gd
```

Test automatic renewal:

```bash
sudo certbot renew --dry-run
```

## Useful commands

Check Gunicorn service logs:

```bash
sudo journalctl -u portfolio -f
```

Restart Gunicorn:

```bash
sudo systemctl restart portfolio
```

Restart Nginx:

```bash
sudo systemctl restart nginx
```

Check Nginx status:

```bash
sudo systemctl status nginx
```

## Deployment summary

1. Run on EC2 directly with Gunicorn on port `5000`
2. Put Nginx in front so users access port `80`
3. Point your domain to EC2
4. Use Certbot to enable HTTPS on port `443`
5. Close public access to port `5000` in the Security Group

## Notes

- `app.py` contains the Flask application
- `wsgi.py` exposes the app for Gunicorn
- Nginx handles incoming web traffic
- Gunicorn serves the Flask app
- Certbot installs and manages SSL certificates
