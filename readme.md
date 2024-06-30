# SWRToSpotiy

A simple python script which parses songs played on SWR 1, searches them on spotify and puts them in a playlist.

You need to provide your own client key and redirect URI.

In order to do so, you need to register you own Spotify app. See the [official documentation](https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app) on how to do that.
Make sure to register the redirect URI you provide to the script in your app.
The client key must be provided by the enviroment key  SPOTIPY_CLIENT and the redirect URL by the environment key SPOTIPY_REDIRECT_URI.

A pipfile with the dependencies is provided.
Use [pipenv](https://pipenv.pypa.io/en/latest/) to install the dependencies.

For info on how to use the script, use the --help options.




