# BurundiSales

BurundiSales is an e-commerce platform built with Django, designed to facilitate online sales in Burundi. It offers a user-friendly interface for browsing products, managing shopping carts, and processing orders, with integration for M-Pesa payments.


## 🚀 Features





•User authentication (registration, login, profile management)



•Product catalog with categories and detailed product pages



•Shopping cart functionality



•Order management and history



•M-Pesa payment integration



•Admin dashboard for managing products, orders, and users



## 🛠 Technologies Used





•Django 4.x



•Python 3.x



•HTML5, CSS3, JavaScript



•SQLite (default database, configurable for others)



•Node.js and npm for frontend dependencies


## ⚙️ Installation

To set up the development environment, follow these steps:





1.**Clone the repository:**

<pre>git clone https://github.com/yourusername/burundisales.git
cd burundisales</pre>




2.**Create and activate a virtual environment:**

<pre>python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate</pre>



3.**Install Python dependencies:**

<pre>pip install -r requirements.txt</pre>



4.**Install Node.js dependencies:**

<pre>npm install</pre>



5.**Run database migrations:**

<pre>python manage.py migrate</pre>



6.**Create a superuser account:**

<pre>python manage.py createsuperuser</pre>



7.**Run the development server:**

<pre>python manage.py runserver</pre>



8.**Access the application:**





•Website: http://127.0.0.1:8000/



•Admin interface: http://127.0.0.1:8000/admin/

**Note:** Use the admin interface to add products, categories, and manage users.

## Usage





•**Browsing Products:** Visit the homepage to view featured products or browse by category using the navigation.



•**Shopping Cart:** Add products to your cart and proceed to checkout when ready.



•**Checkout:** Enter your details and select M-Pesa as the payment method.



•**Order History:** Check your past orders in your profile.

## Configuration





•**M-Pesa Integration:** To enable M-Pesa payments, configure the necessary credentials in settings.py (e.g., MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET, MPESA_SHORTCODE, etc.).



•**Email Settings:** For sending order confirmations or notifications, set up the email backend in settings.py.

## Contributing

Contributions are welcome! Please follow these steps:





1. Fork the repository.



2. Create a new branch for your feature or bugfix.



3. Make your changes and commit them with descriptive messages.



4. Push your branch to your fork.



5. Submit a pull request to the main repository.

## License

© 2025 Grey Okeyo


## Acknowledgments

- Built with ❤️ using Django and React.
- Thanks to all contributors and users!

## Contact

Have questions? Email me at greyokeyo@gmail.com or open an issue.
