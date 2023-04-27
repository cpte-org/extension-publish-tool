# Auto-Publish Browser Extension

This script allows you to publish your browser extension to Chrome, Firefox, and Edge stores automatically.

## Installation

1. Clone this repository: `git clone https://github.com/username/repo.git`
2. Install the required packages: `pip install -r requirements.txt` and `npm install --global sign-addon`
3. Set the required environment variables (see below)

## Usage

python publish.py --chrome --firefox --edge --extension_id <extension_id> --zip_file_path <zip_file_path>


## Required Environment Variables

- For Chrome Web Store publishing:
  - `CHROME_CLIENT_ID`: Your Chrome Web Store API client ID
  - `CHROME_CLIENT_SECRET`: Your Chrome Web Store API client secret
  - `CHROME_REFRESH_TOKEN`: Your Chrome Web Store API refresh token

- For Firefox Add-ons publishing:
  - `FIREFOX_API_KEY`: Your Firefox Add-ons API key
  - `FIREFOX_API_SECRET`: Your Firefox Add-ons API secret

- For Microsoft Edge Add-ons publishing:
  - `EDGE_TENANT_ID`: Your Microsoft Azure AD tenant ID

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
