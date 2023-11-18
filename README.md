<h1>flight-club</h1>
<p><strong>Flight finder system created in early 2023.</strong></p>
<p><strong>This is not a real product! The project was created only for learning purposes.</strong></p>

<h2>How does it work?</h2>
<p><strong>Access home page from your browser</strong></p>
<img src="./readme_media/home_page.png" alt="Image of home page">

<p><strong>Navigate to flight form</strong></p>
<img src="./readme_media/empty_flight_form.png" alt="Image of an empty flight form">

<p><strong>Fill the flight form with your desired trip information and submit</strong></p>
<img src="./readme_media/full_flight_form.png" alt="Image of a flight form with trip information">

<p><strong>System informs user by email after finding a cheap flight</strong></p>
<img src="./readme_media/mail_top.png" alt="Image of the email">
<img src="./readme_media/mail_mid.png" alt="Image of the email">
<img src="./readme_media/mail_bottom.png" alt="Image of the email">

<h2>Server explained</h2>
<p><strong>Standard scenario:</strong></p>
<ul>
    <li>Server receives the flight form, saves it into MySQL database.</li>
    <li>Server periodically makes API calls to a flight search provider.</li>
    <li>Sends user an email if the found flight is cheaper than the maximum price.</li>
</ul>
<p><strong>Other features:</strong></p>
<ul>
    <li>Most of the basic errors are handled, e.g., incorrect destinations, incorrect dates, etc.</li>
    <li>Email unsubscribe.</li>
    <li>Does not send similar flight offers (to previous flight offers).</li>
</ul>

<h2>Built with</h2>
<ul>
    <li>Python Flask</li>
    <li>MySQL</li>
    <li>GoogleCloud - for hosting</li>
    <li>HTML</li>
    <li>CSS</li>
</ul>
<p><strong>The project used to be hosted on GoogleCloud, but no longer is.</strong></p>
