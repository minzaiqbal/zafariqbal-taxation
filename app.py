from flask import Flask, render_template, request, flash, redirect, url_for, Response
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('service') or 'General'
        message_body = request.form.get('message')

        if request.form.get('website'):  # honeypot: bots fill hidden field
            return redirect(url_for('contact'))

        try:
            msg = Message(
                subject=f"New Enquiry: {subject}",
                sender=os.getenv('MAIL_USERNAME'),
                recipients=[os.getenv('RECIPIENT_EMAIL')],
                reply_to=email
            )
            msg.body = f"""
You have received a new enquiry from your website.

Name    : {name}
Email   : {email}
Phone   : {phone}
Subject : {subject}

Message:
{message_body}
"""
            mail.send(msg)
            flash('Your message has been sent successfully! We will contact you soon.', 'success')
        except Exception as e:
            flash('Sorry, there was an error sending your message. Please try again.', 'danger')

        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/robots.txt')
def robots():
    body = '\n'.join(['User-agent: *', 'Allow: /', f'Sitemap: {request.host_url}sitemap.xml', ''])
    return Response(body, mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    urls = ''.join(f'<url><loc>{url_for(e, _external=True)}</loc></url>'
                   for e in ('index', 'about', 'services', 'contact'))
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return Response(xml, mimetype='application/xml')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
