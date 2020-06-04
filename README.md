# immoviewer.com Panorama Downloader
Little script that extracts and stitches together the panorama images delivered by immoviewer.com based panoramas. The output is a cubical panorama (https://krpano.com/docu/panoformats/index.php?lang=de). Tools like https://nadirpatch.com/cube2sphere/ can be used to convert it to a "conventional" equirectangular panorama, if needed.

# How to use
`python3 download_immoviewer.py 'URL'`

e.g. `python3 download_immoviewer.py 'https://app.immoviewer.com/portal/tour/1561022?accessKey=5dc8'`
