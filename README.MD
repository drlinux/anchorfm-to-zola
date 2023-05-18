# anchorfm-to-zola

The anchorfm-to-zola script is a tool for fetching podcast metadata and episodes from an AnchorFM RSS feed and creating individual post files using a template. The template is compatible with the [Zola](https://www.getzola.org/) static site generator, but it can be easily adapted to your preferred static site generator.

## Installation

1. Clone the repository or download the script files.
2. Install the required dependencies by running the following command:

   ```shell
   pip install -r requirements.txt

3. Configure the script by editing the config.py file and providing the appropriate values for the feed URL and content directory.

## Usage

1. Run the script by executing the following command:

   ```shell
   python main.py

The script will fetch the podcast metadata and episodes from the specified feed URL, create individual post files in the content directory which you configured in config.py.

## License

This project is licensed under tHE BEER-WARE license. See the LICENSE file for more details.
