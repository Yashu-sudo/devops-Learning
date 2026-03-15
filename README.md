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
|-- run.sh
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

Run these commands in the project folder:

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
- your EC2 public IP `44.223.71.73` or domain `yashopslib.work.gd` points to the server
- you connect with SSH

### 1. Launch the EC2 instance

Allow these inbound rules in the Security Group:

- `22` for SSH
- `5000` for initial Gunicorn testing
- `80` for HTTP
- `443` for HTTPS

### 2. Connect to the server

```bash
ssh -i your-key.pem ubuntu@44.223.71.73
```

### 3. Install required packages

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip nginx
```

### 4. Copy the project to EC2

```bash
git clone https://github.com/Yashu-sudo/devops-Learning.git
cd devops-Learning
```

### 5. Run the app directly on port 5000

```bash
chmod +x run.sh
./run.sh
```

Open:

```text
http://44.223.71.73:5000
```

If this works, your app is running correctly on EC2.

## Run Gunicorn as a service

Copy the service file from [portfolio.service](C:\Users\Lenovo\Documents\Playground\deploy\portfolio.service):

```bash
sudo cp deploy/portfolio.service /etc/systemd/system/portfolio.service
```

Then reload systemd and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl start portfolio
sudo systemctl enable portfolio
sudo systemctl status portfolio
```

## Put Nginx in front of Gunicorn

Copy the Nginx config from [nginx-portfolio.conf](C:\Users\Lenovo\Documents\Playground\deploy\nginx-portfolio.conf):

```bash
sudo cp deploy/nginx-portfolio.conf /etc/nginx/sites-available/portfolio
```

Enable the site:

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

Now open:

```text
http://44.223.71.73
```

At this stage:

- Nginx listens on port `80`
- Nginx forwards traffic to Gunicorn on port `5000`

After Nginx is working, remove port `5000` from the EC2 Security Group so Gunicorn is no longer public.

## Enable HTTPS with SSL

Make sure your DNS points:

```text
yashopslib.work.gd -> 44.223.71.73
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

After success, your site will be available on:

```text
https://yashopslib.work.gd
```

Test automatic renewal:

```bash
sudo certbot renew --dry-run
```

## Useful commands

Check Gunicorn logs:

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

## Deployment summary

1. Run Gunicorn on port `5000`
2. Test with `http://44.223.71.73:5000`
3. Put Nginx in front on port `80`
4. Point `yashopslib.work.gd` to `44.223.71.73`
5. Enable HTTPS with Certbot on port `443`
6. Remove public access to port `5000`
