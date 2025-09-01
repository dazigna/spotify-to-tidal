# Spotify to Tidal

Spotify to Tidal is a Python application that allows you to transfer your playlists from Spotify to Tidal. This application uses the Spotify and Tidal APIs to authenticate and transfer your playlists.

## Features

- Authenticate with Spotify and Tidal
- Transfer playlists from Spotify to Tidal
- Run the server in the background to handle callbacks

TODO:
Store pulled song into a small file for now or a db eventually ? SQlite or else or a FUCKING HASHMAP

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/spotify-to-tidal.git
cd spotify-to-tidal
```

Install the required dependencies:

```bash
uv sync
```

## Usage

1. Register your application with Spotify and Tidal to get your client IDs and client secrets.
2. Update the configuration files with your client IDs and client secrets.
3. Run the application:

```bash
uv run main.py
```

## Configuration

### Spotify Configuration

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and register your application.
2. Add a redirect URI to your application settings.
3. Update the `.env` file with your client ID and client secret.

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:3000/auth/spotify/callback
```

### Tidal Configuration

1. Go to the [Tidal Developer Portal](https://developer.tidal.com/) and register your application.
2. Add a redirect URI to your application settings.
3. Update the `env` file with your client ID and client secret.

```env
TIDAL_CLIENT_ID=your_tidal_client_id
TIDAL_CLIENT_SECRET=your_tidal_client_secret
TIDAL_REDIRECT_URI=http://localhost:3000/auth/tidal/callback
```

## Running the Application

1. Start the application:

```bash
uv run main.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

Spotify to Tidal is a Python application that allows you to transfer your playlists from Spotify to Tidal. This application uses the Spotify and Tidal APIs to authenticate and transfer your playlists.

## Features

- Authenticate with Spotify and Tidal
- Transfer playlists from Spotify to Tidal
- Run the server in the background to handle callbacks

TODO:
Store pulled song into a small file for now or a db eventually ? SQlite or else or a FUCKING HASHMAP

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/spotify-to-tidal.git
cd spotify-to-tidal
```
Install the required dependencies:

```bash
uv sync

```

## Usage

1. Register your application with Spotify and Tidal to get your client IDs and client secrets.
2. Update the configuration files with your client IDs and client secrets.
3. Run the application:

```bash
uv run main.py
```

## Configuration

### Spotify Configuration

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and register your application.
2. Add a redirect URI to your application settings.
3. Update the `.env` file with your client ID and client secret.
```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:3000/auth/spotify/callback
```

### Tidal Configuration

1. Go to the [Tidal Developer Portal](https://developer.tidal.com/) and register your application.
2. Add a redirect URI to your application settings.
3. Update the `env` file with your client ID and client secret.

```
TIDAL_CLIENT_ID=your_tidal_client_id
TIDAL_CLIENT_SECRET=your_tidal_client_secret
TIDAL_REDIRECT_URI=http://localhost:3000/auth/tidal/callback
```

## Running the Application

1. Start the application:

```bash
uv run main.py
```

Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

License
This project is licensed under the MIT License. See the LICENSE file for details.