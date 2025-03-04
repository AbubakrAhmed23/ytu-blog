from flask import Flask, render_template, request
import smtplib
import requests

posts = requests.get("https://api.npoint.io/23d651abeb4c685f2a03").json()
OWN_EMAIL = 'abubakrahmed.work@gmail.com'
OWN_PASSWORD = 'soxz kwnj kofj lxxh'
app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:index>')
def show_post(index):
    requested_post = next((post for post in posts if post['id'] == index), None)
    return render_template('post.html', post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"""Subject: New Message From Blog\n
    Name: {name}
    Email: {email}
    Phone: {phone}
    Message: {message}
    """

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(OWN_EMAIL, OWN_PASSWORD)
            connection.sendmail(
                from_addr=OWN_EMAIL,
                to_addrs=OWN_EMAIL,
                msg=email_message.encode('utf-8')
            )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
