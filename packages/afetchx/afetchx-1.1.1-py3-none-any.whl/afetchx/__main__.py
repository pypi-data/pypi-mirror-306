"""
Asynchronously fetch images from URLs using httpx.

This script parses command-line arguments to determine the list of image URLs to fetch,
the maximum number of concurrent connections, the cooldown time between requests, and
optionally a JSON file containing URLs. It then fetches the images and prints the number
of successfully downloaded images.

Command-line arguments:
- urls: List of image URLs to fetch (positional arguments).
- -n, --max_connections: Max number of concurrent connections (default: 5).
- -c, --cooldown: Cooldown time between requests in seconds (default: 1.0).
- -j, --json: Path to a JSON file containing URLs to fetch.

Error handling:
- If both URLs and a JSON file are provided, an error message is printed and the program exits.
- If neither URLs nor a JSON file are provided, an error message is printed and the program exits.
"""
import asyncio
import json
import sys
import os
import argparse
import httpx
from tqdm.asyncio import tqdm_asyncio
import aiofiles

# pylint: disable=line-too-long
# pylint: disable=eval-used


async def fetch_image(client: httpx.AsyncClient, url: str) -> bytes | None:
    """
    Fetches an image from the given URL using an asynchronous HTTP client.

    Args:
        client (httpx.AsyncClient): The asynchronous HTTP client to use for the request.
        url (str): The URL of the image to fetch.

    Returns:
        bytes | None: The content of the image as bytes if the request is successful, 
        otherwise None if an error occurs.

    Raises:
        httpx.HTTPStatusError: If the HTTP request returns an unsuccessful status code.
        Exception: For any other exceptions that occur during the request.
    """
    try:
        response = await client.get(url, timeout=20, follow_redirects=True)
        response.raise_for_status()
        return response.content
    except httpx.HTTPStatusError as exc:
        print(f"HTTP error occurred for {url}: {exc}")
    except Exception as exc:
        print(f"An error occurred for {url}: {exc}")
        raise exc
    return None


async def fetch_images_async(urls: list[str], output_dir: str, max_connections: int = 5, cooldown: float = 1.0, filename_formatter=None) -> None:
    """
    Asynchronously fetches images from a list of URLs and saves them to the specified output directory.
    Args:
        urls (list[str]): A list of image URLs to fetch.
        output_dir (str): The directory where the fetched images will be saved.
        max_connections (int, optional): The maximum number of concurrent connections. Defaults to 5.
        cooldown (float, optional): The cooldown period (in seconds) between consecutive downloads. Defaults to 1.0.
        filename_formatter (callable, optional): A function to format the filenames of the saved images. If None, the original filenames from the URLs will be used. Defaults to None.
    Returns:
        None
    """
    os.makedirs(output_dir, exist_ok=True)

    async with httpx.AsyncClient() as client:
        sem = asyncio.Semaphore(max_connections)

        async def fetch_and_save(url):
            async with sem:
                image_data = await fetch_image(client, url)
                if image_data:
                    custom_filename = filename_formatter(url) if filename_formatter else os.path.basename(url)
                    await save_image(output_dir, custom_filename, image_data)
                    if cooldown:
                        await asyncio.sleep(cooldown)

        tasks = [fetch_and_save(url) for url in urls]
        await tqdm_asyncio.gather(*tasks, desc="Downloading images")


async def save_image(output_dir: str, filename: str, image_data: bytes) -> None:
    """
    Asynchronously saves image data to a specified directory with the given filename.

    Args:
        output_dir (str): The directory where the image will be saved.
        filename (str): The name of the file to save the image as.
        image_data (bytes): The image data to be written to the file.

    Raises:
        OSError: If there is an error saving the image to the specified file path.
    """
    try:
        file_path = os.path.join(output_dir, filename)
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(image_data)
    except OSError as e:
        print(f"Error saving image to {file_path}: {e}")
        raise e


def load_urls_from_json(json_path: str) -> list[str]:
    """
    Load a list of URLs from a JSON file.

    Args:
        json_path (str): The path to the JSON file containing the URLs.

    Returns:
        list[str]: A list of URLs as strings.

    Raises:
        ValueError: If the JSON file does not contain a list of URLs as strings.
        OSError: If there is an error loading the JSON file.
    """
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not all(isinstance(url, str) for url in data):
                raise ValueError("JSON file must contain a list of URLs as strings.")
            return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        raise e


def main() -> None:
    """
    Main function to asynchronously fetch images from URLs using httpx.
    This function sets up an argument parser to handle command-line arguments,
    validates the provided arguments, and initiates the asynchronous image
    fetching process.
    Command-line arguments:
    - urls: List of image URLs to fetch.
    - -n, --max_connections: Max number of concurrent connections (default: 5).
    - -c, --cooldown: Cooldown time between requests in seconds (default: 1.0).
    - -j, --json: Path to a JSON file containing URLs to fetch.
    - -o, --output-dir: Directory to save downloaded images (default: ./downloaded/).
    - --filename-format: Lambda function as a string to format filenames.
    The function ensures that either a list of URLs or a JSON file is provided,
    but not both. It also validates the provided filename format if specified.
    If the arguments are valid, it calls the `fetch_images_async` function to
    download the images asynchronously.
    Raises:
        SystemExit: If the provided arguments are invalid or if there is an error
                    in parsing the filename format.
    """
    parser = argparse.ArgumentParser(description="Asynchronously fetch images from URLs with httpx.")
    parser.add_argument("urls", nargs="*", default=[], help="List of image URLs to fetch")
    parser.add_argument("-n", "--max_connections", type=int, default=5, help="Max number of concurrent connections (default: 5)")
    parser.add_argument("-c", "--cooldown", type=float, default=1.0, help="Cooldown time between requests in seconds (default: 1.0)")
    parser.add_argument("-j", "--json", type=str, help="Path to a JSON file containing URLs to fetch")
    parser.add_argument("-o", "--output-dir", type=str, default=f"{os.getcwd()}/downloaded", help="Directory to save downloaded images (default: ./downloaded/)")
    parser.add_argument("--filename-format", type=str, help="Lambda function as a string to format filenames, e.g., \"lambda url: url.split('/')[-1].split('.')[0] + '.png'\"")

    args = parser.parse_args()

    if args.urls and args.json:
        print("Error: Provide either a list of URLs or a JSON file, not both.")
        raise SystemExit(1)
    if not args.urls and not args.json:
        print("Error: No URLs provided. Use positional arguments or --json to specify URLs.")
        raise SystemExit(1)

    urls = args.urls if args.urls else load_urls_from_json(args.json)

    filename_formatter = None
    if args.filename_format:
        try:
            filename_formatter = eval(args.filename_format)
            if not callable(filename_formatter):
                raise ValueError("The filename format provided is not callable.")
        except ValueError as e:
            print(f"Error parsing filename format: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error parsing filename format: {e}")
            raise e

    asyncio.run(fetch_images_async(
        urls,
        output_dir=args.output_dir,
        max_connections=args.max_connections,
        cooldown=args.cooldown,
        filename_formatter=filename_formatter
    ))
    print(f"Images downloaded successfully to {args.output_dir}.")


if __name__ == "__main__":
    main()
