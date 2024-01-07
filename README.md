# Telegram Tracker

![python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)

The Telegram Tracker is a Python project designed to monitor the online/offline activity of your Telegram contacts and store this data in a MySQL/SQLite database.

The motivation for creating this project came from my desire to study data science and data analysis.

## Features

- **Contact Monitoring**: Keep track of when your Telegram contacts go online and offline.
- **Data Storage**: Store the timestamps of online and offline events in a MySQL database.
- **Activity Insights**: Gain insights into your contacts' online patterns over time.

## Setup and Usage

1. **Clone the repository**: Start by cloning this repository to your local machine.

   ```bash
   git clone https://github.com/cubicbyte/telegram-tracker.git
   cd telegram-tracker
   ```

2. **Install dependencies**: Install the necessary dependencies using the provided `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup .env configuration file**: Copy `.env.example` to `.env` and modify it according to your needs. Update the `API_ID` and `API_HASH` with your Telegram API credentials (https://my.telegram.org):

4. **Database setup**: Depending on the chosen database type, run either `scripts/setup_mysql_db.py` or `scripts/setup_sqlite_db.py` to set up the database structure. Default database is sqlite.

5. **Run the tracker**: Execute the main script:

   ```bash
   python main.py
   ```

   At first startup the program will guide you through the login process for Telegram.

## Disclaimer

This project is meant for personal and educational purposes as it said in the description. Respect the privacy of your contacts and ensure you have their consent before tracking their online activity.

## Contributing

Contributions are welcome! If you find issues or have feature ideas, feel free to open an issue or pull request.

## License

This project is licensed under the [MIT License](LICENSE).
