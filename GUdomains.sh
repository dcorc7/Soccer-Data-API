#!/bin/bash

echo "Cleaning previous build..."
rm -rf website/Soccer-Data-API

echo "Rendering Quarto website..."
quarto render website

echo "Setting permissions..."

find website/Soccer-Data-API -type f -exec chmod 644 {} \;
find website/Soccer-Data-API -type d -exec chmod 755 {} \;

read -p "Deploy website to GU Domains? (y/n): " answer

if [[ "$answer" == "y" || "$answer" == "Y" ]]; then

    echo "Deploying website..."

    scp -r website/Soccer-Data-API/* \
    corcoran@corcoran.georgetown.domains:/home/corcoran/public_html/

    echo "Deployment complete."

else

    echo "Deployment skipped."

fi